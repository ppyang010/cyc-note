---
Title: 从 Spring Boot 4.1 到 gRPC 回潮，我追问了 7 轮，答案指向了 AI
Url: "https://zhuanlan.zhihu.com/p/2048545381638837307"
Author: gangdada
Origin: 知乎专栏
Description: Spring Boot 4.1 突然内置 gRPC，和 AI 爆发的隐秘关联 一篇技术对谈记录。从一个框架版本的发布，一路追问到了 AI Agent 时代的通信协议选择。一、Spring Boot 4.1 有什么新东西？ 问：Spring Boot 4.1 相较于 3.…
Tags:
  - Spring Boot
Created: "2026-06-23 11:13:17"
Cover: "https://pic1.zhimg.com/v2-abed1a8c04700ba7d72b45195223e0ff_l.jpg?source=32738c0c&needBackground=1"
---
9 人赞同了该文章

## Spring Boot 4.1 突然内置 gRPC，和 AI 爆发的隐秘关联

> 一篇技术对谈记录。从一个框架版本的发布，一路追问到了 AI Agent 时代的 [通信协议](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E9%80%9A%E4%BF%A1%E5%8D%8F%E8%AE%AE&zhida_source=entity) 选择。

---

### 一、Spring Boot 4.1 有什么新东西？

**问：Spring Boot 4.1 相较于 3.5 有什么不一样？**

2026 年 6 月 10 日，Spring Boot 4.1.0 正式发布。如果从 3.5 直接跳过来，变化很大：

**新面孔：**

- **Spring gRPC 正式支持** — 自动配置 gRPC 客户端和 [服务端](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E7%AB%AF&zhida_source=entity)， `@GrpcAdvice` 声明式 [异常处理](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86&zhida_source=entity)，连测试 starter 都备齐了
- **HTTP 客户端 SSRF 防护** — `InetAddressFilter` 自动拦截出站请求访问内网/保留地址
- **统一 [可观测性](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%8F%AF%E8%A7%82%E6%B5%8B%E6%80%A7&zhida_source=entity)** — [OpenTelemetry](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=OpenTelemetry&zhida_source=entity) SDK [环境变量](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F&zhida_source=entity) 自动支持，追踪-日志关联开箱即用
- **`@AutoConfigureWebServer`** — 测试时可以动态切换 Web 服务器类型和端口，不用改 application.properties
- **Jackson 3.x** — 从 Jackson 2 跳到了 3，需要检查自定义 [序列化器](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%BA%8F%E5%88%97%E5%8C%96%E5%99%A8&zhida_source=entity)
- **`LazyConnectionDataSourceProxy`** — [数据库连接](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%9E%E6%8E%A5&zhida_source=entity) 懒加载，减少启动开销

**底层换血：**

| 依赖 | Boot 3.5 | Boot 4.1 |
| --- | --- | --- |
| [Spring Framework](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Spring+Framework&zhida_source=entity) | 6.x | 7.0.8 |
| [Spring Security](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Spring+Security&zhida_source=entity) | 6.x | 7.1.0 |
| Jakarta EE | 10 | 11 |
| [Tomcat](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Tomcat&zhida_source=entity) | 10.x | 11.0.22 |
| Java 要求 | 17+ | 21+ |

顺带一句：3.5 的 OSS 支持到 2026 年 6 月 30 日就结束了，升级是早晚的事。

但最值得聊的，是那个排在第一位的新特性。

---

### 二、Spring 为什么突然重视 gRPC？

**问：为什么以前不搞，现在突然内置 gRPC 了？**

三个原因叠在一起：

**1\. 微服务 [内部通信](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%86%85%E9%83%A8%E9%80%9A%E4%BF%A1&zhida_source=entity) 的痛点到了临界点。** 当微服务数量上去之后，REST + JSON 的文本序列化开销、无 [强类型](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%BC%BA%E7%B1%BB%E5%9E%8B&zhida_source=entity) 契约、HTTP/1.1 的队头阻塞，都开始成为实际问题。不是因为 REST 变差了，而是调用密度太高了。

**2\. [Kubernetes](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Kubernetes&zhida_source=entity) 生态的推动。** gRPC 是 CNCF 毕业项目，Istio、 [Envoy](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Envoy&zhida_source=entity)、OpenTelemetry 都对 gRPC 有一等公民支持。这个 [生态位](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E7%94%9F%E6%80%81%E4%BD%8D&zhida_source=entity) Spring 不占，就会被 Go 和 [Rust](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Rust&zhida_source=entity) 生态吃掉。

**3\. [虚拟线程](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E8%99%9A%E6%8B%9F%E7%BA%BF%E7%A8%8B&zhida_source=entity) 补齐了最后一块短板。** gRPC 在 Java 生态推广最大的阻力是 [线程模型](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B&zhida_source=entity) ——传统的每请求一线程模型撑不住 gRPC 的长连接和 [流式调用](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%B5%81%E5%BC%8F%E8%B0%83%E7%94%A8&zhida_source=entity)。Spring Boot 4.0 默认启用虚拟线程（ [Project Loom](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Project+Loom&zhida_source=entity)）之后，这个问题从根本上解决了。4.1 立刻跟进 gRPC，不是巧合。

---

### 三、那我之前用的 OpenFeign 怎么办？

**问：我之前在服务间调用用的 OpenFeign，现在更推荐 gRPC 了吗？**

不一定是二选一。

|  | OpenFeign | gRPC |
| --- | --- | --- |
| 开发体验 | 接口 + 注解，和写 Controller 一样，零成本上手 | .proto 文件 + [代码生成](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E4%BB%A3%E7%A0%81%E7%94%9F%E6%88%90&zhida_source=entity)，有学习曲线 |
| 契约保证 | 靠人为约定 | .proto 编译期 [强制契约](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%BC%BA%E5%88%B6%E5%A5%91%E7%BA%A6&zhida_source=entity) |
| 调用模型 | HTTP/1.1 同步请求-响应 | HTTP/2 [多路复用](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%A4%9A%E8%B7%AF%E5%A4%8D%E7%94%A8&zhida_source=entity)，支持流式 |
| 序列化 | JSON 文本， [可读性](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%8F%AF%E8%AF%BB%E6%80%A7&zhida_source=entity) 好但体积大 | [Protobuf](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Protobuf&zhida_source=entity) 二进制，体积小 3-10x |
| 调试 | 浏览器/curl 直接看 | 需要 [grpc](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=grpc&zhida_source=entity) url 等专用工具 |
| Spring 生态 | 成熟多年 | 4.1 刚刚 GA |

**继续用 OpenFeign 的情况：** 性能够用、团队不熟悉 Protobuf、调用模式简单、已有完善的基础设施。

**值得引入 gRPC 的场景：** 某个 [调用链](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E8%B0%83%E7%94%A8%E9%93%BE&zhida_source=entity) 的延迟或吞吐成了实际瓶颈（）、需要服务端推送/流式传输、正在新建一套微服务且团队愿意接受 Protobuf 工作流、多语言异构场景。

更务实的方案是 **渐进式引入**：新服务用 gRPC，旧服务保持 OpenFeign，两种方式共存。Spring 4.1 不排斥这个。

---

### 四、给前端用 gRPC 行不行？

**问：我见过有人后端提供 gRPC 给前端调用，这种推荐吗？**

绝大多数情况下不推荐，这是 [反模式](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%8F%8D%E6%A8%A1%E5%BC%8F&zhida_source=entity)。

核心问题是 **浏览器对 gRPC 不友好**。浏览器的 `fetch` 和 `XMLHttpRequest` 不暴露 HTTP/2 的流控制和 Trailers 等特性，而这是 gRPC 协议正常工作的前提。所以必须走变通方案：

**gRPC-Web 方案：** 浏览器端用 `grpc-web` 库，前面架一个 Envoy 代理专门把 `grpc-web` 翻译成标准 gRPC。架构变成 `浏览器 → [gRPC-Web] → Envoy → gRPC 服务`，引入了一个不解决业务问题的 [代理层](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E4%BB%A3%E7%90%86%E5%B1%82&zhida_source=entity)。而且 [gRPC-Web](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=3&q=gRPC-Web&zhida_source=entity) 是阉割版协议——不支持客户端流和双向流。

**[gRPC-Gateway](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=gRPC-Gateway&zhida_source=entity) 方案：** 在 gRPC 服务上挂一个 [transcoder](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=transcoder&zhida_source=entity)，对外暴露 REST JSON。架构变成 `浏览器 → REST/JSON → Gateway → gRPC 服务`。这其实回到了”对外 REST，对内 gRPC”的经典架构。

而且浏览器场景下，Protobuf 二进制序列化的性能优势几乎消失——浏览器网络栈的限制、前端渲染的开销、以及实际传输的 [payload](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=payload&zhida_source=entity) 量，让那点收益可以忽略不计。

**一个例外：** 如果不是浏览器，而是原生移动 App 或桌面应用，用完整 gRPC 是合理的。

合理分界线很简单： **gRPC [服务间通信](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%9C%8D%E5%8A%A1%E9%97%B4%E9%80%9A%E4%BF%A1&zhida_source=entity)，REST 对外/前端。**

---

### 五、那用 JSON 走 gRPC 呢？

**问：可以不换成 Protobuf，继续用 JSON 走 gRPC 吗？**

技术上可以。gRPC 支持两种序列化格式：

| Content-Type | 序列化 |
| --- | --- |
| application/grpc+proto | Protobuf 二进制（默认） |
| application/grpc+ [json](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=json&zhida_source=entity) | JSON 文本 |

但实际用 `grpc+json` 的效果：

- ✅ 保留了 HTTP/2 多路复用和 [流式传输](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=2&q=%E6%B5%81%E5%BC%8F%E4%BC%A0%E8%BE%93&zhida_source=entity)
- ✅ 肉眼可读，方便调试
- ❌ 序列化速度没变快
- ❌ payload 体积没变小
- ❌ 强类型契约丢了——没有 `.proto`，回到靠约定

等于拿了 gRPC 一半的好处，丢掉了另一半。

更常见的做法是 **gRPC JSON Transcoder**：服务端内部还是 Protobuf，一个代理把 REST JSON 请求翻译成 gRPC Protobuf 调用。一个 gRPC 服务同时暴露 REST JSON 和 gRPC Protobuf 两 [套接口](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%A5%97%E6%8E%A5%E5%8F%A3&zhida_source=entity)，不用写两遍代码。

---

### 六、真正推动 gRPC 回潮的，是 AI

**问：那现在 AI 盛行，gRPC 是不是也和这个有关系？**

对，这是真正推动 gRPC 被重新重视的力量。

**最直接的事件：** 2024 年 11 月 [Anthropic](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Anthropic&zhida_source=entity) 发布 MCP（模型上下文协议，AI Agent 调用工具的标准）时，底层用的是 [JSON-RPC](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=JSON-RPC&zhida_source=entity) + [SSE](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=SSE&zhida_source=entity)。2026 年 1 月，Google 直接贡献了 gRPC 作为 MCP 的原生 [传输层](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E4%BC%A0%E8%BE%93%E5%B1%82&zhida_source=entity)。企业已有的大量 gRPC 微服务，可以 **直接被 AI Agent 调用，零改造接入 MCP。**

已经有项目在做这件事——比如 [ggRMCP](https://github.com/aalobaidi/ggRMCP)，利用 gRPC Reflection 自动发现服务方法，直接 [映射](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%98%A0%E5%B0%84&zhida_source=entity) 为 AI Agent 可调用的 Tool。

**AI 架构天然偏爱 gRPC，有三个原因：**

**1\. 多语言异构是刚需，不是选择。**

AI 系统的标准 [技术栈](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E6%A0%88&zhida_source=entity) 本身就是 [跨语言](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E8%B7%A8%E8%AF%AD%E8%A8%80&zhida_source=entity) 的：

| 层 | 语言 | 原因 |
| --- | --- | --- |
| [模型推理](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E6%A8%A1%E5%9E%8B%E6%8E%A8%E7%90%86&zhida_source=entity) | [Python](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Python&zhida_source=entity) | [PyTorch](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=PyTorch&zhida_source=entity)、vLLM、 [Transformers](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=Transformers&zhida_source=entity) |
| [API](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=API&zhida_source=entity) 网关/调度 | Go | [高并发](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E9%AB%98%E5%B9%B6%E5%8F%91&zhida_source=entity)、低内存 |
| 向量搜索/ [高性能计算](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E9%AB%98%E6%80%A7%E8%83%BD%E8%AE%A1%E7%AE%97&zhida_source=entity) | [C++](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=C%2B%2B&zhida_source=entity) /Rust | 性能极致 |

三种语言之间怎么通信？gRPC 是唯一在三种语言中都有生产级实现的跨语言方案——一套 `.proto`，三端通用。

**2\. LLM 的流式输出 = gRPC 的 server-streaming。**

LLM 的 token-by-token 输出天然是流式场景。gRPC 的双向流允许 Agent 在接收推理结果的同时发送新指令（取消/调整参数），截止时间/ [超时机制](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E8%B6%85%E6%97%B6%E6%9C%BA%E5%88%B6&zhida_source=entity) 可以自动取消无意义的推理请求，流控防止推理服务输出淹没 Agent 的消费能力。SSE 也能做流式，但缺少这些控制。

**3\. AI Agent 的工具调用需要强类型契约。**

Agent 调用你的服务（查数据库、发邮件、创建工单），需要精确知道参数类型。用 REST 描述这些，靠的是自然语言 [schema](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=schema&zhida_source=entity)，AI 容易”猜错”。用 gRPC，`.proto` 是 [编译器](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E7%BC%96%E8%AF%91%E5%99%A8&zhida_source=entity) 验证过的类型定义——这恰好是 AI 调用工具时最需要的东西。

所以 Spring Boot 4.1 内置 gRPC，看似是一个微服务通信的优化， **本质上是一次面向 AI Agent 时代的 [基建布局](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%9F%BA%E5%BB%BA%E5%B8%83%E5%B1%80&zhida_source=entity)。** Spring 赌的是：未来 AI Agent 通过 gRPC 调用你的 `@GrpcService`，就像今天前端通过 REST 调用你的 `@RestController`。

---

### 七、但是 RESTful 也能做 MCP，没错吧？

**问：但是 RESTful 也可以做 MCP 吧？**

完全可以。而且今天 MCP 的标准传输就是 JSON-RPC over HTTP。你的 RESTful 服务通过 [MCP Server](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=MCP+Server&zhida_source=entity) 暴露给 AI Agent，没有任何问题：

```
AI Agent  ←→  MCP Client  ←→   MCP Server  ←→  你的 RESTful 服务
       JSON-RPC          JSON-RPC         HTTP GET
```

[MCP 协议](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=MCP+%E5%8D%8F%E8%AE%AE&zhida_source=entity) 只关心 Agent 和工具之间的对话，不关心工具内部怎么实现。你用 REST、gRPC、直接查数据库、 [命令行脚本](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E5%91%BD%E4%BB%A4%E8%A1%8C%E8%84%9A%E6%9C%AC&zhida_source=entity)，对 Agent 来说都一样。

那 gRPC 在 MCP 里争的是什么？三个维度：

**1\. 避免重复劳动。** 如果你已经有大量 gRPC 服务，用 MCP 的 HTTP 传输需要每个服务都写一层 JSON ↔ Protobuf 转换。gRPC 原生 MCP 传输省了这层。对于用 REST 的团队，这事跟你没关系。

**2\. 流式质量。** MCP 的 [HTTP SSE](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=HTTP+SSE&zhida_source=entity) 是单向的（服务端→客户端）。Agent 在接收流时想取消或改参数，需要额外处理。gRPC 双向流天然支持。这个差距在简单场景（Agent 调一个 tool）里感觉不到，在复杂场景（Agent 边接收推理结果边动态调整）会有差异。

**3\. [类型安全](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=%E7%B1%BB%E5%9E%8B%E5%AE%89%E5%85%A8&zhida_source=entity)。** MCP 工具的参数定义用 [JSON Schema](https://zhida.zhihu.com/search?content_id=276740707&content_type=Article&match_order=1&q=JSON+Schema&zhida_source=entity)，Agent 只能从自然语言描述中”理解”参数含义。gRPC 的 `.proto` 在编译期就确定了类型，消除了 Agent 调用工具时的一类错误。

---

### 最后的务实建议

| 你的现状 | 建议 |
| --- | --- |
| 已用 RESTful，性能够用，MCP 工作正常 | 不要动。 gRPC 不会带来质的飞跃 |
| 正在用 OpenFeign，没有遇到瓶颈 | 继续用。不要为了技术而技术 |
| 新建微服务，未来可能被 Agent 大量调用 | 可以考虑 gRPC，但不是必须 |
| 已有大量 gRPC 服务，想做 MCP 集成 | 等 MCP gRPC 原生传输稳定后直接用，省转换层 |
| 要把 gRPC 暴露给浏览器前端 | 别干。 这是反模式 |

gRPC 的重新崛起，本质上不是因为 REST 不够用，而是 AI Agent 时代来了——多语言异构、流式通信、强类型契约，这三个 AI 系统的天然需求恰好对应了 gRPC 的长处。Spring Boot 4.1 的这一步，放在 AI 的背景下看，是一步明棋。

但技术选型永远看投入产出比。RESTful 今天做 MCP 毫无问题，不要因为 gRPC 热闹就瞎折腾。

---

### 附：对话的推导路径

这篇文章的每个问题都是上一轮追问的结果。如果你对其他环节也有兴趣，顺着这个链条补：

1. Spring Boot 4.1 相比 3.5 增加了什么？
2. 为什么突然内置 gRPC？
3. 现有 OpenFeign 用户怎么办？
4. gRPC 给前端是什么样的体验？
5. 不用 Protobuf 用 JSON 走 gRPC 行不行？
6. AI 的爆发是不是 gRPC 回潮的真实推手？
7. RESTful 也能做 MCP，gRPC 到底在争什么？

---

*本文内容由作者与 AI 助手对谈整理而成。*

*作者：\[gangdada\]*

编辑于 2026-06-11 23:26・甘肃・包含 AI 辅助创作 作者对内容负责

[Spring Boot](https://www.zhihu.com/topic/20044714)