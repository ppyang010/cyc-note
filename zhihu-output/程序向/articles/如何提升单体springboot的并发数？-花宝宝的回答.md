---
id: "2012864406883680864"
title: "如何提升单体springboot的并发数？"
author: "花宝宝"
type: zhihu-answer
source: "https://www.zhihu.com/question/650929663/answer/2012864406883680864"
created: "2026-03-05 12:17"
updated: "2026-03-06 14:19"
collected: "2026-03-05 12:17"
downloaded: "2026-08-16"
---
一个默认配置的 Spring Boot 应用，Tomcat 最大线程数是 200。也就是说同一时刻最多处理 200 个请求，第 201 个请求进来就得排队。排队队列满了（默认 100），直接拒绝连接。

200 听起来不少，但你的接口里只要有一个操作稍微慢一点——比如查了一次没走索引的 SQL、调了一个响应慢的第三方接口——线程就会被占住。10 个慢请求占住 10 个线程，快请求能用的线程就只剩 190 个了。线上一个慢接口拖垮整个服务，十有八九就是这么来的。

提升并发数不是调一个参数的事。

### 别上来就调线程数

很多文章一上来就教你改 `server.tomcat.max-threads=500`。线程数调大了，并发请求确实能多接一些。但如果瓶颈不在线程数上，你调到 5000 也白搭——线程全卡在别的地方排队呢。

你的服务能扛多少并发，取决于**整条链路上最慢的那个环节**。

**CPU 打满了？** 说明计算密集，加线程只会让 CPU 更忙，上下文切换还会浪费性能。这时候该优化代码逻辑或者加机器。

**数据库连接池满了？** 200 个线程同时查数据库，但连接池默认也就十来个连接。190 个线程在等连接，线程数再多也是干等着。

**在等外部接口响应？** 调了一个第三方支付接口，对方要 2 秒才返回。你的线程就傻等这 2 秒。200 个线程全卡在等支付接口上，新请求一个都处理不了。

所以第一步永远是定位瓶颈。`jstack` 导出线程快照，看看线程都卡在哪一行代码上。或者用 Arthas 在线看方法耗时：

```text
java -jar arthas-boot.jar

# 进入 Arthas 后
trace com.example.OrderService createOrder
```

这条命令会打印 `createOrder` 方法内部每一步的耗时，谁慢一目了然。

### Tomcat 线程池：调大但别调太大

确认瓶颈不在下游之后，可以动 Tomcat 线程池了：

```text
server:
  tomcat:
    threads:
      max: 400
      min-spare: 50
    max-connections: 10000
    accept-count: 200
```

`min-spare` 是最小空闲线程数，提前备着避免突发流量时临时创建线程太慢。`max-connections` 是 Tomcat 能持有的最大连接数，`accept-count` 是连接数打满之后还能排队等待的数量——排队队列也满了，就直接拒绝连接了。

线程数不是越大越好。每个线程默认占 1MB 栈内存，400 个线程光栈就吃掉 400MB。而且线程多了 CPU 频繁切换上下文，吞吐量反而会掉——见过把线程数调到 2000 结果 TPS 比 200 还低的，CPU 全花在切换上了，没空干正事。

IO 密集型业务，线程数设到 CPU 核心数的 20~50 倍比较合理。CPU 密集型就别折腾了，核心数的 1~2 倍就到头了。4 核机器跑普通业务接口，200~400 差不多。

### 数据库连接池：最容易忽略的瓶颈

Spring Boot 默认用 HikariCP，HikariCP 自身的默认最大连接数是 10（Spring Boot 较新版本可能会根据 CPU 核心数动态调整，但通常也就十几个）。你 Tomcat 线程数调到 400 了，但数据库连接池只有十来个——这就像修了一条 8 车道高速公路，收费口只开了 1 个。

```text
spring:
  datasource:
    hikari:
      maximum-pool-size: 30
      minimum-idle: 10
      connection-timeout: 3000
      idle-timeout: 600000
```

连接池该设多大？HikariCP 官方有一篇 “About Pool Sizing”，里面的结论挺打脸的：**大部分人的连接池都设太大了**。他们给了一个公式——连接数 = (CPU 核心数 \* 2) + 磁盘数。4 核机器大概 10~15 个连接就够了。

听起来少得离谱，但数据库那头每个连接都要占内存、维护状态，连接数太多数据库自己先撑不住了。连接池不是越大越好，这个跟线程池一样反直觉。

`connection-timeout` 设成 3000 毫秒（3 秒），3 秒拿不到连接就报错。别设太长，不然请求一直挂着，用户看到的就是页面一直在转圈。

如果你的 SQL 都很快（50ms 以内返回），30 个连接每秒能处理 600 个数据库请求，足够撑住很高的并发了。SQL 慢才是瓶颈，加连接数治不了慢 SQL。

### 异步化：别让线程傻等

一个下单接口里，扣库存和创建订单是必须同步做的，但发短信通知、发邮件、加积分这些不需要用户等。

```text
@Async("taskExecutor")
public void sendOrderNotification(Long orderId) {
    smsService.send(...);
    emailService.send(...);
    pointsService.add(...);
}
```

配一个专门的线程池：

```text
@Bean("taskExecutor")
public Executor taskExecutor() {
    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(10);
    executor.setMaxPoolSize(30);
    executor.setQueueCapacity(500);
    executor.setThreadNamePrefix("async-");
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    return executor;
}
```

`CallerRunsPolicy` 是兜底策略——线程池满了之后由调用者线程自己执行，不至于丢任务。

异步化之后，下单接口只做核心逻辑，100ms 内返回。非核心任务丢到异步线程池里慢慢跑。用户体验好了，Tomcat 线程也释放得快了，能接更多请求。

如果非核心任务比较重、量比较大，再进一步——用消息队列替代 `@Async`。RabbitMQ 或者 Kafka 把任务扔到队列里，由专门的消费者服务处理。好处是任务不怕丢（队列有持久化），而且消费速度可以独立控制，不影响主服务。

### 缓存：少查一次数据库就是赚了

商品详情页、用户信息、配置数据——这些读多写少的数据，每次都查数据库是浪费。放到 Redis 里缓存起来：

```text
@Cacheable(value = "product", key = "#productId", unless = "#result == null")
public Product getProduct(Long productId) {
    return productMapper.selectById(productId);
}
```

Redis 单线程都能扛到每秒十几万次读取，加了缓存之后数据库压力直接降一个数量级。

但缓存有三个经典问题要处理。

**缓存穿透**：查一个不存在的 ID，缓存里没有，每次都打到数据库。解法是缓存空值，或者用布隆过滤器拦截。

**缓存击穿**：热点 key 刚好过期的瞬间，大量请求同时打到数据库。解法是用互斥锁（`setnx`），只放一个请求去查数据库，其他请求等着。

**缓存雪崩**：大量 key 同时过期。解法是给过期时间加个随机偏移量，别让它们集中过期。

加缓存本身不难，真正费脑子的是缓存和数据库的数据一致性——这个坑够单独写一篇的，这里不展开了。

### 虚拟线程：Java 21 之后的大杀器

如果你用的是 Java 21+ 和 Spring Boot 3.2+，有一个几乎零成本的优化手段：

```text
spring:
  threads:
    virtual:
      enabled: true
```

一行配置，Spring Boot 自动把 Tomcat 的工作线程换成虚拟线程。

传统线程是操作系统线程，每个占 1MB 栈内存，创建和切换成本高。虚拟线程是 JVM 层面的轻量级线程，初始栈只有几 KB，创建成本极低。你可以同时跑几十万个虚拟线程，操作系统根本不知道它们的存在。

效果有多猛？有人做过对比测试：同样的代码同样的硬件，开虚拟线程后吞吐量从 1400 req/s 飙到 2700 req/s，接近翻倍。IO 密集场景下效果尤其明显——虚拟线程在等 IO 的时候会自动让出底层的操作系统线程，让别的虚拟线程上去跑。以前 200 个线程傻等 IO，现在几万个虚拟线程轮流用这 200 个操作系统线程，利用率一下就上来了。

不过虚拟线程不是万能药。你的接口要是主要在做 CPU 计算（加密、压缩、复杂业务逻辑），开虚拟线程没啥用——CPU 本身就是瓶颈，跟线程模型没关系。

还有一个坑：Java21 里虚拟线程在synchronized块中会"钉"在操作系统线程上不让出来（pinning）。Java 24（JEP 491）已经修了这个问题，如果用Java 24+（Spring Boot 3.4+）就不用担心了。还在21/23 上的话，遇到synchronized频繁阻塞的场景可以先换成ReentrantLock绕过去。

### 不要本末倒置

聊了这么多手段，但实际操作的时候别搞反了顺序。

投入产出比最高的是**查慢 SQL、加索引**。一条慢 SQL 从 2 秒优化到 20 毫秒，等于释放了 100 倍的线程占用时间，比任何参数调优都猛。

然后是**加缓存**——热点数据丢 Redis，数据库压力直接降一个数量级。再然后是**异步化**——非核心逻辑扔到异步线程池或消息队列里。Java 21+ 的话**虚拟线程**一行配置就完事，IO 密集场景下吞吐量翻倍。

Tomcat 和连接池参数是最后微调的东西。至于 WebFlux——代码写法跟 Spring MVC 完全不一样，学习成本高、调试困难、生态兼容性也差。除非真的要扛每秒几万并发，否则 Spring MVC + 虚拟线程已经够了。

大部分”并发上不去”的问题，最后发现都不是线程不够，是某条 SQL 太慢或者某个外部调用太磨叽。把这些钉子拔掉之后，默认的 200 线程可能就够用了。