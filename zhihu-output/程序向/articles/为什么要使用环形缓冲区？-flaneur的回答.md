---
id: "4220126272"
title: "为什么要使用环形缓冲区？"
author: "flaneur"
type: zhihu-answer
source: "https://www.zhihu.com/question/723167785/answer/4220126272"
created: "2024-10-05 11:40"
updated: "2024-10-07 12:23"
collected: "2024-10-05 11:40"
downloaded: "2026-08-16"
---
ring buffer 基本上是经过几十年探索后高性能 ipc 的最优解了，这东西又简单又对 cache 友好，还对同步友好。

吞吐高的时候对着 ring buffer 跑 busy polling 秒杀中断，讲究一个力大砖飞。

NVMe 跟网卡队列就都是 ring buffer。这块的套路就是中断嫌慢了就 busy loop。

go 的 channel 里面也是个 ring buffer。

[高性能交易系统](https://link.zhihu.com/?target=https%3A//www.evanjones.ca/lmax-disruptor.html)也用 ring buffer。