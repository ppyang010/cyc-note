---
Title: "为什么 AQS 成为 Java 并发的基石？"
Url: "https://zhuanlan.zhihu.com/p/2061000684242317463"
Author: "zhuhongyu这个世界有BUG"
Origin: "知乎专栏"
Description: "一个问题，也许每个写过 synchronized 的 Java 程序员都曾模糊地想过：为什么 ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock——这些看起来功能完全不同的并发工具——内部却共享着同一套骨…"
Tags:
  - "Java"
Created: "2026-07-28 15:15:23"
Cover: "https://picx.zhimg.com/v2-dd3df27551d774b27df2117b482fe640_l.jpg?source=32738c0c&needBackground=1"
---

[收录于 · 代码背后](https://www.zhihu.com/column/c_2060016088281248196)

8 人赞同了该文章

一个问题，也许每个写过 `synchronized` 的 Java 程序员都曾模糊地想过：

为什么 `ReentrantLock`、 `Semaphore`、 `CountDownLatch`、 `ReentrantReadWriteLock` ——这些看起来功能完全不同的并发工具——内部却共享着同一套骨架？

答案藏在一个不起眼的 [抽象类](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%8A%BD%E8%B1%A1%E7%B1%BB&zhida_source=entity) 里： `AbstractQueuedSynchronizer`，简称 AQS。它没有一句 [业务逻辑](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91&zhida_source=entity)，却撑起了整个 Java 并发大厦。这不是巧合，而是一场发生在 2000 年代初、关于”如何驯服锁”的工程运动的终点。

### 故事背景：monitor 的黄金时代与它的裂缝

Java 1.0 时代，并发的答案只有一个词： `synchronized`。这是 James Gosling 团队从 Hoare 和 Brinch Hansen 在 1970 年代提出的” [管程](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%AE%A1%E7%A8%8B&zhida_source=entity) ”（Monitor）模型里直接搬来的设计——每个对象自带一把锁， `wait()` / `notify()` 负责协调。

这个设计在当时是相当先进的。管程理论本身就是为了解决比 [信号量](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E4%BF%A1%E5%8F%B7%E9%87%8F&zhida_source=entity) 更容易出错的并发编程而生的：把锁和 [等待队列](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%AD%89%E5%BE%85%E9%98%9F%E5%88%97&zhida_source=entity) 封装进对象内部，程序员不用再手动摆弄 `P()` / `V()` 操作。

但进入 2000 年代， [服务端](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E7%AB%AF&zhida_source=entity) Java 开始承载真实世界的高并发系统——Web 容器、消息中间件、 [数据库连接池](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%9E%E6%8E%A5%E6%B1%A0&zhida_source=entity)。工程师们发现 `synchronized` 有一堆无法绕过的短板：

- 没有 [超时机制](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%B6%85%E6%97%B6%E6%9C%BA%E5%88%B6&zhida_source=entity)。线程一旦阻塞，只能死等，或者被 `interrupt`，没有”等 3 秒拿不到就放弃”这种选项。
- 不支持公平性选择。JVM 内置的 monitor 唤醒策略是不确定的，可能造成某些线程长期饥饿。
- 无法响应中断。线程在 `synchronized` 块里阻塞时， `Thread.interrupt()` 基本无能为力。
- 锁语义固定死。你没法自己实现一把” [读写分离](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%AF%BB%E5%86%99%E5%88%86%E7%A6%BB&zhida_source=entity) ”的锁，或者一个”允许 N 个线程同时通过”的信号量——除非从零手搓一套等待队列。

而”从零手搓”正是当时的常见做法：每一种同步工具都自己维护一个链表或队列，自己处理线程的挂起和唤醒，自己应对 [虚假唤醒](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%99%9A%E5%81%87%E5%94%A4%E9%86%92&zhida_source=entity) （spurious wakeup）、 [竞态条件](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%AB%9E%E6%80%81%E6%9D%A1%E4%BB%B6&zhida_source=entity)、内存可见性。代码重复、极易出错，而且性能参差不齐——因为每个人对”如何高效地排队等锁”的理解深度都不一样。

### 旧方案为什么不够用？

在 AQS 出现之前，业界已经尝试过不少排队等锁的方案，各有各的道理，也各有各的死角。

**基于 `synchronized` 手写等待逻辑**：简单，但如前所述，功能贫瘠，且每个 [开发者](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%BC%80%E5%8F%91%E8%80%85&zhida_source=entity) 重新发明轮子，质量参差不齐。

**[自旋锁](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%87%AA%E6%97%8B%E9%94%81&zhida_source=entity) （Spin Lock）**：线程不断轮询锁状态，避免了线程 [上下文切换](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E4%B8%8A%E4%B8%8B%E6%96%87%E5%88%87%E6%8D%A2&zhida_source=entity) 的开销。在锁持有时间极短、CPU 核心充裕的场景下很快，但一旦锁被长时间占用，自旋线程会疯狂空转，白白烧掉 CPU。

**简单的 FIFO [链表队列](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E9%93%BE%E8%A1%A8%E9%98%9F%E5%88%97&zhida_source=entity) + 全局锁保护**：用一把”锁的锁”来保护等待队列本身的增删操作。这带来了新的瓶颈——排队这件事本身又变成了一个热点竞争点， [高并发](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=2&q=%E9%AB%98%E5%B9%B6%E5%8F%91&zhida_source=entity) 下反而互相拖累。

真正棘手的问题不是”要不要排队”，而是 **如何用尽可能少的 CAS（Compare-And-Swap）操作、尽可能不加锁的方式，维护一条正确、高效、可中断、可超时的等待队列**。这是一个纯粹的 [数据结构](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84&zhida_source=entity) 与并发算法问题，而不是业务问题——这正是它需要被单独抽象出来的原因。

### 真正的突破：Doug Lea 与 CLH 队列的变形

2004 年， [JDK 5](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=JDK+5&zhida_source=entity) 发布， `java.util.concurrent` 包横空出世。这背后的主要设计者是 Doug Lea—— [纽约州立大学](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%BA%BD%E7%BA%A6%E5%B7%9E%E7%AB%8B%E5%A4%A7%E5%AD%A6&zhida_source=entity) 奥斯威戈分校的教授，也是 Java 社区流程（JCP）中 JSR-166 提案的负责人。

Doug Lea 早年做过大量关于并发 [数据结构与算法](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%8E%E7%AE%97%E6%B3%95&zhida_source=entity) 的研究，他没有从零发明一种排队算法，而是敏锐地借用并改造了一个已有的 [学术成果](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%AD%A6%E6%9C%AF%E6%88%90%E6%9E%9C&zhida_source=entity)： **[CLH 锁](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=CLH+%E9%94%81&zhida_source=entity)**。

CLH 锁得名于三位发明者——Travis Craig、Erik Landin、Anders Hagersten，最早是为了解决多处理器系统中的自旋锁扩展性问题而提出的一种链式队列锁。它的巧妙之处在于：每个等待的线程只需要自旋检测”前一个节点”的状态，而不是竞争同一个 [共享变量](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%85%B1%E4%BA%AB%E5%8F%98%E9%87%8F&zhida_source=entity)，从而把竞争压力分散到了整条链上，极大缓解了多核环境下的 [总线](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%80%BB%E7%BA%BF&zhida_source=entity) 争用。

Doug Lea 把这个思路做了一次关键的改造：原始 CLH 是纯自旋的，不适合等待时间可能很长的锁场景（自旋会白白耗电、耗 CPU）。他把它改造成了一个 **[双向链表](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%8F%8C%E5%90%91%E9%93%BE%E8%A1%A8&zhida_source=entity)**，并引入了线程的 **阻塞（park）与唤醒（unpark）** 机制——排在队列前面的线程可以自旋一小段时间尝试抢锁，抢不到就彻底挂起，把 CPU 让出来；被释放锁的线程负责显式唤醒队列中的下一个节点。

这个设计后来被写进了他 2004 年发表的论文《The java.util.concurrent Synchronizer Framework》，AQS 由此诞生。

### 源码里的体现：一个 state，两个抽象方法

AQS 的核心其实极简，只有一个 `volatile int state` 和一个 CLH 变体队列。真正体现 [设计哲学](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%AE%BE%E8%AE%A1%E5%93%B2%E5%AD%A6&zhida_source=entity) 的，是它的入队尝试逻辑：

```
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

这一行代码值得细品。 `tryAcquire` 是一个 **留白** 的方法，AQS 本身完全不实现它，只是先调用一下，看子类”你能不能直接拿到锁”。拿到了，直接返回，队列都不用碰。拿不到，才会走 `addWaiter` 把当前线程包装成节点塞进等待队列，然后在 `acquireQueued` 中反复尝试获取、必要时挂起。

这是一种典型的 **模板方法模式**：AQS 负责”排队、挂起、唤醒”这套通用而复杂的机制，把”到底什么叫拿到锁”这个业务判断，完全下放给子类。 `ReentrantLock` 里， `tryAcquire` 判断的是”state 是否为 0，或者当前线程是不是已经持有这把 [可重入](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%8F%AF%E9%87%8D%E5%85%A5&zhida_source=entity) 锁”； `Semaphore` 里，判断的是”剩余许可证数量是否大于 0”； `CountDownLatch` 里，判断的是”计数器是否已经归零”。同一套排队引擎，装上不同的判断逻辑，就变成了完全不同的并发工具。

### 设计思想：把”排队”这件事彻底工程化

AQS 集中体现了几种经典的 [工程思想](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%B7%A5%E7%A8%8B%E6%80%9D%E6%83%B3&zhida_source=entity)：

**模板方法模式**：框架定骨架，子类填血肉， `tryAcquire` / `tryRelease` / `tryAcquireShared` / `tryReleaseShared` 都是留给子类的钩子。

**CAS [无锁编程](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%97%A0%E9%94%81%E7%BC%96%E7%A8%8B&zhida_source=entity)**： `state` 的更新几乎全部通过 `compareAndSet` 完成，避免了”锁保护锁”的悖论。

**先自旋、后阻塞**：在真正调用 `LockSupport.park()` 让出 CPU 之前，会先做有限次数的快速重试，兼顾了短期竞争下的低延迟和长期等待下的 [低功耗](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E4%BD%8E%E5%8A%9F%E8%80%97&zhida_source=entity)。

**独占与共享两种模式**： `ReentrantLock` 用 [独占模式](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%8B%AC%E5%8D%A0%E6%A8%A1%E5%BC%8F&zhida_source=entity) （同一时刻只有一个线程能拿锁）， `Semaphore`、 `CountDownLatch`、 `ReentrantReadWriteLock` 的读锁用共享模式（多个线程能同时通过）。同一条队列、同一套唤醒逻辑，靠一个模式位区分行为，这是极致的复用。

### 为什么它最终赢了？

因为它把”造一把新锁”这件事的门槛，从”你得懂 [多线程](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%A4%9A%E7%BA%BF%E7%A8%8B&zhida_source=entity) 内存模型和 [无锁队列](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%97%A0%E9%94%81%E9%98%9F%E5%88%97&zhida_source=entity) ”降低到了”你只需要写清楚一个 `state` 该怎么增减”。

`ReentrantLock`、 `ReentrantReadWriteLock`、 `Semaphore`、 `CountDownLatch`、 `FutureTask`、 `ThreadPoolExecutor` 内部的 Worker [线程控制](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%BA%BF%E7%A8%8B%E6%8E%A7%E5%88%B6&zhida_source=entity)，全部构建在 AQS 之上。此后整个 Java 生态里，几乎所有需要”自定义同步语义”的场景，第一反应都是”继承 AQS”，而不是”自己写队列”。这也是为什么后来大量 [开源项目](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%BC%80%E6%BA%90%E9%A1%B9%E7%9B%AE&zhida_source=entity) （比如 Netty 的部分 [同步组件](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%90%8C%E6%AD%A5%E7%BB%84%E4%BB%B6&zhida_source=entity)、各种连接池实现）都选择直接复用或模仿这套框架，而不是重新发明。

它真正改变的，不是某一个 API，而是”实现 [同步器](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%90%8C%E6%AD%A5%E5%99%A8&zhida_source=entity) ”这件事本身的抽象层级——从算法问题，变成了配置问题。

### 有没有更好的方案？今天会不会不一样？

如果今天重新设计，一些边界确实已经开始松动。

[Project Loom](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=Project+Loom&zhida_source=entity) 带来的 **[虚拟线程](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E8%99%9A%E6%8B%9F%E7%BA%BF%E7%A8%8B&zhida_source=entity)** （JDK 21 正式发布）改变了”线程”本身极其昂贵的前提——过去 AQS 拼命省着用的挂起/唤醒开销，在虚拟线程的世界里成本结构完全不同了。JDK 团队为此专门对 `synchronized` 做了改造，让虚拟线程在阻塞时不再固定占用宝贵的平台线程（Carrier Thread）； `ReentrantLock` 系的 AQS 体系本身，在这方面反而比传统 `synchronized` 更早就对虚拟线程友好，因为它从来就是基于 [用户态](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%94%A8%E6%88%B7%E6%80%81&zhida_source=entity) 调度、而不依赖 JVM monitor 的。

`StampedLock` （JDK 8 引入）在读多写少的场景下，用乐观读的方式进一步减少了 CAS 竞争，是 AQS 思路的一次延伸而非替代。

但 AQS 的核心骨架——”用一个 [原子](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%8E%9F%E5%AD%90&zhida_source=entity) 状态位加一条无锁化的等待队列来解耦排队机制和业务语义”——这个思想本身并没有过时。硬件在变，语言特性在变,但”多个 [执行流](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E6%89%A7%E8%A1%8C%E6%B5%81&zhida_source=entity) 竞争一个有限资源”这个问题的数学本质没有变。

### 现实中的应用

`ReentrantLock`、 `ReentrantReadWriteLock`、 `Semaphore`、 `CountDownLatch`、 `CyclicBarrier` 的部分实现、 `FutureTask`、 [线程池](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E7%BA%BF%E7%A8%8B%E6%B1%A0&zhida_source=entity) `ThreadPoolExecutor` 的任务执行控制——几乎整个 JDK 并发包的骨架都建立在 AQS 上。这也是为什么无数依赖 JDK 并发工具的框架——Tomcat 的连接管理、各种数据库连接池、 [限流组件](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E9%99%90%E6%B5%81%E7%BB%84%E4%BB%B6&zhida_source=entity) ——本质上都在间接使用这套排队引擎。

### 一句话总结

优秀的 [并发框架](https://zhida.zhihu.com/search?content_id=279127818&content_type=Article&match_order=1&q=%E5%B9%B6%E5%8F%91%E6%A1%86%E6%9E%B6&zhida_source=entity)，从不是发明一种更聪明的锁，而是把”排队”这件最容易出错、最难写对的事情，从每个人的手里，收回到一个被反复验证过的骨架里。

![](https://pica.zhimg.com/v2-6e10f6fdf9eb1e5e409afab96b4655f6_1440w.jpg)

还没有人送礼物，鼓励一下作者吧

[所属专栏 · 5 小时前 更新](https://zhuanlan.zhihu.com/c_2060016088281248196)

![](https://pic1.zhimg.com/v2-e262780f3da97fefa4c795ef4ebd3e9c_720w.jpg?source=172ae18b)

代码背后

![](https://picx.zhimg.com/v2-dd3df27551d774b27df2117b482fe640_l.jpg?source=172ae18b)

zhuhongyu

34 篇内容 · 653 赞同

最热内容 ·

谁发明了 LSM Tree？

编辑于 2026-07-16 08:15・河南

[Java](https://www.zhihu.com/topic/19561132)

[程序员0基础入门大模型的学习路线！](https://zhuanlan.zhihu.com/p/31864213680)

0基础入门大模型，transformer、bert这些是要学的，但是 你的第一口不一定从这里咬下去。真的没有必要一上来就把时间精力全部投入到复杂的理论、各种晦涩的数学公式还有编程语言上，这...