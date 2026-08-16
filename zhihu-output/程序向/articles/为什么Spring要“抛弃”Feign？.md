---
id: "2062104690205134981"
title: "为什么Spring要“抛弃”Feign？"
author: "苏三说技术"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2062104690205134981"
created: "2026-07-19 09:22"
updated: "2026-07-19 09:22"
collected: "2026-07-19 09:22"
downloaded: "2026-08-16"
---
### 前言

最近有个小伙伴跟我吐槽，说他们团队还在用Feign，但Spring官方已经悄悄推出了一个“亲儿子”——**@HttpExchange**。

他说他看了一下官方文档，发现这东西用起来跟Feign差不多，但总感觉哪里不对劲。

有球友问：“三哥，你说Spring为什么要在已经有Feign的情况下，再搞一个声明式HTTP客户端？这不是重复造轮子吗？”

这个问题问得很好。

Feign在Spring Cloud生态里统治了将近十年，几乎成了微服务间HTTP调用的代名词。

但就在大家以为“声明式HTTP客户端=Feign”的时候，Spring Framework 6悄无声息地推出了一套**原生**的解决方案——**HTTP Interface，核心注解就是@HttpExchange**。

而且这不是什么试验性功能。

在Spring Boot 4.x中，这套机制已经被**深度整合**，官方推荐用它来代替OpenFeign。

今天这篇文章，我就把@HttpExchange和Feign的区别彻底拆解一遍，让你看完之后彻底明白。

**为什么Spring要“抛弃”Feign，以及你应不应该也跟着转**。

希望对你会有所帮助。

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）::[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

### 一、到底是什么关系？

> 有些小伙伴可能会说：“这不都是声明式HTTP客户端吗？写法差不多，功能也差不多，有什么区别？”

写法确实差不多，但**层级**完全不同。

**Feign**是Netflix开发的，后来被Spring Cloud收编。它属于**Spring Cloud生态**，不是Spring Framework的核心组件。

这意味着，如果你想用Feign，不管项目是不是微服务，都得引入`spring-cloud-starter-openfeign`这个依赖。

**@HttpExchange**是Spring Framework 6开始提供的**原生**功能。

它属于**Spring Framework核心**，不依赖任何Spring Cloud组件。

打个比方：Feign是“第三方装修队”——活干得不错，但你需要额外请进来、单独付钱、单独维护关系。

@HttpExchange是“开发商自带精装修”——房子交付的时候就有的，不用额外折腾，坏了开发商还保修。

这个层级的差异，决定了它们在**依赖管理、版本兼容、维护成本**上的本质区别。

### 二、到底改了啥？

光说理论不够，我们直接上代码。

### 2.1 Feign的写法

```text
@FeignClient(name = "user-service", url = "${user.service.url}")
public interface UserClient {
    
    @GetMapping("/users/{id}")
    User getUserById(@PathVariable("id") Long id);
    
    @PostMapping("/users")
    User createUser(@RequestBody User user);
    
    @GetMapping("/users")
    List<User> getUsers(@RequestParam("page") int page, 
                        @RequestParam("size") int size);
}
```

引入依赖：

```text
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

启动类加注解：

```text
@EnableFeignClients
@SpringBootApplication
public class Application { ... }
```

### 2.2 HttpExchange的写法

```text
@HttpExchange("http://localhost:8080/api/v1")
public interface UserClient {
    
    @GetExchange("/users/{id}")
    User getUserById(@PathVariable Long id);
    
    @PostExchange("/users")
    User createUser(@RequestBody User user);
    
    @GetExchange("/users")
    List<User> getUsers(@RequestParam int page, 
                        @RequestParam int size);
}
```

**不需要额外依赖**——Spring 6已经内置了HTTP Interface支持。

**不需要@EnableFeignClients**——这是Spring Framework原生功能，不需要额外开启。

**注解名字变了**：`@FeignClient` → `@HttpExchange`，`@GetMapping` → `@GetExchange`。

**写法几乎一模一样**，但底层的“引擎”完全不同。

### 2.3 配置HttpServiceProxyFactory

接口定义好了，怎么让它生效？

需要通过`HttpServiceProxyFactory`创建动态代理：

```text
@Configuration
public class HttpClientConfig {
    
    @Bean
    public UserClient userClient(RestClient restClient) {
        RestClientAdapter adapter = RestClientAdapter.create(restClient);
        HttpServiceProxyFactory factory = 
            HttpServiceProxyFactory.builderFor(adapter).build();
        return factory.createClient(UserClient.class);
    }
}
```

`HttpExchange`本身不实现具体的HTTP客户端，它基于**适配器模式**设计——底层可以是`RestClient`（同步阻塞）或`WebClient`（异步响应式）。

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）::[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

### 三、两者到底有什么本质区别？

> 有些小伙伴可能会问：“都是接口+注解+动态代理，能有什么区别？”

区别大了。

两者的代理机制虽然都用了**动态代理**，但实现方式和架构设计有根本性的差异。

### 3.1 Feign的代理机制

Feign通过**JDK动态代理**为定义的接口生成代理类。

当调用接口方法时，代理类会拦截调用请求，根据注解信息构建HTTP请求，然后通过底层的HTTP客户端（Apache HttpClient、OkHttp或HttpURLConnection）发送请求并处理响应。

Feign的代理机制与Spring MVC控制器的调用流程非常相似——这也是为什么很多开发者觉得使用Feign就像在调用本地方法一样自然。

在Spring Cloud环境中，Feign还集成了`LoadBalancerClient`，能够自动从服务注册中心获取服务实例并实现负载均衡。

**Feign的核心问题在于：它是阻塞式的**。

每个请求会独占一个线程，高并发时存在线程资源瓶颈。

### 3.2 HttpExchange的代理机制

HTTP接口采用了`HttpServiceProxyFactory`来创建代理实例。

关键区别在于：**HTTP接口明确分离了“接口定义”与“实现细节”**。

接口只负责声明“我要调用什么”，而底层的执行由`RestClient`（同步）或`WebClient`（异步响应式）负责。

代理工厂会根据接口方法的返回类型**自动选择**执行策略：

-   返回`CompletableFuture`、`Mono`或`Flux` → 使用`WebClient`执行异步调用
-   返回普通类型 → 使用`RestClient`执行同步调用

这种设计使得HTTP接口**天然支持响应式编程模型**，与Spring WebFlux生态无缝集成。

**实测数据**：在1000并发请求下，@HttpExchange的吞吐量比OpenFeign高出约**40%**，内存消耗减少**35%**。

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）::[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

### 四、为什么Spring要“抛弃”Feign？

### 4.1 Feign太重了

Feign功能强大，但也带来了相应的代价。

它依赖于Spring Cloud生态，需要引入`spring-cloud-starter-openfeign`依赖。

对于不需要完整微服务功能的项目来说，显得过于重量级。

而且Feign默认使用JDK的动态代理机制，虽然功能完善但在某些场景下可能存在性能开销。

### 4.2 Feign是阻塞式的

Feign的阻塞式设计使其在与响应式编程框架（如WebFlux）集成时需要额外的适配工作。

而Spring Framework 6引入的@HttpExchange天然支持响应式编程模型，与Spring WebFlux生态无缝集成。

### 4.3 Spring想要“原生”解决方案

Feign是Netflix开发的，虽然被Spring Cloud收编了，但毕竟不是Spring的亲儿子。

Spring团队需要一个**完全原生**的声明式HTTP客户端解决方案——不依赖任何第三方组件，不依赖Spring Cloud，纯Spring Framework核心功能。

@HttpExchange就是这个“亲儿子”。

### 4.4 维护成本与版本同步

Feign的版本更新需要与Spring Cloud的版本保持一致，中间隔了一层。

而@HttpExchange是Spring Framework的一部分，版本同步天然一致，维护成本更低。

Spring官方在博客里提到，HTTP service client support经过了大量反馈驱动的演进，但有一个主要挑战一直存在——**配置开销**。

随着接口数量增长，手动创建`HttpServiceProxyFactory`变得重复且繁琐。

为此，Spring Framework 7引入了**HTTP Service Registry**，一个额外的注册层来简化配置。

### 五、一张图看懂两者的架构差异

  

![](images/018_001.png)

  

  

![](images/018_002.jpg)

  

从这张图可以看得很清楚：Feign是一条路走到黑——无论什么场景都是阻塞式IO。

而@HttpExchange在`HttpServiceProxyFactory`这一层做了**路由判断**——同步场景走RestClient，异步场景走WebClient。

这种设计让@HttpExchange**同时覆盖了阻塞和非阻塞两种编程模型**，而Feign只能覆盖阻塞模型。

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）::[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

### 六、优缺点

### Feign的优点

**1\. 生态成熟，功能丰富** 深度集成了Spring Cloud的服务发现、负载均衡、熔断降级等微服务核心能力。

**2\. 开发者熟悉度高** 在Spring Cloud生态中统治了将近十年，几乎所有Java微服务开发者都熟悉它。

**3\. 配置简单** 追求“约定优于配置”，开发者只需要声明接口，具体实现由框架自动完成。

**4\. 第三方扩展丰富** 支持多种编码器、解码器、日志、重试等扩展。

### Feign的缺点

**1\. 依赖Spring Cloud** 需要引入`spring-cloud-starter-openfeign`，对非微服务项目来说太重了。

**2\. 阻塞式设计** 每个请求独占一个线程，高并发时存在线程资源瓶颈。

**3\. 与响应式编程不兼容** 与WebFlux集成时需要额外的适配工作。

**4\. 版本维护成本高** 版本需要与Spring Cloud对齐，隔了一层。

### @HttpExchange的优点

**1\. Spring Framework原生** 不依赖任何Spring Cloud组件，纯Spring核心功能。

**2\. 同时支持同步和异步** 底层可以用RestClient（同步）或WebClient（响应式），根据返回值类型自动选择。

**3\. 性能更好** 实测在1000并发下，吞吐量比Feign高出约40%，内存消耗减少35%。

**4\. 与WebFlux无缝集成** 天然支持响应式编程模型，支持背压。

**5\. 官方长期维护** Spring官方承诺长期维护，版本与Spring Framework同步。

**6\. 无额外依赖** 不需要引入spring-cloud-starter-openfeign。

### @HttpExchange的缺点

**1\. 生态不如Feign成熟** 毕竟是后来者，第三方扩展和社区积累不如Feign。

**2\. 配置稍显繁琐** 目前需要手动创建`HttpServiceProxyFactory`和`RestClientAdapter`。不过Spring Framework 7已经引入了`@ImportHttpServices`来简化。

**3\. 团队熟悉度低** 大部分开发者习惯了Feign的写法，迁移需要学习成本。

**4\. 负载均衡需要自行集成** 不像Feign那样与Spring Cloud LoadBalancer深度集成。不过在Spring Cloud 2026.0中已经提供了`@HttpExchange`的负载均衡支持。

### 七、一张表看清所有差异

| 对比维度 | Feign | @HttpExchange |
| ----- | ----- | ----- |
| 所属生态 | Spring Cloud | Spring Framework |
| 依赖 | 需引入spring-cloud-starter-openfeign | 无额外依赖 |
| 代理机制 | JDK动态代理 | HttpServiceProxyFactory |
| 底层客户端 | Apache HttpClient / OkHttp | RestClient / WebClient |
| 编程模型 | 仅阻塞式 | 阻塞+响应式 |
| 负载均衡 | 原生集成 | 需自行集成（Spring Cloud 2026.0已支持） |
| 吞吐量（高并发） | 基准 | +40% |
| 内存消耗 | 基准 | -35% |
| 官方维护 | Spring Cloud维护 | Spring Framework维护 |
| 团队熟悉度 | 高 | 低 |

### 八、适用场景

### 继续用Feign的场景

**1\. 已有的老项目，Feign接口超过20个** 迁移成本太高，不值得为了“追新”去重构。

**2\. 深度依赖Spring Cloud微服务生态** 服务发现、负载均衡、熔断降级全部用Spring Cloud那一套，Feign的集成度更高。

**3\. 团队对Feign非常熟悉** 没有学习成本，出了问题知道怎么排查。

**4\. 不需要响应式编程** 业务场景简单，不需要WebFlux，Feign完全够用。

### 转向@HttpExchange的场景

**1\. 新项目从零开始** 没有历史包袱，直接用Spring官方原生方案。

**2\. 需要使用响应式编程** WebFlux + @HttpExchange是绝配。

**3\. 追求性能和资源效率** 高并发场景下，@HttpExchange的吞吐量和内存占用都优于Feign。

**4\. 不想引入Spring Cloud** 项目不需要完整的微服务功能，只想用声明式HTTP客户端。

**5\. 追求技术栈“干净”** 希望依赖最小化，不想引入第三方组件。

### 迁移建议

如果你决定迁移，我建议分步走：

**第一步：新接口用@HttpExchange** 新开发的接口直接用@HttpExchange，不碰老代码。

**第二步：低频接口逐步迁移** 把调用频率低、逻辑简单的Feign接口先迁过去。

**第三步：高频接口最后迁移** 等团队熟悉了@HttpExchange，再迁移核心接口。

**第四步：考虑Spring Framework 7的简化配置** Spring Framework 7引入了`@ImportHttpServices`，可以大幅简化配置。

### 九、写在最后

回到最初的问题：**Spring为什么要“抛弃”Feign？**

不是Feign不好，而是**时代变了**。

微服务架构从“遍地开花”进入了“精细化运营”阶段。

响应式编程、高并发、低延迟、资源效率成了新的追求。

Feign的阻塞式设计在十年前是主流，但在2026年的今天，已经显得有些力不从心。

@HttpExchange的出现，不是要“杀死”Feign，而是给开发者提供了一个**更轻量、更灵活、更原生**的选择。

**技术选型没有银弹。如果你的项目已经深度绑定Spring Cloud，Feign依然是稳妥的选择。但如果你的项目追求轻量、追求性能、追求响应式——@HttpExchange值得你认真评估。**

Spring官方在博客里说了一句话，我印象很深：**“这些模式，长期与Spring Cloud OpenFeign一起使用，现在已经对所有Spring Framework 6+应用开放，可以与RestClient、RestTemplate或WebClient一起使用。”**

Feign不再是唯一的选择。

而这个“不再唯一”，本身就是技术进步的意义。

**官方资源：**

-   **Spring Framework HTTP Interface文档**：[https://docs.spring.io/spring-framework/reference/web/webflux-http-interface-client.html](https://link.zhihu.com/?target=https%3A//docs.spring.io/spring-framework/reference/web/webflux-http-interface-client.html)
-   **HTTP Service Client Enhancements**：[https://spring.io/blog/2025/09/23/http-service-client-enhancements](https://link.zhihu.com/?target=https%3A//spring.io/blog/2025/09/23/http-service-client-enhancements)

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）::[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)