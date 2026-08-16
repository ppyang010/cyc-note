---
id: "66770881567"
title: "Java协程的引入会导致GC Root枚举复杂度大大增加，JVM是如何解决的呢？"
author: "rlei"
type: zhihu-answer
source: "https://www.zhihu.com/question/7919364045/answer/66770881567"
created: "2024-12-29 15:25"
updated: "2024-12-29 15:25"
collected: "2024-12-29 15:25"
downloaded: "2026-08-16"
---
Java Virtual Threads不是GC roots，根据[JEP 444](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/444):

> Unlike platform thread stacks, virtual thread stacks are not GC roots. Thus the references they contain are not traversed in a stop-the-world pause by garbage collectors, such as G1, that perform concurrent heap scanning.