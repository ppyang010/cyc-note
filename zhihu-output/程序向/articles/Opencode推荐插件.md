---
id: "1997105479244067641"
title: "Opencode推荐插件"
author: "靳伟"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/1997105479244067641"
created: "2026-01-21 00:44"
updated: "2026-01-22 23:36"
collected: "2026-01-21 00:44"
downloaded: "2026-08-16"
---
假使你不使用anthropic家的大模型，那么使用claude code还不如直接用opencode。

opencode的插件生态也很繁荣，除了非常全能的 \`oh-my-opencode\` (OmO) 和superpowers之外，以下是目前社区中口碑极高、能显著提升“AI 代理”开发体验的插件推荐：

PS: 很多人使用windows安装superpowers失败, 看这里: [opencode can't start after install superpowers in win11 · Issue #256 · obra/superpowers](https://link.zhihu.com/?target=https%3A//github.com/obra/superpowers/issues/256%23issuecomment-3750433383)

  

\---

1\. 流程与安全类（Workflow & Safety）

**opencode-worktree (强烈推荐)**

AI 代理在修改代码时偶尔会搞乱你的本地分支。这个插件会自动为 AI 任务创建 Git Worktree。它在一个独立的临时目录中运行，完成后自动合并或清理，确保你的主工作区永远是干净的。

**opencode-pty**

默认情况下，很多 AI Agent 无法处理需要交互的终端命令（如 \`y/n\` 确认）。这个插件为 OpenCode 注入了伪终端（PTY）支持，让 AI 能够运行交互式脚本并在后台监听进程输出，极大地增强了它自动化部署和测试的能力。

  

**2\. 深度上下文与智能类（Intelligence & Context）**

  

**opencode-supermemory**

AI 往往只有短时记忆。该插件集成了向量数据库，可以将你过去所有 OpenCode 会话的对话历史和决策逻辑索引化。当你在新项目提问时，它能检索出“你之前是如何处理类似架构问题的”，实现跨项目的经验继承。

**opencode-type-inject**

如果你在写 TypeScript 或 Svelte，这个插件是刚需。它会在 AI 读取文件前，自动利用 LSP 提取相关的类型定义并注入到 Prompt 中，避免 AI 因为看不见 \`node\_modules\` 里的复杂类型而写出垃圾代码。

**opencode-morph-fast-apply**

针对大型文件的修改，传统的“全量重写”非常耗费 Token 且缓慢。它利用了 Morph API 的流式局部更新技术，让代码修改速度提升 10 倍以上，且极大地降低了 API 费用。

  

**3\. 自动化与外部能力类（Automation & MCP）**

  

**opencode-browser (基于 Playwright)**

让你的 CLI 代理拥有“眼睛”。如果你在调试前端 UI 或需要抓取文档，它可以让 AI 启动一个无头浏览器进行截图、点击和分析。这在调试复杂的 OAuth 回调或 SSR 问题时非常有用。

**opencode-arise**

这是一个影子军团插件。它允许 OpenCode 充当“君主”，派生出多个轻量级的从属代理（Shadow Agents）并行处理任务（比如一个写后端，一个写测试，一个写文档），大幅缩短大型任务的等待时间。

  

**4\. 辅助与体验类（Utilities）**

  

**opencode-notificator**

当 AI 在跑一个长达 5 分钟的重构任务时，你可能会去喝杯咖啡。这个插件会在任务完成或需要你“授权执行命令”时，发送系统级桌面通知（甚至是手机通知）。

**@plannotator/opencode**

在执行复杂任务前，AI 会列出一个 Plan。这个插件提供了一个可视化的 UI 界面（在终端内或侧边栏），让你能像审阅 PR 一样逐条批注、修改 AI 的计划，比纯文本交互直观得多。

  

补充：

在 2026 年的 OpenCode 生态中，**Context（上下文）管理**是区分“初级用户”和“高阶开发者”的分水岭。随着项目规模扩大，Token 消耗过快或上下文污染（AI 被旧的调试日志干扰）是常见痛点。

除了 `opencode-supermemory`，以下是目前公认最强的上下文管理与压缩插件：

* * *

### 1\. `opencode-dcp` (Dynamic Context Pruning) —— **最推荐**

这是由 `tarquinen` 开发的“动态上下文裁剪”插件，是目前管理长对话的首选。

-   **核心功能**：它为 AI 提供了一个 `discard`（丢弃）和 `extract`（提取）工具。
-   **它是如何工作的**：

-   **自动清理**：AI 在运行一系列测试或读取大量文件后，可以主动调用 `discard` 来删除那些“已经完成任务”的工具输出（比如 500 行的测试报错日志），只留下结论。
-   **上下文蒸馏**：通过 `extract`，它可以命令另一个轻量级模型（如 Gemini 1.5 Flash 或 GPT-4o-mini）将过去 50 个回合的对话总结为 500 个字的关键决策记录，然后清空原始历史。

-   **安装**：`opencode plugin add @tarquinen/opencode-dcp`

### 2\. `opencode-skillful` —— **按需加载插件**

AI 有时会因为加载了太多的“系统提示词”或“操作指南”而浪费大量初始 Token。

-   **核心功能**：它将复杂的 Prompt 碎片化为“技能”。
-   **优势**：默认情况下上下文是空的，只有当 AI 识别到任务（比如“现在需要进行 Docker 部署”）时，它才会动态“注入”相关的专业知识和规则。这能节省约 **20%-40%** 的静态上下文空间。

  

### 3\. `mem0` (via MCP/Plugin) —— **长期记忆层**

相比于 Supermemory，`mem0` 更倾向于“用户偏好”和“事实”的提取。

-   **场景**：它可以记住“用户讨厌使用 class 组件，更倾向于 hooks”或“项目中数据库连接池的超时设置是 30s”。
-   **管理方式**：这些信息以 KV 对形式存储，只有在相关搜索命中时才极简地插入上下文，而不是作为一个庞大的文档库。

* * *

### 5\. 进阶：改 OpenCode 原生配置文件（无需额外插件）

很多用户不知道 OpenCode 在 2026 版本中已经内置了强大的自动压缩（Compaction）逻辑。你可以在 `~/.config/opencode/opencode.json` 中优化这些参数：

Code snippet

```text
{
  "compaction": {
    "auto": true,           // 开启自动压缩
    "strategy": "summarize", // 压缩策略：可选择 summarize（总结）或 prune（直接裁剪）
    "threshold": 0.8,       // 当上下文占用到 80% 时触发
    "prune_tool_outputs": true // 优先清理工具执行的冗余输出
  },
  "cache": {
    "provider": "auto", 
    "enabled": true
  }
}
```

* * *