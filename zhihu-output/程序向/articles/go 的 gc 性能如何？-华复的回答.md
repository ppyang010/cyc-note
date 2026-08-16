---
id: "2928177117"
title: "go 的 gc 性能如何？"
author: "华复"
type: zhihu-answer
source: "https://www.zhihu.com/question/583328068/answer/2928177117"
created: "2023-03-09 11:29"
updated: "2023-03-09 11:29"
collected: "2023-03-09 11:29"
downloaded: "2026-08-16"
---
go的gc基本就是只关心延迟，不关心吞吐。每次宣传只宣传"STW时间低于1毫秒"，不说有多少百分比用作GC，以及内存碎片导致长期运行的程序的内存分配被拖慢了多少