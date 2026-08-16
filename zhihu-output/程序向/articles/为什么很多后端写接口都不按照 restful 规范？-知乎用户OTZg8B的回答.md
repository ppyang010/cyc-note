---
id: "1691981151"
title: "为什么很多后端写接口都不按照 restful 规范？"
author: "知乎用户OTZg8B"
type: zhihu-answer
source: "https://www.zhihu.com/question/438825740/answer/1691981151"
created: "2021-01-22 18:29"
updated: "2022-06-02 20:58"
collected: "2021-01-22 18:29"
downloaded: "2026-08-16"
---
这个问题我觉得可以分为三大方面。

## RESTful 本身的缺陷

1.  RESTful 不是一种规范，而是一种风格，它不具有强制性。
2.  RESTful 定义本身包含很多“模糊性”，导致“自由发挥的空间”很大，因此各家有各家的理解，也就造就了各种“方言”。
3.  RESTful 是一种基于“资源”的接口设计形式，核心是名词。这对于**只有**增删改查的业务来说很合适，但现实业务并不只有增删改查。比如常见的业务有冻结/解冻等。这时候你至少会纠结这种接口应该用PATCH/PUT呢还是POST/DELETE呢？
4.  **抽象资源**。所谓的抽象资源是“不直接对应数据库表的资源”。比如“登录/登出”。如果你用RPC式的接口设计，这就很直接：**POST /login** 和 **POST /logout**。但是你要硬套RESTful，你就得挖空心思的想出一个抽象资源“会话”（session）。登录 = 创建会话，登出 = 销毁会话。于是你把接口设计成 **POST /sessions** 和 **DELETE /sessions**。这就很**反直觉**，且背离RESTful的设计初衷。
5.  也许这不能算是 RESTful 的缺陷，更应该算作 HTTP （或实现 HTTP 的服务器/客户端）的缺陷，那就是 GET 请求不能带 body！所以，对于复杂查询，如果用 GET，URL可能超长；如果用 POST，又不符合 REST 的要求。
6.  元数据如何返回也是个问题。比如分页查询是很常见的需求。但是当前是第几页，一共多少条记录等，这些元数据放在响应的哪儿呢？如果放在body里，有点不REST，因为REST的响应应该只包含数据；如果放在header里，则又要和客户端商定协议细节，客户端实现也变得更困难。
7.  RESTful 和 HTTP 绑的太死，很难用在其他传输协议里，比如你很难把 REST 用在 Redis PubSub 里。相比之下，一个包含指令和数据的RPC包通过HTTP发还是通过Kafka发都没问题。

## 英语的不一致性

1.  光名词就有可数名词、不可数名词、集合名词、动名词等，其中可数名词又有单复同形、单复异形，单复异形里又有规则变化和不规则变化，规则变化里又有y结尾、s结尾、x结尾等，总之很复杂，设计接口有时候会很迷茫。有些连英语国家自己的语言学家都搞不定，比如media究竟是一个单复同形的集合名词，还是medium的不规则复数形式？
2.  对于描述状态的动词的过去分词形式，也有类似问题。

## 国情

1.  国内很多程序员英语不过关。
2.  国内的教育/培训大多只注重“能跑通”和“结果正确”，而对于“风格”这种虚无缥缈的东西很少关注。
3.  “反正有文档和swagger，接口设计不漂亮没关系。”
4.  对于接口调用方来说，“是不是RESTful无所谓，反正都是复制粘贴URL”，甚至还有人觉得在path里嵌id的风格代码很难写（尤其对于Java这种没有字符串内插特性的语言更是如此）。
5.  英语可以很简单地把动词变成名词，但中文里动词就是动词，名词就是名词。这会导致国人设计RESTful API的难度上升。比如“报废一个资产”（注意这不是删除），用英文理解可以是“**dispose** an asset”，也可以是“create an asset **disposal**”，所以接口很自然地就设计成了 **POST /assets/:asset\_id/disposal**。但是你用中文随便怎么想都想不到“创建一个资产报废”，因为在中文里“报废”就是动词。
6.  如果你去看微信和阿里的API设计，粗看就能看出很多不规范的地方。大厂尚且如此，更何况小作坊呢？

## 结论

我现在设计API更倾向于使用RPC式的API，且一律 **POST /命名空间/资源类型/动作**。参数全都带在body里。

## 附录

有网友留言说GET请求支持body，于是我去试了一下。下面看看我是怎么测的：

1.  **用TCP Socket自己实现一个简易（简陋？）的HTTP Server，且支持带body的GET请求，（echo\_server.rb）**

```rb
#!/usr/bin/env ruby
require 'socket'

# 处理HTTP请求（不支持压缩格式的请求）
def handle_http_request(client)
  # 读取请求行（请求的第一行）
  method, uri, protocol = client.gets.chomp.split
  # 读取请求头
  headers = client.each
    .take_while{|line| !line.chomp.empty?}
    .map(&:chomp)
    .map(&:downcase)
    .map{|line| line.split(/:\s*/, 2)}
    .to_h

  # 读取请求body
  content_length = headers['content-length'].to_i
  body = client.read(content_length)

  # 写响应
  client.write %Q[
#{protocol} 200 OK
Content-Type: #{headers['content-type']}
Content-Length: #{headers['content-length']}

#{body}
  ].strip.gsub(/\r?\n/, "\r\n")

  # 关闭TCP连接
  client.close
end

# 监听端口号2000
server = TCPServer.new(2000)

loop do
  client = server.accept
  handle_http_request(client)
end
```

**2\. 配置NGINX反向代理**

```nginx
# /etc/nginx/sites-enabled/fake
server {
  listen 8080;
  gzip off;

  location / {
    proxy_pass http://localhost:2000;
    proxy_redirect off;
  }
}
```

**3\. 用curl发送POST请求测试自制HTTP服务器实现是否正确**

```text
$ curl -XPOST \
       -d'foo=bar' \
       -H'Content-Type: application/x-www-form-urlencoded;charset=utf-8' \
       -i \
       http://localhost:2000/foo/bar
```

结果正常

**4\. 用curl不通过NGINX发送带body的GET请求到自制服务器**

```text
$ curl -XGET \
       -d'foo=bar' \
       -H'Content-Type: application/x-www-form-urlencoded;charset=utf-8' \
       -i \
       http://localhost:2000/foo/bar
```

结果正常

**5\. 用curl通过NGINX代理发送带body的GET请求到自制服务器**

```text
$ curl -XGET \
       -d'foo=bar' \
       -H'Content-Type: application/x-www-form-urlencoded;charset=utf-8' \
       -i \
       http://localhost:8080/foo/bar
```

结果依然正常

**结论：至少NGINX和curl支持带body的HTTP请求。但是具体是否任何服务器和任何客户端都支持，我不敢保证。至少用Chrome的fetch API发GET请求时明确报错：Request with GET/HEAD method cannot have body**

## **更新**

REST的流行还导致了另一个问题，那就是URL的路径（path）部分不再是静态的了，而是会有动态的参数（例如id）嵌在里面，于是路由器的设计变得更困难（实现静态路由器只需要一张哈希表或一个Trie就行，但是动态路由器可能就得玩数组/链表的顺序查找了）。这对于路径比较少的web应用可能还感觉不出来性能差异，但是对大量路由的web应用，这方面也是个性能开销。