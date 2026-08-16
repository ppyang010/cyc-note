---
id: "2973109071"
title: "如何说服技术老大用redis？"
author: "rui0608"
type: zhihu-answer
source: "https://www.zhihu.com/question/592335961/answer/2973109071"
created: "2023-04-07 19:40"
updated: "2023-04-09 09:19"
collected: "2023-04-07 19:40"
downloaded: "2026-08-16"
---
你说的对，但是 Redis 的全称是 Remote Dictionary Server，即远程的字典服务。

据 Google 计算机科学家 Jeff Dean 发布的数据 “[Latency Numbers Everyone Should Know](https://link.zhihu.com/?target=https%3A//static.googleusercontent.com/media/sre.google/zh-CN//static/pdf/rule-of-thumb-latency-numbers-letter.pdf)”，从 1Gbps 网络获取 1MB 数据时间开销大约为 10ms，而假如我们能直接从内存中读取，那么这 1MB 数据仅需要 0.002ms，就带来了 5000 倍的性能提升。

国内互联网大厂大量利用 Redis 作为缓存中间层，其网络序列化开销、IO 系统调用开销，经常成为 IO-Bounded 服务的最大瓶颈，大量的微服务每天只再重复做一件事情，那就是接收一个请求，反序列化、序列化发送给另一个地方，接收响应后再反序列化、再序列化。

面对这种世纪性性能难题，您的技术老大使用了一种具有革命性的全新缓存架构，后来我们才得知，这种技术称作 Local Dictionary Service，简称 Lodis，该技术架构另辟蹊径，以巧妙的方式，在达到相同功能的前提下，不但规避掉了四次序列化与反序列化中的至少两次，并且完全避免了系统 IO 调用，甚至还节省了大量外部 Paas 服务的使用需求和成本。

首次看到基于 Lodis 缓存架构的时候，我甚至为之一振，世间竟可用如此巧妙的方法解决现实问题，大量减少 CPU 使用开销，明显提升单机性能，并大量减少 Paas 服务的资源需求，这非常契合当今互联网公司降本增效的主旋律。

目前看，Lodis 也是新兴的技术，但下一代的高级字典服务（High-level Dictionary Service，简称 Hides）也已如雨后春笋般如火如荼地进行，Hides 将在并发访问、分区、面向 CPU Cache 优化等方向继续更进一步，深耕整个服务端缓存架构行业。

我很羡慕您能跟着您的技术老大，了解当今世界最先进的缓存架构技术，您的技术老大可能是仅次于 Jeff Dean 般的存在，相信您的前途也是无量。