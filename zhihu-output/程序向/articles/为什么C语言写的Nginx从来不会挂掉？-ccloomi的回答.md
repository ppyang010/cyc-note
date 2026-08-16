---
id: "3210318655"
title: "为什么C语言写的Nginx从来不会挂掉？"
author: "ccloomi"
type: zhihu-answer
source: "https://www.zhihu.com/question/356952229/answer/3210318655"
created: "2023-09-14 08:29"
updated: "2024-04-07 16:30"
collected: "2023-09-14 08:29"
downloaded: "2026-08-16"
---
这和语言没啥关系，听过恋爱病毒不，就是两个进程互相监督，谁死了就把对方重启，nginx就是这样保证服务不挂的。erlang的核心也是这样的，所以erlang写的服务极其稳定。