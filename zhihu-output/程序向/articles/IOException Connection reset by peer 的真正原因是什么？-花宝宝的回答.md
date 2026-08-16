---
id: "1987463589578167072"
title: "IOException: Connection reset by peer 的真正原因是什么？"
author: "花宝宝"
type: zhihu-answer
source: "https://www.zhihu.com/question/270504360/answer/1987463589578167072"
created: "2025-12-25 10:04"
updated: "2026-03-13 10:32"
collected: "2025-12-25 10:04"
downloaded: "2026-08-16"
---
这个报错我排查过不下二十次了，每次原因都不太一样。

看你的堆栈，是在 `SocketChannelImpl.read` 抛的，说明是读的时候收到了RST。

说白了就是：**对方把连接强制关了，你这边还在读/写，就会收到这个错。**

但问题是，对方为什么要发RST？原因太多了，我挨个说。

* * *

## 第一步：先搞清楚RST是谁发的

别急着猜原因，先抓包看看RST到底是谁发的：

```text
tcpdump -i eth0 'tcp[tcpflags] & tcp-rst != 0' and host 对方IP
```

输出类似这样：

```text
14:23:15.123456 IP 10.0.1.5.3306 > 10.0.2.8.52341: Flags [R], seq 0
```

10.0.1.5发的RST，那就是服务端的问题。这一步很关键，方向搞错了排查就跑偏了。

* * *

## 服务端全连接队列满了

这个最常见。

服务端的accept队列是有上限的，满了之后新连接直接被RST掉。

怎么看队列满没满？

```text
ss -ltn 'sport = :8080'
State    Recv-Q    Send-Q    Local Address:Port
LISTEN   129       128       0.0.0.0:8080
```

Recv-Q是129，Send-Q是128，Recv-Q比Send-Q还大，说明队列溢出了。

调大队列：

```text
sysctl -w net.core.somaxconn=65535
```

应用层也得配合，Nginx的话改 `listen 8080 backlog=65535;`

* * *

## 服务端进程挂了

进程crash或者被kill -9，操作系统会对所有连接发RST。

这种情况好判断——所有连接都会报错，不是单个连接的问题。看看服务端进程还在不在，翻翻日志有没有OOM或者crash记录。

* * *

## 服务端处理完就close了，你还在读

这个属于代码层面的问题。

服务端觉得请求处理完了，直接close。但客户端这边还在等数据，一读就收到RST了。

常见于HTTP短连接场景，服务端返回完响应就关了，客户端还想复用这个连接。

* * *

## 防火墙/负载均衡把连接掐了

这坑我踩过好几次。

连接建好一段时间，中间的防火墙或者云厂商的SLB觉得连接空闲太久，直接给你掐断。

特点是：不是每次都复现，空闲一会儿就出问题，一直有数据传输反而没事。

解决办法是开TCP keepalive：

```text
sysctl -w net.ipv4.tcp_keepalive_time=60
sysctl -w net.ipv4.tcp_keepalive_intvl=10
sysctl -w net.ipv4.tcp_keepalive_probes=3
```

应用层也得配合，数据库连接池、HTTP客户端都要设置心跳。

* * *

## 服务端扛不住了主动丢连接

压力大的时候，有些服务会主动关连接来自保。

Nginx有个 `limit_conn`，并发超了直接拒。还有些框架有降级逻辑，忙不过来就不接客了。

这种情况看服务端的监控，CPU、内存、连接数，肯定有一个指标飙了。

* * *

## 客户端自己超时了

这个反过来了，RST是客户端发的。

客户端设了读超时，等太久不耐烦了直接close。服务端还在慢慢处理呢，想write的时候发现连接没了。

```text
socket.setSoTimeout(5000);  // 5秒超时
// 服务端处理了10秒
// 客户端等不及close了
// 服务端write的时候就收到RST
```

抓包看RST是谁发的就能确认。

* * *

## 排查命令速查

```text
# 抓RST包
tcpdump -i eth0 'tcp[tcpflags] & tcp-rst != 0'

# 看队列
ss -ltn

# 看溢出统计
netstat -s | grep -i "listen"

# 看连接状态
ss -tan | awk 'NR>1 {print $1}' | sort | uniq -c | sort -rn
```

* * *

## 说个真事

上个月帮人排查，Java应用连MySQL偶发reset。

抓包一看，RST是MySQL发的。查max\_connections，设的500，当时连接数490多了。连接池不够用，新连接进来直接被拒。

调大max\_connections，好了。

所以这破问题就是得具体分析，没有银弹。

* * *

## 跨机器排查是真的烦

这类问题最麻烦的是得同时看客户端和服务端。

客户端在A机器，服务端在B机器，中间还有个负载均衡。三台机器同时抓包、同时看日志，跳来跳去脑子都乱了。

我现在的做法是用组网把这几台机器串一起，本地开三个终端直接SSH上去，不用跳板机绕来绕去。特别是跨机房的时候，网络本来就抖，再走公网跳转，抓包都抓不利索。

* * *

评论区有问题可以聊，这错误变种太多了，一篇写不完。