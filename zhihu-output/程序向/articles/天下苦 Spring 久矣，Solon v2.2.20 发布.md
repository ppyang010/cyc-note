---
id: "631149598"
title: "天下苦 Spring 久矣，Solon v2.2.20 发布"
author: "门前一棵树"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/631149598"
created: "2023-05-22 09:18"
updated: "2023-07-22 08:52"
collected: "2023-05-22 09:18"
downloaded: "2026-08-16"
---
### Solon 是什么框架？

一个，**Java 新的生态型应用开发框架**。它从零开始构建，有自己的标准规范与开放生态。与其他框架相比：

```text
它解决了两个重要的痛点：启动慢，费资源。
```

### 解决痛点？

由于Solon Bean容器的独特设计：

```text
不会因为扩展依赖变多而启动很慢（开发调试时，爽快）！
```

以开源项目“小诺”为例：

-   [“snowy-spring 版”](https://link.zhihu.com/?target=https%3A//gitee.com/xiaonuobase/snowy) 启动 30-50秒
-   [“snowy-solon 版”](https://link.zhihu.com/?target=https%3A//gitee.com/xiaonuoadmin/snowy-solon) 启动3-5秒（有兴趣的，可以拉取代码体验）

所谓：“时间就是金钱，效率就是生命”，“天下武功，唯快不破”。

### 相对于 Spring Boot 和 Spring Cloud 的项目：

-   启动快 5 ～ 10 倍。 **（更快）**
-   qps 高 2～ 3 倍。 **（更高）**
-   运行时内存节省 1/3 ~ 1/2。 **（更少）**
-   打包可以缩小到 1/2 ~ 1/10；比如，300Mb 的变成了 23Mb。 **（更小）**
-   同时支持 jdk8, jdk11, jdk17, jdk20, **graalvm native**

### 似曾相识的体验，入门更简单，迁移很方便：

```java
@Controller
public class App {
    public static void main(String[] args) {
        Solon.start(App.class, args, app->{
            //手写模式
            app.get("/", ctx -> ctx.outputAsJson("{message:'Hello world!'}"))
        });
    }

    //注解模式
    @Get
    @Socket
    @Mapping("/hello")
    public String hello(String name) {
        return String.format("Hello %s!", name);
    }
}
```

### 本次更新：

-   发布 Solon Native （**整合 Solon + Java AOT + GraalVM Native 三者的编译能力**）
-   发布 Solon Aot （Java AOT 的 Solon 增强版）
-   调整 solon server maxThreads 默认为 coreThreads 的 32 倍
-   调整 solon server 的 maxBodySize,maxFileSize 配置处理
-   增加 日志框架在 window 下的彩色打印支持
-   增加 solon.boot.jdkhttp 对 HttpServerConfigure 接口的支持，方便添加端口及ssl的编程控制
-   增加 solon.boot.jlhttp 对 HttpServerConfigure 接口的支持，方便添加端口及ssl的编程控制
-   增加 solon.boot.smarthttp 对 HttpServerConfigure 接口的支持，方便添加端口及ssl的编程控制
-   增加 solon.boot.jetty 对 HttpServerConfigure 接口的支持，方便添加端口及ssl的编程控制
-   增加 solon.boot.undertow 对 HttpServerConfigure 接口的支持，方便添加端口及ssl的编程控制
-   增加 solon.logging.logback 插件，文件扩展名配置（.log, .log.gz）
-   增加 solon.logging.log4j2 插件，文件扩展名配置（.log, .log.gz）
-   增加 Props::bindTo 接口
-   修复 solon.boot.undertow 的 maxBodySize 配置无效问题
-   修复 solon.boot.smarthttp + ssl 在某些情况下会慢的问题
-   snack3 升为 3.2.72

### 项目仓库：

-   gitee：[https://gitee.com/noear/solon](https://link.zhihu.com/?target=https%3A//gitee.com/noear/solon)
-   github：[https://github.com/noear/solon](https://link.zhihu.com/?target=https%3A//github.com/noear/solon)