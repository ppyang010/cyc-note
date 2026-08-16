---
id: "2153467464"
title: "线程切换（context switch）大概需要多长时间？"
author: "Tony"
type: zhihu-answer
source: "https://www.zhihu.com/question/490502122/answer/2153467464"
created: "2021-10-04 10:55"
updated: "2021-10-04 10:55"
collected: "2021-10-04 10:55"
downloaded: "2026-08-16"
---
一般按us级别进行估算，即大几百个ns到几个us，都有可能。

但事情没有这么简单，因为contex switch切换，不仅仅是这个动作需要耗费多少时间，更重要的是，它导致cache丢失，包括两个：

1.  CPU cache
2.  TLB cache

这个丢失的cache的性能影响才是最大的，但多少无法估量，因为不知道程序后面（即切换回来）是如何读代码以及读数据的（即cache丢失和重新恢复的严重程度）。

所以，一般而言，我们用Context Switch，去换一个更慢的动作，比如磁盘或网络IO，这些IO，一般是ms级别的，这样做Thread Context Switch才是划算的。否则，不要轻易用Thread Context Switch，一般应该让线程尽量留在CPU core去进行尽可能多的运算（包括涉及某些IO接口，但实际很可能是读内存的IO接口，比如epoll，特别是non-blocking模式）。

如果有多个运算任务需要协调，可以考虑用协程（Coroutine或Goroutine），这些协程的Context Switch相比线程的Thread Context Switich，一样有Cache的损失，但要小一些（你可以估算为至少10倍左右的损失，相比单线程单计算任务）。

可以参考下面这个文章：

[Tony：单线程就比多线程性能差吗？不一定](https://zhuanlan.zhihu.com/p/397039359)