---
id: "3236229560"
title: "C语言中自己实现了一个排序，为什么会比 qsort 的速度慢几十倍不止?"
author: "小人物"
type: zhihu-answer
source: "https://www.zhihu.com/question/624637687/answer/3236229560"
created: "2023-10-04 13:00"
updated: "2023-10-04 13:00"
collected: "2023-10-04 13:00"
downloaded: "2026-08-16"
---
qsort一般主体是快排（快速排序），然后写法上有些优化，比如最大递归深度不超过32/64（取决于32/64位平台）、排的差不多了就转为插入排序。可以参考如下链接

[https://codebrowser.dev/glibc/glibc/stdlib/qsort.c.html](https://link.zhihu.com/?target=https%3A//codebrowser.dev/glibc/glibc/stdlib/qsort.c.html)