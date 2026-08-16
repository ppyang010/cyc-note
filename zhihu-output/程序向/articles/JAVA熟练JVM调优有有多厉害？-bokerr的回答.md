---
id: "3148735027"
title: "JAVA熟练JVM调优有有多厉害？"
author: "bokerr"
type: zhihu-answer
source: "https://www.zhihu.com/question/427461208/answer/3148735027"
created: "2023-08-03 19:09"
updated: "2023-08-03 19:09"
collected: "2023-08-03 19:09"
downloaded: "2026-08-16"
---
有两次调优经验，事实上证明都是人的锅，代码写好点哪里有需要JVM调优。

或者你可以把我的话翻译成，jvm调优某种程度上能帮助你发现你代码上的问题，改掉他自然就不会OOM了。推荐的工具： JProfile 能直接打堆快照进行对比，很容易发现问题的症结在哪。

试想一下，一门语言需要开发者频繁调试它的虚拟机环境，这说明它可能缺陷蛮大的。