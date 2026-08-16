---
id: "526002088"
title: "Paxos、Raft算法当前阶段比较稳定的，经过生产环境验证的开源实现有哪些？"
author: "codedump"
type: zhihu-answer
source: "https://www.zhihu.com/question/53344734/answer/526002088"
created: "2018-11-06 13:12"
updated: "2022-03-17 14:46"
collected: "2018-11-06 13:12"
downloaded: "2026-08-16"
---
我详细看过etcd的raft实现（这个部分应该是我看的最仔细的开源项目，目前没有之一），粗略看过微信团队的paxos实现。

  

etcd raft封装的很好，它不关注网络和具体的存储，把这部分留给上层使用者来实现，对外的接口就是各种Message，状态发生了改变需要通知上层的时候，通过一个叫Ready的数据结构来通知上层使用者。

  

这样做的好处是功能纯粹，易于测试验证。在etcd raft的测试用例中，大量标记的有针对大论文中哪一个部分进行验证测试的。（这里的“大论文”指的是《CONSENSUS: BRIDGING THEORY AND PRACTICE》）

  

我根据大论文做了一个我自己演绎的Raft算法原理分析，在这里：

[Raft算法原理](https://link.zhihu.com/?target=https%3A//lichuang.github.io/post/20180921-raft/)

另外也针对etcd raft做了一个比较详细的分析：

[etcd Raft库解析](https://link.zhihu.com/?target=https%3A//lichuang.github.io/post/20180922-etcd-raft/)

当我通读过之后，我发现etcd raft基本就是按照大论文的思路来写的，几乎没有什么太多的改动。我根据etcd 3.1.10版本拉出来一个项目，在这里加了很多阅读过程中的注释：

  

[https://github.com/lichuang/etcd-3.1.10-codedump](https://link.zhihu.com/?target=https%3A//github.com/lichuang/etcd-3.1.10-codedump)

  

而通常提到的另一篇论文，《In search of an Understandable Consensus Algorithm》，只能说是理解基本的raft算法原理吧，要真正写一个生产可用的，还是推荐看大论文，对着etcd raft一起看格外酸爽，因为没有了网络和存储，其实代码量并不大，再加上有对应的用例，我认为是性价比很高的项目，强烈推荐。

  

我自己也照着etcd raft的Go代码，撸了一份C++的，连用例也照着写了一份：

[lichuang/libraft](https://link.zhihu.com/?target=https%3A//github.com/lichuang/libraft)

  

当然etcd raft也不是啥问题都没有，我最想吐槽的是那个叫Storage的接口，里面声明的函数只有读相关的，没有写相关的，但是真正实现这个接口的MemoryStorage又自带了写相关的函数，那为啥又不把这些写相关的函数也放在接口声明里面呢？我给etcd项目提了一个问题，回答也不甚让我满意：

  

[Why raft.Storage interface not declare all MemoryStore function? · Issue #10183 · etcd-io/etcd](https://link.zhihu.com/?target=https%3A//github.com/etcd-io/etcd/issues/10183)

  

说完了etcd，接着说微信团队的paxos实现，我看的不算深入，就简单说两句。个人感觉对比起来，加上了网络、存储的时候就难测试，另外我之前尝试着在项目里面使用微信开源的协程库结果也出现了各种问题，市面上并没有除了微信团队之外使用这个paxos库的其他项目，所以基于此，不太推荐其他项目使用微信的项目，这是我自己得到的教训。

  

另外还有其他朋友看过braft的也说实现的很好，我有时间了一起看看再做个分析。

  

  

\======= 分割线 =========

2022.03.17更新，最近开始玩Rust，也加入了新的团队，目前我们有一款Rust版本的Raft库openraft，openraft是打造databend([https://github.com/datafuselabs/databend](https://link.zhihu.com/?target=https%3A//github.com/datafuselabs/databend))中metasrv的raft基础库，欢迎围观：

[https://github.com/datafuselabs/openraft](https://link.zhihu.com/?target=https%3A//github.com/datafuselabs/openraft)