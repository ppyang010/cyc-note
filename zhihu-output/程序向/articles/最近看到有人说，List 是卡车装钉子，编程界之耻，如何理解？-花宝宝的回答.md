---
id: "2012079191538029301"
title: "最近看到有人说，List<Integer> 是卡车装钉子，编程界之耻，如何理解？"
author: "花宝宝"
type: zhihu-answer
source: "https://www.zhihu.com/question/13077935547/answer/2012079191538029301"
created: "2026-03-03 08:17"
updated: "2026-03-04 10:07"
collected: "2026-03-03 08:17"
downloaded: "2026-08-16"
---
有人在代码审查里看到 `List<Integer>`，直接评论：卡车装钉子，编程之耻。

被审查的人懵了。他只是想存几个用户 ID，这有什么问题？

`List<Integer>` 里的 `Integer` 是对象，不是基本类型 `int`。一个 `int` 占 4 字节，一个 `Integer` 对象在 JVM 里是 16 字节对象头加 4 字节的值，内存对齐后 24 字节。存一个数字，实际用了 6 倍的内存。

还没完。`List<Integer>` 不是直接存对象本身，存的是引用——64 位 JVM 下每个引用 8 字节（开启指针压缩是 4 字节）。每个元素是一个引用指向一个散落在堆里的 Integer 对象，访问的时候 CPU 缓存命中率极低。

对比 `int[]`：元素紧密排列，连续内存，CPU 预取一次能拿一堆。

“卡车装钉子”这个比喻没错，你用一辆大卡车（Integer 对象）运一颗钉子（int 值），还把钉子散放在城市各处，要用的时候再一颗一颗去取。

但这不是你的写法有问题，是 Java 泛型设计的历史债。

Java 泛型有个东西叫**类型擦除**——泛型信息在编译后会被抹掉，`List<Integer>` 在运行时就是 `List<Object>`。这意味着 Java 的泛型根本没法用基本类型，`List<int>` 直接编译报错，你只能用 `List<Integer>`。

Kotlin 的 `List<Int>` 在编译后会尽量优化成 `int[]`，C# 的泛型是真泛型，`List<int>` 就是真的存 int。Java 在这一点上确实落后了，但这是 1998 年设计决策留下的坑。

“编程之耻”骂的其实是 Java 的泛型设计，不是写代码的人。

## 什么时候真的有问题

几十个、几百个元素的 `List<Integer>`，完全没问题，那点内存差距连噪声都算不上。

真正需要在意的是数据量上去之后。处理百万级整数的算法——排序、统计、矩阵运算——这时候 `List<Integer>` 的内存占用、GC 压力、缓存不友好会叠加起来，换 `int[]` 或者 `IntStream`，性能差距可以是数量级的。

业务逻辑里传几个 ID 的场景：

```text
List<Integer> userIds = getUserIds();
for (Integer id : userIds) {
    process(id);
}
```

这种代码不要动它，可读性好，没有性能问题。

`Set<Integer>` 和 `Map<Integer, ?>` 同理，功能上完全正确，只是有装箱开销。如果是高频查找的热点路径，Eclipse Collections 或 Koloboke 这类库提供了原始类型集合（`IntHashSet` 之类），但大多数业务场景根本用不到。

`Optional<Integer>` 稍微特殊一点，问题不只是装箱，还多了一层 Optional 对象的包装。Java 专门提供了 `OptionalInt` 来解决这个：

```text
OptionalInt result = IntStream.of(1, 2, 3).filter(x -> x > 1).findFirst();
```

性能敏感的路径上值得换，业务代码里没必要。

## Valhalla 做了快十年

Project Valhalla 从 2014 年就开始立项了，目标就是让 Java 支持值类型（Value Types）——让你能写 `List<int>`，让泛型真的能用基本类型，彻底解决这个历史问题。

到现在还没完全落地。Java 知道这是个问题，修了十年还没修完，可见这个历史债有多难还。