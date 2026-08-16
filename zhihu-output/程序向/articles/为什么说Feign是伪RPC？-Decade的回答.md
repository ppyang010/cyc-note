---
id: "2003576858491516504"
title: "为什么说Feign是伪RPC？"
author: "Decade"
type: zhihu-answer
source: "https://www.zhihu.com/question/298707085/answer/2003576858491516504"
created: "2026-02-07 21:12"
updated: "2026-02-07 21:12"
collected: "2026-02-07 21:12"
downloaded: "2026-08-16"
---
根据现在主流的想法 主要有三个原因：

**第一，协议问题。** 传统RPC（Dubbo、gRPC这些）用的是TCP长连接+私有二进制协议。而Feign默认走HTTP/1.1+JSON，每次请求都带着一堆HTTP头，序列化也是JSON这一套。所以很多人觉得这不就是调REST接口吗，跟RPC差远了。

**第二，性能确实差一截。** 二进制协议解析快、 payload 紧凑、复用长连接。HTTP+JSON呢，头部开销不小，JSON序列化也比Protobuf慢。并发一高，差距就出来了。这也是为什么内网高性能链路大家都用Dubbo或者gRPC，没人用Feign。

**第三，阵营斗争的锅。** 2016到2020年那会儿，Spring Cloud和Dubbo两边吵得凶。Dubbo阵营特别喜欢说"Feign是伪RPC，你们那是HTTP调用，我们才是真RPC"，差不多成了个梗。Spring Cloud官方也懒得纠正，直接把自己叫"声明式 REST Client“。

但回过头看看，RPC的核心定义是啥？”RPC协议（Remote Procedure Call Protocol）是一种通过网络请求远程计算机服务而无需关注底层网络技术的协议"

这是度娘里的定义 Feign做到了吗？做到了。你定义个接口，加几个注解，然后就可以`userService.getUserById(123)`了 跟调本地方法一样。URL拼接、序列化、HTTP客户端创建、响应解析、异常转换……这些破事全被屏蔽了。

所以说，Feign能不能算RPC？其实是可以算的，只不过：

-   Feign = 基于HTTP的RPC（**其实硬要解释，http不也是RPC的一种实现吗？**）
-   Dubbo/gRPC = 基于自定义二进制协议或HTTP/2的RPC

对大部分业务系统来说，Feign够用了，开发效率还高。这才是它真正值钱的地方。