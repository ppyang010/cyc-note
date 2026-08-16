---
id: "2429917972"
title: "为什么Go的web框架速度还不如Java？"
author: "雅枫"
type: zhihu-answer
source: "https://www.zhihu.com/question/360929863/answer/2429917972"
created: "2022-04-08 20:25"
updated: "2022-04-08 20:25"
collected: "2022-04-08 20:25"
downloaded: "2026-08-16"
---
因为golang的优势是高并发，高并发并不等于QPS，举个例子，单纯比qps，基于同步多进程的apache并不比异步模型的nginx差多少（最多2-3倍的样子，没有数量级的劣势），但是由于nginx是异步模型，他可以搞定同时保持几十万个连接。而apache估计10000个连接就直接炸了，因为系统没能力管理几十万个线程/进程。

所以高并发只取决于编程模型，只要是异步或者协程模型的服务器，qps可能不高，但是能切实解决高并发问题，比如python写的tornado。