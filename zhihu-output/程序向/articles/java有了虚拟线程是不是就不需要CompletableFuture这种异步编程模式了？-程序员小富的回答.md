---
id: "2059922531734312753"
title: "java有了虚拟线程是不是就不需要CompletableFuture这种异步编程模式了？"
author: "程序员小富"
type: zhihu-answer
source: "https://www.zhihu.com/question/641001582/answer/2059922531734312753"
created: "2026-07-13 08:50"
updated: "2026-07-13 08:50"
collected: "2026-07-13 08:50"
downloaded: "2026-08-16"
---
不是，CompletableFuture 和 虚拟线程它俩解决的问题有交集但不完全重叠。

**虚拟线程替代了 CompletableFuture 的一部分**

CompletableFuture 被大量使用的一个核心原因是：**平台线程太贵了**。

以前一个线程占 1MB 栈内存，开几千个线程 JVM 就扛不住了。所以你不敢给每个 IO 操作都分配一个线程去同步等待，只能用 CompletableFuture 把阻塞操作变成非阻塞的回调链。

```text
// 以前不得不这么写，因为线程不够用
CompletableFuture.supplyAsync(() -> queryUser(userId))
    .thenApply(user -> queryOrders(user))
    .thenApply(orders -> calcTotal(orders))
    .thenAccept(total -> sendResponse(total));
```

用回调链来避免线程阻塞等待，让少量线程能服务大量请求。

虚拟线程出来之后，可以同时开几十万个虚拟线程，每个虚拟线程成本极低，也就是几 KB。所以上面那段代码可以直接写成同步风格：

```text
// 虚拟线程下，直接写同步代码就行
Thread.startVirtualThread(() -> {
    User user = queryUser(userId);      // 阻塞没关系，虚拟线程会自动挂起
    List<Order> orders = queryOrders(user);
    BigDecimal total = calcTotal(orders);
    sendResponse(total);
});
```

代码直观了十倍，没有回调问题，没有 thenApply 套 thenApply，debug 的时候堆栈也是正常的调用链，不像 CompletableFuture 那样堆栈断裂。

这部分场景，纯粹为了避免线程阻塞而使用 CompletableFuture 的，确实可以被虚拟线程替代。

**但 CompletableFuture 还有虚拟线程替代不了的部分**

CompletableFuture 不只是异步执行，它还是一个**编排工具**。

**1\. 并发组合**

比如要同时查用户信息、查订单列表、查积分余额，三个接口并行调用，全部完成后合并结果。

```text
CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> queryUser(id));
CompletableFuture<List<Order>> orderFuture = CompletableFuture.supplyAsync(() -> queryOrders(id));
CompletableFuture<Integer> pointsFuture = CompletableFuture.supplyAsync(() -> queryPoints(id));

CompletableFuture.allOf(userFuture, orderFuture, pointsFuture).join();

// 三个结果都拿到了，合并
UserProfile profile = merge(userFuture.join(), orderFuture.join(), pointsFuture.join());
```

虚拟线程也能做，但得自己管理：

```text
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var userTask = scope.fork(() -> queryUser(id));
    var orderTask = scope.fork(() -> queryOrders(id));
    var pointsTask = scope.fork(() -> queryPoints(id));
    scope.join();
    scope.throwIfFailed();
    UserProfile profile = merge(userTask.get(), orderTask.get(), pointsTask.get());
}
```

StructuredTaskScope 是 Java 21 引入的结构化并发 API，可以看作是虚拟线程世界里的 `allOf`。但这个 API 到现在还是预览状态，而且功能上不如 CompletableFuture 灵活。

**2\. anyOf / 竞速模式**

三个搜索引擎同时查，谁先返回用谁的结果：

```text
CompletableFuture.anyOf(searchGoogle(), searchBing(), searchBaidu())
    .thenAccept(result -> useResult(result));
```

这种谁先完成用谁的模式，用虚拟线程写起来要麻烦不少，得用 `StructuredTaskScope.ShutdownOnSuccess`，代码更啰嗦。

**3\. 异常处理和降级**

```text
CompletableFuture.supplyAsync(() -> queryFromMainDB())
    .exceptionally(ex -> queryFromBackupDB())  // 主库挂了自动切备库
    .thenApply(data -> transform(data))
    .handle((result, ex) -> {
        if (ex != null) return defaultValue();
        return result;
    });
```

这种链式的异常处理和降级逻辑，CompletableFuture 的 API 天然支持。虚拟线程里你得用 try-catch 一层层写，功能一样但代码组织方式不同。

**4\. 超时控制**

```text
CompletableFuture.supplyAsync(() -> slowQuery())
    .orTimeout(3, TimeUnit.SECONDS)           // 3秒超时
    .completeOnTimeout(defaultValue(), 3, TimeUnit.SECONDS);  // 超时给默认值
```

这种声明式的超时控制，写起来很简洁。虚拟线程也能做，但得配合 `Future.get(timeout)` 或者 `StructuredTaskScope` 的超时参数。

  

虚拟线程让在新代码里可以少写很多 CompletableFuture，尤其是那种纯粹为了异步不阻塞而写的场景。但 CompletableFuture 作为任务编排工具的价值还在，短期内不会消失。

  

实际开发建议，新项目里简单的异步 IO 用虚拟线程 + 同步写法；复杂的多任务编排、竞速、降级场景，CompletableFuture 该用还是用。

两者混用也完全没问题，CompletableFuture 可以提交到虚拟线程的 Executor 上跑。