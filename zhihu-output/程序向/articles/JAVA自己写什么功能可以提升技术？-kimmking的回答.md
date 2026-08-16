---
id: "20633949997"
title: "JAVA自己写什么功能可以提升技术？"
author: "kimmking"
type: zhihu-answer
source: "https://www.zhihu.com/question/616660274/answer/20633949997"
created: "2024-11-01 22:18"
updated: "2024-11-17 20:55"
collected: "2024-11-01 22:18"
downloaded: "2026-08-16"
---
17 天 手写一个完整的微服务框架（每天花1个小时完成一个分支）：

[ArchCamp/kkrpc](https://link.zhihu.com/?target=https%3A//gitee.com/ArchCamp/kkrpc)

具备以下功能：

```text
1. RPC的基本概念
  1. 从基本原理图讲解
  2. 作用与用途
2. 网络协议，序列化协议
  1. 网络协议：TCP/HTTP/HTTP2
  2. 序列化：JSON，XML，hessian，thrift自定义格式
3. 设计服务接口与元数据
  1. 服务接口设计
  2. 元数据描述信息
4. 服务提供者Skeleton，服务消费者Stub
  1. 动态代理生成stub
  2. 元数据映射关系
5. 设计网络协议和序列化协议
  1. JSON格式
  2. HTTP，复用springboot
6. 设计服务Skeleton
  1. 服务端寻址
  2. 添加注解
  3. 注解处理，注意优雅启动
7. 设计服务Stub
  1. 客户端调用关系
  2. 过滤掉非业务方法
  3. 添加注解
8. 基于ZK设计服务注册功能
  1. 实现ZK操作
  2. 实现优雅启动注册
  3. 实现优雅停机关闭
  4. 实现namespace隔离
9. 基于ZK实现服务发现功能
  1. 实现ZK订阅处理
  2. 实现ZK变动处理
  3. 实现优雅停机关闭
  4. 实现namespace隔离
10. 实现服务的路由机制
  1. 路由接口设计
  2. 默认路由实现
  3. 基于tag的路由实现
11. 实现服务的负载均衡机制
  1. 随机
  2. RR
  3. 权重
12. 实现服务的过滤器机制
  1. 客户端filter
  2. 服务端filter
  3. cache filter实现
13. 调优服务提供者和消费者性能
  1. 服务提供者调优，线程池调优
  2. 服务消费者调优，线程池和连接池调优
14. 实现服务的限流机制
  1. 整合Sentinel或独立实现
  2. 不同服务层级限流
  3. 数据库访问限流
  4. 线程池与调用计数
15. 实现服务的容错机制
  1. 实现错误分类设计
  2. 实现错误的时间窗口计数
  3. 实现故障隔离机制
  4. 实现故障探测与恢复
16. 实现重试与超时机制
  1. 实现不同层级的超时控制
  2. 实现重试策略和回退策略
  3. 实现超时漏斗设计
17. 实现挡板机制
  1. 实现服务挡板
  2. 实现网关挡板
18. 实现优雅启停机制
  1. 服务预热
  2. 延迟注册
  3. 线程池优雅关闭
  4. 连接池优雅关闭
  5. 注册中心、配置中心连接优雅关闭
19. 实现多机房容灾
  1. 基于Tag实现DC/zone 路由支持
  2. 基于DC/zone 实现流量调拨
  3. 实现多DC/zone 的服务调用和LB
20. 实现滚动部署/蓝绿部署
  1. 实现滚动发布
  2. 实现蓝绿发布
21. 实现灰度发布
  1. 支持不同层级服务灰度
  2. 支持全链路灰度发布
```

这个组织下，还有其他组件的手把手实现：

第二部分：MQ消息系统  
第三部分：Cache缓存系统  
第四部分：Gateway网关  
第五部分：Sharding分库分表  
第六部分：Registry注册中心  
第七部分：Config配置中心  
第八部分：DFS分布式文件系统

如有问题，可以知乎联系。

更多信息或者寻求帮助可以通过：

[知识星球 | 深度连接铁杆粉丝，运营高品质社群，知识变现的工具](https://link.zhihu.com/?target=https%3A//wx.zsxq.com/group/15552551848522)

  

  

* * *

  

【kimmking知乎高赞内容推荐悦读】：

[kimmking：谈谈AI领域的认知误区、机会点与面临的挑战](https://zhuanlan.zhihu.com/p/718302731)

[kimmking：【0101】技术的定位：程序员是这个时代的手艺人](https://zhuanlan.zhihu.com/p/716621029)

[中国的程序员数量是否已经饱和或者过剩？](https://www.zhihu.com/question/356982241/answer/921109077)

[如何摆脱程序员内卷？](https://www.zhihu.com/question/441933392/answer/1725274377)

[为什么大部分码农做不了软件架构师？](https://www.zhihu.com/question/36658435/answer/1778614690)

[好的程序员有什么特质呢？](https://www.zhihu.com/question/22094459/answer/20273339)

[kimmking：银行数据库选型：1-银行数据库选型要点](https://zhuanlan.zhihu.com/p/659005938)

[kimmking：千亿数据的潘多拉魔盒：从分库分表到分布式数据库](https://zhuanlan.zhihu.com/p/352202284)

[kimmking：00.什么是微服务架构](https://zhuanlan.zhihu.com/p/71772093)

[kimmking：微服务架构深度解析与最佳实践（全篇汇总）](https://zhuanlan.zhihu.com/p/137051324)

[kimmking：百亿流量微服务网关的设计与实现](https://zhuanlan.zhihu.com/p/97985176)

[要达到什么样的规模才适合分布式/微服务架构?](https://www.zhihu.com/question/384102981/answer/1119478764)

[kimmking：JSON&Fastjson最佳实践](https://zhuanlan.zhihu.com/p/97982717)

[kimmking：分布式高并发系统如何保证对外接口的幂等性？](https://zhuanlan.zhihu.com/p/97628732)

[有些上古程序猿一直坚持反对使用redis怎么办？](https://www.zhihu.com/question/383926405/answer/1118300686)

[kimmking：RPC与MQ的区别以及MQ的使用场景](https://zhuanlan.zhihu.com/p/97841943)

[Kafka、RabbitMQ、RocketMQ 之间的区别是什么 ?](https://www.zhihu.com/question/275090117/answer/1832889993)

[RabbitMQ在国内为什么没有那么流行？](https://www.zhihu.com/question/449611434/answer/1824707689)

[Spring Boot + MyBatis 如何优雅的实现数据库读写分离？](https://www.zhihu.com/question/381631883/answer/1100642927)

[如何在没高并发的生产环境下学习高并发分布式架构？](https://www.zhihu.com/question/41674361/answer/905509206)

[为什么有人说弄懂了《算法导论》的 90%，就超越了 90%的程序员？](https://www.zhihu.com/question/315201616/answer/1756148937)

[大一新生应该先学习什么软件技能呢？](https://www.zhihu.com/question/407232850/answer/1364709912)

[如何阅读大型项目的代码？](https://www.zhihu.com/question/351618643/answer/893413586)

[为什么几乎所有的开源数据库中间件都是国内公司开源的？并且几乎都停止了更新？](https://www.zhihu.com/question/352256403/answer/878523206)

[如何看待国内开源项目的不可持续性？](https://www.zhihu.com/question/355691918/answer/895472300)

[《设计数据密集型应用》一书有没有比较好的学习方法？](https://www.zhihu.com/question/268832961/answer/909972555)

[你在开源项目里看到过哪些精髓的代码片段？](https://www.zhihu.com/question/352847684/answer/889567006)

[kimmking：研发体系建设](https://zhuanlan.zhihu.com/p/97869309)

[各位都是怎么进行单元测试的？](https://www.zhihu.com/question/27313846/answer/36132954)

[想参与开源项目，但又不知道从哪里下手，有没有系统化的课程推荐一下。？](https://www.zhihu.com/question/353078587/answer/890604287)

[淘宝是如何实现高并发下抢单的锁单机制？](https://www.zhihu.com/question/27894855/answer/906948755)

[为何说spring cloud适合中小型项目，而不适合大型项目？](https://www.zhihu.com/question/289129028/answer/905544634)

[CSDN现在发展怎么样？](https://www.zhihu.com/question/331463014/answer/754736910)

[阿里如果全面将java替换成rust，能省下多少服务器资源？](https://www.zhihu.com/question/557052024/answer/3212682681)

[程序员都干过哪些很刺激的事情？](https://www.zhihu.com/question/615181969/answer/3154450321)

[程序员的护城河是什么 ？](https://www.zhihu.com/question/604014261/answer/3625572828)

[现在有什么好的方案替换zookeeper+ dubbo吗？](https://www.zhihu.com/question/333043329/answer/737576924)

[springjpa和mybatis哪个查询效率高?](https://www.zhihu.com/question/356307466/answer/919908635)

[GraphQL 为何没有火起来?](https://www.zhihu.com/question/38596306/answer/921027553)

[Spring Cloud各个微服务之间为什么要用http交互？难道不慢吗？](https://www.zhihu.com/question/270355472/answer/3238160454)

[阿里云机房着火是因为java的原因嘛？](https://www.zhihu.com/question/667085074/answer/3625665267)

[ZGC有什么缺点?](https://www.zhihu.com/question/356585590/answer/2298574930)

[创建springboot项目不使用maven是否可以？](https://www.zhihu.com/question/381148343/answer/1101510577)

[如何看待“Hutool”工具类库广受欢迎？](https://www.zhihu.com/question/404254947/answer/3610135830)

[JAVA自己写什么功能可以提升技术？](https://www.zhihu.com/question/616660274/answer/20633949997)

[用 go 重写 java 的消息队列，例如 kafka, rocketmq 可行吗？](https://www.zhihu.com/question/346624074/answer/904418311)

[既然redis那么快，为什么不用它做主数据库，只用它做缓存？](https://www.zhihu.com/question/384184784/answer/2996172207)

[java 是不是可以通过代码动态代码生成技术来代替大部分反射调用？](https://www.zhihu.com/question/1250420263/answer/10247479734)