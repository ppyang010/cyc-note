---
id: "2050523117496297035"
title: "你天天在填的那个 /v1/chat/completions，到底是个什么东西"
author: "情酱"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2050523117496297035"
created: "2026-06-17 10:21"
updated: "2026-06-17 19:01"
collected: "2026-06-17 10:21"
downloaded: "2026-08-16"
---
前两天帮一个朋友配 AI 客户端，他截图问我，这个 Base URL 到底怎么填，/v1 要不要带，后面那个 /chat/completions 又是个啥

我说你先告诉我你看到的是什么字段名

他说，API Base

我说那你填到 /v1 就行，后面 SDK 会自己拼到一块

他问我为什么

我不知道怎么说

你想想看，我们每天都在跟这些路径打交道，复制粘贴一百遍了，但真正停下来想过它们是什么的人，好像并不多

```text
/v1/chat/completions
/v1/responses
/v1/messages
/v1/embeddings
/v1beta/models/{model}:generateContent
```

这些后缀看着眼熟吧

它们不是随便写的，每一个都代表一套完整的接口协议，规定了你怎么跟模型沟通，请求长什么样，响应长什么样，错误怎么报，流式怎么传，工具怎么调

我觉得，如果你在用 AI API 做任何事情，花十分钟搞清楚这件事，会省掉后面很多困惑

### 最早的接口只做一件事

最早的大语言模型接口，长这样

```text
POST /v1/completions

{
  "model": "chatgpt",
  "prompt": "Translate this sentence into Chinese: Hello, how are you?"
}
```

整个接口只干一件事，你给一段文本，模型往后面续写

没有角色的概念，没有系统消息，没有对话历史。模型眼里只有一串字符，它的任务就是预测下一个 token

如果你想让它当一个助手进行对话，你得自己在 prompt 里手动拼这些东西

```text
System: You are a helpful assistant.
User: Hello.
Assistant: Hi, how can I help?
User: Explain API suffixes.
Assistant:
```

这个方案能用，但问题很明显

模型要靠猜来区分哪句话是系统指令，哪句话是用户说的，哪句话是自己之前回复的。猜对了还好，猜错了整个对话逻辑就乱了。而且当你想传一张图片进去，或者让模型调用一个工具的时候，你没有任何优雅的方式在一个纯文本 prompt 里表达这些东西

所以 /v1/completions 慢慢就退居二线了

### /v1/chat/completions，过去几年用得最多的接口

OpenAI 后来做了一件对整个行业影响很大的事，就是把对话结构化了

```text
POST /v1/chat/completions

{
  "model": "gpt-4o",
  "messages": [
    { "role": "system", "content": "You are a concise technical explainer." },
    { "role": "user", "content": "Explain what /v1/chat/completions means." }
  ]
}
```

从一整段 prompt 变成了一个 messages 数组。每条消息有明确的 role，system 是系统指令，user 是用户输入，assistant 是模型之前的回复，tool 是工具返回的结果

这个变化看起来不大，但后面几乎所有 AI 应用的开发方式都跟着变了

一旦上下文变成了结构化的消息数组，你就可以精确地控制模型看到什么，以什么身份看到，按什么顺序看到。多轮对话、角色设定、工具调用，都有了落脚点

然后这套协议被整个行业接受了

OpenAI 用 /v1/chat/completions，Mistral 也用，xAI 也用，DeepSeek 用 /chat/completions 但格式基本兼容，Groq 用 /openai/v1/chat/completions，OpenRouter 用 /api/v1/chat/completions

路径前缀不一样，但协议内核是同一套

这就带来一个很实际的好处，你用 OpenAI 的 SDK 写完代码，想切到别的平台，很多时候只需要改三个变量

```text
base_url = "https://api.other-provider.com/v1"
api_key = "YOUR_KEY"
model = "their-model-name"
```

剩下的 SDK 调用代码一行不用动

我自己的感受是，/v1/chat/completions 能成为事实标准，主要是因为它出现得够早，生态铺得够快。SDK、IDE、前端聊天界面、RAG 框架，全都围着它转了一圈

但是有一个事情需要说清楚

兼容不等于完全兼容

大家都说自己 OpenAI-compatible，但兼容程度差很多。基础的文本聊天几乎都能跑通，stream 流式输出大部分也没问题。但到了 tools 工具调用、response\_format 结构化输出、vision 图片输入、audio 音频输入这些能力，各家的支持程度就参差不齐了

我自己遇到过一个具体的坑，某平台声称兼容 OpenAI，结果 parallel\_tool\_calls 不支持，streaming 下的 tool\_call delta 格式也跟 OpenAI 不一样，调试了半天才发现是协议层面的差异

所以如果你做的事情超出了基础聊天，不要假设兼容就是完全兼容，最好去看一下对方文档里具体支持哪些字段

### /v1/messages，Claude 自己的协议

Anthropic 没有跟着 OpenAI 的路走，Claude 用了自己的一套协议

```text
POST /v1/messages

{
  "model": "claude-sonnet-4-8",
  "max_tokens": 1024,
  "system": "You are a careful technical explainer.",
  "messages": [
    { "role": "user", "content": "Explain /v1/messages." }
  ]
}
```

乍一看跟 chat/completions 很像，但仔细看会发现几个差异

Claude 把 system 提到了顶层字段。OpenAI 的做法是把系统消息放进 messages 数组里当一个普通 role，Claude 则是单独拿出来作为请求体的一级参数

响应结构也不同。OpenAI 的解析路径是 `choices[0].message.content`，Claude 的是 `content[0].text`。而且 Claude 的 content 是一个 block 数组，文本是一个 block，图片是一个 block，工具调用结果也是一个 block

流式输出的事件格式差异更大。OpenAI 用 `data: {"choices":[{"delta":{"content":"xx"}}]}`，Claude 用的是 `event: content_block_delta` 这种命名事件流

反正结论就是，如果你要接 Claude 的官方能力，别强行用 OpenAI 的 SDK 和解析逻辑去套，老老实实用 Anthropic 的 SDK 或者按它的文档来

### /v1/responses，OpenAI 新出的接口

这个比较新，也是我觉得值得关注的一个方向

你想想 /v1/chat/completions 这个名字，chat + completions，聊天补全。这个名字本身就暗示了它的设计初衷，用户丢一段聊天历史过来，模型补全下一条消息

但现在的模型早就不只是聊天了

读图片、处理音频、搜网页、查文件、调函数、跑代码解释器、调 MCP 工具、维护服务端上下文、输出结构化 JSON、返回推理摘要、产生多个中间事件

把这些能力全塞进一个叫 chat.completion 的对象里，确实有点拧巴

```text
POST /v1/responses

{
  "model": "gpt-4o",
  "input": [
    {
      "role": "user",
      "content": [
        { "type": "input_text", "text": "Search the web and summarize the result." }
      ]
    }
  ],
  "tools": [
    { "type": "web_search" }
  ]
}
```

Responses API 的思路是，不再把交互框定为聊天，而是把它抽象为任务

chat/completions 的逻辑是，这是聊天记录，请补全下一条回复

responses 的逻辑是，这是任务、上下文和可用工具，请给我执行后的完整响应

输出也不再是单一的 assistant message，而是一个 response object，里面可以有多个 output item，文本、工具调用、工具结果、中间推理步骤，都可以作为 item 存在

如果你只是做简单的聊天机器人，chat/completions 依然够用，生态兼容性也最好。但如果你在做 agent、做复杂的工具编排、做多步骤的任务流，Responses API 的设计明显更贴合实际需求

### Gemini 走了一条完全不同的路

Google 的风格一贯如此

```text
POST /v1beta/models/gemini-2.5-pro:generateContent
```

拆开看

```text
/v1beta         → API 版本，beta 表示预览
/models/gemini-2.5-pro  → 模型资源
:generateContent        → 对这个资源执行的方法
```

这是典型的 Google API 设计风格，把模型当成一种资源，generateContent 是对这个资源执行的一个方法

数据结构也不同，Gemini 用的是 contents 和 parts，不是 messages 和 content

概念上可以这样对应

```text
OpenAI:     messages → role + content
Anthropic:  messages → role + content blocks
Gemini:     contents → role + parts
```

三家的思路都是把对话分成角色和内容两层，但具体的字段命名和嵌套方式各不相同

另外 Gemini 有 v1 和 v1beta 两个版本，v1 是稳定版，v1beta 有最新的预览能力。稳定项目用 v1，想试新功能再用 v1beta

### 顺便聊两个经常一起出现的接口

/v1/embeddings 是向量化接口

```text
POST /v1/embeddings

{
  "model": "text-embedding-3-large",
  "input": "AI API suffixes explained"
}
```

它把文本变成一组浮点数向量。你做 RAG 的时候，先用 embeddings 把文档切片转成向量存起来，用户提问时再把问题也转成向量去检索最相似的文档片段，最后把检索到的片段塞进 chat/completions 或 responses 生成答案

embeddings 负责找资料，chat/completions 负责组织答案，两个搭着用

/v1/models 就更简单了，GET 请求，返回当前 API key 能用的模型列表。你调试的时候怀疑模型名写错了，或者想看看当前账号有哪些模型可用，调这个接口就行

### 一个很多人搞混的事情

/v1 不是模型版本，是 API 版本

我见过不少人以为 /v1 对应第一代模型，/v2 会对应第二代模型。这是不对的

API 版本约束的是接口规范，请求字段叫什么、响应字段叫什么、错误格式是什么、流式事件怎么发、鉴权方式是什么

模型版本约束的是模型能力，上下文长度、推理能力、价格、速度、多模态支持

gpt-5.5、claude-sonnet-4.6、gemini-3.1pro，这些是模型版本。/v1 是 API 版本。openai Python SDK 1.x 和 2.x，那是 SDK 版本。三个东西各管各的

为什么要有 API 版本号？因为厂商需要在不破坏现有应用的前提下演进接口

假设今天响应里是 `choices[0].message.content`，明天厂商突然改成 `output[0].content[0].text`，所有依赖旧格式的应用瞬间全挂

所以正经做法是，要么新开一个 /v2 路径，要么新增一套接口比如 /v1/responses，让旧的继续跑着

### 关于 Base URL，一个很实际的配置问题

我发现这个问题困扰过很多人，所以单独说一下

如果软件让你填的字段名是 Base URL / API Base / OpenAI Base URL

填到 /v1 就行，不要带后面的 /chat/completions

比如

```text
https://api.openai.com/v1
 https://openrouter.ai/api/v1
```

因为 SDK 会自动在后面拼接 /chat/completions。如果你把完整路径填进去，实际请求会变成

```text
https://api.openai.com/v1/chat/completions/chat/completions
```

然后你会拿到一个 404，百思不得其解

如果软件让你填的是 Endpoint / Full URL / Request URL

那就填完整路径

```text
https://api.openai.com/v1/chat/completions
```

再说一下那些前缀。Groq 的路径里有个 /openai，OpenRouter 有个 /api，阿里云百炼有个 /compatible-mode

这些都是各平台自己加的命名空间，表达的意思是，我不是 OpenAI，但我提供一套兼容 OpenAI 协议的入口，你可以用 OpenAI 的 SDK 来调我

### 所以到底该用哪个

我是这样想的

做普通聊天应用，用 /v1/chat/completions。原因很简单，生态最成熟，兼容性最好，几乎所有 SDK 和工具都支持

新项目接 OpenAI 并且涉及工具调用、多模态、agent 这些能力，优先看 /v1/responses

接 Claude，用 /v1/messages，不要强行套 OpenAI 的协议

接 Gemini，用 /v1/models/{model}:generateContent

做 RAG，/v1/embeddings 负责检索 + 聊天接口负责生成，两个搭配用

接第三方聚合平台，先搞清楚它兼容的是哪套协议，然后选对应的 SDK 和路径

这些接口路径的差异，说到底是各家厂商对模型调用方式的不同选择。OpenAI 从聊天补全起步，现在在往统一响应的方向走。Anthropic 一开始就坚持自己的消息协议。Google 用的是他们一贯的资源+方法的 API 风格。其他平台大多选择兼容 OpenAI，因为生态红利太大了

我们作为使用者，不需要押注某一家，但需要知道自己在用的到底是哪套协议，它能做什么，不能做什么

搞清楚这些，配置和调试的时候会少走很多弯路

### 参考文献

L站帖子：[https://linux.do/t/topic/2306861](https://link.zhihu.com/?target=https%3A//linux.do/t/topic/2306861)

OpenAIAPIReference：[https://platform.openai.com/docs/api-reference](https://link.zhihu.com/?target=https%3A//platform.openai.com/docs/api-reference)

AnthropicClaudeAPIReference：[https://docs.anthropic.com/en/api/messages](https://link.zhihu.com/?target=https%3A//docs.anthropic.com/en/api/messages)

GoogleGeminiAPI：[https://ai.google.dev/docs](https://link.zhihu.com/?target=https%3A//ai.google.dev/docs)