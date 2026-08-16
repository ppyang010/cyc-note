---
id: "3507988674"
title: "tomcat 源码为啥不采用netty 处理并发？"
author: "江小北"
type: zhihu-answer
source: "https://www.zhihu.com/question/53498767/answer/3507988674"
created: "2024-05-23 22:32"
updated: "2024-05-23 22:32"
collected: "2024-05-23 22:32"
downloaded: "2026-08-16"
---
行，兄弟，这个问题有点意思。其实Tomcat选择不用Netty而用JDK NIO处理并发请求，是有它的一套道理的。咱们得从多个角度来分析这个问题：

### 1\. 历史原因

首先，得说说历史背景。Tomcat是个老牌子了，从上世纪90年代就有了。当初设计的时候，Netty还没出现呢，那时候大家都用JDK自带的API来处理网络编程。Tomcat在发展过程中，一直是基于JDK NIO的，后来随着Java版本的升级，JDK NIO也不断改进，Tomcat的架构也逐渐稳定下来。改变这种底层架构是需要很大成本的，尤其是一个已经成熟并被广泛使用的项目。

### 2\. 性能和稳定性

虽然Netty的性能确实很强大，但JDK NIO也不差。尤其是到了Java 7以后，JDK NIO的性能和稳定性已经大大提升。Tomcat团队对JDK NIO进行了大量的优化，使其能够很好地满足高并发的需求。换句话说，虽然Netty性能更强，但JDK NIO已经“够用”了，满足了Tomcat的需求。

### 3\. 兼容性和维护

Tomcat是个历史悠久的项目，有很多企业在使用。引入Netty意味着要对大量现有的代码进行重构，这不仅会带来兼容性问题，还会增加维护的复杂度。很多公司和开发者依赖Tomcat的稳定性，如果贸然引入新的技术，可能会带来很多未知的问题和风险。

### 4\. 社区和生态

Tomcat有着庞大的用户群体和社区支持。很多开发者对Tomcat的代码非常熟悉，习惯了它的API和使用方式。引入Netty后，很多习惯和使用方式可能需要改变，这对于开发者来说也是一种负担。社区的接受度也是Tomcat团队必须考虑的问题。

### 5\. 定位不同

最后，得说说Tomcat和Netty的定位。Tomcat是一个Servlet容器，主要用来运行Java Web应用。而Netty则是一个通用的网络框架，可以用来构建各种网络应用。两者的设计目标和应用场景有所不同。Tomcat团队更关注的是如何在现有架构上提升性能和稳定性，而不是彻底重写整个网络层。

### 总结

所以，Tomcat选择继续使用JDK NIO而不是Netty，主要是出于历史原因、性能和稳定性、兼容性和维护成本、社区接受度以及两者的定位不同等多方面的考虑。虽然Netty性能更好，但对Tomcat来说，JDK NIO已经足够应对高并发的需求，同时还能保持代码的稳定和兼容。换句话说，Tomcat选择的技术路线，是在综合考虑了各方面因素后的最佳选择。

## 说在最后

最后再推荐一个Tomcat源码和Netty源码的免费专栏课程，帮助你更好的了解这两个框架的底层原理

### Tomcat源码分析

[01、Tomcat源码：导入tomcat源码进eclipse](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9124)

[02、Tomcat源码：tomcat主类](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9126)

[03、Tomcat源码：Bootstrap类代码分析](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9128)

[04、Tomcat源码：tomcat配置文件解析工具Digester](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9130)

[05、Tomcat源码：catalina类](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9132)

[06、Tomcat源码：tomcatjmx管理](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9134)

[07、Tomcat源码：tomcat组件之Server](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9136)

[08、Tomcat源码：tomcat组件之Service](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9138)

[09、Tomcat源码：tomcat組件之Container和Engine](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9140)

[10、Tomcat源码：tomcat組件之Host](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9142)

[11、Tomcat源码：Host的LifecycleListener--------->HostConfig](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9144)

[12、Tomcat源码：tomcat组件之Context](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9146)

[13、Tomcat源码：tomcatContextConfig](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9148)

[14、Tomcat源码：tomcatContextConfig](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9150)

[15、Tomcat源码：tomcatWrapper](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9152)

[16、Tomcat源码：tomcatConnector](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9154)

[17、Tomcat源码：socket处理概览](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9156)

[18、Tomcat源码：tomcat中并发的情况和处理](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9158)

[19、Tomcat源码：tomcatStandardEngineValve](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9160)

[20、Tomcat源码：tomcatsocket处理流程分析](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D9162)

  

### Netty源码分析

[01、Netty源码分析：HelloWorld案例](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4470)

[02、Netty源码分析：NioEventLoopGroup](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4472)

[03、Netty源码分析：SelectorProvider](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4474)

[04、Netty源码分析：NioEventLoop](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4476)

[05、Netty源码分析：NioEventLoop构造函数](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4478)

[06、Netty源码分析：NioEventLoop.executor](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4480)

[07、Netty源码分析：NioEventLoop.selectStrategy](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4482)

[08、Netty源码分析：NioEventLoop.selector](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4484)

[09、Netty源码分析：NioEventLoopGroup.chooser](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4486)

[10、Netty源码分析：ServerBootstrap](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4488)

[11、Netty源码分析：ChannelOption](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4490)

[12、Netty源码分析：ChannelHandler](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4492)

[13、Netty源码分析：ChannelFactory](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4494)

[14、Netty源码分析：NioServerSocketChannel](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4496)

[15、Netty源码分析：ServerSocketChannel](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4498)

[16、Netty源码分析：ChannelId](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4500)

[17、Netty源码分析：AbstractUnsafe](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4502)

[18、Netty源码分析：Unsafe.bind()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4504)

[19、Netty源码分析：Unsafe.register()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4506)

[20、Netty源码分析：Unsafe.connect()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4508)

[21、Netty源码分析：Unsafe.read()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4510)

[22、Netty源码分析：ChannelOutboundBuffer（上）](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4512)

[23、Netty源码分析：ChannelOutboundBuffer（下）](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4514)

[24、Netty源码分析：Unsafe.write()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4516)

[25、Netty源码分析：Unsafe.close()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4518)

[26、Netty源码分析：ChannelPipeline](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4520)

[27、Netty源码分析：ChannelPipeline.add](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4522)

[28、Netty源码分析：ChannelPipeline.fireChannelRegistered与bind](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4524)

[29、Netty源码分析：ChannelPipeline的active与read](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4526)

[30、Netty源码分析：ChannelPipeline的fireChannelRead](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4528)

[31、Netty源码分析：ChannelPipeline的write](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4530)

[32、Netty源码分析：ChannelPipeline的flush](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4532)

[33、Netty源码分析：ChannelPipeline的Unregistered](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4534)

[34、Netty源码分析：ChannelPipeline的close](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4536)

[35、Netty源码分析：ChannelPipeline的connect与disconnect](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4538)

[36、Netty源码分析：DefaultChannelPromise](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4540)

[37、Netty源码分析：ChannelConfig](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4542)

[38、Netty源码分析：ByteBufAllocator](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4544)

[39、Netty源码分析：PoolSubPage](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4546)

[40、Netty源码分析：PoolSubPage的内存分配](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4548)

[41、Netty源码分析：PoolSubPage的内存释放](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4550)

[42、Netty源码分析：SizeClasses](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4552)

[43、Netty源码分析：PoolChunk](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4554)

[44、Netty源码分析：PoolChunk.runsAvail](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4556)

[45、Netty源码分析：PoolChunk.runsAvailMap](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4558)

[46、Netty源码分析：PoolChunk.allocate](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4560)

[47、Netty源码分析：PoolChunk释放内存](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4562)

[48、Netty源码分析：PooledByteBuf](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4564)

[49、Netty源码分析：PooledByteBuf的方法](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4566)

[50、Netty源码分析：缓存池ObjectPool](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4568)

[51、Netty源码分析：PoolArena](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4570)

[52、Netty源码分析：PoolArena的内存分配](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4572)

[53、Netty源码分析：PoolArena的内存释放与扩容](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4574)

[54、Netty源码分析：PoolThreadCache](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4576)

[55、Netty源码分析：PoolThreadCache的功能](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4578)

[56、Netty源码分析：PoolThreadLocalCache](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4580)

[57、Netty源码分析：InternalThreadLocalMap](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4582)

[58、Netty源码分析：PooledByteBufAllocator](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4584)

[59、Netty源码分析：RecvByteBufAllocator](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4586)

[60、Netty源码分析：MessageSizeEstimator](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4588)

[61、Netty源码分析：ServerBootstrap.bind()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4590)

[62、Netty源码分析：NioEventLoop.execute()](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4592)

[63、Netty源码分析：ServerBootstrapAcceptor](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4594)

[64、Netty源码分析：ByteToMessageDecoder](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4596)

[65、Netty源码分析：解码器](https://link.zhihu.com/?target=https%3A//cxykk.com/%3Fp%3D4598)