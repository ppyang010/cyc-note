---
title: "Agent SDK 设计模式与实战经验"
aliases:
  - "有没有大佬分享一下做agent时的一些经验？"
author: "MicrolabV"
source: "https://www.zhihu.com/question/1982512240482619481/answer/2046729747087021588"
site: "知乎"
published: 2026-06-06
created: 2026-11-26
summary_model: "gpt-6.2-sol"
tags:
  - 阅读笔记
  - AI智能体
  - AgentSDK
  - 软件架构
---

# Agent SDK 设计模式与实战经验

原文是 MicrolabV 于 2026 年 6 月 6 日发布的知乎回答。作者结合 Claude Code、Hermes、Codex CLI、OpenClaw 和自己的项目整理经验。知乎标注回答包含 AI 辅助创作。总结模型为 `gpt-6.2-sol`。[知乎原文](https://www.zhihu.com/question/1982512240482619481/answer/2046729747087021588)

## 目录

- [[#先确定做哪一种 Agent]]
- [[#八种 SDK 设计模式]]
- [[#六个踩坑经验]]
- [[#最小实现里要看什么]]
- [[#原文剪藏]]
  - [[#拆了 Claude Code、Hermes、Codex 的源码后，我总结了一套做 Agent 的 SDK 设计模式]]
    - [[#先说三个背景，让你知道我有没有资格讲这个]]
    - [[#先搞清楚一件事：你要做哪种 Agent？]]
    - [[#市面上有什么 Agent SDK？我该怎么选？]]
    - [[#我的推荐路径]]
    - [[#从源码拆出来的 8 条 SDK 设计模式]]
      - [[#模式 1：Agent 核心循环 = AsyncGenerator，不是 while(true) + 回调]]
      - [[#模式 2：Tool 不是 {name, call} 函数，而是一个”协议对象”]]
      - [[#模式 3：工具执行不是 call()，是 6 层管线]]
      - [[#模式 4：Transcript（对话流）= 唯一真理源 = Append-Only JSONL]]
      - [[#模式 5：上下文管理不是”扩大窗口”，是”聪明的压缩 + 状态重注入”]]
      - [[#模式 6：工具系统的三层架构]]
      - [[#模式 7：工具并发控制要”声明式”，不要”硬编码 if-else”]]
      - [[#模式 8：多 Agent 协作——不是”多个 Agent 聊天”]]
    - [[#我自己踩过的 6 个最大的坑]]
      - [[#坑 1：一上来就做框架，而不是先解决真实问题]]
      - [[#坑 2：上下文窗口管理是”事后才想”的问题]]
      - [[#坑 3：工具系统的”超市迷路”问题]]
      - [[#坑 4：没有”后悔药”机制]]
      - [[#坑 5：把 Prompt Engineering 当架构设计]]
      - [[#坑 6：”先跑起来再说”和”设计好再动手”的平衡]]
    - [[#一个最小 Agent SDK 的骨架]]
    - [[#最后三条建议]]
      - [[#1. 先用 Claude API 原生 tool_use 写个 200 行的 Agent]]
      - [[#2. 去读 Hermes 的 run_agent.py]]
      - [[#3. 去了解 Claude Code 的架构设计]]
    - [[#一句话总结]]

## 先确定做哪一种 Agent

| 类型 | 主要设计目标 |
| --- | --- |
| 个人 Agent | 从自己的高频问题起步，优先验证速度、流程和成本是否可接受。 |
| 产品 Agent | 面向其他用户使用，需要可验证的权限控制、故障恢复和日志。 |
| SDK 或框架 | 面向开发者使用，重点是接口清晰、能力可组合，以及对不同模型的适配。 |

作者的学习顺序是先用模型 API 的原生工具调用写一个小型 ReAct 循环，再读 Hermes 的 `run_agent.py` 理解运行机制，最后结合 Claude Code 的架构分析学习工具对象、上下文压缩和会话存储。

## 八种 SDK 设计模式

| 设计 | 实现要点 |
| --- | --- |
| 1. 用异步生成器输出事件 | 核心循环统一产出流式文本、工具结果和压缩事件，由界面、SDK 或无界面调用方消费。工具结果回到消息后继续下一轮。 |
| 2. 把工具定义为协议对象 | 除工具名、描述和参数 Schema 外，工具还声明是否只读、能否并行、是否有破坏性，并提供权限判定、语义校验和结果展示的接口。 |
| 3. 分阶段处理工具调用 | 依次做 Schema 校验、语义校验、参数补全、执行前钩子、权限判定和实际执行。可纠正的参数错误作为工具结果回传，供下一轮调整。 |
| 4. 用追加式 JSONL 保存会话 | 顺序记录消息和工具结果，恢复时读取记录重建状态。子代理单独保存会话日志。 |
| 5. 压缩后重新注入任务状态 | 根据负载裁剪、摘要或合并消息，同时保留当前目标、已做的决定、进展和待做事项。 |
| 6. 把工具系统拆成三层 | Registry 定义工具，Toolset 为角色组合所需工具，模型适配层把描述转成各模型支持的 Schema。 |
| 7. 由调度层控制并发 | 根据工具声明、访问路径和顺序依赖决定并发批次。需要用户交互的工具，以及对同一资源有读写冲突的操作，按顺序处理。 |
| 8. 为子代理隔离上下文 | 每个子代理有独立的会话、工具子集和迭代预算，主 Agent 获取可用于决策的结构化结果。 |

原文把默认串行和默认非只读作为保守的调度元数据。同段代码里的 `checkPermissions()` 示例返回 `allow`。阅读示例时，工具调度属性和执行授权应分别核对。

## 六个踩坑经验

1. **从真实需求验证接口。** 先用少量工具完成一件经常要做的事。作者的例子是在 Chromium 代码库里查函数调用链。
2. **尽早处理上下文预算。** 给循环设压缩触发条件，并在压缩后保留关键状态，防止恢复到错误的任务。
3. **按任务暴露工具。** 减少含义重叠的工具，用描述写明适用场景，按角色或阶段切换工具集。
4. **为有副作用的操作准备恢复路径。** 原文举了临时文件、数据库事务和命令预演三个例子。
5. **把可验证的判断放进代码。** 由代码处理安全、路由和校验，提示词描述角色和行为，并随变更记录版本。
6. **先稳定循环、工具接口和会话记录。** 用少量工具验证这三项，再逐步扩展并发、界面和多 Agent 协作。

## 最小实现里要看什么

原文的 Python 骨架展示了三个接口的连接方式。`Agent.query()` 调用模型并发出事件，`Tool.call()` 的执行结果回到消息，`Transcript.append()` 将会话记录追加到 JSONL。达到轮数上限时停止循环。模型调用和工具请求解析在示例中留作待实现的方法。

相关笔记可以继续查学习顺序与循环设计。[[ai-output/AI Agent 学习路线|AI Agent 学习路线]] · [[ai-output/全网爆火的Loop到底是什么？|Agent Loop 阅读笔记]]

## 原文剪藏

### 拆了 Claude Code、Hermes、Codex 的源码后，我总结了一套做 Agent 的 SDK 设计模式

> 不是”我听说 Agent 是这么做的”——是我拆了源码，逐行看完，踩过坑之后的总结。

---

#### 先说三个背景，让你知道我有没有资格讲这个

我过去三个月做了三件事：

**1\. 拆了四款工业级 Agent 的源码**

- **Claude Code** （Anthropic）：npm 泄露源码事件，1902 个源文件、51 万行 TypeScript。我从程序入口一路拆到 6 Phase 安全执行链、20+ Bash 验证器、三层 Multi-Agent Runtime。
- **Codex CLI** （OpenAI）：Rust 实现。从 ExecPolicy 声明式策略引擎到三平台 OS 级沙箱，14 个月 6996 次提交的生长历程全看了。
- **Hermes** （NousResearch 开源）：Python 实现，生产级 Agent 框架。run\_agent.py 虽然 12000 行，但核心循环设计极其精妙。
- **OpenClaw** （开源）：TypeScript + Bun。对比着看——它的 4 种工具死循环检测器默认关闭，是个反面教材；TOCTOU 防护（CWD inode 快照 + SHA256）又是个好实践。

**2\. 从零做了个 13 角色的 Agent 团队**

取名「维弈阁」（Weiyige）。不是在 Jupyter 里跑个 Demo——它每天在生产环境帮我写 Chromium 内核代码、管理部署、发布内容。半年 300+ 提交，从架构到 CLI 到调度全撸了一遍。

**3\. 在真实项目里验证**

Agent 不是玩具。我在 Chromium 浏览器内核开发里用它查 bug、修死锁、分析 crash。在 macOS 桌面应用开发里用它写 Swift 代码、打 DMG 包。在内容创作里用它分析选题、排版文章、发布微信公众号。

> 这篇文章不讲理论。讲我从源码里拆出来的设计模式，和我踩过的坑。 如果你正在做或准备做 Agent，这些应该能帮你省几个月弯路。

---

#### 先搞清楚一件事：你要做哪种 Agent？

Agent 分三种，设计思路完全不同。 **大多数人踩的第一个坑就是搞混了：**

| 类型 | 给谁用 | 核心追求 | 代表产品 | 典型错误 |
| --- | --- | --- | --- | --- |
| 个人 Agent | 自己用 | 快、灵活、低成本 | 我自己的 weiyige | 过度设计安全 |
| 产品 Agent | 给别人用 | 安全、可靠、可观测 | Codex CLI | 不安全就给别人用 |
| SDK/框架 | 给开发者用 | API 设计、可组合性 | Hermes | 抽象泄漏 |

**个人 Agent 根本不需要 7 层安全**——你盯着它执行，出事随时 Ctrl+C。而给别人用的产品 Agent，哪怕一次执行失误（删了个文件、执行了恶意命令）就是灾难。

我做的是从 1 走到 2——先用 Claude Code API 写了个自己能用的，然后再考虑安全。这是最务实的路径。

---

#### 市面上有什么 Agent SDK？我该怎么选？

如果你今天开始做 Agent，这是选型参考（基于我实际用过/拆过的产品）:

| SDK/方案 | 适合场景 | 我能用一句话说清它的核心设计 |
| --- | --- | --- |
| Claude API 原生 tool\_use | 从零开始，完全掌控 | 模型直接返回 tool\_use block，你写循环去执行——最干净 |
| Claude Code SDK (@anthropic-ai/claude-code) | 快速验证想法 | 把 Claude Code 当程序调用，有完整工具系统但你是黑盒用户 |
| OpenAI Agents SDK | OpenAI 生态 | 官方出品，设计简洁但深度绑定 GPT |
| Vercel AI SDK | Web/全栈项目 | 多模型支持、流式处理做得好，但 Agent 能力偏弱 |
| LangChain/LangGraph | 复杂工作流 | 生态大但抽象层太厚，新手容易被埋 |
| Hermes | 需要完整方案，学架构 | 全套内置（工具/网关/记忆/压缩），架构设计极佳 |
| 自己写 | 有特殊需求 | 完全掌控，但很容易漏掉边界情况 |

#### 我的推荐路径

```
第一步：用 Claude API 原生 tool_use 写一个 200 行的 ReAct 循环
       → 理解 Agent 的核心心跳：什么时候思考、什么时候调工具、什么时候停

第二步：去读 Hermes 的 run_agent.py（别看 12000 行吓到，核心循环就 300 行）
       → 学"生产级 Agent 循环该怎么写"

第三步：去读 Claude Code 的架构分析
       → 学"Tool 协议对象该怎么设计""上下文压缩怎么做""会话怎么存"
```

---

#### 从源码拆出来的 8 条 SDK 设计模式

以下每一条，都有源码证据，都有我的踩坑经历。

---

##### 模式 1：Agent 核心循环 = AsyncGenerator，不是 while(true) + 回调

Claude Code 最让我震撼的设计：`query()` 是一个 `AsyncGenerator<StreamEvent>`。

```
// Claude Code 的核心——伪代码还原
async function* query(userMessage, systemPrompt): AsyncGenerator<StreamEvent> {
  let messages = buildInitialMessages(userMessage, systemPrompt);

  while (true) {
    // 1. 流式调用模型
    for await (const chunk of api.stream(messages)) {
      yield { type: 'thinking', chunk };  // UI 实时看到模型在"想"
    }

    // 2. 提取 tool_use block
    const toolCalls = extractToolCalls(messages);
    if (toolCalls.length === 0) break;  // 模型说完了，结束

    // 3. 执行工具（并行/串行自动分批）
    for (const result of runToolsWithPartitioning(toolCalls)) {
      yield { type: 'tool_result', result };  // UI 看到工具执行结果
    }

    // 4. 工具结果回流 → 下一轮
    messages = appendToolResults(messages, results);

    // 5. 检查是否需要压缩上下文
    if (shouldCompact(messages)) {
      messages = await compactConversation(messages);
      yield { type: 'compact', summary };
    }
  }
}
```

**这个设计优雅在哪** ：

- **同一个 `query()` 同时驱动 REPL / SDK / headless / subagent** 四种场景——不存在两套实现的差异风险
- 每个 `yield` 都是一个实时事件，UI 层只需要 `for await (const event of query(...))` 消费就行
- 不用回调地狱，不用事件总线，状态管理清晰

**我的教训** ：weiyige 第一版用的是经典 `while(true)` + 回调通知 UI。结果 UI 更新逻辑和循环逻辑耦合在一起，改一次行为要动三个地方。第二版改成 generator 模式后，代码量减少 40%，bug 减少更多。

> **怎么用** ：不管什么语言，Agent 核心循环建模为 Iterator/Generator，而不是函数调用链。Python 用 `yield`，JS/TS 用 `AsyncGenerator`，Rust 用 `Iterator trait`。这是架构层面的决策，不是实现细节。

---

##### 模式 2：Tool 不是 {name, call} 函数，而是一个”协议对象”

做 Agent 的人一开始都只定义工具的 `name` 和 `call()`。Claude Code 告诉我们——工具的设计空间大得多。

Claude Code 的 `Tool` 协议对象包含这些属性：

```
Tool {
  // 模型可见的
  name, description, inputSchema (Zod)

  // 安全元数据 —— 必须显式声明
  isConcurrencySafe()    // 能不能和别的工具并行执行？
  isReadOnly()           // 是否只读？
  isDestructive()        // 是否有破坏性？
  checkPermissions()     // 权限判定逻辑

  // 运行时校验
  validateInput()        // 超越 Schema 的业务校验

  // UI 渲染
  renderToolUseMessage()        // 工具调用前的 UI 展示
  renderToolResultMessage()     // 工具执行完的 UI 展示
  renderToolErrorMessage()      // 出错的 UI 展示
}
```

**最关键的设计——Fail-Closed 默认值** ：

```
const TOOL_DEFAULTS = {
  isConcurrencySafe:  () => false,   // 默认不能并发 ← 保守
  isReadOnly:         () => false,   // 默认非只读   ← 保守
  isDestructive:      () => false,   // 默认非破坏性
  checkPermissions:   () => ({ behavior: 'allow' }),  // 默认放行
}
```

它宁可假设工具不安全（不能并发、非只读），强迫开发者 **显式声明** 安全属性。这种设计比”默认安全”更安全——因为”默认安全”经常被偷懒的开发者忽略，而”默认不安全”则强制思考。

**我的教训** ：第一版工具就写了 `{name, run}`。后来发现——文件写入工具可以并发吗？不行，会乱序。网络请求工具可以并发吗？可以。但框架不知道，所有工具一视同仁。结果就是用户说”帮我创建三个文件”，Agent 并行写，文件内容乱掉了。

> **怎么用** ：每定义一个工具，至少声明 `isReadOnly` 和 `isConcurrencySafe`。并发控制逻辑在框架层统一处理，开发者只需要声明属性。

---

##### 模式 3：工具执行不是 call()，是 6 层管线

Claude Code 里，一个 tool\_call 到达后不是直接调函数的——它经过 6 层：

```
tool_use 到达
  → 1. Zod Schema 校验（参数类型/必填/范围）
  → 2. 业务语义校验（validateInput()）
  → 3. 隐式依赖补全（如自动展开 ~/Documents 为绝对路径）
  → 4. PreToolUse Hook（外部可拦截/修改参数）
  → 5. 权限判定（allow / deny / ask user）
  → 6. tool.call() 实际执行
```

**最大教训不是”要加这么多层”，而是 Schema 校验失败后怎么处理：**

Claude Code 的做法： **不崩溃，把 zod error 作为 tool\_result 抛回给模型** 。模型看到 `"Error: parameter 'path' is required"` 后会自己纠正重试。这种设计让 Agent 的健壮性提升了不止一个量级——模型会从错误中学习调整，而不是直接中断。

**我的教训** ：第一版用 try-catch 兜底，工具调用出错就报错终止。后来改成”错误回流给模型”——Agent 居然能自己修！`read_file('/nonexistent')` 失败 → 模型说”哦，文件不存在，我换个路径试试”。

---

##### 模式 4：Transcript（对话流）= 唯一真理源 = Append-Only JSONL

Claude Code 的会话存储不是一个可变的状态对象，而是一个 **Append-Only JSONL 文件** ：

```
{"role":"user","content":"帮我看看 auth.ts 的鉴权逻辑","timestamp":"2026-06-06T10:00:00Z"}
{"role":"assistant","content":"好的，我先读一下文件","timestamp":"2026-06-06T10:00:05Z"}
{"role":"assistant","tool_use":{"name":"read_file","input":{"path":"src/auth.ts"}},"timestamp":"10:00:06Z"}
{"role":"user","tool_result":{"content":"export function authenticate...","path":"src/auth.ts"},"timestamp":"10:00:07Z"}
{"role":"assistant","content":"鉴权逻辑是这样的...","timestamp":"10:00:15Z"}
```

**为什么 Append-Only JSONL 比”定时快照”好得多** ：

- 写入层极其简单：只追加，不修改。崩溃时最多丢最后一条
- 恢复只需要读完整个文件重建状态，逻辑清晰
- Subagent 的对话是独立 sidechain（`<sessionId>/subagents/agent-<agentId>.jsonl`），互不干扰
- 天生可审计——每一条记录都有时间戳

**我的教训** ：Weiyige 第一版用内存状态对象 + 定时写 JSON 快照。结果会话中断时，恢复的永远是不完整的快照——用户说”它忘了我们聊到哪了”。改成 JSONL 后，中断恢复从”看运气”变成”基本可靠”。

> **怎么用** ：不要设计一个复杂的 Session 对象然后用 `save()`。设计一个 `Transcript` 类，只有一个方法 `append(entry)`。恢复时 `loadAll()` 重建状态。简洁 = 可靠。

---

##### 模式 5：上下文管理不是”扩大窗口”，是”聪明的压缩 + 状态重注入”

很多人做 Agent 遇到上下文窗口不够，第一反应是”买更大的模型”。Claude Code 和 Hermes 告诉我们——要压缩，不要扩容。

**Claude Code 的 4 种 compact 策略** ：

| 策略 | 做法 | 什么场景用 |
| --- | --- | --- |
| 截断 | 删除最旧的消息（保留头 2 轮 + 尾 3 轮） | 对话很短时 |
| 摘要 | 用模型自己总结中间的对话 | 对话中等时 |
| 合并 | 合并连续的 tool\_use → tool\_result 对 | 有大段工具交互时 |
| 话题切分 | 按话题分块，保留相关块，摘要无关块 | 对话很长且话题分散时 |

**不是简单删消息——压缩后必须重注入”模型记忆状态”** 。最后一条系统消息会包含：”当前任务进度是…；已确认但未实现的决策是…；待处理的 pending 项是…“。

**Hermes 的 TrajectoryCompressor 更激进** ：

- 压缩后的对话仍保持 `user → assistant → user → assistant` 的严格 role 交替
- 摘要以 user 消息注入（不是 system），这样不消耗 Anthropic prompt cache
- 压缩阈值可配置：按 token 数、按轮次数、按时间

**我的教训** ：第一版只做了”截断最旧消息”，结果 Agent 忘了前面的上下文后行为诡异——”它刚刚还在改 auth.ts，突然就开始改 README 了”。加了状态重注入后，即使压缩了一半对话，Agent 也知道”我在做鉴权相关的事”。

---

##### 模式 6：工具系统的三层架构

Hermes 的工具系统是我见过最干净的——不是”注册+调用”，而是三层：

```
Layer 1: Registry     — 全局工具注册表，定义每个工具是什么
Layer 2: Toolset      — 按 Agent 角色组合，"这个 Agent 能用哪些工具"
Layer 3: Model Tools  — 将工具描述转为特定模型的 tool_use schema
```

**为什么要三层？**

Registry 是全局的——一次定义，到处使用。Toolset 是按角色组合的——PM Agent 不需要文件写入工具，内容 Agent 不需要系统命令工具。Model Tools 是按模型适配的——GPT-4o 和 Claude 的 tool\_schema 格式不同，这一层做转换。

```
# Hermes 的设计思路——伪代码
class ToolRegistry:
    tools: Dict[str, Tool]  # 全局注册

class Toolset:
    # 按角色组合
    pm_tools = [registry['read_file'], registry['search_code']]
    dev_tools = [registry['read_file'], registry['write_file'], registry['run_shell']]

class ModelToolAdapter:
    # 适配不同模型
    def to_claude_schema(tool):  ...
    def to_openai_schema(tool):  ...
```

**我的教训** ：做 weiyige 时我把所有工具平铺成一个大列表，13 个角色共享所有工具。结果内容创作 Agent（辞）的 prompt 里包含了 `execute_shell` 工具——它虽然没调过，但这就像给实习生 root 权限，”万一”就是灾难。三层分离后，每个角色只看到它需要的工具。

---

##### 模式 7：工具并发控制要”声明式”，不要”硬编码 if-else”

当一个 Agent 调用返回了多个 tool\_use block，哪些可以并行？这是所有 Agent 框架都要解决的问题。

**Claude Code 的做法** ：`partitionToolCalls()` 按 `isConcurrencySafe` 声明分批：

```
输入: [Read(a.ts), Read(b.ts), Write(c.ts), Read(d.ts)]

分批结果:
  Batch 1 (并发): [Read(a.ts), Read(b.ts)]  ← 都只读，可以并发
  Batch 2 (串行): [Write(c.ts)]             ← 有写入，独占
  Batch 3 (串行): [Read(d.ts)]              ← 写入后读，必须串行
```

**Hermes 的做法** ：

```
NEVER_PARALLEL_TOOLS = {'clarify', 'ask_user'}  # 需要用户交互的永远串行

# Path-scoped tools 根据路径是否独立判断
# read_file('a.ts') + write_file('b.ts') → 可以并行，路径不冲突
# read_file('a.ts') + write_file('a.ts') → 必须串行，同文件
```

**核心原则** ：并发控制逻辑在框架层统一处理，开发者只需声明属性。不要在每个工具调用处写 `if (tool.name === 'write_file') await; else Promise.all`——这是框架该做的事。

---

##### 模式 8：多 Agent 协作——不是”多个 Agent 聊天”

很多人以为 Multi-Agent 就是”让 Agent A 调用 Agent B”。Claude Code 的三层设计格局大得多：

```
Level 1: Subagent        — 基础委派，"帮我去这个目录里找个东西"
Level 2: Coordinator     — 调度器，"任务拆成三步，分别发给三个 subagent"
Level 3: Swarm           — 团队协作，"三个 Agent 同时工作，互相通信"

关键设计：每层有独立 transcript，独立的上下文预算
```

**Subagent 和主 Agent 是完全隔离的** ：

- 独立的 JSONL transcript（sidechain）
- 独立的上下文窗口
- 独立的工具预算（默认 50 次迭代）
- 返回结构化结果，不是原始对话

这避免了一个经典问题：subagent 把主 Agent 的上下文占满。

**Hermes 的设计** ：

```
# Hermes 的子代理创建——伪代码
sub = agent.create_sub_agent(
    tools=subset_tools,       # 工具子集，不是所有
    max_iterations=50,        # 独立预算
)
result = sub.run(prompt)
# 结果直接合并进主 Agent 的对话流
```

---

#### 我自己踩过的 6 个最大的坑

这些不是别人的教训——每一个都让我重写过代码。

##### 坑 1：一上来就做框架，而不是先解决真实问题

**症状** ：花 3 个月设计 Agent 架构、定义 SDK 接口、写配置系统、做插件机制。没写过一个能用的 Agent。

**真相** ：Agent 框架的设计直觉，只能从”做一个能解决真实问题的 Agent”中获得。你都不知道 Agent 会在哪里卡住，怎么设计得好框架？

**解法** ：先写一个 200 行的 Agent 解决你每天遇到的问题。我的第一个 Agent 是”帮我在 Chromium 代码库里找一个函数的调用链”——100 行，`read_file` + `grep` 两个工具，但 **真的有用** 。用完一周后我才知道 Agent 循环应该怎么写。

> **铁律** ：第一行代码必须是 Agent 循环，不是框架设计。

---

##### 坑 2：上下文窗口管理是”事后才想”的问题

**症状** ：Agent 跑得好好的，第 15 轮突然报 `context_length_exceeded`，然后崩溃。用户看到的是”突然不工作了”。

**真相** ：上下文管理不是 feature——是 Agent 的基础设施。从第一天就应该有 compact 机制。

**解法** ：最简单的方式——当 token 数超过阈值时，用模型自己摘要前面 80% 的对话，保留最近的 20%。不要截断（会丢失重要上下文），要摘要 + 关键信息保留。

---

##### 坑 3：工具系统的”超市迷路”问题

**症状** ：给了 Agent 50 个工具，结果它选工具准确率不到 60%。甚至在应该 `read_file` 的时候调了 `search_web`。

**真相** ：工具太多 = 模型在”超市”里迷路。每个工具的描述要足够区分，工具总数要控制。

**解法** ：

- 单次对话最多给 15-20 个工具
- 工具描述必须有”什么时候用 / 什么时候不用”
- 相似功能的工具合并（如 `read_file` + `read_json` → 一个 `read` 工具，通过参数区分）
- 按场景动态切换工具集（写代码时不需要内容发布工具）

---

##### 坑 4：没有”后悔药”机制

**症状** ：Agent 误删了一个文件，没有 undo 能力。用户心态爆炸。

**真相** ：Agent 一定会犯错。关键是犯错后能不能恢复。

**解法** ：所有破坏性操作必须有”软执行”模式。文件写入先写临时文件、数据库操作包在事务里、系统命令用 dry-run。不是所有操作都需要 undo——但每类危险操作至少该有一种恢复手段。

---

##### 坑 5：把 Prompt Engineering 当架构设计

**症状** ：Agent 表现不好 → 改 prompt → 好了一点 → 几天后又坏了 → 再改 prompt → prompt 越来越长 → 5000 字的系统 prompt，没人知道怎么维护。

**真相** ：prompt 不是架构。把核心逻辑写在 prompt 里 = 把重要逻辑写在没有版本管理、没有测试、没有类型检查的地方。

**解法** ：

- Prompt 只描述 Agent 的角色和行为风格
- 核心判断逻辑（安全/路由/校验）写在代码里
- Tool 的描述由代码自动生成，不是手写
- Prompt 也要版本管理，每次变更记录原因

---

##### 坑 6：”先跑起来再说”和”设计好再动手”的平衡

**症状** ：在两种极端之间反复横跳——要么永远在设计，要么永远在”快速迭代”导致架构债堆积。

**真相** ：最好的平衡是： **核心循环设计好再动手，其他都是插件** 。

**解法** ：

- Agent 循环（ReAct）、Tool 接口、Transcript 存储——这 3 个设计好再写代码
- 安全层、多 Agent、上下文压缩、UI——这些都是可以后续加的插件
- 不要试图设计”完美的 Tool 接口”——定义 3 个工具就够验证接口设计了

---

#### 一个最小 Agent SDK 的骨架

如果你想今天就开始写，这是最小核心。Python 版（TypeScript 同理）：

```
from typing import AsyncGenerator, Protocol, Any
from dataclasses import dataclass, field
import json

# ── 1. Tool 协议对象 ──
@dataclass
class Tool:
    name: str
    description: str
    parameters: dict  # JSON Schema
    is_readonly: bool = False

    async def call(self, params: dict) -> str:
        """子类覆盖。返回值是字符串，直接回流给模型。"""
        raise NotImplementedError

# ── 2. Transcript 存储 ──
@dataclass
class TranscriptEntry:
    role: str        # 'user' | 'assistant' | 'tool'
    content: str
    tool_name: str = None
    tool_input: dict = None

class Transcript:
    """Append-Only JSONL"""
    def __init__(self, path: str):
        self.path = path
        self.entries: list[TranscriptEntry] = []

    def append(self, entry: TranscriptEntry):
        self.entries.append(entry)
        with open(self.path, 'a') as f:
            f.write(json.dumps(entry.__dict__, ensure_ascii=False) + '\n')

    def to_messages(self) -> list[dict]:
        """转为 LLM API 格式"""
        messages = []
        for e in self.entries:
            if e.role == 'tool':
                messages.append({
                    'role': 'user',
                    'content': [{
                        'type': 'tool_result',
                        'tool_use_id': e.tool_name,
                        'content': e.content
                    }]
                })
            else:
                messages.append({'role': e.role, 'content': e.content})
        return messages

# ── 3. Agent 核心循环 ──
class Agent:
    def __init__(self, api_key: str, model: str = 'claude-sonnet-4-20250514'):
        self.api_key = api_key
        self.model = model
        self.tools: dict[str, Tool] = {}
        self.transcript: Transcript = None

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool

    async def query(self, user_message: str) -> AsyncGenerator[str, None]:
        """核心循环——AsyncGenerator 模式"""
        self.transcript = Transcript(f'session-{hash(user_message)}.jsonl')
        self.transcript.append(TranscriptEntry(role='user', content=user_message))

        messages = [{'role': 'user', 'content': user_message}]
        system_prompt = self._build_system_prompt()
        loop_count = 0
        max_loops = 30

        while loop_count < max_loops:
            # 1. 调用模型
            response = await self._call_llm(messages, system_prompt)

            # 2. 检查是否有 tool_use
            tool_blocks = self._extract_tool_use(response)
            if not tool_blocks:
                yield response.content  # 最终回答
                self.transcript.append(TranscriptEntry(role='assistant', content=response.content))
                break

            # 3. 执行工具
            yield f'🔧 调用 {len(tool_blocks)} 个工具...'
            for block in tool_blocks:
                tool = self.tools.get(block['name'])
                if not tool:
                    result = f'Error: unknown tool {block["name"]}'
                else:
                    try:
                        result = await tool.call(block['input'])
                    except Exception as e:
                        result = f'Error: {str(e)}'  # 错误回流给模型，不崩溃

                self.transcript.append(TranscriptEntry(
                    role='tool', content=result,
                    tool_name=block['name'], tool_input=block['input']
                ))
                messages.append({
                    'role': 'assistant',
                    'content': [{'type': 'tool_use', 'name': block['name'], 'input': block['input'], 'id': block['id']}]
                })
                messages.append({
                    'role': 'user',
                    'content': [{'type': 'tool_result', 'tool_use_id': block['id'], 'content': result}]
                })

            loop_count += 1

        if loop_count >= max_loops:
            yield '⚠️ 达到最大循环次数，强制终止'

    def _build_system_prompt(self) -> str:
        tool_descriptions = '\n'.join([
            f'- {t.name}: {t.description}' for t in self.tools.values()
        ])
        return f"""You are a helpful agent. Available tools:
{tool_descriptions}

Rules:
- Use tools when you need real information
- If a tool fails, try an alternative approach
- Do not fabricate file contents or command outputs
"""

    async def _call_llm(self, messages, system):
        """调用 Claude API（你需要实现这部分）"""
        ...

    def _extract_tool_use(self, response) -> list[dict]:
        """从模型响应中提取 tool_use block"""
        ...
```

**这个骨架的核心设计决定** ：

1. **AsyncGenerator** — 驱动 REPL/SDK/API 三种场景
2. **Tool 协议对象** — 不只是 name+call，包含元数据
3. **Transcript JSONL** — Append-Only，不丢数据
4. **错误回流** — 工具调用失败不崩溃，错误信息给模型让它自己修

从这 200 行开始，再逐步加：并发控制、上下文压缩、多 Agent、安全管线。

---

#### 最后三条建议

##### 1. 先用 Claude API 原生 tool_use 写个 200 行的 Agent

不要套任何框架。你会理解 ReAct 循环的真正心跳——模型什么时候思考、什么时候调工具、什么时候停止。这个理解是后面所有设计决策的基础。

##### 2. 去读 Hermes 的 run_agent.py

别看它 12000 行吓人——核心循环就 300 行。读完之后你会理解：生产级 Agent 循环怎么写、工具注册和组合怎么设计、并发控制怎么统一处理。

##### 3. 去了解 Claude Code 的架构设计

它的 AsyncGenerator 循环、Tool 协议对象、6 层执行管线、Transcript JSONL 存储、4 种上下文压缩策略——每一项都是经过工业级验证的设计模式。

---

#### 一句话总结

> **Agent SDK 的本质不是一个”大框架”，而是一套设计模式的组合。你先理解了模式，用什么语言、什么框架实现都行。**

Agent 是发动机，不是方向盘。先跑起来解决一个真实问题，再考虑架构。

---

*作者：MicroLabV，Chromium 内核开发者，个人 Agent 团队系统创造。拆解过 Claude Code、Codex CLI、Hermes、OpenClaw 四款工业级 Agent 的源码。这篇文章不是理论推导，是 51 万行源码 + 300+ 次提交的实战总结。*
