---
title: "AI Agent 学习路线"
aliases:
  - "有没有完整的AI Agent学习路线推荐?"
author:
  - "小林coding"
  - "程序员吴师兄"
source:
  - "https://www.zhihu.com/question/1979245388159537776/answer/2050883508709729088"
  - "https://www.zhihu.com/question/1979245388159537776/answer/2029860455544513217"
site: "知乎"
created: 2026-11-26
summary_model: "gpt-6.2-sol"
tags:
  - 阅读笔记
  - AI智能体
  - 学习路线
  - RAG
---

# AI Agent 学习路线

两份材料来自同一个知乎问题。程序员吴师兄给出四阶段的工程实践顺序，小林coding 提供可按阶段配合阅读的面试题目录。总结模型为 `gpt-6.2-sol`。

- 小林coding，2026 年 6 月 18 日发布。[知乎原回答](https://www.zhihu.com/question/1979245388159537776/answer/2050883508709729088)
- 程序员吴师兄，2026 年 4 月 21 日发布。[知乎原回答](https://www.zhihu.com/question/1979245388159537776/answer/2029860455544513217)

## 目录

- [[#按阶段对照学习]]
- [[#工程实践要点]]
  - [[#工具、记忆和链路追踪]]
  - [[#用数据说明项目效果]]
- [[#面试材料入口]]
- [[#原文剪藏]]
  - [[#小林coding的回答]]
    - [[#大模型面试题：4 大专题，74 道题全部列给你]]
      - [[#一、Agent 面试题（16 题 · 158 张图 · 6.4 万字）]]
      - [[#二、RAG 面试题（20 题 · 142 张图 · 6 万字）]]
      - [[#三、LLM 工具调用面试题（16 题 · 127 张图 · 4.6 万字）]]
      - [[#四、大模型工程面试题（22 题 · 188 张图 · 8.1 万字）]]
    - [[#进阶专栏：图解 Agent & 图解 Claude Code]]
      - [[#图解 Agent：吃透 AI 智能体的前沿与底层（6 篇万字长文）]]
      - [[#图解 Claude Code：从源码到实战，吃透最强编程 Agent（10 篇）]]
        - [[#源码解析（6 篇）]]
        - [[#实战技巧（4 篇）]]
    - [[#这份面试题合集适合谁？怎么搭配看？]]
    - [[#常见问题 FAQ]]
    - [[#结语]]
  - [[#程序员吴师兄的回答]]
    - [[#第一阶段：搞懂 Agent 的底层机制]]
    - [[#第二阶段：LangGraph 专项突破]]
    - [[#第三阶段：核心模块的工程深度]]
    - [[#第四阶段：做一个有数据的项目]]
    - [[#一个容易踩的坑]]
    - [[#最后，再给大家送上点干货！]]

## 按阶段对照学习

顺序取自程序员吴师兄的回答。表中的阅读主题来自小林coding 的题集，练习验收项根据两篇回答整理。

| 阶段 | 动手练习 | 搭配阅读 | 怎样判断练会了 |
| --- | --- | --- | --- |
| 1. 手写最小 Agent | 直接调用模型 API，解析 Function Calling 返回，调用本地工具，把结果放回消息。观察 ReAct 循环中的反复重试、上下文增长和提前结束。 | Agent 架构、Workflow 与 Agent、ReAct、手写 Agent、Function Calling | 能追踪一次从模型发出工具请求到读取工具结果的完整过程，并说明循环在哪里停止。 |
| 2. 用 LangGraph 编排 | 定义 `State`、`Node` 和 `Edge`。用条件边决定调用工具、重试或结束，用 Checkpointer 保存和恢复运行状态。 | Agent 工作流、任务拆分、ReAct 与 Plan-and-Execute 的区别 | 能演示成功、失败重试和中断后恢复，并解释每条分支的进入条件。 |
| 3. 补齐工程能力 | 完善工具参数描述和返回结构，按用途拆分会话记忆、跨会话记忆与知识库，给节点和工具调用加追踪。 | 工具调用专题、Agent 记忆专题、RAG 文档处理与检索 | 给出一条失败记录，能追到对应节点、工具输入输出和消耗的 Token。 |
| 4. 做一个可评估的项目 | 用一组有标准答案的题目先测基线，再针对失败类型改进。吴师兄以 Text2SQL 为例。 | RAG 效果评估、Agent 的规划与反思、模型评测 | 能拿同一批题目对照改进前后的完成率、工具调用和耗时。 |

## 工程实践要点

### 工具、记忆和链路追踪

- **工具定义**写清用途、使用条件、参数类型、范围和枚举值。应用代码负责执行调用，将结构化结果交回模型。
- **记忆分层**保留当前会话的近期消息，将跨会话记忆按相关度和时间检索，再用独立的 RAG 知识库管理系统文档。逐层明确何时写入、怎样读回。
- **链路追踪**用同一个 `trace ID` 串起节点进出状态、带时间戳的工具输入输出和模型消耗的 Token。吴师兄举的工具是 LangSmith。

### 用数据说明项目效果

Text2SQL 可以用 SQL 执行结果核对答案。吴师兄建议记录三项指标。

- **任务完成率**。在评估样本中，SQL 能执行且结果正确的比例。
- **工具调用准确率**。检查该调的工具有没有遗漏，以及是否发生多余调用。
- **平均耗时**。以同一组样本比较优化前后的时间开销。

原文举了一个 Spider 数据集上的项目描述，准确率从 61% 提升到 79%，改动包括改进表和字段匹配，以及增加 SQL 执行失败后的修正节点。复盘时可沿用这个写法，交代基线、具体改动和评估结果。

吴师兄建议先把单 Agent 做到可评估、可排障，再练多 Agent 的状态同步、消息格式和部分失败处理。

## 面试材料入口

小林coding 的回答列出了 74 道题。面向 AI 应用开发，作者在备考建议中将 Agent、RAG 和工具调用作为主线。大模型工程专题更侧重算法、推理和模型自研，应用方向可选读采样、提示词、幻觉、缓存与部署。

| 专题 | 题数 | 重点 | 目录 |
| --- | ---: | --- | --- |
| Agent | 16 | 架构、任务拆分、ReAct、规划、记忆与多 Agent 协作 | [Agent 面试题](https://xiaolinnote.com/ai/agent/agent_info.html) |
| RAG | 20 | 文档切分、向量化、检索、查询改写、召回与评估 | [RAG 面试题](https://xiaolinnote.com/ai/rag/rag_info.html) |
| LLM 工具调用 | 16 | Function Calling、MCP、Skill、A2A、流式传输与网关 | [LLM 工具调用面试题](https://xiaolinnote.com/ai/tools/tools_info.html) |
| 大模型工程 | 22 | Transformer、训练与对齐、采样、缓存、量化和推理部署 | [大模型工程面试题](https://xiaolinnote.com/ai/llm/llm_info.html) |

原回答还收录了 6 篇《图解 Agent》和 10 篇《图解 Claude Code》的目录，按主题可查 Agent 基础、Loop 与 Harness、上下文压缩、记忆和子代理调度。[小林面试笔记总入口](https://xiaolinnote.com/ai/)

## 原文剪藏

### 小林coding的回答

如果你在准备AI 大模型/AI Agent开发岗面试，先把这套面试题收藏好了：

> **小林面试笔记： [https://xiaolinnote.com](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/)** 专注 AI Agent 开发方向的面试题网站，图解 Agent + RAG + LLM 面试题，让一部分人先跑赢 AI Agent 开发面试。

为什么值得你专门收藏一个网站？我先把家底亮出来——这套 **大模型面试题** 目前已经沉淀了：

- **74 道** 大厂真实高频面试题（Agent / RAG / 工具调用 / 大模型工程）
- ️ **615 张** 纯手绘图解，复杂原理一张图看懂
- ✍️ **25 万+字** 详细答案解析，每题都讲到能自己推导
- **全部免费** ，且每月持续更新，紧跟 MCP、A2A 等新协议

而且每一道题都做了四件别的八股不会做的事： **题目全部来自字节、阿里、腾讯等大厂真实面经** 、开头先来一段「面试翻车现场」让你感受踩雷体验、复杂架构全部配手绘图解 **、** 从根子上把原理讲透——不是让你背答案，而是面试官怎么换着问你都能推出来。

![](https://pica.zhimg.com/50/v2-42eabd2d40be156fc24bf282ea422beb_720w.jpg?source=2c26e567)

AI大模型面试题汇总：Agent面试题、RAG面试题、Transformer面试题

#### 大模型面试题：4 大专题，74 道题全部列给你

进入 2026，AI 岗面试的重心已经从「大模型基础」快速转向「AI 应用落地」， **大模型面试题、Agent 面试题、AI 应用开发面试题** 成了应届和社招必刷的三大方向。下面 4 大专题的题目我全部列出来，点开任意一题都是一篇完整图解长文。

![](https://pica.zhimg.com/50/v2-774298abe8a09ab5ef5a090853ddb56c_720w.jpg?source=2c26e567)

大模型面试题：4 大专题，74 道题全部列给你

##### 一、Agent 面试题（16 题 · 158 张图 · 6.4 万字）

> 专题介绍与完整目录： [Agent 面试题介绍页](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/agent_info.html)

2026 最火的方向，也是 **Agent 面试题** 问得最深的一块。开放题「让你设计一个客服 Agent，任务怎么拆？记忆怎么存？工具调用失败怎么兜底？」全靠这 16 道题打底。

![](https://pic1.zhimg.com/50/v2-93b5e8249fd08bfff2540b9e7bea33c9_720w.jpg?source=2c26e567)

Agent 面试题（16 题 · 158 张图 · 6.4 万字）

- [1\. 什么是 Agent？与大模型有什么本质不同？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/1_whatisagent.html)
- [2\. Agent 的基本架构由哪些核心组件构成？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/2_components.html)
- [3\. Workflow，Agent，Tools 这三个的概念和区别介绍一下？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/3_workflow_tools.html)
- [4\. 了解哪些其他的 Agent 设计范式？Agent 和 Workflow 的区别是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/4_patterns.html)
- [5\. Agent 推理模式有哪些？ReAct 是啥？具体是怎么实现的？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/5_react.html)
- [6\. ReAct、Plan-and-Execute、Reflection 三种范式有什么核心区别？实际项目中该如何选型？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/6_three_patterns.html)
- [7\. 复杂任务怎么做的任务拆分？为什么要拆分？效果如何提升？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/7_tasksplit.html)
- [8\. 请你介绍一下 AI Agent 的记忆机制，并说明在实际开发中应该如何设计记忆模块？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/8_memory.html)
- [9\. Agent 的长短期记忆系统怎么做的？记忆是怎么存的？粒度是多少？怎么用的？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/9_memory_storage.html)
- [10\. 什么是 Multi-Agent？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/10_multiagent.html)
- [11\. 说说 Single-Agent 和 Multi-Agent 的设计方案？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/11_single_multi.html)
- [12\. Agent 记忆压缩通常有哪些方法？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/12_memcompress.html)
- [13\. 在工程实践中，为什么有时候选择「手搓」Agent，而不是直接用成熟框架？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/13_handcode.html)
- [14\. 如何赋予 LLM 规划能力？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/14_planning.html)
- [15\. 讲讲 Agent 的反思机制？为什么要用反思？具体怎么实现？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/15_reflection.html)
- [16\. 如何设计多 Agent 的协作与动态切换机制？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/agent/16_collab.html)

##### 二、RAG 面试题（20 题 · 142 张图 · 6 万字）

> 专题介绍与完整目录： [RAG 面试题介绍页](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/rag_info.html)

RAG 是 Agent 面试题与 AI 应用开发面试题的共同基础，几乎每家大厂必问，建议第一个吃透。这 20 道把 RAG 从原理到线上落地完整过一遍。

![](https://pica.zhimg.com/50/v2-901ef9343a139d992e0a50c3413fed58_720w.jpg?source=2c26e567)

RAG 面试题（20 题 · 142 张图 · 6 万字）

- [1\. 什么是 RAG？详细描述一个完整 RAG 系统的详细工作流程？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/1_whatisrag.html)
- [2\. 大模型的 RAG 主要用来解决什么问题？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/2_rag_problems.html)
- [3\. 相比直接微调 LLM，RAG 解决了什么问题？微调和 RAG 各自的优劣势是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/3_rag_vs_finetune.html)
- [4\. RAG 中的文档是怎么存的？粒度是多大？详细说说文档切割（Chunking）策略？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/4_chunking.html)
- [5\. 怎么规避语义被切割掉的问题？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/5_semantic_cuts.html)
- [6\. 在 RAG 中 Embedding 究竟是什么？如何选择和评估一个 Embedding 模型？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/6_embedding.html)
- [7\. Embedding 有哪几种算法你了解过吗？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/7_embedding_algos.html)
- [8\. 什么是向量数据库？有没有做过向量数据库的对比选型？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/8_vectordb.html)
- [9\. 讲讲你用的向量数据库？数据量级是多大？性能如何？遇到过性能瓶颈吗？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/9_vectordb_practice.html)
- [10\. 你使用 RAG 给大模型一个输入，系统是怎样的工作流程？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/10_online_workflow.html)
- [11\. 请你介绍一下向量检索和关键词检索的区别？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/11_retrieval_types.html)
- [12\. 如何润色用户的 Query（Query Rewrite）？目的是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/12_query_rewrite.html)
- [13\. 什么是多路召回？具体怎么做？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/13_multi_retrieval.html)
- [14\. RAG 检索优化策略有哪些？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/14_retrieval_opt.html)
- [15\. 了解哪些更复杂的 RAG 范式？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/15_advanced_paradigms.html)
- [16\. 在什么场景下，你会选择使用图数据库来增强传统的向量检索？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/16_graph_db.html)
- [17\. 如何规避 RAG 系统中大模型的幻觉？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/17_hallucination.html)
- [18\. 怎么量化你的 RAG 效果？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/18_evaluation.html)
- [19\. RAG 知识库如何实现动态与持续更新？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/19_dynamic_update.html)
- [20\. 在实际落地中，你觉得 RAG 最难的地方是哪里？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/rag/20_hardest_parts.html)

##### 三、LLM 工具调用面试题（16 题 · 127 张图 · 4.6 万字）

> 专题介绍与完整目录： [LLM 工具调用面试题介绍页](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/tools_info.html)

这是 **AI 应用开发面试题** 的核心场景。2026 一线大厂已经把 MCP 写进 JD，Function Calling 的 Schema 设计、工具调用失败重试、SSE 与 WebSocket 选型答不好，送分题就成了送命题。

![](https://picx.zhimg.com/50/v2-684d02da0f533f138ce1a58eab9c2bc2_720w.jpg?source=2c26e567)

LLM 工具调用面试题（16 题 · 127 张图 · 4.6 万字）

- [1\. 什么是 Function Calling？原理是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/1_function_calling.html)
- [2\. LLM 是如何学会调用外部工具的？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/2_llm_tool_learning.html)
- [3\. 大模型的 Function Call 能力是怎么训练出来的？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/3_fc_training.html)
- [4\. 什么是 MCP（模型上下文协议）？讲讲它的核心内容？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/4_what_is_mcp.html)
- [5\. MCP 由哪几部分组成？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/5_mcp_components.html)
- [6\. MCP 和 Function Calling 有什么区别？有没有实际跑过 MCP？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/6_mcp_vs_fc.html)
- [7\. Function Calling 也属于工具调用，请问什么场景下使用 Function Calling，什么场景下使用 MCP？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/7_fc_vs_mcp_usage.html)
- [8\. 为什么有些特定的推理模型不支持 MCP 协议？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/8_reasoning_no_mcp.html)
- [9\. Skill 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/9_skill.html)
- [10\. MCP 和 Agent Skill 的区别是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/10_mcp_vs_skill.html)
- [11\. Function Calling、Skill、MCP 这三个有什么区别？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/11_fc_skill_mcp.html)
- [12\. 什么是 A2A 协议？它和 MCP 协议的区别是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/12_a2a_protocol.html)
- [13\. MCP 协议通常采用什么通信方式？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/13_mcp_transport.html)
- [14\. 说说 WebSocket 和 SSE 通信的区别及局限性？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/14_sse_vs_websocket.html)
- [15\. 为什么要用 WebRTC 协议？它和 WebSocket 在 AI 对话流中的核心差异是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/15_webrtc_vs_ws.html)
- [16\. 有没有用过大模型的网关框架？网关层解决了什么问题？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/tools/16_llm_gateway.html)

##### 四、大模型工程面试题（22 题 · 188 张图 · 8.1 万字）

> 专题介绍与完整目录： [大模型工程面试题介绍页](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/llm_info.html)

**大模型面试题** 的工程深水区，P6+ 算法岗与推理工程岗的高频加试。专门聚焦「模型在生产环境为什么跑不快、跑不稳、跑不省成本」这类高阶追问。

![](https://picx.zhimg.com/50/v2-d15bc56231634afce919b657a8a3f975_720w.jpg?source=2c26e567)

大模型工程面试题（22 题 · 188 张图 · 8.1 万字）

- [1\. 什么是大语言模型？和传统 NLP 模型有什么区别？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/what_is_llm.html)
- [2\. 讲讲 Transformer 架构基本原理？Encoder 和 Decoder 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/transformer_architecture.html)
- [3\. 多头注意力（MHA）有哪些局限？MQA、GQA、Flash Attention 怎么解决？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/mha_mqa_gqa_flash_attention.html)
- [4\. 大模型的位置编码是干什么用的？sin/cos、RoPE、ALiBi 有什么区别？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/position_encoding.html)
- [5\. 什么是大模型项目的分词器？原理是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/tokenizer.html)
- [6\. 大模型是怎么训练出来的？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/llm_training.html)
- [7\. 什么是 Scaling Law？大模型的「涌现能力」是怎么回事？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/scaling_law_emergence.html)
- [8\. 大模型微调的方案有哪些?](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/finetuning.html)
- [9\. 请讲一下 LoRA 技术，除了减少参数量，它还有哪些优点？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/lora.html)
- [10\. SFT 之后还有哪些 Post-Training？RLHF、DPO、GRPO、拒绝采样什么关系？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/post_training.html)
- [11\. 大模型的 DPO 和 PPO 的区别是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/dpo_vs_ppo.html)
- [12\. 大模型生成文本时的解码策略有哪些？贪心、Beam Search、采样分别什么时候用？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/decoding_strategies.html)
- [13\. 大模型的参数：温度值、Top-P、Top-K 分别是什么？各个场景下的最佳设置是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/temperature_top_p_top_k.html)
- [14\. KV Cache 是什么？Prompt Caching 的原理是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/kv_cache_prompt_caching.html)
- [15\. 大模型量化是什么？INT8/INT4/AWQ/GPTQ 怎么选？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/quantization.html)
- [16\. 如何写好 Prompt？分享下 Prompt 工程实践经验？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/prompt_engineering.html)
- [17\. 什么是 CoT？为啥效果好？它有什么缺点或局限性？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/cot.html)
- [18\. 大模型为什么会出现幻觉？怎么缓解？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/hallucination.html)
- [19\. MoE 混合专家模型是什么？DeepSeek V3、Qwen 为什么用 MoE？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/moe.html)
- [20\. 大模型部署有哪些主流方案？vLLM、TGI、llama.cpp、SGLang 实际项目里怎么选？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/deployment_frameworks.html)
- [21\. 大模型能力评测指标有哪些？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/evaluation_metrics.html)
- [22\. 对比使用过哪些主流大模型？你们项目中最终选用了哪个模型？为什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/llm/model_selection.html)

> 此外还有《LangChain 框架面试题》专题持续更新中。完整大模型面试题入口： [xiaolinnote.com/ai/](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/ai/)

#### 进阶专栏：图解 Agent & 图解 Claude Code

逐题八股能让你「会答题」，但想真正「懂原理」、在面试官连环追问下不慌，还得看这两个 **「一文讲透」** 的图解专栏。和八股不同，这里每篇都是一个主题的万字长文，把来龙去脉、设计取舍、源码细节一次性讲穿——这也是网站和其他面试题站点最不一样的地方。

##### 图解 Agent：吃透 AI 智能体的前沿与底层（6 篇万字长文）

不只是面试题，而是带你看懂当下最火的 Agent 概念、生态与工程方法论。很多内容是全网少有人讲透的前沿话题：

![](https://picx.zhimg.com/50/v2-f2a839b76feb50f9ec818ccdea2d6b3c_720w.jpg?source=2c26e567)

图解 Agent：吃透 AI 智能体的前沿与底层（6 篇万字长文）

- [AI Agent 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/concept/agent.html) ：从 0 讲清 Agent 与 LLM 的本质区别、四大核心模块，以及 MCP / A2A 协议，新手入门第一篇。
- [OpenClaw 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/concept/openclaw.html) ：GitHub 一度霸榜的爆火开源 Agent，扒一遍它到底凭什么火、架构怎么设计。
- [RAG 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/rag/rag.html) ：让大模型不再「一本正经胡说八道」的核心技术，一篇看懂检索增强全流程。
- [GraphRAG 和 LightRAG 详解](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/rag/graphrag-lightrag.html) ：传统 RAG 撞墙之后的两条进阶路线，原理、对比与选型一次说清。
- [Harness Engineering 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/engineering/harness-engineering.html) ：被 OpenAI 官方验证的「让 AI Agent 越用越聪明、不再重复犯错」的工程方法论。
- [Loop Engineering 是什么？](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/agent/engineering/loop-engineering.html) ：Claude Code 作者那句「我的工作就是写 loop」背后，AI 编程从 Prompt 到 Loop 的范式转变。

##### 图解 Claude Code：从源码到实战，吃透最强编程 Agent（10 篇）

Claude Code 源码泄漏的 51 万行代码全网刷屏，越来越多大厂面试开始追问它的实现原理。这个专栏带你 **扒源码 + 练实战** ，是目前少有的成体系的 Claude Code 深度解析。

![](https://pic1.zhimg.com/50/v2-52a2d2b55cd22a98e49939a578fc8de3_720w.jpg?source=2c26e567)

图解 Claude Code：从源码到实战，吃透最强编程 Agent（10 篇）

###### 源码解析（6 篇）

- [源码总览](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_source.html) ：51 万行泄漏代码里的整体架构设计，先建立全局视角。
- [主循环 Query](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_query_loop.html) ：一轮对话到底怎么跑起来的，异步生成器与 fake tool\_result 全讲透。
- [上下文管理](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_compact.html) ：Compact 自动压缩机制，长对话为什么不会爆上下文。
- [代码检索](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_grep.html) ：为什么用 grep 而不用 RAG 检索代码——字节高频面试题。
- [记忆机制](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_memory.html) ：为什么偏偏不上向量数据库，而用 CLAUDE.md + 文件系统。
- [多 Agent 机制](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/source/cc_multi_agent.html) ：SubAgent 怎么拆任务、并发调度与上下文隔离。

###### 实战技巧（4 篇）

- [基础使用技巧](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/playbook/cc_use.html) ：新手入门必学，快速上手少走弯路。
- [/powerup 教程](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/playbook/cc_powerup.html) ：官方内置的 18 个互动课程逐个过一遍。
- [CLAUDE.md 怎么写](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/playbook/cc_claude_md.html) ：项目记忆文件的正确维护姿势，别再堆上千行无效配置。
- [百万行大代码库实战](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/claudecode/playbook/cc_large_codebase.html) ：公司几百万行代码，Claude Code 怎么扛得住。

#### 这份面试题合集适合谁？怎么搭配看？

先记住一条总原则： **做 AI 应用开发，主看 Agent + RAG + LLM 工具调用三大专题；大模型工程面试题偏算法底层、难度更高，应用方向当进阶选看，算法 / 大模型自研方向当主线** 。

- **应届校招（投 AI 应用 / Agent 开发岗）** ：主攻 **Agent 面试题 + RAG 面试题 + LLM 工具调用面试题** ，这三块就能覆盖 90% 的一面二面追问；大模型工程面试题里挑「应用相关」的（采样参数、Prompt、CoT、幻觉、KV Cache、部署选型）选看即可，训练对齐那部分可以先跳过。
- **后端 / 算法转 AI 应用开发** ：已有工程底子，缺的是 AI 落地范式——按 **Agent → RAG → LLM 工具调用（MCP、网关）** 的顺序补，最快补齐应用层短板。
- **AI 应用工程师（社招）** ：把 **Agent + RAG + 工具调用** 三块往深里抠（Multi-Agent 协作、Agent 可观测性、成本与并发、幻觉规避、MCP / 网关治理），冲 P6 / P7 深水区。
- **算法 / 推理 / 大模型开发工程师（非应用层）** ： **大模型工程面试题** 才是你的主战场——Transformer、Flash Attention、RoPE、LoRA、RLHF / DPO / GRPO 对齐、量化、MoE、推理部署这些底层硬骨头，难度最高，是算法岗与大模型自研岗的核心考点；Agent 与 RAG 作为加分项。

#### 常见问题 FAQ

**AI 应用开发面试主要考什么？** 主要考三块： **Agent** （架构、ReAct、任务拆分、记忆、Multi-Agent 协作）、 **RAG** （切割、Embedding、向量库、检索优化、Rerank）、 **LLM 工具调用** （Function Calling、MCP、A2A、网关治理）。这三块对应网站的 Agent / RAG / 工具调用三大专题，是应用方向的必刷重点。

**大模型工程面试题难吗？应用开发同学要看吗？** 偏难，更偏算法底层（Transformer、Flash Attention、RoPE、LoRA、RLHF/DPO/GRPO、量化、MoE）。它更适合 **算法 / 推理 / 大模型自研** 方向的同学当主线；应用开发同学当进阶，挑「应用相关」的（采样参数、Prompt、CoT、幻觉、KV Cache、部署选型）选看即可。

**大模型面试题和算法面试题有什么区别？** 算法题考数据结构与系统设计，偏通用基础；大模型面试题聚焦 Transformer、注意力机制、训练推理优化、对齐方式等 LLM 专属知识。大厂 AI 岗两类都考，权重随岗位倾斜。

**没有大模型项目经验，能学 Agent 面试题吗？** 能。Agent 面试题的核心是工程思维（任务拆分、记忆机制、工具调用、失败处理），配合网站的图解和代码示例就能掌握，建议再搭一个 MVP 级 Agent Demo 写进简历。

**这套大模型面试题要刷多久？怎么安排？** 应用方向 1 个月足够：先 Agent，再 RAG，最后工具调用；每道题按「先看面试翻车现场 → 再看图解原理 → 合上网页自己复述」三步走，比死记硬背高效得多。

**网站内容免费吗？会持续更新吗？** 全部免费。题目每月更新，紧跟大厂 JD 与新协议（MCP、A2A、Skills、AG-UI 等），建议直接收藏 [xiaolinnote.com](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/) 随用随查，春招提前 2 个月开始系统刷题。

#### 结语

以上就是 2026 年最新的 **大模型面试题、Agent 面试题、AI 应用开发面试题** 三大方向合集。建议直接收藏网站作为面试备战主入口，随用随查：

> **小林面试笔记： [https://xiaolinnote.com](https://link.zhihu.com/?target=https%3A//xiaolinnote.com/)** —— 大厂新题、新协议（MCP、A2A、AG-UI 等）第一时间更新，助你在 AI 岗招聘季跑赢多数候选人。

### 程序员吴师兄的回答

**先给个结论：网上流传的 Agent 学习路线，大多数是错的，不是内容错，是顺序错。**

几乎所有路线都从”学框架”开始： **先 LangChain，再 LangGraph，然后 AutoGen，最后做个 demo。结果就是学了一堆 API，但搭出来的东西一遇到真实场景就崩，因为你根本不知道它为什么会崩，也不知道怎么让它不崩。**

正确的学习顺序应该反过来： **先搞懂 Agent 在工程上会坏在哪里，再去学怎么用框架把这些坑填上。**

#### 第一阶段：搞懂 Agent 的底层机制

这个步骤不要跳过。

很多人急着上手框架，这一步就跳了，然后后面卡死在各种莫名其妙的问题上。

需要搞清楚三件事：

**Function Calling 到底是怎么工作的。** LLM 不是真的在”调用”工具，它只是根据你给的 [schema](https://zhida.zhihu.com/search?content_id=778339383&content_type=Answer&match_order=1&q=schema&zhida_source=entity) 描述，输出了一段 JSON。你的代码解析这个 JSON，去调真实的函数，把结果塞回对话，模型再继续。整个过程里，模型完全依赖你写的 schema 描述来理解每个工具的用途和参数。描述写得含糊，模型就传错参数；参数类型没说清楚，模型就传错类型。这不是玄学，是工程问题。

**[ReAct 循环](https://zhida.zhihu.com/search?content_id=778339383&content_type=Answer&match_order=1&q=ReAct+%E5%BE%AA%E7%8E%AF&zhida_source=entity) 是什么，以及它在哪里会出问题。** 现代 Agent 框架底层几乎都是 ReAct：Thought（我要干什么）→ Action（调工具）→ Observation（看结果）→ 再 Thought。知道这个循环之后，你才能理解 Agent 的常见失败模式、死循环（一直 Observation 不满意，一直重试）、Context 爆炸（循环轮次太多，历史塞满上下文）、早停（模型在还没拿到关键信息时就判断”任务完成”）。

**Token 和 Context Window 的物理限制。** Agent 的 Context 不是无限的。GPT-4o 的 context window 是 128k token，Qwen 系列不同版本在 8k 到 128k 之间。一个 ReAct 循环跑 10 轮，每轮塞进 Thought + Action + Observation，很快就能把 context 吃满。吃满之后发生什么？模型开始”遗忘”早期的内容，行为变得不可预测。这就是为什么 Memory 管理是 Agent 工程的核心问题之一。

这三件事，不需要读论文，自己动手写一个 50 行的最小 Agent，不用框架，直接调 OpenAI API，手动解析 function calling 的返回，手动拼 messages 数组，花一个下午就能把这些机制摸清楚。这 50 行代码比很多教程值钱。

#### 第二阶段：LangGraph 专项突破

为什么推荐 LangGraph 而不是 LangChain？

LangChain 是工具集合，功能很全，但过于灵活，没有强制你思考流程的状态和边界条件。LangGraph 把 Agent 的执行过程建模成一张有向图——Node 是处理逻辑，Edge 是跳转条件，State 是贯穿整个流程的数据容器。这个抽象迫使你在写代码之前先想清楚：这个 Agent 有哪些状态？从 A 节点到 B 节点的条件是什么？失败了应该跳回哪里？

这种强迫症式的设计思路，正是生产级 Agent 需要的。

LangGraph 的学习顺序建议是这样的：

先理解 StateGraph 的三要素：State 定义（用 TypedDict，明确每个字段的类型和用途）、Node（纯函数，输入 State，输出更新后的 State）、Edge（普通边和条件边）。把这三个东西搞清楚，LangGraph 90% 的能力就解锁了。

然后重点研究条件边（Conditional Edge）的写法。条件边是 Agent 产生”智能”的地方，模型判断任务是否完成、是否需要重试、应该调用哪个工具，都在这里体现。很多教程跳过这一块，但这恰恰是面试里最常问的。

最后是 Checkpointer 机制，也就是状态的持久化。Agent 跑到一半崩了怎么办，用户中途断开了怎么处理，这些是生产场景里必须面对的问题，LangGraph 的 Checkpoint 就是为了解决这个。搞懂它之后，”Agent 的容错和恢复”这个面试题你就有话说了。

#### 第三阶段：核心模块的工程深度

只会 LangGraph 还不够，面试官会往下挖三个模块：

**Tool 设计。** 不只是会接入 API，而是知道怎么设计 schema 让模型用对工具。一个好的工具描述应该包含：这个工具能做什么（一句话）、什么情况下应该用它（使用场景）、参数说明（类型、取值范围、示例值）。参数里如果有枚举值，一定要把所有合法值列出来，不要让模型自由发挥。工具调用的结果也要设计好结构，返回一大段自然语言，模型很难从里面提取关键信息；返回结构化的 JSON，模型处理起来更稳定。

**Memory 分层。** 这是最容易拿到加分的模块，因为大多数人的实现就是把对话历史塞进 context，面试官一问就露馅了。生产级的 Memory 需要区分三层：当前会话的短期记忆（最近 N 轮，直接在 messages 里）、跨会话的长期记忆（向量数据库存储，检索时按语义相关度 + 时间衰减排序）、系统级知识（RAG，知识库文档，和用户的个人记忆分开管理）。能把这三层画出来，说清楚每层的读写策略，面试里就已经超过大多数人了。

**可观测性。** Agent 出了问题你怎么定位？这个问题大多数人答不上来，因为他们的 Agent 根本没有日志，或者日志全是 print 语句。生产环境里需要记录的最低限度：每次工具调用的输入输出（带时间戳）、每个 Node 的进出状态（带 trace ID，方便串联一次完整的 Agent 执行链路）、模型调用的 token 消耗（成本控制的基础）。LangSmith 是 LangGraph 官方的可观测性工具，学 LangGraph 的同时把 LangSmith 配上，这个习惯值很多钱。

#### 第四阶段：做一个有数据的项目

这一阶段是大多数路线里缺失的，但它决定你能不能通过面试。

学到第三阶段之后，很多人的状态是：概念都懂，能跑通 demo，但一问”你做的 Agent 效果怎么样”就卡住了，因为没有评估，不知道效果怎么样。

需要做的事情是：选一个有 [ground truth](https://zhida.zhihu.com/search?content_id=778339383&content_type=Answer&match_order=1&q=ground+truth&zhida_source=entity) 的场景（比如 Text2SQL，输入自然语言问题，输出 SQL，结果对不对是可以精确判断的），搭一个 Agent，然后跑评估。评估指标至少要有：任务完成率（SQL 能执行且结果正确的比例）、工具调用准确率（有没有冗余调用或遗漏调用）、平均耗时。

然后做优化，把指标从基线往上推，记录每次优化的手段和效果。这个过程就是你简历上的项目，也是面试时能讲 30 分钟的素材。

一个我见过的有说服力的项目描述是这样的：”基于 LangGraph 构建了一个 Text2SQL Agent，在 Spider 数据集上从基线的 61% 准确率优化到 79%，主要手段是改进了 schema linking 的工具设计和增加了 SQL 执行失败后的反思-修正节点。”这种描述，面试官能顺着追问十个方向，你每个方向都有话说。

#### 一个容易踩的坑

Multi-Agent 不是越早学越好。很多路线把 Multi-Agent 放得很靠前，但实际上，如果你连单 Agent 的 Memory 管理和错误处理都没搞清楚，上 Multi-Agent 只会让问题指数级复杂。两个 Agent 之间的状态同步、消息传递格式、循环依赖、部分失败的处理——这些问题，在单 Agent 没吃透之前，上手就是陷阱。

把单 Agent 做到能量化评估、能定位问题、能优化指标，再去碰 Multi-Agent，这个顺序不会错。

参考阅读： [mp.weixin.qq.com/s/aG6l](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/aG6lFCzu9uEE7aZq-5mg8Q)

#### 最后，再给大家送上点干货！

关于 RAG 系列，我写了很多高质量的原创文章，建议大家 **点赞&收藏** ，Mark住别丢了。

1、 [面试官问：RAG有哪些优化手段？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/KCxwaLtkMW_auOdJYgRt9A)

2、 [面试官问：LLM 到底能不能自己做规划？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/_WTjjSCKssTd20lBoGzycQ)

3、 [面试官问：RAG 的知识库是怎么构建的？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/D9OMXg05KSfzlrOsNu5zog)

4、 [面试官问：RAG 的检索模块是怎么优化的？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/pcnA8rP4mieKx-PpvD1oww)

5、 [面试官问：RAG 的生成模块是怎么设计的？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/rExFJyth3zzcRYhxPT81rA)

6、 [面试官问：RAG 的 Query 理解模块是怎么做的？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/hAqLa-OvAqpYVrKOQHWZ7w)

7、 [面试官问：你们的 RAG 系统是怎么评估的？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/ewxnJ_sVwhbps2jOGaE7bQ)

8、 [如何写一个有深度RAG项目经历](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/WUMza9Ta1L7hF7x6NNcW-Q)

9、 [面试官问：RAG 系统的整体架构要怎么优化？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/TBOj1eENd86sCjcby3IyWQ)

10、 [面试官问：RAG 的文档解析为什么这么关键？](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/Qx91rDRbKmhuykUpXcg76w)

**赶紧点赞和收藏吧~**
