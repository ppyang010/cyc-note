---
id: "1996522606258565627"
title: "Kafka 为什么要抛弃 ZooKeeper？"
author: "花宝宝"
type: zhihu-answer
source: "https://www.zhihu.com/question/624795964/answer/1996522606258565627"
created: "2026-01-19 10:01"
updated: "2026-01-19 10:01"
collected: "2026-01-19 10:01"
downloaded: "2026-08-16"
---
说白了，Kafka 当初用 ZooKeeper，就是创业公司租共享办公室的逻辑——基础设施让别人管，自己专心写业务。ZooKeeper 那套 Paxos/ZAB 协议，搞分布式一致性是真的稳，Kafka 直接拿来用省了多少事。  
  
但问题是，Kafka 长大了。  
  
当年设计 ZooKeeper 的时候，没人想过会有系统需要管理几十万个分区。ZooKeeper 的数据模型是个树形结构，所有写操作都要过 Leader，读可以分散但写是串行的。Kafka 每创建一个分区、每次 Leader 切换，都要往 ZooKeeper 里写一笔。分区少的时候没感觉，分区一多，ZooKeeper 就成了整个系统的咽喉。  
  
我见过最夸张的情况是，一个大集群创建 Topic 要等好几分钟，不是 Kafka 慢，是 ZooKeeper 那边排队呢。  
  
还有个更头疼的问题：Kafka 的 Controller 选举依赖 ZooKeeper 的 Session 机制。这玩意儿对网络抖动特别敏感，JVM 来一次长 GC，Session 超时，ZooKeeper 就认为 Controller 挂了，触发重新选举。然后整个集群的分区 Leader 跟着重新分配，业务侧看到的就是一波短暂的不可用。明明啥事没有，就是虚惊一场。  
  
运维的兄弟们最烦的是出问题的时候。Kafka 集群出故障，你得先判断是 Kafka 自己的问题还是 ZooKeeper 的问题。两套系统，两套监控，两套升级流程，两套知识体系。有时候 Kafka 看着正常，但 ZooKeeper 那边 Session 过期了，症状还是 Kafka 不可用。这种"症状在 A，病根在 B"的架构，排查起来想骂人。  
  
KRaft 干的事情很简单：把元数据管理这块收回来自己干。  
  
技术上，它用 Raft 协议替代了 ZooKeeper 的 ZAB。Raft 和 ZAB 本质上都是解决分布式一致性的，但 KRaft 的实现是专门为 Kafka 的场景优化的。元数据不再存在外部系统里，而是作为一个特殊的内部 Topic（\_\_cluster\_metadata）存在 Kafka 自己的日志里。Controller 现在叫 Quorum Controller，选举走的是 Raft，不再依赖外部 Session。  
  
实际效果：部署从"先搭 ZK 再搭 Kafka"变成"直接启动 Kafka"，集群启动时间从分钟级降到秒级，分区数上限从十万级跃升到百万级。  
  
对于新集群，直接用 KRaft 模式，没有任何理由再引入 ZooKeeper。老集群的话，官方提供了迁移工具，但迁移有风险，建议找个业务低峰期，先在测试环境跑通了再上生产。  
  
从 2.8 开始试验，到 3.3 正式 GA，再到现在 3.6/3.7 彻底稳定，KRaft 已经不是什么新鲜事物了。如果你的集群还在用 ZooKeeper，不是不能用，但确实该开始规划迁移了。