---
id: "3578004449"
title: "相较于 Dubbo，Spring Cloud 有何优缺点？"
author: "架构师专栏"
type: zhihu-answer
source: "https://www.zhihu.com/question/50806354/answer/3578004449"
created: "2024-07-30 10:43"
updated: "2024-07-30 10:43"
collected: "2024-07-30 10:43"
downloaded: "2026-08-16"
---
好，兄弟，微服务这块，你不懂不要紧，哥来给你上上课。今儿个就把Dubbo和Spring Cloud扒拉个底儿朝天，咱就看看到底谁更胜一筹。拿个小本本记好了。

### 微服务大时代

你公司业务发展，往微服务方向走，那是大势所趋。单体应用就像胖子跑马拉松，扛不住的。微服务一出，瞬间解决了扩展性和维护性的问题。这时候Dubbo和Spring Cloud就成了焦点，一个是国内的老炮儿，一个是国外的明星选手。咱们就来看看，谁能更好地扛起微服务的大旗。

最近无意间获得一份阿里大佬写的刷题笔记，一下子打通了我的任督二脉，进大厂原来没那么难。这是大佬写的， [七千页的BAT大佬写的刷题笔记，让我offer拿到手软](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/share/index.html)

### Dubbo vs Spring Cloud：基本盘

### Dubbo：老炮儿的底气

Dubbo可是阿里巴巴亲生的，出道早，在国内互联网公司里有不少粉丝。服务治理、负载均衡、服务注册发现这些基本操作，那是信手拈来。不过它的命运有点坎坷，曾经一度被“废弃”，不过最近又重新活跃起来了。

**优点：**

1.  **高性能**：Dubbo的RPC性能相当不错，二进制协议，速度飞快，适合高并发场景。
2.  **易集成**：和Spring搭配起来很自然，集成方便，配置也简单。
3.  **灵活扩展**：扩展性好，各种插件随便装，满足定制化需求。

**缺点：**

1.  **生态不全**：Dubbo的生态圈相对单薄，缺乏一些高级功能和配套工具。
2.  **社区活跃度低**：社区相对冷清，遇到问题找人帮忙不太容易。

### Spring Cloud：国际明星

Spring Cloud，那可是Spring家族的亲儿子，功能全到令人发指。它涵盖了服务注册与发现、配置管理、服务间调用、负载均衡、熔断、监控、链路追踪，几乎囊括了微服务需要的所有功能。

**优点：**

1.  **功能全面**：Spring Cloud生态系统完整，微服务需要的功能一应俱全，几乎是为微服务量身定做的。
2.  **社区活跃**：社区非常活跃，文档、教程、示例一应俱全，遇到问题基本都能找到解决方案。
3.  **无缝集成**：与Spring生态系统无缝集成，自然优势。

**缺点：**

1.  **学习曲线陡**：功能多，学习起来需要一定时间和精力。
2.  **性能一般**：使用HTTP协议，性能比Dubbo的二进制协议差一些。

### 深度对比：公司里的真刀实枪

### 性能对比

Dubbo在性能上绝对是优势明显。它使用的是二进制协议的RPC调用，速度快，适合高并发场景。而Spring Cloud使用的是HTTP/RESTful风格的接口，性能上稍逊一筹。不过，性能并不是唯一的考量因素，得看具体业务需求。

### 扩展性和灵活性

Spring Cloud的扩展性和灵活性无出其右。它提供了一整套完整的微服务解决方案，各种服务治理、链路追踪工具都能现成使用。而Dubbo虽然在扩展性上也不错，但在功能的全面性和配套工具的丰富度上稍显不足。

### 社区支持和生态系统

Spring Cloud在社区支持和生态系统方面遥遥领先。GitHub上那么多的Star和Fork，各种问题都有大佬们帮忙解决。而Dubbo的社区相对冷清，遇到问题需要更多的自力更生。

### 学习成本

Dubbo的学习成本相对较低，上手快，尤其是对国内的开发者来说，中文文档和资料丰富。而Spring Cloud因为功能多，学习曲线相对陡峭，需要花更多的时间和精力去掌握。

### 实战经验：公司里的那些事儿

### 用Dubbo的公司

很多老牌互联网公司还在用Dubbo，尤其是那些系统已经稳定运行，改动成本高的公司。Dubbo的高性能在高并发场景下很受欢迎。然而，当需要更复杂的服务治理和链路追踪时，Dubbo显得有点吃力，往往需要自己手动填坑。

### 用Spring Cloud的公司

那些新兴公司和追求新技术的公司更倾向于Spring Cloud。它功能全面，配套工具齐全，服务治理、配置中心、熔断限流这些都有现成的，非常适合快速搭建微服务架构。然而，性能上的不足在高并发场景下需要特别注意和优化。

### 总结：该选谁？

最后总结一下，Dubbo和Spring Cloud各有优劣，具体选择要看你的业务需求。如果你追求高性能、系统相对简单，Dubbo是个不错的选择。如果你追求功能全面、服务治理和监控一步到位，Spring Cloud无疑是更好的选择。

总之，兄弟，咱们做技术的，不仅要看眼前的需求，还得放眼未来的发展。选择技术栈就像选对象，适合自己的才是最好的。希望你能在微服务的道路上顺风顺水，越走越远！

推荐一个可以免费看，500套技术教程的网站，希望对你有帮助

[弟弟快看-教程，程序员编程资料站 | DDKK.COM](https://link.zhihu.com/?target=https%3A//www.ddkk.com/)

### 推荐一些系列教程，希望能帮到你

Dubbo 实战系列教程

-   [01、Dubbo 实战 - 入门示例](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/1.html)
-   [02、Dubbo 实战 - 架构](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/2.html)
-   [03、Dubbo 实战 - 框架设计](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/3.html)
-   [04、Dubbo 实战 - 设计模式](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/4.html)
-   [05、Dubbo 实战 - 扩展Spring Schema](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/5.html)
-   [06、Dubbo 实战 - Spring加载Bean流程](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/6.html)
-   [07、Dubbo 实战 - 扩展点](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/7.html)
-   [08、Dubbo 实战 - 扩展点装饰](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/8.html)
-   [09、Dubbo 实战 - ExtensionFactory](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/9.html)
-   [10、Dubbo 实战 - 代理](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/10.html)
-   [11、Dubbo 实战 - 远程调用流程](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/11.html)
-   [12、Dubbo 实战 - Refer](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/12.html)
-   [13、Dubbo 实战 - Export](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/13.html)
-   [14、Dubbo 实战 - 生产者发布服务](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/14.html)
-   [15、Dubbo 实战 - 消费者引用服务](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/15.html)
-   [16、Dubbo 实战 - 集群容错](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/16.html)
-   [17、Dubbo 实战 - telnet](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/4/17.html)

Dubbo 3.x 源码解析系列文章

-   [01、Dubbo 3.x 源码解析 - RPC是什么？RPC与HTTP的关系](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/1.html)
-   [02、Dubbo 3.x 源码解析 - 源码调试环境准备](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/2.html)
-   [03、Dubbo 3.x 源码解析 - Dubbo SPI机制的介绍与使用](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/3.html)
-   [04、Dubbo 3.x 源码解析 - Dubbo SPI机制的源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/4.html)
-   [05、Dubbo 3.x 源码解析 - Dubbo xml配置的加载源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/5.html)
-   [06、Dubbo 3.x 源码解析 - Dubbo3域模型以及Model和Environment初始化【一万字】](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/6.html)
-   [07、Dubbo 3.x 源码解析 - Dubbo配置的加载入口源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/7.html)
-   [08、Dubbo 3.x 源码解析 - Dubbo配置中心的加载与优先级源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/8.html)
-   [09、Dubbo 3.x 源码解析 - Dubbo启动元数据中心源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/9.html)
-   [10、Dubbo 3.x 源码解析 - Dubbo初始化导出/引用模块配置源码](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/10.html)
-   [11、Dubbo 3.x 源码解析 - Dubbo服务的发布与引用的入口](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/11.html)
-   [12、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(1)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/12.html)
-   [13、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(2)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/13.html)
-   [14、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(3)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/14.html)
-   [15、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(4)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/15.html)
-   [16、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(5)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/16.html)
-   [17、Dubbo 3.x 源码解析 - Dubbo服务发布导出源码(6)](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/dubbo/2/17.html)

SpringCloud Alibaba 系列文章

-   [01、SpringCloud Alibaba 简介](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/34.html)
-   [02、SpringCloud Alibaba（1）版本管理规范](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/35.html)
-   [03、SpringCloud Alibaba（2）依赖管理](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/36.html)
-   [04、SpringCloud Alibaba（3）父项目的创建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/37.html)
-   [05、SpringCloud Alibaba Nacos（1）Nacos 整体简介](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/38.html)
-   [06、SpringCloud Alibaba Nacos（1）Nacos Discovery 简介](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/39.html)
-   [07、SpringCloud Alibaba Nacos（2）Nacos Server 安装](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/40.html)
-   [08、SpringCloud Alibaba Nacos（3）框架的搭建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/41.html)
-   [09、SpringCloud Alibaba Nacos（4）使用 Nacos 做注册中心-5100字匠心出品](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/42.html)
-   [10、SpringCloud Alibaba Nacos（5）负载均衡测试](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/43.html)
-   [11、SpringCloud Alibaba Nacos（6）Nacos Discovery 对外暴露的 Endpoint](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/44.html)
-   [12、SpringCloud Alibaba Nacos（7）Nacos Discovery Starter 更多的配置项](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/45.html)
-   [13、SpringCloud Alibaba Nacos（1）Nacos Config 简介](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/46.html)
-   [14、SpringCloud Alibaba Nacos（2）项目的搭建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/47.html)
-   [15、SpringCloud Alibaba Nacos（3）在 nacos-server 里面添加配置](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/48.html)
-   [16、SpringCloud Alibaba Nacos（4）获取配置信息](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/49.html)
-   [17、SpringCloud Alibaba Nacos（5）获取配置规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/50.html)
-   [18、SpringCloud Alibaba Nacos（6）配置划分实战](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/51.html)
-   [19、SpringCloud Alibaba Nacos（7）配置回滚](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/52.html)
-   [20、SpringCloud Alibaba Nacos（8）获取多个配置](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/53.html)
-   [21、SpringCloud Alibaba Nacos（9）SpringCloud Alibaba NacosConfig 常用的配置](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/54.html)
-   [22、SpringCloud Alibaba Sentinel（1）Sentinel 简介](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/55.html)
-   [23、SpringCloud Alibaba Sentinel（2）Sentinel 控制台安装](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/56.html)
-   [24、SpringCloud Alibaba Sentinel（3）搭建客户端](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/57.html)
-   [25、SpringCloud Alibaba Sentinel（4）流控规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/58.html)
-   [26、SpringCloud Alibaba Sentinel（5）降级规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/59.html)
-   [27、SpringCloud Alibaba Sentinel（6）热点规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/60.html)
-   [28、SpringCloud Alibaba Sentinel（7）系统规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/61.html)
-   [29、SpringCloud Alibaba Sentinel（8）授权规则](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/62.html)
-   [30、SpringCloud Alibaba Sentinel（9）@SentinelResource 简介以及框架初步搭建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/63.html)
-   [31、SpringCloud Alibaba Sentinel（10）完善 sentinel-provider](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/64.html)
-   [32、SpringCloud Alibaba Sentinel（11）完善 sentinel-consumer](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/65.html)
-   [33、SpringCloud Alibaba Sentinel（12）异常回退方法的其他用法](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/66.html)
-   [34、SpringCloud Alibaba Seata（1）Seata 简介与安装](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/67.html)
-   [35、SpringCloud Alibaba Seata（2）框架的搭建-7800字匠心出品](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/68.html)
-   [36、SpringCloud Alibaba Seata（3）代码的完善（分布式事务演示）-15800字匠心巨作](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/69.html)
-   [37、SpringCloud Alibaba Seata（4）集成 Feign 测试 Seata](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/70.html)
-   [38、SpringCloud Alibaba Dubbo（1）项目简介与功能完成度](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/71.html)
-   [39、SpringCloud Alibaba Dubbo（2）框架的搭建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/72.html)
-   [40、SpringCloud Alibaba Dubbo（3）代码的完善](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/73.html)
-   [41、SpringCloud Alibaba Dubbo（4）负载均衡调用测试](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/74.html)
-   [42、SpringCloud Alibaba RocketMQ（1）RocketMQ 介绍以及基本使用](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/75.html)
-   [43、SpringCloud Alibaba RocketMQ（2）Spring Cloud Stream 介绍](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/76.html)
-   [44、SpringCloud Alibaba RocketMQ（3）测试框架搭建](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/77.html)
-   [45、SpringCloud Alibaba RocketMQ（4）完善 rocketmq-produce-example 项目](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/78.html)
-   [46、SpringCloud Alibaba RocketMQ（5）完善 rocketmq-consumer-example 项目](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/79.html)
-   [47、SpringCloud Alibaba RocketMQ（6）测试案例测试](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/j2ee/springcloudalibaba/2/80.html)

### 这个东西：让我offer拿到手软

最近无意间获得一份阿里大佬写的刷题笔记，一下子打通了我的任督二脉，进大厂原来没那么难。这是大佬写的， [七千页的BAT大佬写的刷题笔记，让我offer拿到手软](https://link.zhihu.com/?target=https%3A//www.ddkk.com/zhuanlan/share/index.html)

### 项目文档&视频：

[开源：项目文档 & 视频 Github-Doc](https://link.zhihu.com/?target=https%3A//www.ddkk.com/%23github-doc)

已收录于，我的技术网站：[ddkk.com](https://link.zhihu.com/?target=https%3A//www.ddkk.com/) 里面有，500套技术系列教程、1万+道，面试八股文、BAT面试真题、简历模版，工作经验分享、架构师成长之路，等等什么都有，欢迎收藏和转发。

### 求一键三连：点赞、分享、收藏

点赞对我真的非常重要！在线求赞，加个关注我会非常感激！