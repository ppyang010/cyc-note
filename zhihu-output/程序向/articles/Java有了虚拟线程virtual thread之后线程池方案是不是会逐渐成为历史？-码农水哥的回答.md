---
id: "3508077714"
title: "Java有了虚拟线程(virtual thread)之后线程池方案是不是会逐渐成为历史？"
author: "码农水哥"
type: zhihu-answer
source: "https://www.zhihu.com/question/557372897/answer/3508077714"
created: "2024-05-24 00:40"
updated: "2024-05-24 00:40"
collected: "2024-05-24 00:40"
downloaded: "2026-08-16"
---
代码如诗，你我皆为诗人。大家好，我是水哥，一个在软件开发领域深耕多年的资深工程师。

水哥今天想聊聊关于在应用 Java 虚拟线程的时候那些该做和不该做的事~

水哥希望通过本文，能给大家提供一些指导，帮助大家了解何时可以使用虚拟线程，何时更适合使用平台线程。

Java 虚拟线程（简称 VT）有别于以往我们熟知的 Java 线程（现在叫平台线程）。在之前的文章《[探秘Java：虚拟线程 Virtual Thread](https://zhuanlan.zhihu.com/p/697067780)》中，水哥已经对VT的定义和工作原理进行了介绍。感兴趣的童鞋可以点击查阅。

我们开始今天的内容。

## 1

**Dos：Write Simple, Synchronous Code Employing Blocking I/O APIs in the Thread-Per-Request Style**

**编写简单、同步的代码，采用“一个请求对应一个虚拟线程”的方式使用阻塞 I/O API。**

**Don'ts：Avoid mixing synchronous, blocking code with asynchronous frameworks.**

**避免将同步、阻塞的代码与异步框架混合使用。**

在使用 VT 之前，我们通常用异步调用处理一些阻塞性的业务，来避免阻塞服务器的请求处理线程。看个官网的例子：

```java
CompletableFuture.supplyAsync(info::getUrl, pool)
.thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofString()))
.thenApply(info::findImage)
.thenCompose(url -> getBodyAsync(url, HttpResponse.BodyHandlers.ofByteArray()))
.thenApply(info::setImageData)
.thenAccept(this::process)
.exceptionally(t -> { t.printStackTrace(); return null; });
```

在这个例子中，需要去处理远程图片资源访问，这是一个耗时的操作，会阻塞当前调用线程。我们通常会把处理逻辑放到异步线程中，并使用 CompletableFuture 对异步返回的结果进行进一步的回调处理。

在使用 VT 时候，上面的代码就不适用了，应该改成下面的写法：

```java
try {
   String page = getBody(info.getUrl(), HttpResponse.BodyHandlers.ofString());
   String imageUrl = info.findImage(page);
   byte[] data = getBody(imageUrl, HttpResponse.BodyHandlers.ofByteArray());   
   info.setImageData(data);
   process(info);
} catch (Exception ex) {
   t.printStackTrace();
}
```

这段代码我们放在 VT 上去执行非常合适，Java runtime 会帮我们调度 VT，我们无需担心对服务器工作线程的影响。现在，我们可以轻松地在一个 Java 进程中执行数百万条 VT，而不用像之前那样写各种异步调用和回调函数，以免对应用的性能造成过多影响。

## 2

**Dos：Represent Every Concurrent Task as a Virtual Thread**

**将每个并发任务都表示为一个虚拟线程。**

**Dont's：Never Pool Virtual Threads**

**永远不要对虚拟线程进行池化。**

平台线程是一种相对昂贵的系统资源，因此我们必须通过池化来管理这些线程，并经常需要考虑应该设置多少线程数。

虚拟线程不是用来表示某个资源的，而是用来表示某个任务，它是一种轻量级线程，因此我们无需对其进行池化。

## 3

**Dos：Use Semaphores to Limit Concurrency**

**使用信号量（Semaphores）来限制并发。**

**Don'ts：不要通过线程池来控制并发数。**

某些情况下，如果我们要去限制并发线程数，之前的做法是通过设定线程池的线程数量来实现的。例如：

```java
ExecutorService es = Executors.newFixedThreadPool(10);
...
Result foo() {
    try {
        var fut = es.submit(() -> callLimitedService());
        return f.get();
    } catch (...) { ... }
}
```

上例定义了一个只有 10 个线程的线程池。

但是，由于创建VT的成本并不高，我们无需对其进行池化。那么，我们如何限制VT的并发数呢？答案是使用**信号量（Semaphore）**。

举个栗子：

```java
Semaphore sem = new Semaphore(10);
...
Result foo() {
    sem.acquire();
    try {
        return callLimitedService();
    } finally {
        sem.release();
    }
}
```

在VT执行时，上述代码将VT的数量限制为最多10条同时执行，其他的VT将被阻塞等待。

## 4

**Dos：所有线程共享同一个不可变对象。**

**Don'ts：Don't Cache Expensive Reusable Objects in Thread-Local Variables**

**不要将昂贵的可重用对象缓存到线程本地变量中。**

一般我们用 ThreadLocal 去保存跟当前线程上下文有关的信息和线程间共享的可重用的对象缓存。VT 对于前一种用法是支持的，但对于后一种用法就不建议了。

对于这种可重用的对象缓存，通常是指那些创建成本高的非线程安全对象。如果每个线程都去创建这样的对象，成本将会非常高。因此，我们通常会通过 ThreadLocal 进行缓存，让所有线程共享同一个对象。例如：

```java
static final ThreadLocal<SimpleDateFormat> cachedFormatter = 
       ThreadLocal.withInitial(SimpleDateFormat::new);

void foo() {
  ...
	cachedFormatter.get().format(...);
	...
}
```

对于 VT 来讲，一个比较好的替代方案就是选择线程安全的对象，让所有 VT 去共享同一个对象。例如：

```java
static final DateTimeFormatter formatter = DateTimeFormatter….;

void foo() {
  ...
	formatter.format(...);
	...
}
```

上例中用了线程安全的 DateTimeFormatter 替换了线程不安全的 SimpleDateFormat，并在每个 VT 中共享同一个对象。

## 5

**Dos：在同步块或同步方法中执行短暂或不频繁的阻塞操作。**

**Don'ts：避免在同步块或同步方法中执行长时间和频繁的阻塞操作。**

在 VT 中的 synchronized 块或方法中执行阻塞操作，会导致到关联的 OS 线程被阻塞，这种情况称为“pinning（绑定、固定）”。这会使得其他 VT 都不能调度到这个 OS 线程，导致系统性能下降。为了避免 pinning 带来的性能问题，我们应使用 ReentrantLock 或其他锁机制来代替 synchronized 关键字。例如：

```java
synchronized(lockObj) {
    frequentIO();
}
```

可以改写为：

```java
lock.lock();
try {
    frequentIO();
} finally {
    lock.unlock();
}
```

## 总结

以上便是水哥总结的五个虚拟线程的“Dos and Don'ts”。

大家可以结合实际情况重新审视现有代码，考虑在升级到Java 21时是否可以利用虚拟线程来提升系统性能。新开发的应用也可以根据以上建议，采用符合虚拟线程设计意图的编码方式，以发挥虚拟线程的优势。

## 参考资料

[https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html](https://link.zhihu.com/?target=https%3A//docs.oracle.com/en/java/javase/21/core/virtual-threads.html)

如果您在技术探索的旅途中偶遇了这篇文章，水哥感到十分荣幸。感谢您抽出宝贵时间阅读至此。

若您觉得有所收获，不妨**点赞、分享**，让更多人一同受益。您的支持是我前进的动力。

想了解**精粹的软件开发技术、前沿的云计算实践、高效的敏捷管理策略**，敬请关注我（**码农水哥**），一起探索技术深度，享受敏捷之美。