---
id: "2066232764375077995"
title: "webflux应用场景是什么？"
author: "程序员小富"
type: zhihu-answer
source: "https://www.zhihu.com/question/292688280/answer/2066232764375077995"
created: "2026-07-30 18:44"
updated: "2026-07-30 18:44"
collected: "2026-07-30 18:44"
downloaded: "2026-08-16"
---
大多数业务用 Spring MVC 就是能搞定。

WebFlux 不是用来替代 Spring MVC 的，它解决的是一类特定问题：**你的服务大量时间花在等 I/O（等数据库返回、等下游接口响应、等消息队列），而不是花在 CPU 计算上。**

Spring MVC 一个请求占一个线程，请求处理完线程才释放。你的接口要调三个下游服务，每个耗时 200ms，这个线程就干等 600ms，啥也不干，就在那阻塞着。Tomcat 默认 200 个线程，并发一上来线程就不够用了，请求开始排队。

WebFlux 底层是 Netty 的事件循环模型，一个线程可以同时处理很多请求。线程发起 I/O 调用之后不傻等，去处理别的请求，等 I/O 结果回来了再继续。用很少的线程就能撑住很高的并发连接数。

不过，**整条链路都得是非阻塞的才行。** 你用了 WebFlux，Service 层还是 JDBC 查 MySQL、RestTemplate 调下游，那没有任何意义。JDBC 是阻塞的，线程该等还是得等，WebFlux 白搭。得用 R2DBC 替代 JDBC，WebClient 替代 RestTemplate，所有 I/O 操作都换成响应式 API，才能真正发挥作用。

这也是大多数人觉得没这个需求的原因，不是 WebFlux 没用，是改造成本太高。整条调用链从阻塞换成非阻塞，数据库驱动、HTTP 客户端、缓存客户端、消息队列客户端全都要换。现有项目改造不现实，新项目又很少有人愿意从零开始用全套响应式技术栈。

### WebFlux 适合的场景

**网关层。** Spring Cloud Gateway 底层就是 WebFlux。网关不做复杂业务逻辑，就是接收请求、转发、等响应、返回，全是 I/O 操作。这种场景用 WebFlux 比 MVC 强很多，同样的机器能撑住多几倍的并发连接。

**大量长连接的推送类服务。** 同时给几万个客户端推消息，或者维持大量 WebSocket、SSE 连接。MVC 模式下每个连接占一个线程，几万个连接要几万个线程，不现实。WebFlux 少量线程就能维持。

**聚合接口，一个请求并行调多个下游。** App 首页同时拉用户信息、推荐列表、消息数、活动 banner，四个下游。MVC 你可以 CompletableFuture 并行调，但线程还是被占着。WebFlux 里 `Mono.zip()` 并行发起四个非阻塞调用，线程完全不阻塞：

```text
Mono.zip(
    userClient.getUser(userId),
    recommendClient.getList(userId),
    messageClient.getCount(userId),
    activityClient.getBanner()
).map(tuple -> {
    HomePageVO vo = new HomePageVO();
    vo.setUser(tuple.getT1());
    vo.setRecommendList(tuple.getT2());
    vo.setMessageCount(tuple.getT3());
    vo.setBanner(tuple.getT4());
    return vo;
});
```

**流式数据处理。** 持续消费 Kafka 消息、实时处理数据流，Reactor 的 Flux 天然适合。

### 不适合的场景

**CPU 密集型。** 接口主要时间花在计算上（加密、图像处理、复杂规则引擎），I/O 占比小，WebFlux 帮不了你。事件循环线程被 CPU 计算占住，其他请求照样等。

**团队没写过响应式代码。** 响应式的调试、异常处理、事务管理都比同步代码复杂得多。一个 `flatMap` 嵌三层，堆栈全是 Reactor 内部调用，出了 bug 排查成本翻倍。没经验的团队上 WebFlux 大概率是给自己挖坑。

**项目里已经用了大量阻塞 API。** ORM 是 MyBatis、数据库驱动是 JDBC、缓存用 Jedis，这些全是阻塞的，链路里有一个环节阻塞，整个非阻塞就白搭。硬上 WebFlux 只会增加复杂度，性能反而可能更差。

### WebFlux 是未来方向

JDK 21 出了虚拟线程之后，这个说法得打个问号。虚拟线程解决的是同一个问题，线程被 I/O 阻塞导致并发上不去——但做法完全不同：它让阻塞变得廉价，不逼你改成非阻塞。你还是写同步代码，JDBC 查询该怎么写怎么写，JVM 底层帮你切换，一个进程里跑几十万个虚拟线程没问题。

Spring Boot 3.2+ 一行配置就能启用：

```text
spring:
  threads:
    virtual:
      enabled: true
```

开了之后 Tomcat 每个请求都跑在虚拟线程上，阻塞式代码照写，并发能力直接上去。不用改代码，不用换技术栈，不用学 Reactor，升级 JDK 加一行配置搞定。

WebFlux 在网关、推送、流式处理这些场景还是有优势，但对大多数写 CRUD 的业务服务来说，虚拟线程已经够用了，没必要折腾响应式那套东西。