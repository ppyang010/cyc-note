---
id: "2175382980"
title: "async/await异步模型是否优于stackful coroutine模型？"
author: "hez2010"
type: zhihu-answer
source: "https://www.zhihu.com/question/65647171/answer/2175382980"
created: "2021-10-17 19:40"
updated: "2021-10-18 02:59"
collected: "2021-10-17 19:40"
downloaded: "2026-08-16"
---
仅 stackless coroutine 不会破坏 CPU 分支预测这一条就足够优于 stackful coroutine 了。利用 stackless coroutine 甚至能拿来做 CPU cache prefetch（可以把内存访问也视为 blocking I/O call），运行效率与手写状态机没有任何差别。

不过不是所有人都需要这样的性能

高性能异步方案：stackless

只是写写业务减小一下线程调度开销，还不想改多少代码：stackful