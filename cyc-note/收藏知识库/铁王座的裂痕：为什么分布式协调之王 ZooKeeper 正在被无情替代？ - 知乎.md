[(99+ 封私信 / 28 条消息) 铁王座的裂痕：为什么分布式协调之王 ZooKeeper 正在被无情替代？ - 知乎](https://zhuanlan.zhihu.com/p/2061364936094356416) 

 一个问题开始
------

> 为什么曾经作为[大数据时代](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%A4%A7%E6%95%B0%E6%8D%AE%E6%97%B6%E4%BB%A3&zhida_source=entity)“绝对统治者”、让 Hadoop、[Kafka](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Kafka&zhida_source=entity)、HBase 心甘情愿交出灵魂控制权的 [ZooKeeper](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=ZooKeeper&zhida_source=entity)，会在云原生时代的滚滚铁骑下，被悄然移出历史的舞台中心？

### 故事背景：[雅虎](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E9%9B%85%E8%99%8E&zhida_source=entity)的“动物园”与失控的分布式世界

那是 2006 年前后，大数据的黄金时代拉开了序幕。

当时的 Google 凭借着“三驾马车”（GFS、[MapReduce](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=MapReduce&zhida_source=entity)、Bigtable）在[分布式](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=2&q=%E5%88%86%E5%B8%83%E5%BC%8F&zhida_source=entity)领域横着走。作为追赶者的雅虎（[Yahoo!](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Yahoo%21&zhida_source=entity)）决定发起绝地反击，孵化了著名的 **Hadoop** [开源生态](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%BC%80%E6%BA%90%E7%94%9F%E6%80%81&zhida_source=entity)。

然而，在分布式世界里，最难的不是写代码，而是**如何避免混乱**。

当数百台甚至数千台廉价服务器组成一个集群时，它们就像一个庞大社会中的市民，面临着永恒的难题：

*   谁是领导者（Master）？
*   谁手里拿到了写数据的锁？
*   配置发生改变时，怎么保证每个人在同一秒收到通知？

在那个时候，每个大数据组件都要自己手写一套简陋的选主逻辑和心跳检测。这导致了灾难性的后果：[脑裂](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%84%91%E8%A3%82&zhida_source=entity)（Split-Brain，两个节点都以为自己是老大，把数据写烂）、配置不同步、死锁频发。

雅虎的工程师们意识到：分布式系统需要一个集中的“协调官”。

因为雅虎内部的组件大多以动物命名（比如 Hadoop 的大象、Pig 的猪），这个协调官最终被命名为 **ZooKeeper（动物园管理员）**。由 Benjamin Reed 领导的研发团队，旨在用一个统一的、高可用的、强一致性的服务，来降服这些难以驯服的“野生动物”。

### 旧方案为什么失败？

在 ZooKeeper 诞生并一统天下之前，业界在处理“分布式一致性”时，尝试过好几种方案。

### 1\. 简陋的“单点集中式”配置器

最直接的设计是配置一台主服务器，所有的状态和锁都存在这台机器的内存或一个单点 [MySQL](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=MySQL&zhida_source=entity) 里。

*   **为什么当年大家都这样设计？** 简单。
*   **致命缺陷：** 

这台机器成了系统的“[单点故障](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%8D%95%E7%82%B9%E6%95%85%E9%9A%9C&zhida_source=entity)”（SPOF）。一旦它[宕机](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%AE%95%E6%9C%BA&zhida_source=entity)，整个集群瞬间瘫痪。而如果引入主备数据库切换，又会在极端网络分区下产生“双主脑裂”的噩梦。

### 2\. 复杂的 [Paxos](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Paxos&zhida_source=entity) 算法手写实现

[莱斯利·兰伯特](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%8E%B1%E6%96%AF%E5%88%A9%C2%B7%E5%85%B0%E4%BC%AF%E7%89%B9&zhida_source=entity)（Leslie Lamport）老爷子提出的 Paxos 算法是分布式一致性的圣经。

*   **为什么当年大家都这样设计？** 它是数学上证明完美的分布式共识方案。
*   **致命缺陷：** 

**Paxos 实在太难实现了。**  业界有一句名言：“世界上只有一种一致性算法，那就是 Paxos；但也只有一种 Paxos，那就是别人没看懂的那种。”手写 Paxos 的难度无异于在沙滩上建高楼，极易出错，几乎没有人能写出工业级无 Bug 的 Paxos 实现。

### 真正的突破：[ZAB 协议](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=ZAB+%E5%8D%8F%E8%AE%AE&zhida_source=entity)与内存树的精妙结合

ZooKeeper 的横空出世，本质上是**对学术界完美主义的一次工程化妥协**。

它没有死磕晦涩难懂的 [Multi-Paxos](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Multi-Paxos&zhida_source=entity) 算法，而是由工程师们自研了一套全新的分布式一致性协议——**ZAB（ZooKeeper Atomic Broadcast，[原子广播协议](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%8E%9F%E5%AD%90%E5%B9%BF%E6%92%AD%E5%8D%8F%E8%AE%AE&zhida_source=entity)）**。

同时，ZooKeeper 做出了一个极其天才的架构决策：**它将[数据模型](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%A8%A1%E5%9E%8B&zhida_source=entity)抽象为一棵跟 Linux [文件系统](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F&zhida_source=entity)一模一样的“树”（[ZNode](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=ZNode&zhida_source=entity)）。** 

```text
                  +---------+ (Root "/")
                  |  /      |
                  +---------+
                   /       \
         +---------+       +---------+
         |  /app1  |       |  /app2  | (服务注册目录)
         +---------+       +---------+
          /
    +---------+
    | /config | (配置信息，临时的/持久的)
    +---------+
```

### 它的核心逻辑优雅在哪？

1.  **全内存[数据结构](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84&zhida_source=entity)**：

这棵树完全保存在内存里，所有的[读请求](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%AF%BB%E8%AF%B7%E6%B1%82&zhida_source=entity)（占分布式场景的 90% 以上）都可以以接近硬件极限的速度直接从内存返回，完全没有磁盘 I/O 损耗。

1.  **临时节点（Ephemeral Nodes）+ [监听机制](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E7%9B%91%E5%90%AC%E6%9C%BA%E5%88%B6&zhida_source=entity)（Watcher）**：

一个服务启动时，在树上挂一个“临时果子”（比如 `/services/node-1`）。只要这个服务和 ZooKeeper 的 T[CP](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=CP&zhida_source=entity) 长连接不断，果子就在。一旦服务挂了，长连接断开，果子自动掉落，并且其他关注这颗树的节点会立刻收到一个**主动推送（Watcher）**。

这套设计极其精妙。原本极其复杂的“[死锁检测](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%AD%BB%E9%94%81%E6%A3%80%E6%B5%8B&zhida_source=entity)”、“[服务发现](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E5%8F%91%E7%8E%B0&zhida_source=entity)”、“[状态同步](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E5%90%8C%E6%AD%A5&zhida_source=entity)”，在 ZooKeeper 里被抽象成了简单的“建节点”、“删节点”和“看节点”。

### 源码里的体现：Watcher 机制的隐患

ZooKeeper 的 Watcher（监听机制）是它最伟大的发明，却也是它日后衰落的[阿喀琉斯之踵](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E9%98%BF%E5%96%80%E7%90%89%E6%96%AF%E4%B9%8B%E8%B8%B5&zhida_source=entity)。

让我们看看 ZooKeeper 源码中处理 Watch 事件触发的核心机制（简化示意）：

```text
/* * org.apache.zookeeper.server.WatchManager
 * 简化示意：ZooKeeper 内部维护 Watcher 的核心逻辑
 */
public class WatchManager {
    // 节点路径到 Watcher 集合的映射
    private final Map<String, Set<Watcher>> watchTable = new HashMap<>();
    private final Map<Watcher, Set<String>> watch2Paths = new HashMap<>();

    public synchronized void triggerWatch(String path, EventType type) {
        // 1. 找到监听该路径的所有 Watcher
        Set<Watcher> watchers = watchTable.remove(path); // 注意：触发后即“一次性”移除！
        if (watchers == null || watchers.isEmpty()) {
            return;
        }
        
        for (Watcher w : watchers) {
            // 2. 异步通知客户端
            w.process(new WatchedEvent(type, KeeperState.SyncConnected, path));
        }
    }
}
```

### 为什么这样写？它隐藏了什么代价？

*   **为什么触发后要立刻从 `watchTable` 里 `remove`（一次性监听）？**

因为保持一个持续激活的[监听器](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E7%9B%91%E5%90%AC%E5%99%A8&zhida_source=entity)需要耗费巨大的服务器内存和网络资源。ZooKeeper 的设计者为了保护系统，强制要求 Watcher 是**一次性的**。客户端收到通知后，如果还想听，必须手动再发起一次注册。

*   **为什么这成了硬伤？**

在[高并发](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E9%AB%98%E5%B9%B6%E5%8F%91&zhida_source=entity)、大规模的[云原生时代](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=2&q=%E4%BA%91%E5%8E%9F%E7%94%9F%E6%97%B6%E4%BB%A3&zhida_source=entity)，这产生了一个致命漏洞。当一个核心节点发生抖动，成千上万个客户端同时收到通知，然后**同时发起重新注册的读请求**。这会在瞬间引发“[惊群效应](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%83%8A%E7%BE%A4%E6%95%88%E5%BA%94&zhida_source=entity)”（Thundering Herd），产生恐怖的网络风暴，直接把 ZooKeeper 顶满到假死。

### 设计思想：完美的强一致性（CP）执念

ZooKeeper 身上体现了浓厚的经典计算机美学：

*   **CP（强一致性 + [分区容错](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%88%86%E5%8C%BA%E5%AE%B9%E9%94%99&zhida_source=entity)）至上**：

在 [CAP 定理](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=CAP+%E5%AE%9A%E7%90%86&zhida_source=entity)中，ZooKeeper 坚决站在了 CP 一侧。它认为分布式系统的配置和状态必须绝对准确，容不得半点沙子。一旦集群发生[网络分区](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=2&q=%E7%BD%91%E7%BB%9C%E5%88%86%E5%8C%BA&zhida_source=entity)，宁可牺牲可用性（AP），拒绝服务，也要保证数据的一致。

*   **内存换速度**：

将所有[元数据](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%85%83%E6%95%B0%E6%8D%AE&zhida_source=entity)存在内存中，避免[磁盘寻道](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E7%A3%81%E7%9B%98%E5%AF%BB%E9%81%93&zhida_source=entity)，实现极低延迟的事务提交。

*   **事务顺序性（Zxid）**：

每一个修改操作都被赋予一个全局递增的 64 位事务 ID（Zxid），这让所有的状态变更在整个集群中拥有严格的时间先后顺序。

### 为什么它正在被新方案替代？

既然它如此完美，为什么今天大家开始抛弃它？

因为**时代变了，机器的规模变了**。

当年的 Hadoop 集群不过百来台机器，但到了今天的云原生时代，[Kubernetes](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Kubernetes&zhida_source=entity) 管理的容器动辄数万，[微服务](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%BE%AE%E6%9C%8D%E5%8A%A1&zhida_source=entity)注册的实例成千上万，Kafka 每天传输的数据高达数万亿条。

在这个背景下，ZooKeeper 的三大缺陷暴露无遗：

### 1\. 垃圾回收（GC）的死穴

ZooKeeper 是用 **Java** 写的。

当内存中的[节点树](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%8A%82%E7%82%B9%E6%A0%91&zhida_source=entity)膨胀到百万、千万级别时，[JVM](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=JVM&zhida_source=entity) 的垃圾回收（GC）就成了噩梦。一次严重的 **Stop-The-World (STW)**，会导致 ZooKeeper 的心跳检测超时。此时，外界会误以为 ZooKeeper 挂了，引发一轮灾难性的集群重新选主，整个大系统陷入剧烈震荡。

### 2\. 无法承载的“服务[注册中心](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%B3%A8%E5%86%8C%E4%B8%AD%E5%BF%83&zhida_source=entity)”职责

在微服务爆发的年代，大家顺理成章地用 ZooKeeper 做服务发现。

但服务发现需要的是 **AP（可用性）**。如果网络出现抖动，ZooKeeper [集群](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=7&q=%E9%9B%86%E7%BE%A4&zhida_source=entity)开始重新选主，期间长达几十秒的时间整个注册中心**无法提供任何服务**。

> “只是为了发现一个服务的 [IP](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=IP&zhida_source=entity) 地址，凭什么要让我的整个微服务[调用链](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%B0%83%E7%94%A8%E9%93%BE&zhida_source=entity)全部挂掉？”

### 3\. Kafka 的自我救赎：脱离 ZooKeeper

曾经，Kafka 将所有的 Broker 状态、Topic 分区信息、消费者的 [Offset](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Offset&zhida_source=entity) 都托管在 ZooKeeper 里。

但在数十万个分区（Partition）的[超级集群](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%B6%85%E7%BA%A7%E9%9B%86%E7%BE%A4&zhida_source=entity)下，ZooKeeper 的[元数据同步](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%85%83%E6%95%B0%E6%8D%AE%E5%90%8C%E6%AD%A5&zhida_source=entity)网络瓶颈彻底锁死了 Kafka 的上限。

2021 年，Kafka 终于发布了 **K[Raft](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Raft&zhida_source=entity)** 协议，彻底将 ZooKeeper 从其架构中剥离，实现了元数据的自我管理。

### 有没有更好的方案？

今天的分布式格局，已经迎来了新的王者。

### 1\. [Raft 协议](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Raft+%E5%8D%8F%E8%AE%AE&zhida_source=entity)与 Etcd 的崛起

在云原生生态中，Google 亲儿子 Kubernetes 最终选择的基石是 **Etcd**。

*   Etcd 使用 **[Go 语言](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Go+%E8%AF%AD%E8%A8%80&zhida_source=entity)**编写，没有 JVM 那让人提心吊胆的 GC 停顿。
*   它底层使用了更简单、更直观、被学术界与工业界共同拥抱的 **Raft** 协议。
*   它天然支持 HTTP+gRPC 协议，相比 ZooKeeper 复杂的私有 [TCP 协议](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=TCP+%E5%8D%8F%E8%AE%AE&zhida_source=entity)，对云原生容器极其友好。

### 2\. [Rust](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=Rust&zhida_source=entity) 的极限重塑

如果今天重新设计[分布式锁](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%88%86%E5%B8%83%E5%BC%8F%E9%94%81&zhida_source=entity)和共识，**Rust** 已经成为首选。比如[蚂蚁金服](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E8%9A%82%E8%9A%81%E9%87%91%E6%9C%8D&zhida_source=entity)等大厂的自研一致性库、各种新一代云原生[分布式数据库](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%88%86%E5%B8%83%E5%BC%8F%E6%95%B0%E6%8D%AE%E5%BA%93&zhida_source=entity)，都在使用 Rust 重新编写 Raft 或 Paxos。

无 GC、零拷贝、极致的内存控制，让强一致性协议在硬件极限下依然能够保持稳定的亚毫秒级延迟。

### 现实中的应用：谁在继承，谁在离去

*   **Kubernetes (Etcd)**：

作为当今云原生的绝对[操作系统](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F&zhida_source=entity)，Etcd 默默支撑着全人类最庞大的[容器集群](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E5%AE%B9%E5%99%A8%E9%9B%86%E7%BE%A4&zhida_source=entity)调度。

*   **Consul**：

微服务领域的老牌悍将，支持多[数据中心](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E4%B8%AD%E5%BF%83&zhida_source=entity)，天然偏向 AP 架构，逐渐蚕食了 ZooKeeper 原有的服务发现领地。

*   **[ClickHouse](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=ClickHouse&zhida_source=entity) (Keeper)**：

为了解决 ZooKeeper 的局限，ClickHouse 在其新版本中干脆用 [C++](https://zhida.zhihu.com/search?content_id=279209522&content_type=Article&match_order=1&q=C%2B%2B&zhida_source=entity) 自己实现了一个完全兼容 ZooKeeper 接口的 `clickhouse-keeper`，直接把 JVM 踢出了依赖。

### 一句话总结

> 优秀的软件，从来不是寻找最复杂的方案，而是在性能、复杂度和维护成本之间找到最好的平衡。ZooKeeper 曾是黑暗中指引群兽的灯塔，但当兽群化作满天繁星时，更轻盈、更弹性的群星，将成为新时代的选择。