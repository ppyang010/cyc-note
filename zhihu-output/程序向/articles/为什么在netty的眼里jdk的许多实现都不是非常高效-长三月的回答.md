---
id: "2748225569"
title: "为什么在netty的眼里jdk的许多实现都不是非常高效?"
author: "长三月"
type: zhihu-answer
source: "https://www.zhihu.com/question/269619656/answer/2748225569"
created: "2022-11-07 16:19"
updated: "2022-11-29 09:41"
collected: "2022-11-07 16:19"
downloaded: "2026-08-16"
---
因为**不能脱离使用场景谈高效**。JDK的设计在通用性上更好，而Netty的设计更适合高并发、网络通信的场景。

随便举几个例子，比较下两者实现上的区别。

**1\. ThreadLocal实现**

就底层的哈希算法而言，ThreadLocal是基于非波拉契散列法和开放寻址，计算结果在空间分布上更加均匀。

而Netty的FastThreadLocal是基于数组下标递增，有效避免了哈希碰撞，并降低了rehash的开销，更适合高并发的场景。

  

**2\. 堆外内存释放机制**

JDK提供堆外内存的封装类DirectByteBuffer，初始化时会默认开启Cleaner，作用是当DirectByteBuffer被GC时能自动调用Cleaner.clean()清理堆外内存，避免泄漏。

但Cleaner在内存分配和回收上会带来额外的性能开销。为此Netty提供了**No Cleaner**策略，不再创建Cleaner，而是通过retain/release操作手动释放，从而获得性能提升。

不过，或许是认识到了该策略带来的内存泄漏风险，Netty 5又将No Cleaner策略设置为默认不开启，作为可选择的高阶用法，需要通过指定JVM启动参数来开启。

  

**3\. 线程池实现**

JDK的线程池内部维护了一个类型为BlockingQueue的taskqueue来保存任务队列，当线程从该队列获取任务会产生锁竞争降低性能。

Netty的解决办法是，每个channel创建时**固定绑定到一个IO线程**(NioEventLoop)上，其后channel上产生的IO任务也固定由这个线程处理，避免了**线程池级别**上的任务竞争。

不过你可能会提出疑问：除了IO任务，IO线程还会处理一些其他线程提交的异步任务和定时任务呀，在**线程内部**不是仍然会发生任务队列竞争吗？

原来Netty在这里使用了JCTools提供的**MpscQueue**（多生产者单消费者队列），它内部使用CAS避免了JDK中BlockingQueue的锁竞争，从来带来更好的性能。

Netty在内部大量使用了MpscQueue，如HashedWheelTimer、Recycler、PoolThreadCache，这些场合都适合使用这种无锁非阻塞队列。