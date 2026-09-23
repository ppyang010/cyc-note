---
Title: "GPT - 6 Astra 的使用焚诀"
Url: "https://juejin.cn/post/7682634449856217115"
Author: "cxuanAI"
Origin: "掘金"
Description: "昨天吐槽了一下为什么 GPT - 6 Astra 没给我推送，我今天早上排查了一下，发现之前有用的一个工具会侵入式的把模型列表给改了，所以 Codex 不管怎么更新用的还是三方的模型列表。。。。 这里"
Tags:
  - "后端"
  - "程序员"
  - "人工智能中文技术社区"
  - "前端开发社区"
  - "前端技术交流"
  - "前端框架教程"
  - "JavaScript 学习资源"
  - "CSS 技巧与最佳实践"
  - "HTML5 最新动态"
  - "前端工程师职业发展"
  - "开源前端项目"
  - "前端技术趋势"
Created: "2026-09-23 11:39:21"
Cover: "https://cdn.jsdelivr.net/gh/crisxuan/searchnews-assets@main/722d8b621fcb20753826eadfbf90e01657ae825d.png"
---

昨天吐槽了一下为什么 GPT - 6 Astra 没给我推送，我今天早上排查了一下，发现之前有用的一个工具会侵入式的把模型列表给改了，所以 Codex 不管怎么更新用的还是三方的模型列表。。。。

这里也给我涨了个教训。

不过呢，在 GPT - 6 Astra 还没发布两天，OpenAI 官方就祭出了 Astra 的使用焚诀。

为啥说是使用焚诀呢，因为我看过之后，发现这些 Prompt 确实有东西，它在防偏移、指令遵循、个性化和写作这些方面做了优化。

尤其是个性化和写作方面，因为大家包括我在内，看 AI Slop 看的也是直犯恶心了，然而 OpenAI 是味儿最大的那一队的。

## GPT - 6 Astra 的新特性

OpenAI 官方列出来了 Astra 的几个新特性，主要在下面这些方面做了优化：

第一个是异步工具（

Async tool calling）调用方面：

在以前标准的 tool use 方面，在模型这一层面基本上是 **同步的、阻塞式的**，需要等待应用返回结果才能继续，虽然开发者的程序可以并行或异步执行工具，但模型本身通常做不到。

而这次 Astra 新增了异步 tool use，这是模型层面的优化，也就是说现在，当你的应用程序执行 tool use 的时候，GPT- 6 Astra 可以继续做其他事儿了。

![同步工具调用 vs 异步工具调用](https://cdn.jsdelivr.net/gh/crisxuan/searchnews-assets@main/722d8b621fcb20753826eadfbf90e01657ae825d.png)

第二个是中途引导（

Mid-turn steering）方面：

这块说的是 Astra 还在执行当前任务时，用户可以直接插话，修改要求或纠正方向，不必等它完整做完。

我看到这里就有一些疑惑，之前使用 Codex 的时候，也支持 steer（插队） 和 queue （排队）啊。

不过，之前你是用的 Codex 产品中的 steer 和 queue 的功能，这一步是在应用编排层实现的插话，这一次，GPT‑6 Astra 把这项能力下沉到 `Responses API`：开发者可以通过标准的 `response.steer` 事件修改正在生成的 Response，由 API 自动保留已完成工作并创建承接新的要求。

第三个是在对话进行过程中更改推理逻辑，同时保留之前的缓存结果（

Change reasoning mid-conversation while preserving cache）：这句话有点拗口，我发现这英文的语言组织逻辑就是偏向于 **描述性的**，不像汉语翻译过来就是： **换个思考强度**。

这块说的是，在同一个长对话中，可以根据任务难度随时切换 Astra 的思考强度。

比如你让它先看一下项目结构，用 `low` 梳理个大概就行。接着发现有个复杂的并发问题，需要认真分析，那就把下一轮切到 `high`。等问题分析完了，只剩整理修改说明，又可以调回 `low`，没必要从头到尾都开着高强度思考。

第四个是偏离检测（

Misalignment monitoring）：

这块说的是 Astra 有没有理解错误用户的真正意图，并且在敏感场景中做出超出授权范围的操作。

比如用户让它删除临时构建文件，它却删除了整个项目目录；用户只授权读取某个客户的数据，它却开始访问其他客户的数据；用户让它发送公开报告，它却把包含密钥的配置文件一起公开了。

Astra 在这块内容上做的是 **后台异步审查 Astra 的推理过程和操作行为**。

![Astra 偏离检测流程：任务执行与后台审查并行，发现潜在偏离后告警，并在支持的请求中停止后续执行](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/a8b0d3b4b3d04617901220e763c15cf6~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgY3h1YW5BSQ==:q75.awebp?rk3s=f64ab15b&x-expires=1790581015&x-signature=0n6q9hqQHP2u0GHW2h93UtT0loI%3D)

这里有个细节：检测在后台异步进行，等它发现问题时，前面的操作可能已经执行完了。 **停止后续执行，也不会把已经做过的操作撤销。**

第五个说的是一条限制方面：

Astra 不支持 `none reasoning effort`，也就是 Astra 不能关闭内部推理，也就是说，在 Astra 中，没有

```
css 代码解读复制代码reasoning: {
  effort: "none"
}
```

这个档位，最低也得是 `low` 的思考档位。

还有一条限制说的是开启欧盟数据驻留的 API 项目，调用 Astra 时不能使用 /fast 模式。（这一条与我们关系不大了）

## Prompt 最佳实践

GPT-6 Astra 比 GPT-5.6 Sol 等早期模型更智能、能力更强，而且可以针对特定场景做 Prompt 优化 Astra 的行为模式。

### GPT - 6 Astra 的行为模式

GPT - 6 Astra 的官方定位就是你 **高效靠谱的伙伴**，所以 OpenAI 对 Astra 的行为模式提出了下面几种定义：

**主动性和贯彻执行力上（Initiative and follow-through）**，它具有更强的主动性和后续跟进能力，因此，当用户输入一些有可能会改变结果的信息时，它会向用户提出问题。这种机制可能导致模型在用户期望它基于合理假设继续执行时停下来。

**指令遵循（Instruction following）**，与之前的 GPT 模型相比，GPT-6 Astra 在遵循指令方面表现更强，让你能够更好的掌控模型。

另外，Astra 对 skills 和 AGENTS.md 中包含的指令很敏感，如果你想用 skills 时，需要留意其中可能影响模型行为的指令。

**个性与写作风格（Personality and writing style）**，Astra 倾向于提供详细且格式规范的回复，并可能在不同会话中重复使用某些短语，所以你需要明确指定你的应用所需的写作风格与结构。

**子代理委托（Subagent delegation）**，Astra 委派 subagent 执行并行任务的频率，可能低于你工作流的预期。请指定模型应在何时以及在多大程度上使用子代理来执行并行工作。

**测试与验证\[Testing and verification）**，在处理编程任务时，该模型往往会在认定任务完成前进行详尽的测试。对于较小的任务，这可能会导致测试范围超出任务实际所需。

我们分别来聊一下。

### 主动性和贯彻执行力

在执行长任务时，GPT‑6 Astra 通常比 GPT‑5.6 Sol 及更早的模型更能保持前后一致。

之前的早期模型往往会自行作出假设，而 Astra 更可能主动向用户询问并确认。

可以用下面这个 Prompt 来鼓励 GPT - 6 Astra 做更自主的工作：

```
代码解读复制代码你应当根据用户的指令和此前的对话上下文，推断用户的真实意图与任务范围。你的工作原则是优先采取行动，并持续推进用户想要完成的任务，直至目标真正实现。

当用户表达开展新工作或修复现有问题的意图时，应主动执行并持续工作，直到用户的预期目标完成。你应自主推动任务向前，例如在必要时创建隔离的工作树或检出目录、解决合并冲突、执行只读操作、创建草稿 PR 等。只有当相关操作明显具有破坏性或不可逆时，才应暂停并向用户确认。
```

当用户的意图不清晰，模型大概率会主动要求用户进行澄清，来继续下面的工作。

下面这段 Prompt，是用来告诉模型，在隐含授权的同时继续执行。

```
代码解读复制代码当用户的提示表明其希望你采取行动时，例如使用“你能不能……”“我想……”“帮我……”等表达，应将其视为要求你实际执行任务的指令。

不要只停留在确认自己具备相关能力，例如仅回答“可以”；也不要只提供计划，或者询问用户是否需要你继续。不要为了节省时间、精力或 token，只交付一个不完整或“差不多够用”的结果，而没有真正满足用户的全部要求。

如果任务需要持续投入和多步执行，请完成所有必要工作，直到用户期望的目标真正实现。
```

对模型输入一段 Prompt，仅在准备好具体且可审查的结果之后才请求批准。这样可以避免在模型完成其力所能及的工作之前阻塞任务，并且通常能更快地完成任务。

```
代码解读复制代码在向用户提出澄清问题之前，你应先完成根据现有上下文已经获得授权，并且为了让后续操作变得具体、可审查而必须完成的工作。用户最终批准的应该是一个明确、可以检查的结果。

例如，在部署修改、向外部应用写入内容、合并 PR 或发布网站之前，应先完成所有必要的准备工作，将用户批准作为执行最终操作前的最后一步。

对于可撤销的任务、只读操作、审查、修复，以及用户先前已经明确授权或任务指令中已经充分暗示获得授权的事项，无须再次征求用户许可。

不要仅仅因为存在假设性的风险，就主动添加用户未要求的警告、免责声明、审批流程或安全与合规检查清单。
```

Astra 默认会在运行过程中提出非阻塞式问题，因此可以根据你的场景所需的自主程度来调整这些提示词。

### 指令遵循

GPT - 6 Astra 能够更好的遵循长指令，同时也对上下文中的信息更为敏感。例如，Skill 文件中不明确或相互冲突的指令可能会导致模型停顿，并过早中断任务。请明确用户指令与 skill 的优先级。

下面是一个例子，说明在用户指令和 skill 指令发生冲突时，应优先用户指令

```
代码解读复制代码用户的指令优先于 skill 中提供的指导原则。如果明确的用户指令与 skill 的指令发生冲突，应优先遵循用户的指令。
```

如果 Astra 因为某个 Skill 中的规则而停下来，改变做法或偏离用户预期，就要求它明确说明是哪一个 skill、其中的哪条指令导致了这个行为。

不能只是单纯的说：“因为相关规则，我无法继续”。

> 举个例子来说：
> 
> Astra 暂停了发布操作，因为 `publishing/SKILL.md` 中写着：“发布前必须获得用户确认。”这条要求适用于当前任务，因为下一步会把内容写入外部平台。

Prompt 如下

```
objectivec 代码解读复制代码如果某个 Skill 导致你请求用户授权或确认、暂停工作、未完成用户要求的任务，或者使你的行为偏离用户意图，请明确指出并链接到你所读取的具体 SKILL.md 文件，引用其中导致该行为的相关指令，并简要说明这条指令如何适用于当前任务。

请明确区分：哪些要求是 Skill 中明文规定的，哪些只是你对 Skill 指南的理解或推断。
```

当应用同时给模型加载很多 Skill、 `AGENTS.md` 和其他指令文件时，使用上面这个 Prompt，可以找出那些在后台悄悄影响模型行为的规则，以及彼此发生冲突的规则。

### 个性与写作风格

GPT - 6 Astra 默认倾向于会把输出内容搞得很结构化。

> 它可能频繁使用：小标题、项目符号、编号列表、表格、粗体、引用块、Markdown 代码块这些标准格式，这样做的好处是为了能够快速阅读，但这种方式并不适用于所有内容，比如写公众号文章、评论文章、邮件或故事时，过多的列表和表格会让内容显得臃肿和死板。

所以，如果希望 Astra 写的更自然一些，就要在系统 Prompt 中明确说明，而不能假设它会自行选择这种风格。

（卧槽，这个 Prompt 绝了，这意思是不是说 Astra 更智能，然后会导致 AI 味儿更小了？）

```
代码解读复制代码默认使用清晰、连贯的自然段表达，每个段落集中说明一个核心观点。

只有当信息天然并列、具有明确先后顺序，或者使用列表能够明显降低理解难度时，才使用列表。只有当读者需要比较多个对象的相同属性时，才使用表格。

避免过多的小标题、粗体、嵌套列表和装饰性 Markdown。让段落之间自然衔接，使最终内容读起来像一篇完整文章，而不是由信息卡片拼接而成。
```

行话和陈词滥调就是大家经常说的 AI Slop，这种看着就反感的词汇和衔接语句

例如下面这些全都是常用的 AI 话术。

![image-20260907063533138](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/cc525a987de3462abde05a87b317bdf9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAgY3h1YW5BSQ==:q75.awebp?rk3s=f64ab15b&x-expires=1790581015&x-signature=cGS63f0yVJGCU4tDB8CYWaZv8Lk%3D)

如果想解决写作中的行话和陈词滥调，可以先使用下面这段提示词。

```
代码解读复制代码避免使用空洞、俗套的词语和句式，例如在结论中使用“核心结论：”，以及“深入探讨”“促进”“充分利用”“值得注意的是”“重要的是”“问题是什么？答案是……”“这不是关于 X，而是关于 Y”“真正地”等表达。避免使用通过连字符生造出来的复合描述语和复合形容词。不要使用“简而言之……”“最简单的理解方式是……”之类的总结句。

直接说明准备执行的操作。不要额外介绍你不会做什么、哪些内容将保持不变，或者你准备如何拆分和归类结果。
不要使用“是 X，而不是 Y”或“X——不是 Y”这样的对比句式，因为它们会主动引入用户并未询问的另一种说法。避免生造类似“精确标题检查”“编辑式行布局”这样的复合标签，也要避免模糊的限定语和套路化的过渡句。使用简单、直接的动词和介词，准确说明事物之间的真实关系。
```

### 子代理委托

GPT - 6 Astra 被训练为能够将任务拆分并委托给 Subagent 并行工作的模型，所以如果你正在搭建和训练自己的多 Agent 系统，可以使用以下提示词来调整 GPT-6 Astra 的任务委派程度：

```
代码解读复制代码无论你是作为父代理还是 subagent 代理，只要能够将任务委派给其他代理从而节省时间或提升质量，来实现工作并行处理，你就应当利用协作工具来执行这一操作。
```

Agent 之间的消息可能会出现语法错误的情况，可以使用如下 Prompt，让 Agent 之间的消息更便于阅读

```
代码解读复制代码你发送给其他代理的消息以及你的最终回答可能会由人工阅读，因此请确保内容清晰易读。请务必在单词和/或数字之间留出适当的空格。
```

使用 GPT - 6 Astra 在关于如何或者何时委托给 Subagent 的提示词指令优化的比较好，大家可以试一下。

### 测试和验证

在进行编码任务时，应根据变更的规模来评估所需的测试与验证工作量，从而避免针对微小的变更进行不必要的测试或重复检查。

```
代码解读复制代码对于可以撤销、影响较小的改动，不要编写只是照搬实现逻辑的测试。如果决定通过测试验证改动，应确保这些测试有实际意义，并且确实是验证实现所必需的。

运行与本次改动相匹配的测试，并完成规定的检查。测试通过后，只有在出现新改动、测试失败或仍有问题尚未解决时，才扩大测试范围或重复运行测试；否则，应继续推进任务直至完成。
```

## 总结

这次 Astra 的几个新特性，主要方便我们让它做长任务：tool use 时能接着做其他任务，用户可以中途补充要求，后续多轮的思考强度也能按任务难度调整。

我比较在意的还是后面这些 Prompt，如果平时光说一句“主动一点”“去掉 AI 味儿”，确实太笼统了。

尤其是写作这块，我还是想看看，OpenAI 自己给出的去味儿配方，到底能去掉多少味儿。

文章来源： [OpenAI 官方指南：Using GPT-6 Astra](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Flatest-model "https://developers.openai.com/api/docs/guides/latest-model")

功能说明参考： [异步工具调用](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Fasync-tool-calling "https://developers.openai.com/api/docs/guides/async-tool-calling")、 [中途引导](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Fsteering "https://developers.openai.com/api/docs/guides/steering")、 [切换思考强度](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Freasoning%23change-reasoning-mid-conversation "https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation")、 [提示词缓存](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Fprompt-caching "https://developers.openai.com/api/docs/guides/prompt-caching")、 [偏离检测](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Fsafety-checks%2Fmisalignment-monitoring "https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring")。

想继续看 Prompt 怎么用，也可以看看下面这些官方资料：

- [Building games with Astra](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fblog%2Fhow-to-build-games-with-astra "https://developers.openai.com/blog/how-to-build-games-with-astra")：用 Astra 做游戏的过程，包含需求描述、视觉参考和试玩后的修改 Prompt。
- [Architectural visualization with Astra](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fblog%2Farchitectural-visualization-with-astra "https://developers.openai.com/blog/architectural-visualization-with-astra")：用 Astra 做建筑和 3D 场景，展示如何从整体效果逐步改到家具、材质和灯光。
- [Prompt engineering](https://link.juejin.cn/?target=https%3A%2F%2Fdevelopers.openai.com%2Fapi%2Fdocs%2Fguides%2Fprompt-engineering "https://developers.openai.com/api/docs/guides/prompt-engineering")：通用提示词指南，讲指令层级、上下文、示例，以及编码和长任务的提示方式。
- [Codex Best practices](https://link.juejin.cn/?target=https%3A%2F%2Flearn.chatgpt.com%2Fguides%2Fbest-practices "https://learn.chatgpt.com/guides/best-practices")：Codex 的通用使用建议，重点是把目标、上下文、限制和完成条件说清楚，再把稳定的规则放进 AGENTS.md 或 skills。

前两篇是 Astra 的实操案例，后两篇是通用指南，可以作为这篇文章的延伸阅读。