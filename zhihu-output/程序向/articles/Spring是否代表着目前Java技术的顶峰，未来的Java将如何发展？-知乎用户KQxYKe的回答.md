---
id: "2079638274"
title: "Spring是否代表着目前Java技术的顶峰，未来的Java将如何发展？"
author: "知乎用户KQxYKe"
type: zhihu-answer
source: "https://www.zhihu.com/question/387902282/answer/2079638274"
created: "2021-08-23 23:38"
updated: "2024-06-26 01:40"
collected: "2021-08-23 23:38"
downloaded: "2026-08-16"
---
我觉得是的，所谓的oracle .jdk一直在升级，对很多人来说不痛不痒，很多公司还是在用jdk 8。但是spring社区新出的东西，都引人关注，很多人学习，做最佳落地实践，从这个意义来说，确实带着oracle在进步，让Java慢一点衰亡。接下来从几个项目来说说看

最新的spring AI推出也是，在Java届引起轰动，实现AI的知识库，RAG，通过function calling 实现业务联动，实现业务智能化。绝对手机可以让Java再AI大模型时代，占有一席之地。

第一，spring native这个是未来，是趋势，虽然在孵化，但是足以见它的野心，抛弃原有的jvm，更快的启动速度，不需要预热的性能顶峰，更好的性能和吞吐量。比所谓oracle 一直升级jdk有意义，有预见性多了。

# 第二，对比侵入式微服务架构，spring cloud整套侵入式微服务是最佳落地实践，在k8s,云原生方面都是可以完美落地的。对比非侵入式的微服务架构istio等，在性能上有巨大优势，社区更加活跃。而在这一点上，oracle 花很多钱，找的写netty高级人员写的Helidon，一开始名称还是Java for cloud，看看这个投入和这个名称，结果如何呢，在市场上没有一点浪花，基本写出来一个寂寞而已，不够丢人的。

第三，对比jdk 8 stream api 和jdk 9 flow api，spring写出来的，异步非阻塞响应式框架，spring webflux＋r2dbc，是一个全链路异步非阻塞的，包括关系型数据库异步非阻塞。关键spring data r2dbc还是一个非常方便的orm框架，和spring data jpa封装的一样优秀。虽然spring webflux实测性能不如vert.x，但是spring webflux在降级熔断隔离，响应式事务上面适配完全没有问题，封装完美，程序员不需要关心。不是vert. x能比的。

综合上诉，我认为java交给oracle完全是拖累，而spring则是再帮oracle尽量延缓它的衰亡，但是也敌不过猪队友的骚操作。