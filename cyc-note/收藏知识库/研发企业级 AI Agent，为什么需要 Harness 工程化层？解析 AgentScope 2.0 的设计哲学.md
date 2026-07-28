---
Title: "研发企业级 AI Agent，为什么需要 Harness 工程化层？解析 AgentScope 2.0 的设计哲学"
Url: "https://zhuanlan.zhihu.com/p/2061417519588680299"
Author: "阿里巴巴中间件专注内容原创"
Origin: "知乎专栏"
Description: "作者：刘军（陆龟） AgentScope Java 2.0 的核心思路，是基于 ReActAgent 推理内核基础上，增加 Harness 工程化层。开发者既可以继续使用轻量的 ReAct 循环，也可以按需启用 Workspace、持久记忆、Session、Sandbo…"
Created: "2026-07-28 15:18:31"
Cover: "https://picx.zhimg.com/v2-37623eda0e312031b717e4434e690269_l.jpg?source=32738c0c&needBackground=1"
---

5 人赞同了该文章

作者： [刘军](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%88%98%E5%86%9B&zhida_source=entity) （陆龟）

AgentScope Java 2.0 的核心思路，是基于 ReActAgent 推理内核基础上，增加 [Harness](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=Harness&zhida_source=entity) 工程化层。 [开发者](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%BC%80%E5%8F%91%E8%80%85&zhida_source=entity) 既可以继续使用轻量的 ReAct 循环，也可以按需启用 [Workspace](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=Workspace&zhida_source=entity)、持久记忆、Session、 [Sandbox](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=Sandbox&zhida_source=entity)、Skill 和 Subagent 等能力，将同一套 Agent 逻辑落地部署到企业级 [分布式服务](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%88%86%E5%B8%83%E5%BC%8F%E6%9C%8D%E5%8A%A1&zhida_source=entity) 中。

经过 5 个 RC 版本迭代，AgentScope Java 2.0 GA 版本正式发布：

本文根据刘军 2026-07 月份关于 AgentScope 2.0 的公开 [技术分](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E5%88%86&zhida_source=entity) 享演讲整理而成，完整复现现场演讲内容。

点击 [此处](https://mp.weixin.qq.com/s/jIWU-aYtBFbRJSQxXVXaDQ)，立即查看现场演讲视频。

## AgentScope 2.0 介绍

AgentScope 框架推出已经有两年的时间了。我们在上半年发布了 2.0 版本，2.0 版本主要的一个核心能力，就是把 Harness 整套方案内置到了框架里面。这也意味着我们面向的场景，主要是企业级的 [分布式智能体](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%88%86%E5%B8%83%E5%BC%8F%E6%99%BA%E8%83%BD%E4%BD%93&zhida_source=entity) 这样一个场景。

**本文主要从三部分来给大家介绍。** 第一部分是大家都关心的 2.0 主要有哪些核心能力。有一些开发者包括企业内已经非常重度地用 AgentScope 1.0 构建了很多生产级的应用和智能体，这套 [设计理念](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E8%AE%BE%E8%AE%A1%E7%90%86%E5%BF%B5&zhida_source=entity) 的差异和怎么迁移，我会简单介绍一下。中间一大部分是介绍整个 Harness 的核心设计和它到底有哪些能力。最后是几个示例，我们来看一下它能做真正的企业级的事情。

### ▍AgentScope 生态全景图

![](https://pic4.zhimg.com/v2-180d893157a94611677f8ecfc08b8c4d_1440w.jpg)

先从全景图开始。大家可以直观地把 AgentScope 理解为一个框架，也就是图中蓝色的这一部分。

作为一个框架， **我们现在有 Python、Java 和 TypeScript 三个语言实现，Go 语言的实现也在开发当中，所以整个框架已经基本涵盖了所有主流的语言实现。**

框架这一层更多定义的是 Agent 怎么开发、怎么定义。比如中间就是整个 Agent Loop 的循环，里面的 Reasoning、Tool Call 都有非常好的设计，这些实现大家不需要去关心。包括里面的 Model，以及整个 Event、Message 的传递，这些都是内置的。

在 2.0 里我们加了 Workspace 这样一个非常核心的抽象，同时也做了更多上下文管理的事情。这就是中间蓝色部分的框架。

往外延伸的，是我们围绕 Agent 的构建过程做的很多生态适配。比如模型这一侧，左边这部分就是国内的 DeepSeek、OpenAI 兼容的这些模型，还有 Qwen 模型，都是支持的。

观测这一块，整个框架现在有默认的 OpenTelemetry 埋点，所以观测数据可以上报到任何兼容 OpenTelemetry 的平台，比如开源的 LangFuse，或者阿里云上的产品——以前 [微服务](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%BE%AE%E6%9C%8D%E5%8A%A1&zhida_source=entity) 时代叫 ARMS，现在有一款专门针对 Agent 时代的 Agent Loop 的产品，都是可以接进去的。

然后是 Higress，前面讲 Agent Teams 的时候提到过，不论是模型的代理还是 MCP 的代理，包括用 Nacos 做 Skill 或者 MCP 市场的管理，整个 Agent 生态都已经完整对接了。

再往上，QwenPaw 和 AgentTeams 都是我们基于这个框架生态衍生出来的具体产品和企业级的 Agent 管理能力。

### ▍ReactAgent 内核与核心组件

![](https://picx.zhimg.com/v2-0c1bb1c7551feba9b417e38ea88249e9_1440w.jpg)

看完大图，我们回到 AgentScope 框架本身。整个 2.0 对底层来说是不变的，也就是 ReAct Agent 这套核心的推理和工具之间的循环，这个没有变。

我这里列了几个核心能力，和 1.0 区别不太大，底层能力这一层是没变的，顶多是做了一些设计上的优化。或者看下面加了一个 Permission，就是工具调用权限这块额外的设计，因为以前是没有工具权限管控能力的。

中间还有个 Middleware [中间件](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E4%B8%AD%E9%97%B4%E4%BB%B6&zhida_source=entity)，这个和以前的 Hook 是对等的，只不过在新版本中我们对整个事件的传递和中间的介入做了一些优化。所以整体看起来，Model、Tool 定义、中间的上下文（上下文这块对应的就是我们以前产生的内容），整体来说是差不多的，就是整个 ReAct Agent 这一块。

### ▍1.0->2.0 迁移指南

![](https://pic4.zhimg.com/v2-71de1ba620c0abbd9a8c81a574ef78ff_1440w.jpg)

虽然核心的底层逻辑不变，我这里还是列了 1.0 到 2.0 需要关注的三个迁移要点，我们从左到右从三个层次来看。

先说绿色这部分。 **升级的时候我们总体保证了兼容性，** 也就是说前面提到的所有这些能力，总的来说都保持了兼容。即使有些 API 做了废弃——比如 Hook 从设计上被 Middleware 替代了——在 2.0 版本里我们还是把它标记为废弃但保留了下来。所以理论上来说，绝大多数能力都可以兼容并且平滑升级。

中间这部分列出来的是你必须要改的。虽然大部分能力保持了兼容性，但还是有些东西改掉了，这部分内容如果不改，可能会有一些 [编译](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%BC%96%E8%AF%91&zhida_source=entity) 或者运行的报错。主要体现在几个方面：

第一个是 [状态管理](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E7%AE%A1%E7%90%86&zhida_source=entity) 这块。我们现在在整个框架里引入了一套 Agent State 的概念，整个 Agent 运行的状态都通过 Agent State 来管理。它和以前的 Session 在底层数据格式上是有一定差异的，这个大家要认识到。如果你以前有运行中的 1.0 版本 Agent 的状态，现在我们做了一层兼容——你把它切到 2.0 然后发布上线，它还是能认你以前 1.0 的状态。但要知道从 API 到实现上，状态管理是发生了变化的。

还有一块非常大的变化：由于我们非常强调 [多租户](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%A4%9A%E7%A7%9F%E6%88%B7&zhida_source=entity) 能力——不论是 User [维度](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%BB%B4%E5%BA%A6&zhida_source=entity) 的隔离，还是 Session 维度的隔离——我们在 Agent 调用的 call 方法和 stream 方法的入口都加上了 [Runtime Context](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=Runtime+Context&zhida_source=entity) 这样一个概念。也就是说，你必须把运行的上下文——比如当前是哪个 User、哪个 Session——这些信息传进来。同时它也提供了 Runtime Context 的拓展性，你可以基于它做很多拓展的事情。

下面几个都是和 State、Session 强相关的。

最后一部分属于大家可以慢慢迁移的。如果你改掉了中间这部分 API 相关的破坏性修改，后面这部分就是标记为废弃的内容，可能我们会在 2.1 版本移除掉，方便大家先迁到 2.0，后面再逐步升级。

这块整体讲起来比较繁琐，官网上有专门的链接讲怎么迁移，大家可以去看看。

## AgentScope Harness 核心设计与功能详解

接下来讲今天比较重要的一部分，就是 AgentScope 整套 Harness 的设计。我们先看整个 Harness 在 AgentScope 上的总体架构。

### ▍Harness 总体架构

![](https://pica.zhimg.com/v2-888b7e07c9b8441c4fec1ff7d9d97a6e_1440w.jpg)

看中间这个大蓝色的部分。 **Harness 是构建在 AgentScope——不论是 1.0 还是现在——底层 Agent 推理执行组件之上的，** 可以理解为在以前 1.0 的 ReAct Agent 之上又包了一层。

在这一层之上，是把你长期运行一个 Agent 必备的能力——上下文管理、上下文压缩、Agent 编排、Skill 的运行、在沙箱环境里隔离工具的执行、 [推理规划](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E6%8E%A8%E7%90%86%E8%A7%84%E5%88%92&zhida_source=entity) 和任务状态的跟踪、甚至包括和一些 IM 消息系统的对接、工具的权限管控——统一作为一个 Harness 套件，在框架底层内置支持了。你可以用一些开关，或者遵循这套 Harness 的开发模式，就可以把它用起来。相当于增加了这么一层能力。

### ▍Harness 快速体验

这里用一个 Java 版本的示例来讲。AgentScope Java 里如果要用 Harness 这一层怎么用呢？第一，你要加一个依赖。因为我们在上面又加了一层，你要把这一层的依赖加进来。

![](https://pic1.zhimg.com/v2-387de3d30352792fa9a13ef59c8279b4_1440w.jpg)

其次是开发的入口。ReActAgent 的 API 入口还在，但现在多了一层新的 API 入口，叫 HarnessAgent。你可以直接用它构建一个 Agent——它底层还是用的 ReAct Agent，但在 API 的感知上你可以直接用 Harness Agent。

我们可以看它们中间的差异：前面是一样的——Name、System、Model；下面你可以看到它有了 Workspace 的概念，可以指定它的 Workspace，可以指定一些压缩策略，还有更多的配置，包括 Sandbox 隔离的配置，都可以在这一层直接用 API 来做。

下面的区别就是调用的时候需要前面提到的 Context 上下文。这里定义了一个 Runtime Context，接下来调用时主要是传 User 和多租户隔离的一些信息。

![](https://pic1.zhimg.com/v2-ca5638ff90805f288607a34bf5ccaffe_1440w.jpg)

### ▍Workspace – 智能体进化的 Source of Truth

![](https://picx.zhimg.com/v2-14e24c909741a3ef2f90cf7db01f82a9_1440w.jpg)

Workspace 是现在主流的 Agent——不论是 Agent 产品还是 Agent 框架——的一个核心设计。我们可以把它理解为一个逻辑概念。它里面有哪些资产呢？

**第一部分是偏静态的资产，** 就是 Agent 定义相关的，比如 AGENTS.md、Skills 或者 Sub-Agent，相当于定义了我这个面向业务的 Agent 里都有哪些东西。这是我定义的、会随着我的镜像打包走的，叫静态资产。

**还有一部分是运行时的数据。** 这部分数据是 Agent 在运行过程中自己产生的，是用户和它交互沉淀下来的——不论是一些实时的 Session 状态记录、Task 任务状态等信息，还是 MEMORY.md 这种沉淀下来的记忆。所有这些静态的或运行时的资产都沉淀在 Workspace 里。这就是 Workspace 的核心概念。

### ▍抽象文件系统 – Workspace 的物理载体

![](https://pic4.zhimg.com/v2-987243ba77f3aca66b11646ff72ebc47_1440w.jpg)

并且在 AgentScope 中，我们对 Workspace 做了更 [细粒度](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%BB%86%E7%B2%92%E5%BA%A6&zhida_source=entity) 的处理。比如一个 Agent 有一个 Workspace，但一个 Agent 会被很多用户使用。对于不同的用户，我们在这一个 Workspace 里做了逻辑上的 [多租户隔离](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=2&q=%E5%A4%9A%E7%A7%9F%E6%88%B7%E9%9A%94%E7%A6%BB&zhida_source=entity) ——可以是用户维度的隔离、Session 维度的隔离，或者是 Agent 维度的。这是不同的隔离维度。

在底层，我们说 Workspace 是一个逻辑概念，那它的物理存储是什么呢？最直观的理解一定是磁盘，这是最直接的。但磁盘有一个问题：比如 On-premise 场景它就只能在你本地的磁盘上，这就是 Workspace 绑定磁盘的限制。

为了解决这个问题——尤其我们面向的是企业级分布式场景——我们把 Workspace 的上层逻辑实现往底层物理实现走的时候抽象了一个接口，就是中间黑色的部分，叫做 Abstract File System，一个抽象的 [文件系统接口](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E6%8E%A5%E5%8F%A3&zhida_source=entity)。

Agent 操作 Workspace 时， [物理层](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%89%A9%E7%90%86%E5%B1%82&zhida_source=entity) 面使用的就是这个抽象文件系统接口。我们为它提供了默认的三种实现，当然你也可以任意拓展：

- 第一种是左边的本地 [On-premise](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=2&q=On-premise&zhida_source=entity)，装在本机，直接操作的是磁盘。
- 如果你要做用户的隔离，就是树形文件系统，一个树状的结构。
- 在 [生产环](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%94%9F%E4%BA%A7%E7%8E%AF&zhida_source=entity) 境部署时，因为一个 Agent 要多实例部署，每个实例都要看到同一个 Workspace，这时你可以把抽象文件系统接口接到数据库比如 MySQL 或者 Redis，或者是阿里云的 OSS。这就实现了 Workspace 的共享——同一个 Workspace 实例能够被不同的 Agent 实例看到。

如果你对 Workspace 的隔离有更高的要求——比如工具的执行（工具执行也是在 Workspace 的空间里进行的），你可以把它接到 Sandbox。一个 Workspace 映射一个 Sandbox，这时只要做好 Sandbox 的生命周期管理，就可以实现多租户隔离了。

这就是 Harness 中 Workspace 的逻辑概念和物理存储实现，这样也就支持了分布式的场景。

### ▍内置上下文压缩策略 – 四道防线

![](https://pic4.zhimg.com/v2-723da4af4b301728ebe8a5b1d534a337_1440w.jpg)

在 Workspace 里我们怎么管理所有的上下文呢？第一，我们内置提供了一些压缩策略。Agent 在一个会话运行的过程中，模型是有上下文窗口限制的，我们怎么保证上下文在这个限制之内呢？

这里提供了几种压缩策略，图中只展示了其中一部分，实际还有更多详细的配置。比如工具执行的结果大于多少之后，我们有截取加落盘的实现——落盘以后给到文件引用的路径；工具入参过大时，也有一些字数上的截断策略，这些都是基本的措施；还包括对过往消息进行压缩、保留最近几条，这些都是大家熟悉的常规压缩策略。

在压缩的过程中，还是有一些注意事项的。最典型的就是：压缩的时候尽量不能丢信息。哪些信息是尽量不能丢的呢？

右下角这部分有几个例子。比如整个任务执行的规划——有些复杂任务是要做规划的，这个规划可能在你消息的前几条，如果不做特殊处理直接压缩，规划就丢掉了。

还有基于这个规划我可能拉起了一些子 Agent，有些子 Agent 是异步的，或者任务是异步的。 [异步](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=3&q=%E5%BC%82%E6%AD%A5&zhida_source=entity) 的情况下任务很可能还没有返回，我要持续地追踪任务状态。这时如果直接粗暴地压缩，这个子 Agent 的状态可能就丢掉了。

因此，像这种需要在全局进行更新的状态——不论是规划的详情、子 Agent 的异步任务状态、我的清单，还是各种工具的权限授权记录——这些信息都要保证不被压缩。所以这两部分内容要进行区别处理。

### ▍双层长期记忆 – 事实自动沉淀

![](https://pic3.zhimg.com/v2-62136dd73359d605f09b26bec5afde2c_1440w.jpg)

还有一个是长期记忆的沉淀。前面讲的压缩偏瞬时状态——是运行当中 [瞬时状态](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=2&q=%E7%9E%AC%E6%97%B6%E7%8A%B6%E6%80%81&zhida_source=entity) 的管理和控制。做压缩的时候必然会丢掉一些信息，这些信息可以把它沉淀为长期记忆。

框架里的一些策略是：在会话压缩以前，可以做一次 Flush 分拣。第一层是记到每天专属的一个文件里，这个结构其实和 QwenPaw 是差不多的，可以记进去。

同时我们还有一个后台任务，它会定期回去扫描当天的、整个 Memory 下沉淀的记忆，把它蒸馏为全局的 MEMORY.md。这个 MEMORY.md 在每次请求进来的时候都会全局加载到你的 System Prompt 里，所以它的大小和里面数据的质量就非常重要。

同时还配套了几个 Memory 管理的相关工具：Memory Search、Memory Get 和 Session Search。模型会根据 MEMORY.md 等内容的引导，在适当的时候去查你的流水账等信息。这是一套相互配合的长期记忆沉淀策略。

所有这些环节——不论是做每日流水账的 Memory 提取，还是定时蒸馏 MEMORY.md，还是做压缩——里面的 Prompt 提示词都是可以定制的，方便大家在不同场景引导做更优化的提取和记忆实现。下面这几个在框架上都有提示词的 Config 入口。

### ▍子智能体编排、委派、并行、异步通知

![](https://pic4.zhimg.com/v2-51e8a1567c64d3d047eaf69334f91ef9_1440w.jpg)

Harness 当中还有一个非常重要的点，是关于智能体的编排。这张图要表达的是： **主 Agent 直接指导所有的子 Agent。**

一个任务进到主 Agent 以后，我们内置了 Agent Fork、Agent Spawn 这些工具，主 Agent 会根据需求来拉起子 Agent。拉起的子 Agent 首先有两种类型：一种是同步的子 Agent，一种是异步的子 Agent。异步的子 Agent 适用于处理时间比较长的任务，并且现在我们支持它在完成以后，主动把结果通知回主 Agent。

还有一种特殊类型是远程的子 Agent，这种模式现在也是支持的，可以拉起一个远端的子 Agent。同时我们给主 Agent 配套了一个叫 Task List 的 Toolkit，覆盖了所有的配套工具。主 Agent 可以主动地去看有哪些子 Agent、每个子 Agent 处于什么状态，这些都有配套的工具。

还有一点值得一提，也是很多企业用户的核心诉求：通常来说用户直接对话的是主 Agent，主 Agent 拉起所有子 Agent 是它自己的事情，它管理子 Agent 是为了完成自己的任务。但实际上有很多用户（包括我们用 Claude Code 的时候也是），会希望直接切到主 Agent 拉起的某个子 Agent，和这个子 Agent 对话，来引导它完成自己的子任务。

同样在 AgentScope 中我们也支持你直接和子 Agent 进行对话。虽然这个子 Agent 是主 Agent 拉起来的，但有一种方式可以把它暴露出来，让你直接和它对话。

子 Agent 的整套设计，前面讲的是几个比较大的层次，里面还有一些细节。比如主 Agent 和子 Agent 之间的上下文是不是共享的，就是下面列的这几项；包括子 Agent 的事件怎么通过主 Agent 透传出来、怎么区分是哪个子 Agent 的还是主 Agent 的（因为大家的事件流都混在一起），我们都是有标记在的。

然后是权限问题——主 Agent 拉起子 Agent 以后，子 Agent 的权限是什么、是不是继承主 Agent 的权限，这些比较细节的事情，在整个框架里都有一套机制存在。

### ▍沙箱管理：隔离、恢复与分布式

![](https://pic4.zhimg.com/v2-2777c7bcfa03fc4b51a56143f6aad01f_1440w.jpg)

还有一套机制是关于沙箱的。 [沙箱](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=4&q=%E6%B2%99%E7%AE%B1&zhida_source=entity) 主要解决 Agent 执行的安全问题，是其中非常重要的一环。Agent 工具执行的过程中，我们可以把工具执行放在沙箱里，整个框架里有一套沙箱生命周期的管理系统。这里就不展开了，感兴趣的话可以进一步查阅官方文档。

### ▍Skills：四层注册中心 & 沙箱内执行

![](https://pic2.zhimg.com/v2-cfdcf6dd8cba1a00f8bdd66df8638c65_1440w.jpg)

关于 Skill 有两部分可以讲一下。

**第一部分是 Skill 的管理。** AgentScope Harness 对于 Skill 管理，对接了类似 Nacos 这种中心化的 Skill 管理系统，可以自动地把中心化管理的 Skill 加载到本地进行识别和使用。同时基于前面讲的 Workspace 细粒度管理机制，你也可以实现不同用户之间 Skill 的隔离使用——我这个用户有自己的 Skill，另一个用户有另外的 Skill，互相是看不到的。这个也是可以实现的。

**另一部分是 Skill 的执行。** Skill 有时不只是简单的流程，里面还有配套的脚本和一些资源文件，这时它的执行就要受到安全管控。我们现在支持把整个 Skill 投影到 Sandbox 中，让 Skill 的所有脚本都能在 Sandbox 里闭环执行。

### ▍计划模式：想清楚 -> 写下来 -> 再动手

![](https://pic2.zhimg.com/v2-a527b3fec72ec9b471c6b13909143f93_1440w.jpg)

**Harness 里现在也支持计划模式。** 熟悉 1.0 的用户应该知道，我们在 1.0 中也有一套叫做 Plan 的计划模式——给一个任务，先规划再执行。

1.0 的实现更偏向于一个内部管理的 [状态机](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E6%9C%BA&zhida_source=entity)，由一套状态机来运转和执行。在 2.0 中我们对整个 [Plan 模式](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=Plan+%E6%A8%A1%E5%BC%8F&zhida_source=entity) 做了优化：首先内置了一整套 Plan 相关的配套工具，比如 PlanEnter、PlanExit 等等。

当用户请求进来的时候，你可以直接开启 Plan。如果大家熟悉 Coding Agent，可以直接理解为和 Coding Agent 的 Plan 模式一样——比如在 Codex 或者 Claude Code 中你可以打开 Plan。我们用 AgentScope 开发的业务 Agent 也是一样的，前面有一个接口可以调，你告诉它要开启 Plan 模式，它就开启了，接下来你问它问题，它就会生成 Plan，后面切到 Agent 模式让它执行，它就基于之前的 Plan 直接往下执行。

或者你让它进入自主识别的模式，它可以根据你的任务自己切到 Plan 模式。因为这里每个工具都有 Permission 权限，它切到 Plan 模式的时候可能会先问你；Plan 执行完了，就像 Coding Agent 那样，它要切换回 Agent 模式时会弹出一个弹窗来问你。整个流程上是一样的，我们可以在前端的 UI 上把这一套串起来。

### ▍Channel：消息平台 -> Gateway-> Agent

![](https://pic3.zhimg.com/v2-b5ebb3d227f6276fadf659431d95bc28_1440w.jpg)

在一些企业的业务场景里，是有对接 Channel 平台的需求的——要把后台运行的任务和企业内的 [即时通讯系统](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%8D%B3%E6%97%B6%E9%80%9A%E8%AE%AF%E7%B3%BB%E7%BB%9F&zhida_source=entity) 等对接起来。这块整个框架也提供了原生的支持。

## AgentScope 企业级智能体实战（官方示例）

前面就是关于整个 Harness 的部分。Harness 的设计内容相对比较多，大家可以去看官方文档里具体的使用方式。最后我们介绍几个示例。

### ▍个人助手 —— 直连本机 FS 与 Shell，随用随长

![](https://pic4.zhimg.com/v2-6d3ab13228906a840e77a9a22c1be167_1440w.jpg)

第一个示例——这几个示例都在我们官方的 GitHub 仓库里——是 AgentScope Java 版的一个类 QwenPaw 产品。它实现了一个非常简化版本的 QwenPaw，不是一个具体的发行产品，我们做它只是为了验证用 AgentScope 怎么开发一个个人助手产品。

和前面讲到的一样，它用的 Workspace 模式是完全绑定本地磁盘的，因此它不支持 [分布式部署](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%88%86%E5%B8%83%E5%BC%8F%E9%83%A8%E7%BD%B2&zhida_source=entity)。

### ▍多租户 Managed Agent 平台 —— 一套自进化 Agent，一个组织共用

![](https://pic2.zhimg.com/v2-ba5d90290d8f217dea7dd179a7f122a1_1440w.jpg)

还有一个示例是一个多租户的 Agent 平台，你可以理解为一个零代码开发的 Agent 平台，叫做 Agent Builder。

它有一个 UI 界面，可以在公司里集中化部署。部署以后它就是一个 SaaS 平台，公司里的每个人都可以在上面创建 Agent。作为管理员，我也可以创建一个共享的 Agent，给公司里的所有人用。

每个用户虽然用的是同一个 Agent，但底层可以做到多租户隔离——依赖的就是下面的 Workspace 和物理 File System 的分组。这样就实现了一个 Agent 的多租户平台，每个用户的数据都是隔离的。同时我也可以定义自己的 Agent，还可以把我的 Agent 共享给别人。

这其实就是 Claude Managed Agents、Langchain Managed Agents、Qoder Cloud Agents 平台的原型，使用 AgentScope 2.0 可以非常快速的搭建出来，只需要开放控制面、数据面 API 即可。

### ▍数据 Agent 平台 —— per-用户进化 + 审批式能力市场

![](https://pica.zhimg.com/v2-fff3b906892c47054da76e531bcd1d9a_1440w.jpg)

最后还有两个示例。一个是 Data Agent，这也是一个多租户场景的示例。

这个 Data Agent 针对每个用户的使用，数据基础都有一套隔离的空间。每个用户还可以有自己的 Skill，不同用户沉淀的 Skill 在这套体系里还有一套审批机制——我的 Skill 可以申请共享给大家，走一个审批流程，通过以后它就是共享的，所有用户都可以用。

### ▍自主编码机器人 —— Thread 路由 + 一次性 Docker 容器

![](https://pic4.zhimg.com/v2-52a66bf1133bf215c05fb6fb21411f4f_1440w.jpg)

最后一个示例是 Coding Agent。这个 Coding Agent 和我们本地安装的比如 Claude Code 或者 Cursor 的使用场景不太一样。

它是一个企业级服务的共享 Agent 场景。比如把这个 Coding Agent 在企业里集中部署以后，一个典型的场景是对接 GitLab——把部署好的 Coding Agent 服务接到 GitLab 上。

每个人在 GitLab 上处理 Issue 或者 Pull Request Review 的时候，发送的所有请求都会被这个 Coding Agent 服务接收。你的整个任务运行和其他用户的运行环境是隔离的——它会自己拉起 Sandbox，专门为你这个用户服务。它确保你处理的所有 Issue 和 Pull Request 状态是连续的，不同用户之间互不影响。

包括你处理每个 Issue 时可能会有连续的对话，整个 Issue 的状态也不会和其他 Issue 或者 Pull Request 混在一起、互相影响。所以它是一个部署在企业内部、为大家的研发协作服务的 Coding Agent 示例。包括把它作为一个 CI/CD 平台架起来、用 AI 来驱动也是没问题的。整套机制底下用的都是 AgentScope Harness 的底层设计。

## AgentScope 在企业中获得广泛应用

自 2024 年开源发布以来，AgentScope 智能体框架已逐步成为一款被企业用户广泛采用的 Agent Framework，尤其是面向分布式、生产级可用的智能体场景。

在 **[阿里巴巴集团](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E9%9B%86%E5%9B%A2&zhida_source=entity) 内部**，AgentScope （Java & Python）已经是使用最广泛的一款框架了，覆盖的具体 [业务线](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E4%B8%9A%E5%8A%A1%E7%BA%BF&zhida_source=entity) 包括飞猪、淘宝闪购、虎鲸文娱、AIDC、阿里控股、淘天交易、淘天手淘、1688、千问 APP、高德、阿里云、蚂蚁国际、蚂蚁全球支付等业务线

而在 **开源与阿里云 [公有云](https://zhida.zhihu.com/search?content_id=279231988&content_type=Article&match_order=1&q=%E5%85%AC%E6%9C%89%E4%BA%91&zhida_source=entity) 用户侧**，则广泛覆盖金融、交通/物流、消费零售、制造、能源、医疗、教育/政媒、互联网、SaaS、咨询等众多行业头部企业。

发布于 2026-07-17 15:35・浙江