---
id: "3624657759"
title: "为什么很多 SpringBoot 开发者放弃了 Tomcat，选择了 Undertow?"
author: "老鬼学长"
type: zhihu-answer
source: "https://www.zhihu.com/question/623790275/answer/3624657759"
created: "2024-09-13 19:20"
updated: "2024-09-13 19:20"
collected: "2024-09-13 19:20"
downloaded: "2026-08-16"
---
谢邀！看来今天有人又在纠结Tomcat和Undertow的问题了。 别急，来给你细说这事儿。

首先说说为啥很多SpringBoot开发者会从Tomcat换到Undertow。主要原因就是性能和资源利用率。Undertow是一个基于NIO的服务器，这使得它在处理并发请求时更加高效，内存占用也更少。

要从源码层面来分析，我们可以看看Undertow是如何处理HTTP请求的。Undertow使用了一种叫做XNIO的非阻塞输入/输出API，这个API是专为高效处理并发请求设计的。简单地说，它可以让一个线程处理多个网络连接，而不是传统的一个连接一个线程，这样就极大地提高了性能。

```text
public class HttpServer {
    public static void main(final String[] args) {
        Undertow server = Undertow.builder()
                .addHttpListener(8080, "localhost")
                .setHandler(new HttpHandler() {
                    @Override
                    public void handleRequest(final HttpServerExchange exchange) throws Exception {
                        exchange.getResponseHeaders().put(Headers.CONTENT_TYPE, "text/plain");
                        exchange.getResponseSender().send("Hello World");
                    }
                }).build();
        server.start();
    }
}
```

这段简单的代码展示了如何使用Undertow创建HTTP服务器。比较一下Tomcat，你会发现Undertow的代码更加简洁，主要是因为Undertow的设计就是为了简化并发处理。

再说说Tomcat，它虽然也支持NIO，但是它的设计和实现依然偏向于传统的阻塞式IO模型。这就意味着在高并发的场景下，Tomcat的性能可能不如Undertow。而且，从配置和管理的角度来看，Tomcat的设置相对复杂一些。

还有一个点，就是Undertow在微服务架构中的表现也非常出色。它天生支持非阻塞，这让它成为构建响应式应用的理想选择。对于现代的云应用和微服务架构，这种轻量级和高性能的特性非常关键。

虽然Undertow提供了很多现代化的特性和改进，但是选择什么服务器还是得看你的具体需求。如果你的应用需要极致的性能和更好的资源利用率，那么Undertow肯定是个不错的选择。如果你需要更稳定的社区支持和丰富的文档，可能Tomcat更合适。

所以啊，别被网上那些一棍子打死的言论迷惑，适合自己的才是最好的。选技术，也是一场修行，心静自然凉！别人家的技术再好，不适合自己也是白搭。

最后，分享一个不错的编程学习网站，里面有大量的免费编程教程供你学习：

[笨鸟Java开发指南 - 笨鸟编程导航](https://link.zhihu.com/?target=https%3A//www.j301.cn/java.html)