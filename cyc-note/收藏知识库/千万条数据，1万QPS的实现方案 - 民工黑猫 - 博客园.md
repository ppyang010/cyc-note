[千万条数据，1万QPS的实现方案 - 民工黑猫 - 博客园](https://www.cnblogs.com/yyee/p/22253356) 

 一千万条数据，1万QPS的实现方案。

需求：主表一千万条数据，每秒1万个http请求，响应时间500毫秒以内。

一次接口访问，需要调用多次数据库，所以数据库本身承载不了那么大的QPS，决方案只有一种，那就是使用缓存。

  
分3个场景：

**场景 1：单 ID 详情查询（商品 / 基础信息，按主键查询）**

1\. L1 本地缓存（IMemoryCache / Caffeine）

*   容量限制：限制本地缓存2 万个热点 key，LRU 淘汰，缓存时间30分钟；
*   命中耗时约1 ms，拦截 80% 流量，大幅减少 Redis 网络往返；
*   多实例一致性：Redis Pub/Sub 发布广播消息，所有 API 节点订阅Redis的广播消息，增量刷新本地缓存，无需全量重载。

2\. L2 Redis 集群（5 台主分片，每主 1 从，共 10节点）

*   存储结构：`detail:{id}` 单条 KV；
*   性能：单从节点支撑 3~5 万读 QPS，5个master分片节点承载 1 万 QPS。

**1） 原始业务数据体积**

      1000万 × 10KB  ≈ 96GB

2） Redis 额外内存开销（key 字符串、dict 哈希表、内存碎片，常规上浮 30%）

      总占用内存 = 96 GB× 1.3 = 124.8GB

3) 整机内存64G，单机最大承载业务内存上限30G    

*   系统、内核、PageCache 预留 34G；
*   Redis `maxmemory` 安全上限 30GB；
*   RDB fork 写时复制内存翻倍峰值 60GB，不超整机 64G，规避 OOM。

4） 计算最少 Master 分片数量

    总内存 123.98 ÷ 30 ≈ 4.13，向上取整 5 台 Master

5) 节点规划（10台64G物理服务器）：

    Master 主节点：5 台 

    Slave 从节点：5 台（一主配一从，高可用） 

    Redis 实例总量：10 个

3\. DB 兜底策略

 仅缓存冷启动、缓存没有数据时从数据库读取。

  
**场景 2：列表分页 + 多条件筛选（千万级产品表，区间 / 分类 / 排序分页）**  
两种对等方案，按需选择。

**方案 2-1：RediSearch + 10个master分片节点**

**2-1-1 存储设计：**   
(1) 每条原始产品存储为HSet

HSET product\_doc:1001 title "荣耀Magic手机" price 99 stock 100 tag "手机,数码" create\_time 1754000000 spec "12+256G" HSET product\_doc:1002 title "漫步者无线耳机" price 199 stock 50 tag "音频,数码" create\_time 1754100000 spec "降噪款"

更新商品：

HSET doc:1001 price 89 stock 80

索引自动同步更新价格、库存，无需手动操作索引。

(2) 创建 1 个全局索引统一匹配所有 product\_d`oc:*` 前缀的 Hash，会自动对 HSET分类、产品名称、、价格、创建时间、规格建立全文 / 数值联合索引；

**2-2-2 原理说明：** 

RediSearch 的 `ON HASH PREFIX N 前缀` 是批量匹配规则：
-------------------------------------------

*   `PREFIX 1 product_doc:` 代表匹配所有 key 以 product\_`oc:` 开头的 Hash，不管后缀是 1001、1002、9999；
*   新增一条 `HSET product_doc:2001 ...`，索引自动实时收录这条数据，无需执行任何索引创建 / 刷新命令；
*   更新 / 删除任意一条 product\_`doc:xxxx`，索引自动同步变更。
*   只需要执行一次创建索引命令，全局所有产品 Hash 全部被索引覆盖。

**2-1-3 创建索引语句示例：** 

![](https://assets.cnblogs.com/images/copycode.gif)

\# 创建产品全局索引，匹配全部 product\_doc: 开头的Hash
FT.CREATE idx\_product ON HASH PREFIX 1 product\_doc: SCHEMA
    product\_id 1001 NUMERIC SORTABLE
    title TEXT WEIGHT 10 SORTABLE       # 产品名称 全文检索，权重拉高
    tag TAG SEPARATOR "," SORTABLE      # 分类标签 多标签逗号分割，精确筛选
    price NUMERIC SORTABLE              # 价格 区间过滤、排序
    create\_time NUMERIC SORTABLE        # 创建时间 时间筛选、排序
    spec TEXT SORTABLE                  # 规格 全文模糊搜索

![](https://assets.cnblogs.com/images/copycode.gif)

**2-1-4 查询能力：** 

RedisSearch 原生支持多条件过滤、limit offset/size、游标分页、多字段排序，无需多次网络交互，单次命令完成分页检索；

检索示例（联合多条件查询）：

\# 筛选数码分类、价格50~200、标题模糊匹配手机，按价格升序
FT.SEARCH idx\_product "@tag:{数码} @price:\[50 200\] @title:手机" SORTBY price ASC LIMIT 0 10

**2-1-5 扩展场景：如果业务需要分多类前缀**

如果后续区分商品、订单，存在 `doc:product:`、`doc:order:` 、doc:categories 三类Hash，可以给索引配置多个前缀：

\# 同时匹配 doc:product: 和 doc:order:  doc:categories 三套Hash
FT.CREATE idx\_all ON HASH PREFIX 3 doc:product: doc:order: doc:categories: SCHEMA ...

**2-1-6 Redis集群部署规划：** 

1\. 内存总量精准估算  
数据总量：1000万条数据，平均单条数据10k。

原始HashSet数据大小：1000万 x 10k  ≈  96 GB。

2\. Redis Hash 底层结构开销（key+hashtable）：原始数据的 30% → 96GB × 0.3 = 28.8 GB

3\. RediSearch 索引额外内存（test/tag/numeric 倒排索引）：等于原始数据的 80%~100% = 76.8 GB ~ 96GB

    总内存占用 = 原始大小 + Hash 开销 + 索引 ≈ 201.6GB ~ 220.8GB 纯内存

4\. 高可用副本翻倍：

    1台副本：1 主 1 从，总内存 ≈ 403.2 ~ 441.6GB  
    2台副本：1 主 2 从，总内存 ≈ 604.8 ~ 662.4GB

**2-1-7 分片数量、节点数量计算规则**

**1，分片计算：** 

单台 Redis 实例安全内存上限：物理机 16G 整机 → Redis 最大分配 10G；32G 整机→Redis最大分配20G；64G 整机→ Redis最大分配31G（封顶，不超 31G 避免压缩指针失效）。

单主节点安全内存阈值：不超过 30G（预留缓冲，防止内存溢出， 持久化 RDB 快照时会调用 `fork()` 创建子进程， fork 瞬间瞬间，内存翻倍）。

总主内存需求 220.8GB，单台 master 最多承载 30GB： 

`220.8 ÷ 30 ≈ 7.3` → 向上取整 8个主分片（master）

**2，Redis节点数计算：** 

Master 主分片：8 台（承载全部数据 + 索引）

每台 master 配 1 台 slave 从节点：8台从

冗余2台master节点 + 冗余2台slave节点 = 4台冗余。

总实例：20个 Redis 实例

因为RediSearch的索引全部在内存，所以需要10台主Redis Stack服务器。

**2-2-8 哈希 Tag 优化（避免跨多节点查询，提速）**

高频按分类筛选，统一 key 增加分类 hash tag，让同分类商品落在同一槽：

\# 同分类手机全部落在同一个槽，查询只访问单台master
HSET product\_doc:{phone}:1001 title "荣耀Magic手机" price 99 stock 100 tag "手机,数码" create\_time 1754000000 spec "12+256G"

**方案 2-2：Elasticsearch 3 主分片集群（行业首选）**

**1\. 索引分片规划**  
    文档索引设置 3 个主分片，2 副本，3 台 ES 数据节点均匀分布分片；单分片承载 3000 + 列表 QPS，3 分片满足 1 万并发；

创建单索引规则:

![](https://assets.cnblogs.com/images/copycode.gif)

POST /products/\_doc/1001 { "product\_id": "1001", "title": "荣耀magic9", "price": 99, "stock": 100, "tag": \["手机","数码"\], "create\_time": 1754000000, "spec": "12+256G" }

![](https://assets.cnblogs.com/images/copycode.gif)

单索引在体积达到30G后，就变得非常缓慢，如果单索引容量超过30B，需要使用滚动索引，创建别名匹配滚动索引。

滚动索引的两种模式：按时间滚动、按容量滚动

**(1) 按时间滚动（时序日志 / 订单）**

命名规则：`orders-2026-08、products-2026-08`、`logs-2026-08-07`，按月 / 日切割

**(2) 按容量 Rollover 滚动（超大静态商品库）**

单索引数据达到 30GB 自动新建 `products-000001`、`products-000002，使用别名访问滚动索引，固定别名：products-write。`

别名规范（读写分离，线上标准）

products-write  # 唯一写入索引，rollover自动切换
products\-read   # 匹配所有products-\* 滚动索引，用于查询

**2\. 分页优化（千万级表必做）**  
     浅分页（前 50 页）：from/size；  
     深度分页：强制 search\_after 游标分页，规避 offset 过大扫描性能衰减；

**3\. 分片数、副本数、节点数规划**

一千万条数据量，单条数据10k的节点数规划。

总原始数据 = 1千万条 x 10k ≈ 96GB。

主分片数量 =  96(GB) ÷ 30(GB) ≈ 3.2 ，向上取整，主分片等于4个，单分片容量建议不超过30GB。创建索引后主分片数量不能更改。

主分片副本数量 = 1，一个副本已经够用，一个节点故障，还有一个节点可用。

控制节点（master节点）数量：3台，需要奇数个选举。

数据节点的数量：4台（一个主分片需要一台数据节点），说明：数据节点数量 >= 设置的最大副本数 + 1，因为副本存存储在主分片以外的节点。

4个主分片的数据节点需要多少台计算汇总：

| 主分片 | 副本数 | 副本总分片 | 集群总分片 | 最小数据节点 | 整体存储容量倍数 |
| 4 | 0 | 0 | 4 | 4台 | 1倍原始数据 |
| 4 | 1 | 4 | 8 | 4台 | 2倍原始数据 |
| 4 | 2 | 8 | 12 | 4台 | 3倍原始数据 |
| 4 | 3 | 12 | 16 | 4台 | 4倍原始数据 |
| 4 | 4 | 16 | 20 | 

5台

(数据节点数量 >= 设置的最大副本数 + 1)

 | 5倍原始数据 |

  
**4\. 数据同步**

    同步方案一：数据更新操作，将最终数据写进MQ，MQ消费端更新数据到ES。  
     同步方案二：Canal 监听 DB Binlog，实时同步全量商品字段至 ES；凌晨全量同步任务修复数据不一致。

**方案2-3 DragonflyDB（Redis 兼容替代，开源） 或 阿里云 Tair（企业版内存库，TairSearch）**

**1\. DragonflyDB（Redis 兼容替代，开源）**

*   完全兼容 Redis 协议，支持 RediSearch 同等检索模块，多线程架构，单机吞吐是原生 Redis 10~25 倍
*   RDB 快照内存 fork 无峰值翻倍，解决 Redis OOM 痛点；冷启动加载速度大幅优化
*   支持集群分片，可无缝替换 Redis+RediSearch

**2. 阿里云 Tair（企业版内存库，TairSearch，优先推荐）** 

*   云原生 Redis 兼容，内置 TairSearch 全文检索，底层优化内存占用、冷热分层
*   服务端自动聚合多分片搜索结果，不用客户端合并，解决开源 Redis Cluster 短板
*   支持磁盘混合存储，部分字段落盘，降低纯内存成本

**场景3：树形数据，父子 / 子孙路径查询（10万条数据）**  
这种情况不能使用Redis或ElasticSearch做缓存了。因为要10万条数据做递归查询一个树型，不能单条读Redis或ElasticSearch，也不能把一个10万条数据的json字符串存到Redis。这种情况只能使用内存缓存了，把10万条数据存到内存。  
**内存缓存有三个方案：**   
**方案3-1：原生 List 内存缓存**

站点启动的时候把10万条数据放进List，整条List存到MemoryCache，在内存里递归查询，部署3台api节点；

**方案3-2：纯进程本地扁平化内存索引（性能最优）**

API 节点 3 台独立部署，每台启动一次性加载全量树形数据，预构建 4 套内存字典索引，彻底消除运行时递归查询：

![](https://assets.cnblogs.com/images/copycode.gif)

// 1. 全节点主键字典：ID → 节点完整实体
Dictionary<long, TreeItem> AllNodeDict; // 2. 父级索引：父ID → 子节点ID列表（查直接子节点O(1)）
Dictionary<long, List<long\>> ChildIndex; // 3. 祖先链路索引：节点ID → 根到自身全路径ID数组（递归向上查询直接取）
Dictionary<long, List<long\>> ParentChainIndex; // 4. 后代全量索引：节点ID → 所有子孙ID（一次性查整棵子树，无需循环递归）
Dictionary<long, HashSet<long\>> DescendantIndex;

![](https://assets.cnblogs.com/images/copycode.gif)

优势：

    直接拿到所有父节点id或子节点id，从全节点字典里查所数据。

多实例分布式一致性方案： 

     数据更新流程：更新 DB → 使用 Redis Publish 广播更新的数据，所有点节订阅广播消息，收到广播消息更新四个字典。

     定时每天全量同步一次数据，修复脏数据。

**方案3-3：用RocksDB或LMDB进程数据库（几十万条数据，内存放不下的情况）**  
关键矛盾：  
10 万～几十万树形数据，全量数据常驻内存会占用过高；

实现机制：

    进程内嵌入式 KV 库，全量树形持久化本地 SSD 磁盘，限制内存`block_cache=512MB。`    

    热点层级（根、一级菜单、高频查询子树）常驻内存，O (1) 读取。

    低频叶子节点存在磁盘，首次访问加载进缓存，超出 512MB 自动淘汰最冷数据，内存不会持续上涨。

数据同步方案：

    数据更新流程：更新 DB → 使用 Redis Publish 广播更新的数据，所有点节订阅广播消息，收到广播消息更新RocksDB。

    定时每天全量同步一次数据，修复脏数据。

RocksDB内存参数控制占用内存上限（防止吃满单机内存）： 

block\_cache\_size = 512MB;  // 热点数据内存上限，固定死，不会无限膨胀
write\_buffer\_size = 64MB;
max\_write\_buffer\_number \= 2;