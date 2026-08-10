**前言**
------

> [Tomcat](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Tomcat&zhida_source=entity)笑麻了，[Jetty](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Jetty&zhida_source=entity)默默上位，[Undertow](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Undertow&zhida_source=entity)用户哭了

最近在帮一个团队做[Spring Boot 4.0](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Spring+Boot+4.0&zhida_source=entity)升级评估的时候，发现了一个让他们措手不及的问题。

“三哥，我们项目里用的Undertow，升级到Spring Boot 4.0之后直接启动不了了，报错说找不到Undertow的实现类。这是什么情况？”

我一看报错信息，心里就有数了——**Spring Boot 4.0正式移除了对Undertow的支持**。

这个小伙伴当场就懵了。

“Undertow不是号称性能最好的[嵌入式容器](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%B5%8C%E5%85%A5%E5%BC%8F%E5%AE%B9%E5%99%A8&zhida_source=entity)吗？Spring为什么要抛弃它？”

这个问题问得很到位。

今天这篇文章，我就把Spring Boot 4.0弃用Undertow的前因后果、底层原因、迁移方案从头到尾给你拆解一遍。

希望对你会有所帮助。

最近缺项目经历想快速提升[项目实战](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E9%A1%B9%E7%9B%AE%E5%AE%9E%E6%88%98&zhida_source=entity)能力（包含多个[AI](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=AI&zhida_source=entity)项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

**一、Undertow是怎么“上位”的？**
-----------------------

在聊弃用之前，我们先花2分钟回顾一下Undertow是怎么进入Spring Boot生态的。

Spring Boot从很早就支持三种嵌入式Web容器：

*   **Tomcat**（默认）——[Apache](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Apache&zhida_source=entity)出品，生态最成熟，Spring Boot的亲儿子
*   **Jetty**——Eclipse[基金会](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%9F%BA%E9%87%91%E4%BC%9A&zhida_source=entity)出品，轻量灵活，在某些场景下表现优异
*   **Undertow**——[Red Hat](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Red+Hat&zhida_source=entity)出品，号称低内存占用、[高并发](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E9%AB%98%E5%B9%B6%E5%8F%91&zhida_source=entity)吞吐、天然支持[持久连接](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E6%8C%81%E4%B9%85%E8%BF%9E%E6%8E%A5&zhida_source=entity)

Undertow之所以能进入Spring Boot的可选列表，靠的是它的**性能优势**。

在高并发场景下，Undertow的内存占用比Tomcat低、[吞吐量](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%90%9E%E5%90%90%E9%87%8F&zhida_source=entity)更高，因此吸引了不少追求极致性能的企业项目。

**但是，成也性能，败也规范。** 

**二、为什么Spring Boot 4.0要弃用Undertow？**
------------------------------------

> 有些小伙伴可能会说：“Undertow性能这么好，Spring团队为什么要抛弃它？这不是自断一臂吗？”

这个问题的答案，不在Spring团队身上，在**[Servlet](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Servlet&zhida_source=entity)规范**身上。

### **2.1 根本原因：Servlet 6.1不兼容**

Spring Boot 4.0基于Spring Framework 7构建，强制依赖**Servlet 6.1规范**。

而Undertow**尚未适配Servlet 6.1**。

Spring团队在官方文档中明确说明了移除Undertow支持的技术原因：

> **“Spring Boot 4.0需要一个Servlet 6.1的[基线](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%9F%BA%E7%BA%BF&zhida_source=entity)，而Undertow目前尚不兼容。因此，我们放弃了对Undertow的支持。”**

这不是Spring团队的主观决策，而是技术生态演进的必然结果。

![](https://picx.zhimg.com/v2-6e249a94d7a7588ee0d9c076c3c1bc59_1440w.jpg)

### **2.2 深层次原因：Red Hat投入有限**

Undertow的主要维护方是**Red Hat**。

而Red Hat对该项目的投入相对有限，导致Undertow无法及时跟进新规范。

在相关讨论中，Undertow团队成员表示Servlet 6.1的支持工作已经启动，但截至2025年10月，该工作仍处于早期阶段。

Spring Boot团队在[GitHub](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=GitHub&zhida_source=entity)上创建了专门的Issue（#46917）来跟踪这一变更。

在Issue中，团队指出：**Undertow尚未适配[Servlet 6.1](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=6&q=Servlet+6.1&zhida_source=entity)，且其维护团队资源不足、迭代效率低，Spring Boot团队已无法承担过高的适配成本**。

简单说就是：**我等了你很久，但你一直跟不上，我只能先走了。** 

### **2.3 还有一些“隐情”：社区活跃度差距**

除了技术兼容性问题，还有一些不那么“官方”的原因：

*   **Undertow社区相对较小**，文档、学习资料等方面都不如Tomcat、Jetty丰富
*   **对传统Servlet模型的支持不够完善**
*   **Red Hat的资源重心可能在其他项目上**

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

**三、Servlet 6.1到底带来了什么变化？**
---------------------------

> 有些小伙伴可能会问：“Servlet 6.1到底有什么新东西，值得Spring Boot这么大动干戈？”

Servlet 6.1于2024年4月作为[Jakarta](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Jakarta&zhida_source=entity) EE 11的核心子规范发布。

相比Servlet 6.0，它带来了多项重要改进：

![](https://pica.zhimg.com/v2-e2366e24772ebe35696d7c50fb2935e0_1440w.jpg)

**① [ByteBuffer](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=ByteBuffer&zhida_source=entity)支持**

在ServletInputStream和ServletOutputStream中新增了ByteBuffer支持，显著改进了非阻塞I/O能力。

```text
// 使用 ByteBuffer 读取请求数据
ByteBuffer buffer = ByteBuffer.allocate(1024);
servletInputStream.read(buffer);

```

**② [HTTP/2](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=HTTP%2F2&zhida_source=entity)推送功能废弃**

Servlet 6.1正式废弃了[HTTP/2 Server Push](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=HTTP%2F2+Server+Push&zhida_source=entity)支持。这个功能在现代Web应用中使用率持续下降。

**③ 移除SecurityManager相关[API](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=API&zhida_source=entity)**

完全删除了对已废弃的Java SecurityManager及相关API的引用。

**④ HTTP会话增强机制**

提供了新机制，让应用程序能在标准[HTTP请求](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=HTTP%E8%AF%B7%E6%B1%82&zhida_source=entity)处理之外与HTTP会话交互，特别是为WebSocket场景提供了更好的支持。

**⑤ HTTP重定向控制增强**

[开发者](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%BC%80%E5%8F%91%E8%80%85&zhida_source=entity)现在对发出HTTP重定向时的状态码和响应体拥有更精细的控制权。

**⑥ 敏感请求头安全处理**

新增了`HttpServlet.isSensitiveHeader`方法，用于识别需要保护的敏感请求头。

**四、对现有项目的影响：升级必看**
-------------------

如果你的项目当前使用了Undertow，升级到Spring Boot 4.0后会遇到什么问题？

### **4.1 典型报错**

如果项目中包含以下依赖：

```text
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>

```

升级到Spring Boot 4.0后，项目将无法启动，并抛出类似错误：

```text
Caused by: java.lang.IllegalStateException: Unable to find Undertow-based WebServer implementation.

```

### **4.2 三大风险点**

| 风险项 | 说明 |
| --- | --- |
| 启动失败 | 缺少Undertow实现类，应用无法启动 |
| 配置失效 | server.undertow.\*配置被完全忽略 |
| 性能回退 | 切换容器后需要重新压测和调优 |

**五、迁移方案：如何平滑过渡？**
------------------

别慌。Spring Boot 4.0仍然支持两种嵌入式[Web容器](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=2&q=Web%E5%AE%B9%E5%99%A8&zhida_source=entity)，迁移并不复杂。

### **5.1 方案一：切换回Tomcat（最推荐）**

Tomcat是Spring Boot的默认容器，生态成熟、文档丰富，且在Spring Boot 4中已全面适配Servlet 6.1。

**步骤1：移除Undertow依赖**

```text
<!-- 删除以下依赖 -->
<!--
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-undertow</artifactId>
</dependency>
-->

```

**步骤2：显式添加Tomcat（通常无需添加）**

`[spring-boot-starter-web](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=spring-boot-starter-web&zhida_source=entity)`已经默认包含了Tomcat：

```text
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-tomcat</artifactId>
</dependency>

```

**步骤3：转换配置**

将`server.undertow.*`配置转换为`server.tomcat.*`：

```text
# 旧配置（Undertow）
server:
  undertow:
    io-threads: 4
    worker-threads: 20
    buffer-size: 1024

# 新配置（Tomcat）
server:
  tomcat:
    threads:
      max: 200
      min-spare: 10
    max-connections: 8192

```

### **5.2 方案二：改用Jetty**

Jetty同样支持Servlet 6.1，在某些[I/O密集型](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=I%2FO%E5%AF%86%E9%9B%86%E5%9E%8B&zhida_source=entity)场景下表现优异。

```text
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>

```

**注意**：需要排除Tomcat依赖，避免冲突：

```text
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>

```

### **5.3 Spring Boot 4.0支持的容器版本**

Spring Boot 4.0对嵌入式Web容器的支持如下：

| 容器 | 版本要求 | Servlet规范 | 支持状态 |
| --- | --- | --- | --- |
| Tomcat | 11.0.x | Servlet 6.1 | ✅ 支持 |
| Jetty | 12.1.x | Servlet 6.1 | ✅ 支持 |
| Undertow | — | — | ❌ 已移除 |

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

**六、一张图看懂完整的变更**
----------------

![](https://pic2.zhimg.com/v2-b5700f8644070aff61c836a6ed9ee43b_1440w.jpg)

**七、优缺点**
---------

### **Spring Boot 4.0移除Undertow的“好处”**

**1\. 规范对齐，[技术栈](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E6%A0%88&zhida_source=entity)更清晰**Spring Boot 4.0强制依赖Servlet 6.1，只保留兼容的容器，减少了技术栈的混乱。

**2\. 减少维护负担**Spring Boot团队不再需要为Undertow维护[兼容层](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=%E5%85%BC%E5%AE%B9%E5%B1%82&zhida_source=entity)，可以集中精力在核心功能上。

**3\. 推动生态向前**这一决策倒逼Undertow社区加快适配Servlet 6.1的步伐。

**4\. 与Jakarta EE 11对齐**Spring Boot 4.0全面升级至Jakarta EE 11，只保留兼容的容器是合理的架构决策。

### **对开发者的“代价”**

**1\. 迁移成本**使用Undertow的项目需要切换到Tomcat或Jetty，并重新配置和调优。

**2\. 性能不确定性**如果之前是因为Undertow的性能优势才选择的它，切换到其他容器后可能需要重新压测和调优。

**3\. 配置需要重写**`server.undertow.*`配置全部失效，需要转换为Tomcat或Jetty的配置格式。

**4\. 短期内的阵痛**对于深度依赖Undertow特性的项目，迁移可能需要一定的开发时间。

**八、适用场景与建议**
-------------

### **如果你在用Undertow**

| 场景 | 建议 |
| --- | --- |
| 正准备升级到Spring Boot 4.0 | 先切换到Tomcat或Jetty，再执行升级 |
| 尚未升级，还在Spring Boot 3.x | 可以继续用Undertow，但建议开始规划迁移 |
| 新项目从零开始 | 直接用Tomcat（默认）或Jetty，别碰Undertow |

### **选Tomcat还是Jetty？**

| 对比维度 | Tomcat | Jetty |
| --- | --- | --- |
| 生态成熟度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 文档丰富度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 默认支持 | ✅ 默认 | ❌ 需手动引入 |
| I/O密集型 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 企业级特性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**我的建议**：大部分项目直接切回Tomcat就行，因为它是Spring Boot的默认容器，生态最成熟、文档最丰富。如果你的应用是[I/O](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=4&q=I%2FO&zhida_source=entity)密集型的，可以考虑Jetty。

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)

**九、写在最后**
----------

回到最初的问题：**Spring Boot 4.0为什么要弃用Undertow？**

答案很清晰——**不是Spring团队不待见Undertow，而是Undertow跟不上Servlet规范的演进速度**。

Spring Boot 4.0强制依赖Servlet 6.1，而Undertow尚未适配。

Red Hat对Undertow的投入有限，导致其无法及时跟进新规范。

Spring Boot团队已经等了很久，但等不下去了。

**Undertow会被永久抛弃吗？**

不一定。

只要Undertow未来支持Servlet 6.1，Spring Boot仍有可能恢复对其支持。

Undertow团队已经在2025年10月发布了2.4.0.Alpha1，开始实现Jakarta Servlet 6.1。

但问题是——**什么时候能正式支持？** 没有人知道确切的时间表。

对于正在做技术选型或准备升级的团队来说，等待Undertow适配不是一个明智的选择。

**我的建议是**：如果你正在使用Undertow，**建议尽快规划迁移到Tomcat或Jetty**。

尤其是新项目，直接用Tomcat（Spring Boot默认）是最省心的选择。

**官方资源：** 

*   **Spring Boot 4.0 Migration Guide**：[https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide](https://link.zhihu.com/?target=https%3A//github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide)
*   **Spring Boot 4.0 [Release Notes](https://zhida.zhihu.com/search?content_id=280054619&content_type=Article&match_order=1&q=Release+Notes&zhida_source=entity)**：[https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Release-Notes](https://link.zhihu.com/?target=https%3A//github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Release-Notes)

最近缺项目经历想快速提升项目实战能力（包含多个AI项目），或者最近找工作，或者想学习AI的小伙伴，可以看看下面👇🏻的这个链接（或许真的能够帮到你）[http://susan.net.cn/project](https://link.zhihu.com/?target=http%3A//susan.net.cn/project)