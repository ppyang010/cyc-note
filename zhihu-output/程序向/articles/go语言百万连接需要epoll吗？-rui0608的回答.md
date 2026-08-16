---
id: "3489689084"
title: "go语言百万连接需要epoll吗？"
author: "rui0608"
type: zhihu-answer
source: "https://www.zhihu.com/question/305373685/answer/3489689084"
created: "2024-05-06 23:53"
updated: "2024-05-08 12:47"
collected: "2024-05-06 23:53"
downloaded: "2026-08-16"
---
虽然是个老问题，给个现实世界案例分享吧，某大厂内部也造了类似这个东西的轮子：

[https://github.com/cloudwego/netpoll](https://link.zhihu.com/?target=https%3A//github.com/cloudwego/netpoll)[GitHub - panjf2000/gnet: gnet is a high-performance, lightweight, non-blocking, event-driven networking framework written in pure Go./ gnet 是一个高性能、轻量级、非阻塞的事件驱动 Go 网络框架。](https://link.zhihu.com/?target=https%3A//github.com/panjf2000/gnet)

也煞有介事地给出了Benchmark，也像这些轮子差不多，说是「特定场景下」「某些指标」能提高「XX%」，提高服务倒是也没有跨越量级，不存在「golang/net不能做到而我能做到」的场合。

然后呢，恰巧隔壁组在真实业务里尝试了一下，基本结论是：

-   对于一般业务类型的 RPC 服务（高吞吐，但非高并发），性能几乎不变
-   对于短时真超高并发（真实业务是热点事件推送服务），能节省很多内存（毕竟Goroutine少了很多很多），但吞吐、响应时间、CPU利用率，这些指标仍然看不出区别

  

如果知道 net 包在 Linux 上底层也是 epoll，并且是每个 IO 事件启动一个 goroutine 的方式来工作，那这个事情就不难理解，造轮子用一个 goroutine 承载多个 IO 事件，其实就是把 goroutine 当系统线程用，然后让这些「系统线程」用异步的方式处理 IO，说到底你做的事情就是把有栈协程换成了无栈协程，所以基本上就可以用「有栈协程 vs 无栈协程」来预测两者性能差别，最大收益当然也就是协程栈的内存开销。而其他方面是快是慢，一是看运气，二是扣细节，但可见的上限也就在那里。

实际上，就算把 goroutine “当作”「系统线程」来用，由于 Go 程序跑起来也是“在相对较少数量的有栈协程上运行无栈协程”，比起跑在系统线程上的无栈协程也是有些开销的，所以也并不是那么的划算。

仅对于以下情况，造/用这种轮子会有较大收益：

-   有大量业务团队只习惯用 Go
-   真的有很多高并发的场合（如果不是网关代理、推送、实时流服务，其实不太多见）
-   那些节省的内存对你们真的很重要

作为代价，用这些轮子要担心：

-   造轮子的成本、bug风险；用第三方轮子的bug风险、出问题时上游响应修复速度的风险
-   生态风险，包括：

-   如果要最强性能，则要基于轮子重造各种新caller代码（就跟造一个C++ IO轮子要重写一堆caller一样）
-   如果继续用开源基于 golang/net 的客户端，那么就是在模拟的无栈协程里启动新的有栈协程，损失性能回到 golang/net 水平，并且带来一定 bug 风险，这类 bug 都是疑难杂症不好解的

  

我个人偏好的答案是，如果坚定用 Go，先别管这些乱七八糟的，用 golang/net 糊一版，吃内存是可能的，但高并发也是能扛的，或者反过来说，golang/net + 堆内存扛不住的，在 golang 下造什么轮子也扛不住。

如果有这么大的决心造这么一个轮子只为了一个服务上用，我还是建议看看 C++ 或 Rust，一方面这种没有 Runtime 的语言效率本身就更好一级，另一方面，Rust 可能把你想要的轮子已经造好了，最流行的 tokio 就是 goroutine 高仿无栈协程版，也有 monoio 这种针对 proxy 类服务特别优化的 M:1 runtime 可供选择，对应场合下，性能上限比 tokio/goroutine 这类 M:N 型的可能更好，毕竟协程间没有跨线程数据同步的开销。