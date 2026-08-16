---
id: "2045201169656582783"
title: "为什么coding agent大多数都基于Nodejs？"
author: "Black code"
type: zhihu-answer
source: "https://www.zhihu.com/question/2044211173227221755/answer/2045201169656582783"
created: "2026-06-02 17:52"
updated: "2026-06-02 17:52"
collected: "2026-06-02 17:52"
downloaded: "2026-08-16"
---
如果你关注 AI Coding Agent 领域，会发现很多明星项目都选择了 Node.js：

-   Claude Code
-   OpenCode
-   Reasonix
-   Aider 的部分生态工具
-   各种 MCP Server
-   前几天kimi-code从原来的kimi-cli(python)用Typescript重构

当然也有一些“清流”：

-   Codex CLI 用 Rust
-   Crush 用 Go
-   一些企业级 Agent 用 Python

但总体来看，Node.js 的占比确实高得离谱。

于是很多人会问：

> Node.js 在 AI Agent 领域到底有什么特殊优势？  
> 为什么不是 Python？为什么不是 Go？为什么不是 Rust？  

我研究了一圈之后，发现答案可能比大家想象得更简单。

### 先说结论

很多人以为：

> Coding Agent 选择 Node.js，是因为 Node.js 特别适合 AI。  

其实不完全对。

更准确地说：

> Coding Agent 选择 Node.js，是因为它特别适合“工具调用（Tool Use）”。  

而现代 Agent，本质上就是：

```text
LLM + Tool Use + Workflow
```

模型负责思考。

Node.js 负责执行。

* * *

### Agent 80% 的时间都在干杂活

很多人以为 Agent 的核心是：

```text
调用 OpenAI
调用 Claude
返回结果
```

实际上完全不是。

真正复杂的是这些：

```text
读取文件
修改文件
搜索代码
执行命令
管理 Git
启动进程
调用 MCP
监听事件
处理流式输出
管理权限
处理重试
上下文压缩
任务编排
```

说白了：

Agent 更像一个自动化运维脚本。

而不是一个 AI Demo。

* * *

### Node.js 天生适合干这种事

举个例子。

Agent 经常需要同时干很多事情：

```text
读文件
跑 grep
监听 stdout
等待模型返回
处理用户输入
```

Node.js 的事件循环模型天然就是干这个的。

写起来也很舒服：

```text
await fs.readFile(...)
await execa(...)
await model.stream(...)
```

整个逻辑非常顺。

而且不会像传统多线程那样到处锁来锁去。

* * *

### 前端开发者太多了

这是一个经常被忽略的原因。

如果今天你做一个 Agent 项目。

你希望谁来贡献代码？

```text
Go 开发者
Rust 开发者
还是前端开发者？
```

答案很明显。

全世界 JS/TS 开发者数量实在太夸张了。

尤其 AI 爆发以后。

很多最早接触 Claude、Cursor、ChatGPT API 的人，本来就是前端工程师。

于是出现一个现象：

```text
Agent 用户是前端
Agent 作者也是前端
Agent 贡献者还是前端
```

最后自然越来越多项目选择 TS。

因为社区最大。

招人最容易。

贡献者最多。

* * *

### MCP 基本就是 Node.js 的主场

还有一个现实原因。

MCP 生态几乎是 Node.js 先起飞的。

很多官方示例：

```text
Filesystem
GitHub
Slack
Notion
Postgres
Browser
```

最早都是 TypeScript 版本。

很多开发者第一次写 MCP Server 时：

```text
npm create ...
```

就直接开始了。

于是整个生态逐渐形成正反馈：

```text
MCP 多
↓
Agent 用 Node
↓
插件更多
↓
更多 Agent 用 Node
```

* * *

### Node.js 的跨平台体验确实好

对于 Coding Agent 来说。

最重要的一件事：

```text
Windows
Mac
Linux
都能跑
```

而 Node.js 在这方面体验确实很好。

安装：

```text
node
npm
npx
```

几乎人人都有。

很多 Agent 甚至直接：

```text
npx xxx
```

就启动了。

用户门槛极低。

这一点对于开源项目特别重要。

* * *

### 那为什么还有人选 Go 和 Rust？

因为 Node.js 也不是没有缺点。

比如：

### Go

优势：

```text
单文件发布
内存占用低
启动快
部署方便
```

像 Crush 这种项目。

发布一个二进制文件。

用户下载就能跑。

体验非常好。

* * *

### Rust

优势：

```text
性能高
资源占用低
安全性好
```

像 Codex CLI。

从工程角度看确实非常优雅。

尤其未来 Agent 越来越复杂以后。

Rust 的优势可能会越来越明显。

* * *

### 未来会不会变？

我觉得会。

但不是马上。

今天的 Agent 领域有点像 2015 年的前端。

大家最关心的是：

```text
功能够不够快
迭代够不够快
生态够不够大
```

而不是：

```text
性能是不是极致
内存是不是最省
```

在这种阶段。

Node.js 的优势非常明显。

所以我们看到：

```text
Claude Code
OpenCode
Reasonix
```

这些项目大多选择了 TS/Node.js。

这不是因为 Node.js 最强。

而是因为它最符合当前 Agent 的工程现实。

* * *

### 如果你想研究 Claude Code 到底是怎么实现的

最近我做了一个开源项目：

**build-claude-code**

目标非常简单：

> 从零开始，一步一步实现一个 Claude Code。  

不是讲概念。

而是真正拆解：

```text
Agent Loop
Tool Call
Context 管理
压缩机制
错误恢复
Provider 适配
MCP 集成
权限系统
```

尽量用最容易理解的方式，把 Claude Code 背后的核心设计讲清楚。

项目地址：

[https://github.com/OPBR/build-claude-code](https://link.zhihu.com/?target=https%3A//github.com/OPBR/build-claude-code)

同时我还配套写了一系列公众号文章，会持续更新实现过程和设计思考。

如果你：

-   对 AI Coding Agent 感兴趣
-   想看懂 Claude Code 的设计
-   想自己实现一个 Agent
-   想从“会用 AI”进阶到“会造 AI 工具”

欢迎来看看。

觉得有帮助的话，也欢迎点个 Star ⭐ 支持一下。