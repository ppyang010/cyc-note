---
id: "231020763"
title: "如何评价百度开源的 RPC 框架 brpc？"
author: "张明锋"
type: zhihu-answer
source: "https://www.zhihu.com/question/65370268/answer/231020763"
created: "2017-09-16 21:03"
updated: "2017-09-17 13:29"
collected: "2017-09-16 21:03"
downloaded: "2026-08-16"
---
文档写的一级棒！！佩服，典范！！真的，这绝对是内部开发文档放出来了。各个技术点讲的通透，框架分解清晰。什么是t8,t9架构师应该有的素养。这就是！佩服

  

  

都说开发文档也是战斗力的体现，绝对是国内开源领域的良心之作。

  

这绝对是个良心项目，学习rpc架构的经典之作。

  

  

  

真心建议rpc开发的同学或者c++开发的同学看下这个项目，该项目的文档绝对是一个宝库。

其中不仅提供了实现说明而且写清楚了技术选型时候的考量。绝对是各个infra架构师值得反复通读的经典之作。我这两天都舍不得睡觉了。好项目，经典！

  

比如：讲bthread m:n模式时候

  

[brpc/brpc](https://link.zhihu.com/?target=https%3A//github.com/brpc/brpc/blob/master/docs/cn/bthread.md)

## NonGoals

  

-   提供pthread的兼容接口，只需链接即可使用。**拒绝理由**: bthread没有优先级，不适用于所有的场景，链接的方式容易使用户在不知情的情况下误用bthread，造成bug。
-   覆盖各类可能阻塞的glibc函数和系统调用，让原本阻塞系统线程的函数改为阻塞bthread。**拒绝理由**:  
    1\. bthread阻塞可能切换系统线程，依赖系统TLS的函数的行为未定义。2. 和阻塞pthread的函数混用时可能死锁。3.  
    这类hook函数本身的效率一般更差，因为往往还需要额外的系统调用，如epoll。但这类覆盖对N:1合作式线程库(fiber)有一定意义：虽然函数  
    本身慢了，但若不覆盖会更慢（系统线程阻塞会导致所有fiber阻塞）。
-   修改内核让pthread支持同核快速切换。**拒绝理由**:  
    拥有大量pthread后，每个线程对资源的需求被稀释了，基于thread-local  
    cache的代码效果会很差，比如tcmalloc。而独立的bthread不会有这个问题，因为它最终还是被映射到了少量的pthread。  
    bthread相比pthread的性能提升很大一部分来自更集中的线程资源。另一个考量是可移植性，bthread更倾向于纯用户态代码。

  

这真心是内部开发文档放出来了呀，我去。

[brpc/brpc](https://link.zhihu.com/?target=https%3A//github.com/brpc/brpc/blob/master/docs/cn/bthread.md)

会。比如有8个pthread worker，当有8个bthread都调用了系统usleep()后，处理网络收发的RPC代码就暂时无法运行了。只要阻塞时间不太长, 这一般**没什么影响**, 毕竟worker都用完了, 除了排队也没有什么好方法.  
在brpc中用户可以选择调大worker数来缓解问题, 在server端可设置[ServerOptions.num\_threads](https://link.zhihu.com/?target=https%3A//github.com/brpc/brpc/blob/master/docs/cn/server.md%23worker%25E7%25BA%25BF%25E7%25A8%258B%25E6%2595%25B0)或[\-bthread\_concurrency](https://link.zhihu.com/?target=http%3A//brpc.baidu.com%3A8765/flags/bthread_concurrency), 在client端可设置[\-bthread\_concurrency](https://link.zhihu.com/?target=http%3A//brpc.baidu.com%3A8765/flags/bthread_concurrency).

那有没有完全规避的方法呢?

  

-   一个容易想到的方法是动态增加worker数. 但实际未必如意, 当大量的worker同时被阻塞时,  
    它们很可能在等待同一个资源(比如同一把锁), 增加worker可能只是增加了更多的等待者.
-   那区分io线程和worker线程? io线程专门处理收发, worker线程调用用户逻辑, 即使worker线程全部阻塞也不会影响io线程. 但增加一层处理环节(io线程)并不能缓解拥塞, 如果worker线程全部卡住, 程序仍然会卡住,  
    只是卡的地方从socket缓冲转移到了io线程和worker线程之间的消息队列. 换句话说, 在worker卡住时,  
    还在运行的io线程做的可能是无用功. 事实上, 这正是上面提到的**没什么影响**真正的含义. 另一个问题是每个请求都要从io线程跳转至worker线程, 增加了一次上下文切换, 在机器繁忙时, 切换都有一定概率无法被及时调度, 会导致更多的延时长尾.
-   一个实际的解决方法是[限制最大并发](https://link.zhihu.com/?target=https%3A//github.com/brpc/brpc/blob/master/docs/cn/server.md%23%25E9%2599%2590%25E5%2588%25B6%25E6%259C%2580%25E5%25A4%25A7%25E5%25B9%25B6%25E5%258F%2591), 只要同时被处理的请求数低于worker数, 自然可以规避掉"所有worker被阻塞"的情况.
-   另一个解决方法当被阻塞的worker超过阈值时(比如8个中的6个), 就不在原地调用用户代码了, 而是扔到一个独立的线程池中运行.  
    这样即使用户代码全部阻塞, 也总能保留几个worker处理rpc的收发. 不过目前bthread模式并没有这个机制, 但类似的机制在[打开pthread模式](https://link.zhihu.com/?target=https%3A//github.com/brpc/brpc/blob/master/docs/cn/server.md%23pthread%25E6%25A8%25A1%25E5%25BC%258F)时  
    已经被实现了. 那像上面提到的, 这个机制是不是在用户代码都阻塞时也在做"无用功"呢? 可能是的.  
    但这个机制更多是为了规避在一些极端情况下的死锁, 比如所有的用户代码都lock在一个pthread mutex上,  
    并且这个mutex需要在某个RPC回调中unlock, 如果所有的worker都被阻塞, 那么就没有线程来处理RPC回调了, 整个程序就死锁了.  
    虽然绝大部分的RPC实现都有这个潜在问题, 但实际出现频率似乎很低, 只要养成不在锁内做RPC的好习惯, 这是完全可以规避的.