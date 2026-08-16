---
id: "2045527331234657654"
title: "为什么coding agent大多数都基于Nodejs？"
author: "萝卜啊"
type: zhihu-answer
source: "https://www.zhihu.com/question/2044211173227221755/answer/2045527331234657654"
created: "2026-06-03 15:28"
updated: "2026-06-04 09:33"
collected: "2026-06-03 15:28"
downloaded: "2026-08-16"
---
更正一下，Codex CLI已经全面转般rust。未来估计转的也会更多。rust有高并发与启动速度，在沙箱隔离上也可以做很多。这点即使TS有Bun也比不了。

但TS贵在快速建项，很多项目都是成功后才用Rust改写。

* * *

不是 Node.js 多强，是它在 2022 年底这波 AI 爆发之前就把"拼图"拼完了。异步 I/O、流式输出、CLI 工具链、类型系统，恰好就是做 coding agent 最顺手的那套。

我数过一遍当前主流的 coding agent，终端向的几乎全是 Node.js / TypeScript：Claude Code（Anthropic）、Codex CLI（OpenAI）、Cline / Roo Code / Kilo Code、opencode、Qwen Code、Kimi CLI、Gemini CLI，全是 TS，发行走 npm。

但另一批大名鼎鼎的 agent 是 Python：Aider、OpenHands（原 OpenDevin）、SWE-Agent、gptme。同样是 coding agent，凭什么分两派？

把这盘棋摊开看，TS 派赢的不是"语言优越"，是路径依赖加上生态契合。Agent 这波爆发赶在 2023-2024 年，恰好是 Claude Code 立项、Codex CLI 立项、Cline 从 VSCode 插件长出 CLI 的窗口期。那时候团队里现成能拉来写 agent 的人，背景里八成都写着 Node / TypeScript。

**异步和流式，是 LLM 时代的原生能力**

一个 coding agent 的核心循环长这样：用户问一句 → 调 LLM API → 拿回一坨流式 token → 模型说要执行工具 → 跑工具（读文件 / 跑命令 / 改代码）→ 把结果喂回 LLM → 继续生成。这个循环里大部分时间都在"等"，等网络 IO、等文件 IO、等子进程结束。

Node.js 干了这件事十年了。从 2009 年 Ryan Dahl 写它那天起，就是为"高并发 + IO 密集"设计的。事件循环 + 非阻塞 I/O 这套东西，和 LLM 的流式响应天然合拍。SSE 进来是 ReadableStream，stdout 进来也是 ReadableStream，写文件、写进程、监听 stdin，全是 async。

说白了，coding agent 本质上就是"一边和 LLM 聊天一边干别的事的进程"。一边读用户的输入，一边等模型吐字，一边把工具跑起来——这正是 Node.js 当年给自己定的活儿。

**TypeScript ≈ 工具调用的原生语言**

这件事没那么显而易见，但你看 Claude Code 2025 年 3 月那次源码泄露就会懂。整个仓库 1,902 个 TypeScript 文件、51 万行代码，AI Agent 的核心是 Tool 系统，每个工具的输入输出都得是结构化的 JSON Schema 发给模型。

而 TypeScript 的类型到 JSON Schema 几乎是天然映射。Zod、AJV、TypeBox 这些库把 `interface { name: string; age: number }` 转成 JSON Schema 是几行代码的事，类型即校验，也直接是喂给模型的指令。你不用再单独维护一份 prompt 里描述参数形状的英文文档，写完 interface，schema 和文档一起就出来了。

Codex CLI 在 npm 上写"0 dependencies"，但它的 TypeScript 类型链一样能生成严格的 tool schema。其他语言要做到这件事，要么手写 schema，要么用 Pydantic 二次映射。不是不行，就是绕。

**npm 生态没有对手**

造一个终端 coding agent，你绕不开这几样东西：

-   Commander / yargs：CLI 参数解析
-   Ink：React 写终端 UI（流式输出、loading 动画、权限确认弹窗全靠它）
-   chalk：终端着色
-   undici：HTTP 客户端，调 LLM API
-   esbuild / tsup：打包
-   ws / node-fetch：流式和 HTTP

这些东西在 npm 上都是现成、文档齐全的。Python 这边有 Click、Rich、httpx、Textual，质量也不差，但量级和一致性差了一截。

你想想，Claude Code 启动时把 React 组件渲染到终端里，靠的就是 Ink。Codex CLI 的流式打字效果、权限弹窗、loading 进度条，全是这一套。Y Combinator W25 那批做 agent 的初创，60-70% 直接拿这套 terminal UI 范式抄作业，省下来的工程量是几个 FTE 的事，这种生态护城河越用越厚。

**Bun 把启动速度的短板也补上了**

Node.js 老被人吐槽启动慢，几百毫秒起步，对一个 CLI 工具来说用户能感觉到。Claude Code 直接换 Bun，用 JavaScriptCore 做引擎，启动比 Node 快几倍，打包时顺带做 tree-shaking 和编译时 feature flag 消除。

Codex CLI 走另一条路，用 esbuild 打成单文件塞进 npm 包，跨平台分发，本质是把"运行时依赖"这个痛点用打包工具绕过去了。

TS/Node 派连"启动慢"这种老被人骂的劣势，都被自家的工具链自己消化掉了。

**反例不是反例，是另一条赛道**

那为什么 Aider、OpenHands、SWE-Agent、gptme 不用 Node.js？

你去看他们的定位：

-   Aider：要做的是"读你整个 repo → 给 LLM 喂代码 map → 自动 git commit"。这种活儿 Python 写起来更短，LLM SDK 也成熟
-   OpenHands：沙箱 + 浏览器 + 多步任务，本质是平台，需要 PyTorch 生态、Web UI 框架、Docker SDK。Python + FastAPI + React 才是这套架构的正解
-   SWE-Agent：学术项目出身，Hugging Face、transformers、datasets 全是 Python 圈，绕不开
-   gptme：通用 agent，工具集里有浏览器、shell、Python REPL——它的核心能力就是执行 Python

说白了，Node.js 派打的是"终端 + LLM 循环 + 工具调用"这一类，Python 派打的是"沙箱 + 平台 + ML 生态"那一类。两边重叠的很少，因为它们解决的不是同一个问题。选 Node.js 的团队在做一个跑在你本机 terminal 里的瑞士军刀；选 Python 的团队在做一个能云端调度、能跑 docker、能直接看 Jupyter 的工程师替身。

**所以不是 Node.js 赢了**

YC X25 这批做 agent 的初创公司里，Mastra AI 创始人 Sam Bhagwat 透露 60-70% 选了 TypeScript。OpenAI 给 Agents SDK 加了 TS 支持，LangChain 也早早出了 TS 版。

但这不是 Node.js"打败"了 Python。这波 coding agent 的核心交互形态——终端、IDE 插件、LLM 流式——刚好落在 Node.js 的甜区里。

你把这个时间点拨回 2010 年，让一群人写个 terminal AI assistant，他们大概率还是用 Node.js。不是因为它完美，是因为它早把"拼图"拼完了。哪天"AI 编程 agent"的主流形态从 terminal 切到云端 sandbox 跑 Python REPL，Node.js 派的窗口才会真正关上。但那是另一个故事了。

* * *

以上是本次回答的全部内容。

我是一个AI时代的践行者，三十年编程老兵， 我把系统的AI知识，梳理在了我的微信公众号【萝卜啊】， 关注后获取最新AI相关知识，期待和你交流。

周一至周五：每日更新ClaudeCode最佳实践一篇，AI最佳开源Agent或Skill一篇。 周六：更新本周AI快讯和Github最佳榜单各一篇。 周天：更新AI Agent领域最佳实践一篇。