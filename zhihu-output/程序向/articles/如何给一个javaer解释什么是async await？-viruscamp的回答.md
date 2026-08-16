---
id: "2226812619"
title: "如何给一个javaer解释什么是async await？"
author: "viruscamp"
type: zhihu-answer
source: "https://www.zhihu.com/question/498592362/answer/2226812619"
created: "2021-11-16 17:29"
updated: "2021-11-16 17:29"
collected: "2021-11-16 17:29"
downloaded: "2026-08-16"
---
Java 直到有了 `CompletableFuture` 才能和 JavaScript 的 `Promise` 或者 C# 的 `Task` 基本对标。 `Future` 就是个残废。 用 `CompletableFuture` 才能用 ea-async 做 async await 的编译时转换。

非要说是语法糖的话， await 是 `CompletableFuture` 链式callback 调用的语法糖。

```java
public class Store
{
    // 转换前
    public CompletableFuture<Boolean> buyItem(String itemTypeId, int cost)
    {
        if(!await(bank.decrement(cost))) {
            return completedFuture(false);
        }
        await(inventory.giveItem(itemTypeId));
        return completedFuture(true);
    }
    // 转换后
    public CompletableFuture<Boolean> buyItem(String itemTypeId, int cost)
    {
        return bank.decrement(cost)
            .thenCompose(result -> {
                if(!result) {
                    return completedFuture(false);
                }
                return inventory.giveItem(itemTypeId).thenApply(res -> true);
            });
    }
}
```