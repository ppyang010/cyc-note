---
Title: "Harness 学习笔记分享（Part 1）"
Url: "https://zhuanlan.zhihu.com/p/2070129665814139506"
Author: "粥里有勺糖​软件开发行业 从业人员"
Origin: "知乎专栏"
Description: "本文仅代表作者个人观点，如果内容有错误或和你理解上有所出入，欢迎交流与指正。 学习过程参考了 Pi Agent 的源码。按照其分层思路和一些实现方案，笔者自行实现了一个 MVP 版本的 Harness。本文主要分享一下整个…"
Tags:
  - "Harness-Engineering"
Created: "2026-09-01 13:18:22"
Cover: "https://pic1.zhimg.com/v2-ca50cc971bdf2e1310815c72304ff22d_720w.jpg?source=172ae18b"
---

3 人赞同了该文章

> 本文仅代表作者个人观点，如果内容有错误或和你理解上有所出入，欢迎交流与指正。  
> 学习过程参考了 [Pi Agent](https://github.com/earendil-works/pi) 的源码。按照其分层思路和一些实现方案，笔者自行实现了一个 MVP 版本的 [Harness](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=Harness&zhida_source=entity)。

本文主要分享一下整个过程中的一些学习心得和个人的一些想法。

### 前言

“Agent” 从最开始文本对话式，到 [多模态](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E5%A4%9A%E6%A8%A1%E6%80%81&zhida_source=entity) （语音/图片/视频） [智能体](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E6%99%BA%E8%83%BD%E4%BD%93&zhida_source=entity)，再到现在的 Agent（能够辅助办公、开发、生成完整项目等），不同阶段 Agent 的定义也不一样。

最近的一阶段是 “Model + Harness = Agent”。

之前是高频使用各种智能体辅助写文档，改项目代码。

最近一段时间准备做一些带 Agent 能力的 AI 应用，所以先学习一下 Harness 相关的知识，知己知彼😋。

**开局先来一张图**

![](https://pica.zhimg.com/v2-1070105e46f1e6111d4cc774e126989e_1440w.jpg)

**Harness 算是模型的运行时**，各家 Agent 的差异也就在这部分，模型都是可以随时切换的。

*所以没有 Harness 的「Agent」，大部分就是纯聊天。*

**先小小总结一下几个主要模块**

| 各个模块 | 作用 |
| --- | --- |
| Model | 读 Context，产出文本或 [结构化](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E7%BB%93%E6%9E%84%E5%8C%96&zhida_source=entity) tool_calls |
| Context | 本轮真正送进模型的内容，不单单是「用户输入的那一句话」 |
| Tools | 实际做外部调用，真正改文件、跑命令 |
| Harness | 负责 循环、校验、执行、上下文组装、回写、权限、资源控制等行为 |
| Agent | 模型跑在 Harness 上、冲着目标多步往前推进，直到完成或达到终止条件 |

### Tools

Tools 是模型和外部沟通的桥：模型只负责发出结构化调用，真正去改文件、跑命令、调 API 的是具体 Tool 实现；调度和校验则由 Harness 来做。

### 先说 Function Calling

Function Calling（现在大部分时候也叫 [Tool Calling](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=Tool+Calling&zhida_source=entity)）解决的问题是：

**避免模型用自然语言描述去说明要调用的工具，而是让它输出可解析的调用结构。**

没有这套约定时，模型可能写

*我需要调用 get_weather([上海](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E4%B8%8A%E6%B5%B7&zhida_source=entity)) 来获取天气信息*

应用侧很难可靠地解析。有了 Function Calling：

1. 先把工具的 **schema** 交给模型（能调什么、参数长什么样）
2. 模型需要时返回 **`tool_calls`** （调用谁、参数是什么、本次调用的 id）
3. **Harness 解析调用工具执行**，把结果以 **`tool` 消息** 写回
4. Harness 再请求模型，基于工具执行结果继续做推理

贴一张官方的图： [function-calling#how-it-works](https://developers.openai.com/api/docs/guides/function-calling?lang=javascript#how-it-works)

![](https://pic4.zhimg.com/v2-e1eedbbfacb08d7a2da24eb8f377d7db_1440w.jpg)

下面是我画的一版 Model / Harness / Tools 怎么流转起来的（对应上面 1→4 步）：

![](https://picx.zhimg.com/v2-ef6c400fd959ff54eb6dc4054565ba03_1440w.jpg)

### 调用示例

下面来个最简 demo（OpenAI Chat Completions，非流式），看一下 **调用结构**：

```
// 1）准备工具声明（schema）——只描述能力，不含实现
const tools = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: '查询某城市当前天气',
      parameters: {
        type: 'object',
        properties: {
          city: { type: 'string', description: '城市名，如上海' },
        },
        required: ['city'],
        additionalProperties: false,
      },
    },
  },
]

const messages = [
  { role: 'user', content: '上海今天天气怎么样？' },
]

// 2）一次请求：messages + tools
const res = await fetch(\`${OPENAI_API_BASE_URL}/v1/chat/completions\`, {
  method: 'POST',
  headers: {
    'Authorization': \`Bearer ${OPENAI_API_KEY}\`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    model: 'gpt-5.6', // 模型 id
    messages,
    tools,
    tool_choice: 'auto', // 模型自己决定是否调用工具，也可设为 none / required / 指定某个工具
  }),
})

const data = await res.json()
const message = data.choices[0].message
// ↓ 输出释义见下方示例
```

一次成功响应（需要调工具时）大致长这样：

```
// data 示意（省略 usage 等）
{
  id: "chatcmpl-xxx",
  choices: [
    {
      index: 0,
      finish_reason: "tool_calls", // 因工具调用结束本轮；最终文本常见 "stop"
      message: {
        role: "assistant",
        content: null, // 也可能是一段说明；有 tool_calls 时经常为 null
        tool_calls: [
          {
            id: "call_abc123",
            type: "function",
            function: {
              name: "get_weather",
              arguments: '{"city":"上海"}', // 注意：是字符串，不是对象
            },
          },
        ],
      },
    },
  ],
}
```

返回结果里，重点关注这几个：

- **`message.tool_calls`**：决定是否需要执行工具
- **`tool_calls[].id`**：回写结果时需要一一对应上id
- **`tool_calls[].function.name` / `arguments`**：工具名和参数
- **`finish_reason`**： `"tool_calls"` 表示「需要执行工具」； `"stop"` 表示本轮结束

### 解析执行示例

Harness 处理工具调用的核心逻辑是：校验 → 执行 → 回写 → 再请求。

```
// 1）先把本轮 assistant（含 tool_calls）写入 messages，下一轮还要带上
// 保持 OpenAI 原始结构即可
messages.push({
  role: 'assistant',
  content: message.content,
  tool_calls: message.tool_calls,
})

// 2）解析参数 → 校验 → 执行 → 回写
for (const tc of message.tool_calls) {
  // 格式化一下参数
  const call = {
    id: tc.id,
    name: tc.function.name,
    arguments: JSON.parse(tc.function.arguments || '{}'), // 字符串 → 对象
  }

  // 按 schema 校验；不合法则回写错误
  if (isInvalid(call)) {
    messages.push({
      role: 'tool',
      tool_call_id: call.id,
      content: '参数不合法',
    })
    continue
  }

  // 执行工具
  const result = await executeTool(call)

  // 回写结果到上下文中
  messages.push({
    role: 'tool',
    tool_call_id: call.id,
    content: result.content, // 字符串
  })
}

// 3）带着更新后的 messages 再请求模型
const res = await fetch(\`${OPENAI_API_BASE_URL}/v1/chat/completions\`, {
  // ... 其他参数
  body: JSON.stringify({ messages, tools, tool_choice: 'auto' }),
})

const data = await res.json()
// 模型再次回复，可能包含 tool_calls 或继续自然语言回复
const message = data.choices[0].message
```

下面是第二次请求模型的 messages 示例，包含了工具调用结果：

```
[
  { "role": "user", "content": "上海今天天气怎么样？" },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_abc123",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"city\":\"上海\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "{\"temp\":28,\"unit\":\"C\"}"
  }
]
```

### 小结

1. **Function Calling** 让模型输出可解析的 `tool_calls` 参数
2. **Tool**：由声明（schema）与实现（handler）组成；声明给到模型，实现留在 Harness 里
3. **Harness** 负责校验 → 执行 → 按 `tool_call_id` 回写 → 再请求
![](https://pic2.zhimg.com/v2-7c7e1f92cb4d63a11b2f7ad75283bd0d_1440w.jpg)

### Agent Loop

真正办事的 Agent，需要把上面的流程 **自动循环起来**：组装上下文 → 请求模型 → 有调用就执行回写 → 再请求，直到给出最终答复，或被 [约束条件](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E7%BA%A6%E6%9D%9F%E6%9D%A1%E4%BB%B6&zhida_source=entity) 强制停掉。

**当然我这里只是一个最简单的实现（用「有没有 `tool_calls` 」来决定要不要自动推进）**，实际的循环推进条件可能还有其它的策略。

![](https://pica.zhimg.com/v2-0845df6fd615b0db103c85a97a677b18_1440w.jpg)

### 精简的循环示意

```
async function runAgent(state) {
  while (true) {
    // 1）组装本轮真正进模型的 Context
    const messages = assembleContext(state)

    // 2）请求模型
    const assistant = await adapter.stream({ messages, tools: state.tools })

    // 3）判断有没有 tool_calls
    if (!assistant.tool_calls?.length) {
      return assistant.content
    }

    // 4）有调用：校验 → 执行 → 回写
    state.messages.push({
      role: 'assistant',
      content: assistant.content,
      tool_calls: assistant.tool_calls,
    })

    for (const call of assistant.tool_calls) {
      const result = await executeTool(call)
      state.messages.push({
        role: 'tool',
        tool_call_id: call.id,
        content: result.content,
      })
    }
    // 5）带着工具结果进入下一轮 while
  }

  return assistant.content
}
```

和纯对话的差别就在第 4 步：模型输出调用指令，Harness 调度 Tools，用执行结果继续推进。

### 其它条件

以 [Pi: agent-loop](https://github.com/earendil-works/pi/blob/main/packages/agent/src/agent-loop.ts) 为例，默认仍是「本轮有没有工具调用」驱动自动续跑，同时还会看下面这些条件：

**1）工具结果不一定需要回传**

- 工具执行结果包含一个 `terminate: true` 字段来决定是否回传
- 有时最终答案已经在工具结果里了（比如结构化输出工具）， **不必再花一轮 LLM** 把结果「复述」一遍
- 如果本轮工具调用全部带 `terminate: true`，就不需要再请求模型
```
// 示意：结构化输出工具跑完就结束本轮自动续跑
async execute(_id, params) {
  return {
    content: [{ type: "text", text: "已保存结构化结果" }],
    details: params,
    terminate: true,
  };
}
```

**2） `shouldStopAfterTurn` （回合结束后可选停）**

内置钩子：回合结束后由调用方决定是否继续；也可在这里选择性地压缩上下文。

**3） [steering](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=steering&zhida_source=entity) / follow-up**

这两个都是「往 Loop 里塞用户消息」，时机不同：

| 名词 | 白话 | 典型时机 |
| --- | --- | --- |
| steering | Agent 还在跑时，用户可以临时插一句进来，改变执行方向 | 当前回合工具跑完后、下一次请求模型前注入 |
| follow-up | Agent 准备结束了，队列里还有一句比如「顺便再总结一下」 | [内层循环](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E5%86%85%E5%B1%82%E5%BE%AA%E7%8E%AF&zhida_source=entity) 要退出前从队列里取出；有则继续跑 |

相关 loop 代码大概就 100 来行，比较容易理解。

![](https://pic2.zhimg.com/v2-b60aecd84126a5a6e229b9d8e93eca85_1440w.jpg)

### 小结

1. Loop [最小模型](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E6%9C%80%E5%B0%8F%E6%A8%A1%E5%9E%8B&zhida_source=entity) = 组装上下文 → 调模型 →（有 `tool_calls` 则）执行工具 → 再请求进行下一轮
2. Trace 可以在 Loop 里记录，通过事件将相关信息暴露出来，在 Loop 外监听，方便后续进一步的分析。

### 运行时约束

Loop 能跑起来之后，接着就是： **怎么让它停得住。**

Prompt 只能做一些软约束：不可逆操作、调用死循环、反复执行等，需要在 Harness 代码里做 [硬约束](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E7%A1%AC%E7%BA%A6%E6%9D%9F&zhida_source=entity)。

![](https://pic3.zhimg.com/v2-586b45442251b8b80831c25fba72426c_1440w.jpg)

### 常见约束

```
const controller = new AbortController()

await runAgent({
  maxSteps: 8, // 最大执行回合数
  timeoutMs: 60_000, // 整次 Run 的超时时间
  stopOnToolError: false, // false：错误写回，模型来纠正
  signal: controller.signal,
  onConfirm: async (call) => {
    // 高危工具执行前二次确认；拒绝则写成错误 tool 结果，不调真实 handler
    if (call.name === 'rm' || call.name === 'bash') {
      return window.confirm(\`允许执行 ${call.name}？\`)
    }
    return true
  },
})

// controller.abort(); 主动取消
```

### 校验

执行工具调用前加一层执行前校验：校验 schema，工具是否存在，参数是否合法等。

异常情况可以回写错误的 Tool 消息，让模型可以自主的重试，用户也能感知到。

### 小结

循环的终止与工具调用安全边界，靠 Harness 代码硬约束。

*执行沙箱等下来仔细研究一下，后面再单开文章。*

### Context Engineering

上下文组装也是 **Context Engineering** 在 Harness 里的应用。

每次给模型推送的，不只是「用户刚输入的那一句」，而是 Harness **组装出来的完整上下文**，常见包括：

1. **系统提示词**：角色、全局行为；项目 **Rules** 也常并进这一层
2. **历史对话**：全文，或先对历史对话内容进行摘要，再保留最近若干轮
3. **tool schemas**：工具声明（本地 + MCP 统一成同一套 [schema](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=7&q=schema&zhida_source=entity)）
4. **工具调用结果**：上一轮 / 本轮 Loop 写回的 `role: "tool"` 消息
5. **本轮用户输入**：当前意图
6. **按需材料**：Memory（跨会话的记忆）、RAG（检索的内容片段）、 [SKILL](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=SKILL&zhida_source=entity) （SOP 说明）等，相关时才注入
![](https://pic2.zhimg.com/v2-fee7c7b046408b3ddb1b886b179230e3_1440w.jpg)

### 示意代码

```
const context = assembleContext({
  system: [identity, ...rules], // ① 系统提示 + Rules
  tools: toolDefs, // ③ schemas（含 MCP 归一后的）
  history: messages, // ②④ 历史里已含 tool 结果；或先摘要
  user: currentUserMessage, // ⑤ 本轮输入
  // skillCatalog / skillBody     // ⑥ SKILL：SKILL 目录和相关SKILL 描述，全文按需注入
  // memoryHits / ragChunks       // ⑥ Memory / RAG：外置命中 → 注入
})
```

### 小结

1. 常驻内容：系统提示词 / 历史摘要 / tool schemas / tool 结果 / 本轮 user；
2. 按需内容：Memory、RAG、SKILL等，相关时才注入

*这块的细节实现，待我下去再多研究几个项目，单独出一期文章。*

### SKILL

可以看成是解决某类问题或完成某项任务的流程规范文档（SOP）。

**SKILL 不是 Tool**，可以看做是一大段提示词，实际执行仍是通过内部的指令描述调用 Tool 来完成任务。

### SKILL 结构

常见就是一份 Markdown（可带 frontmatter），大致三块：

| 部分 | 内容 |
| --- | --- |
| [元数据](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E5%85%83%E6%95%B0%E6%8D%AE&zhida_source=entity) | name、description（何时该用）；可选权限（允许的工具） / 依赖说明 |
| 正文 | 步骤、约束、输出格式、决策规则（真正的 SOP） |
| 其它 | (可选) references/、模板、脚本、workflow 等，这块一般是渐进式披露的 |

```
---
name: weather-brief
description: 用户要天气简报时使用
---

1. 先调 get_weather …
2. 再按固定结构输出 …
```

### 怎么进 Context

学到的几种方式：

| 方式 | 谁决定加载全文 | 全文怎么进 |
| --- | --- | --- |
| 手工 / 显式 | 用户指定（如 /skill:name） | 直接写入 Context |
| Harness 匹配 | 按 SKILL 描述与用户输入做简单的关键词匹配 | 匹配到的正文写入 Context |
| 模型决定 | 模型自己选要加载哪个 | 先把SKILL目录里的（name + description）给模型，模型决策后，再调工具 load_skill，SKILL 正文以 tool 结果回写 |

三种方式的逐步流程（同一例子 `weather-brief`）：

![](https://picx.zhimg.com/v2-f1c734c600c239af1c4da68bc6c07343_1440w.jpg)

### 小结

SKILL 可以由 Harness 发现并注入上下文，也可以给模型披露一些基本信息让模型自己决定加载哪个。

### MCP

MCP（ [Model Context Protocol](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=Model+Context+Protocol&zhida_source=entity)）是一套 [开放协议](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E5%BC%80%E6%94%BE%E5%8D%8F%E8%AE%AE&zhida_source=entity)，用来标准化 AI 应用怎么连接外部系统（数据、工具等）。

本文先只看 Tools 部分：统一发现与调用。

收到 `tool_calls` 后的 [执行路径](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E6%89%A7%E8%A1%8C%E8%B7%AF%E5%BE%84&zhida_source=entity)：

Harness → 选则 Client → Server → 返回的结果回写 Context。

![](https://picx.zhimg.com/v2-04c395bfafc426d1703bf1af0f5605e1_1440w.jpg)

| 角色 | 职责 |
| --- | --- |
| MCP Host | 创建/管理多个 Client，这里就是 Harness 去负责管理 |
| MCP Client | 与单个 Server 的会话连接：提供listTools、callTool 等常用方法 |
| MCP Server | 暴露 Tools 并执行（本地进程或远程服务；另有 Resources / Prompts，本文不展开） |

传输：本地多用 **stdio**，远程多用 **Streamable HTTP**； [数据传输协议](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE&zhida_source=entity) 使用 **JSON-RPC**。

### MCP Server（Tools）

```
// mcp-server.mjs —— Host spawn 的就是这个进程
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { z } from 'zod'

const server = new McpServer({ name: 'demo', version: '1.0.0' })

server.registerTool(
  'add',
  {
    description: '计算两个数字之和',
    inputSchema: {
      a: z.number().describe('加数 a'),
      b: z.number().describe('加数 b'),
    },
  },
  async ({ a, b }) => ({
    content: [{ type: 'text', text: String(a + b) }],
  }),
)

const transport = new StdioServerTransport()
await server.connect(transport) // stdout 专给 JSON-RPC；日志用 console.error
```

### 接入到 Harness 中

下面提到的 `registry` 可以看做是 **Harness 里负责管理工具注册和发现的模块**

包含本地 Tools + MCP Tools 的管理

```
import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

// 连接 MCP Server
const transport = new StdioClientTransport({
  command: 'node',
  args: ['./mcp-server.mjs'],
})
const client = new Client({ name: 'my-harness', version: '0.1.0' })
await client.connect(transport) // spawn + initialize

const { tools } = await client.listTools()
for (const t of tools) {
  // 写入 Harness 工具表
  registry.register({
    name: t.name,
    description: t.description ?? '',
    parameters: t.inputSchema ?? { type: 'object', properties: {} },
    source: { kind: 'mcp', client },
  })
}

async function executeTool(call: ToolCall): Promise<ToolResult> {
  const meta = registry.get(call.name)
  if (meta?.source.kind === 'mcp') {
    const res = await meta.source.client.callTool({
      name: call.name,
      arguments: call.arguments,
    })
    return {
      toolCallId: call.id,
      content: JSON.stringify(res.content),
      isError: Boolean(res.isError),
    }
  }
  return localHandlers[call.name](call)
}
```

CLient 连接是 **长生命周期** 的：

- 启动时 `new Client` → `connect` → `listTools` 注册一次工具；
- 之后多轮 Agent Loop 里反复 `callTool`，复用之前的连接；
- 一般只有 Harness 退出或用户主动停止该 Server 时才 `close()`。

*MCP 还包含 Resources 和 Prompt 能力，这块还要再下来研究一下与 Harness 的 [联动机](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E8%81%94%E5%8A%A8%E6%9C%BA&zhida_source=entity) 制*

### 最后

到这里 0-1 搞一个 MVP 版可跑的 Agent 应该是妥妥的了

下一篇（Part 2）大概会是以下的内容：

1. **Memory / RAG**：怎么检索、何时注入、怎么裁切；准备看一下各大 Agent 框架的实现细节，和一些业界开源库对比一下效果
2. **执行沙箱和 [权限管控](https://zhida.zhihu.com/search?content_id=280977295&content_type=Article&match_order=1&q=%E6%9D%83%E9%99%90%E7%AE%A1%E6%8E%A7&zhida_source=entity)**：部分工具执行时怎么与用户项目环境隔离；工具白名单，执行权限控制等
3. **MCP 其它内容**：Resources / Prompts

### 相关链接

- 实验项目： [notes/my-harness](https://github.com/ATQQ/leran-ai-note/blob/main/notes/my-harness/ROADMAP.md)
- PI Agent： [pi/agent](https://github.com/earendil-works/pi/blob/main/packages/agent/README.md)

发布于 2026-08-10 12:53・四川・包含 AI 辅助创作 作者对内容负责

[Harness-Engineering](https://www.zhihu.com/topic/2022053061212795744)

[Qwen3.8-Max首发尝鲜，个企双版超值优惠低至39元/月起](https://click.aliyun.com/m/20000000945/?cb=https%3A%2F%2Fsugar.zhihu.com%2Fplutus_adreaper_callback%3Fsi%3D4c43b8e6-dbeb-412a-b008-fb70bf5712ea%26os%3D3%26zid%3D1629%26zaid%3D3782460%26zcid%3D3799971%26cid%3D3799971%26event%3D__EVENTTYPE__%26value%3D__EVENTVALUE__%26score%3D__EVENTSCORE__%26ts%3D__TIMESTAMP__%26cts%3D__TS__%26mh%3D6f8f92f4fd73bb058d55979bdb706a03%26adv%3D645640%26ocg%3D0%26cp%3D0%26ocs%3D0%26aic%3D0%26atp%3D0%26ct%3D0%26ed%3DGiBNJgVzfCMmUW9XFyEvRA8xBGxJICwkOhh0FlwxKw1ZY0gnWzUoISkYdBZcPC1XVnEfO1UvKX1-AycSWDRxAV58CXoKdGlwdxVlVwJnfhYEK1wjXH5pd34SY1EDYWpcHngKfQh0a3Z8FHQVRDlxBlkjXXtdJjxtLxVqXhxkfFMPaAByXnB3cy0XZFMCNikGW3cLVkW1dXqCd94%3D&spu=biz%3D0%26ci%3D3799971%26si%3D62fd1eef-a089-40cd-98f3-3c2643fe6022%26ts%3D1788239897%26zid%3D1629)

Qwen3.8-Max 首发尝鲜、上新 deepseek-v4-flash，更多模态和旗舰模型共享额度，个企双版本超值优惠低至 39 元/...