---
title: DSH Java 从0到1：Java 版 Agent 运行时框架与配套课程
date: 2026-10-23
tags:
  - AI/Agent
  - Java
  - 架构/DDD
  - 插件化
  - 课程/学习
aliases:
  - DSH Java
  - DeepSeek Harness Java
  - dsh-java
summary_model: DeepSeek-V4.1-Flash
source_type: 微信公众号文章
author: 小傅哥（公众号「bugstack虫洞栈」）
source: https://mp.weixin.qq.com/s/e1gEo5JAinMEvU53tElsBA
published: 2026-10-19
repo: https://github.com/deepseek-harness-java
site: https://dsh-java.xiaofuge.cn/
---

# DSH Java 从0到1：Java 版 Agent 运行时框架与配套课程

> [!abstract] 来源与整理说明
> 原文为小傅哥（公众号「bugstack虫洞栈」，博客 bugstack.cn）2026-10-19 发布的项目与课程介绍，含 Web 版/桌面版演示、Plugin Skills 说明、100 个场景案例清单、架构设计与 12 Part 课程计划。
> **总结模型：DeepSeek-V4.1-Flash**；原文作者署名为小傅哥，本笔记仅作提炼整理，不替代原作者。
> 文中 Star 数、版本号（v0.1.8）、里程碑编号（M1–M8）等均为原文陈述；课程与星球为付费内容，本笔记不对其质量作评价。

## 目录

- [[#一、核心结论]]
- [[#二、DSH Java 是什么]]
  - [[#定位]]
  - [[#核心能力]]
- [[#三、两种运行形态]]
  - [[#Web 版]]
  - [[#桌面版]]
- [[#四、Plugin Skills 与 100 个场景]]
  - [[#27 个独立 AI 产品]]
  - [[#74 个行业场景案例]]
- [[#五、架构设计]]
  - [[#DDD 模块划分]]
  - [[#内核与插槽]]
  - [[#桌面端启动流程]]
  - [[#对话流程]]
- [[#六、课程计划：12 Part、五个阶段]]
  - [[#阶段一 · 定语言、先能答（Part 01–02）]]
  - [[#阶段二 · 会思考、会干活（Part 03–04）]]
  - [[#阶段三 · 有记忆、有约束（Part 05–06）]]
  - [[#阶段四 · 成产品、可扩展（Part 07–10）]]
  - [[#阶段五 · 平台与收管（Part 11–12）]]
  - [[#四条横向主线]]
- [[#七、提炼与参考价值]]

## 一、核心结论

- **DSH Java 是 Java 版的 DeepSeek Harness 复刻**：用 Spring Boot + DDD 多模块，1:1 还原一个「稳定内核 + 统一插槽 + 插件化扩展」的 AI Agent 运行时。作者写了一个多月，含大量架构分析与领域建模。
- **一套代码、两种交付形态**：既能作为 Web 服务独立部署（MySQL），也能打成 jar 被 Tauri 桌面端内嵌拉起（standalone 模式 + H2 文件库）。
- **真正的差异化在插件体系**：ClassLoader + SPI 实现 Java 插件热插拔，与内核同 JVM，工具直接调用零序列化开销，还能注册 Hook 拦截工具调用——这一点是纯提示词 Skills 和进程外 MCP 都做不到的。
- **配套规模很大**：27 个独立 AI 产品 + 74 个行业场景案例 + 12 Part 课程计划，共迭代 8 个版本，v0.1.8 为冻结基线。
- **已有外部认可**：2026-10-14 桌面版被 AppImage 官方仓库收录（PR #9999）；作者称已有企业伙伴在实际使用。

## 二、DSH Java 是什么

### 定位

一个以「稳定内核 + 统一插槽 + 插件化扩展」为核心的 **AI Agent 运行时框架（Java 版）**，采用 Spring Boot DDD 多模块单体结构。

目标场景不是"再做一个聊天客户端"，而是：让已有的 N 个业务系统（电商、旅游、信贷、运维…）在任何需要智能体能力的地方，低成本地把 Agent 接进去。

![[ai-output/assets/dsh-java-agent-runtime-course/05.png]]
*原文配图 · 整体全景：`dsh-java-plugin-skills` 技能包指导构建插件（mysql-plugin / mail-agent-plugin），业务应用（MySQL 运维平台、2D 周末商城）经 HTTP 调用插件；上层用户从浏览器、桌面客户端、AI Agent 客户端（Claude Code / Copilot，走 MCP / SSE）三路进入同一套运行时内核。*

### 核心能力

| 能力 | 实现要点 |
| --- | --- |
| 推理循环 | ReAct 循环，`ReactLoopAgent` |
| 工具注册 | 统一 `ToolRegistry`，覆盖 fs / shell / web / mcp / lsp / terminal / skill |
| 拦截链 | Hook 机制，工具调用前后均可注入切面（审计、脱敏、风控） |
| 插件热插拔 | ClassLoader + SPI，运行时装载 |
| 进程外扩展 | MCP、sidecar、子代理 |
| 配套 | Web 版、桌面版、插件开发技能、archetype 脚手架 |

## 三、两种运行形态

### Web 版

启动方式即常规 Spring Boot 工程：

1. 先执行工程内 `deepseek_harness_java.sql` 建库；
2. 在 `application.yml` 配置 MySQL 连接；
3. IDEA 启动，默认访问 `http://localhost:8090/`；
4. 进设置页填入自己的模型，即可开始对话。

![[ai-output/assets/dsh-java-agent-runtime-course/06.png]]
*原文配图 · 在 IntelliJ IDEA 中启动 Web 版*

![[ai-output/assets/dsh-java-agent-runtime-course/07.png]]
*原文配图 · Web 版访问效果*

### 桌面版

基于 **Tauri** 构建，核心思路值得记一笔：

> 把后端 Agent 的 Spring Boot 可执行 Jar 作为资源文件"复制"进客户端安装包，并内置一份精简 JRE。

结果是用户安装后**无需配置 Java 环境**即可直接运行。对 Java 桌面分发来说，这是绕开"用户机器上有没有 JDK、版本对不对"这类经典问题的实用解法。

![[ai-output/assets/dsh-java-agent-runtime-course/08.png]]
*原文配图 · 打包动作本身：把 `deepseek-harness-java-app/target/deepseek-harness-java-app.jar` 复制到桌面端工程的 `resources/agent/runtime/` 下（两侧均为 v0.1.8）。*

界面形态接近 XxxBuddy 类产品；设置页含完整的模型配置、数字人（A2A）、Skills、MCP、CLI 以及插件安装。作者明说这套桌面端可以拿去二开做自己的 AI 产品。

![[ai-output/assets/dsh-java-agent-runtime-course/09.png]]
*原文配图 · 桌面版对话界面*

![[ai-output/assets/dsh-java-agent-runtime-course/10.png]]
*原文配图 · 桌面版设置界面（模型、A2A 数字人、Skills、MCP、CLI、插件安装）*

## 四、Plugin Skills 与 100 个场景

作者认为 DSH Java 最核心的价值是 **Plugin 能力**：业务系统有任何智能体诉求时，能方便地接入 Agent。

安装方式很"AI 原生"——直接把一段话丢给 AI Agent 工具：

```text
请帮我安装 dsh-java-plugin-skills 技能，地址：https://github.com/deepseek-harness-java/dsh-java-plugin-skills
并告诉我它的实际用途以及如何使用
```

![[ai-output/assets/dsh-java-agent-runtime-course/11.png]]
*原文配图 · 按上面这段话让 AI 工具自行安装技能*

### 27 个独立 AI 产品

原则：**工具优先**，每个产品解决一类真实工作流（开发 / 数据 / 运维 / 写作），AI 可组合多工具完成"一句话任务"；数据本地优先（`~/.dsh-java-<name>/`），不依赖外部 SaaS。

**开发者工具（10）**

| 仓库 | 能力 |
| --- | --- |
| dsh-java-git | Git Story Studio · 历史分析 / 变更摘要 / 回滚建议（不改写历史） |
| dsh-java-log | Log Lens · 日志筛选 / 模式聚类 / 异常定位 |
| dsh-java-api | API Sketch · 接口草图 / OpenAPI 生成 / 字段校验 |
| dsh-java-cron | Cron Forge · cron 解析 / 触发时间 / 校验 |
| dsh-java-env | Env Doctor · 环境一致性体检 / 密钥脱敏扫描 |
| dsh-java-dep | Dependency Radar · 依赖雷达 / 版本冲突 / CVE 提示 |
| dsh-java-diff | Diff Narrator · 变更叙事 / 风险扫描 / 回滚计划 |
| dsh-java-regex | Regex Forge · 正则解释 / 测试 / 生成 / 优化 |
| dsh-java-shell | Shell Buddy · 命令解释 / 风险提示 / 安全替代建议 |
| dsh-java-json | JSON Lens · 解析 / 校验 / 对比 / 路径查询 |

**数据与效率（11）**

| 仓库 | 能力 |
| --- | --- |
| dsh-java-csv | CSV Studio · 清洗 / 转换 / 校验 / 统计 |
| dsh-java-markdown | Markdown Doctor · 文档体检 / 结构修复 / 链接检查 |
| dsh-java-meeting | Meeting Digest · 会议纪要 / 行动项提取 |
| dsh-java-inbox | Inbox Triage · 邮件分诊 / 优先级（不代发） |
| dsh-java-backlog | Backlog Shaper · 需求整理 / 用户故事 / 优先级矩阵 |
| dsh-java-glossary | Term Atlas · 团队中英术语典 / 双语卡片 |
| dsh-java-recall-deck | Recall Deck · 记忆卡工坊 / SM-2 间隔重复 |
| dsh-java-style | Tone Tuner · 文风画像 / 可读性 / 术语校对 |
| dsh-java-faq | FAQ Builder · 客服记录聚类 / FAQ 草稿 / 覆盖缺口 |
| dsh-java-storymap | Story Mapper · 用户旅程画板 / 痛点 / 情绪曲线 |
| dsh-java-release | Release Notes Hub · 发布中枢 / 渠道文案变体 |

**安全与运维（6）**

| 仓库 | 能力 |
| --- | --- |
| dsh-java-secret | Secret Sweeper · 密钥泄漏扫描 / 熵检查 / 轮换清单 |
| dsh-java-docker | Docker Lens · 镜像容器清单 / 瘦身 / dockerfile lint（不 stop/rm） |
| dsh-java-nginx | Nginx Composer · 配置解析 / 路由表 / 错误 lint（不写回不 reload） |
| dsh-java-ssh-fleet | SSH Fleet Notes · 服务器舰队手册 / 巡检清单（不发起真实连接） |
| dsh-java-firewall-plan | Port Guard · 端口快照 / 冲突诊断 / 防火墙建议（不 kill） |
| dsh-java-backup-audit | Backup Auditor · 备份健康检查 / 3-2-1 策略评估 |

> [!tip] 值得注意的设计约束
> 这 27 个产品的描述里几乎都带一句"不做某事"：不改写历史、不代发邮件、不 stop/rm 容器、不写回不 reload、不 kill 进程、不删不改备份。这是**只读 / 建议型 Agent** 的权限设计范式，比"给 Agent 全部权限"保守得多，也更适合嵌进生产环境。

### 74 个行业场景案例

每个案例 = 「业务应用 + 内嵌 AI 助手 + Java Native 插件」的完整可运行仓库。

| 分组 | 数量 | 代表案例 |
| --- | --- | --- |
| 商城零售与生活电商 | 10 | 虚拟数码商城、生鲜社区团购、外卖订餐、周边探店点评 |
| 金融与个人事务 | 4 | 个人记账、小额信贷模拟器、保险理赔、费控报销 |
| 出行 · 物流 · 酒旅 · 文旅 | 7 | 城市出行规划（三网聚合三方案）、快递查寄、酒店预订、景区导览 |
| 生活服务与门店经营 | 38 | 在线问诊、牙科诊所、宠物医院/寄养/美容、健身房、家政、洗衣、美发、摄影、物业、自习室、智慧农场 |
| 工作协作与内容 | 3 | 团队看板、兴趣社区广场、直播带货复盘 |
| 产研测运维工作台 | 5 | 发布上线监控台（GO-NO-GO/一键回滚）、研发协作、测试用例、需求工作台、生产值班 |
| 教育学习 | 4 | 教师工作台、数学思维、语文阅读写作、英语听说 |
| 角色工作台 | 3 | 销售 CRM、律师办案、HR 招聘 |

同样延续了"AI 不越界"的边界：在线问诊只导诊不诊断、汽车养护不做故障诊断、HR 不做录用决定、律师助手不构成法律意见。

## 五、架构设计

![[ai-output/assets/dsh-java-agent-runtime-course/12.png]]
*原文配图 · DeepSeek Harness Java 整体架构设计（Java 17 / Spring Boot 4.x / DDD 六边形架构 / 单实例 Agent 运行时）。自下而上：types 公共类型被所有模块依赖 → infrastructure 适配器实现 → domain 领域核心 → case 用例层 → app 应用装配 → trigger 触发层。*

这张图比正文更完整地交代了两件事：**模块全名与技术基线**（`deepseek-harness-java-*` 六个模块、Java 17、Spring Boot 4.x、H2/MySQL 共 12 张 Harness 表），以及 **domain 内部的子域切分**——agent（`ReactLoopAgent`）/ llm / channel / tool + mcp / session + storage / sandbox + terminal / plugin + skill，外加 task、workflow、goal、guard、hooks、credentials、lsp、sdk、shared 等公共子域。

### DDD 模块划分

工程按 DDD 四层拆分，依赖方向自外向内：

| 模块 | 职责 |
| --- | --- |
| `app` | 启动与装配：`Application.main()`、启动初始化器（Startup / ModelSync / Schema / PresetPlugin） |
| `trigger` | HTTP/SSE 入口：`AgentController`（stream / message / status / cancel）、控制台、审批控制器 |
| `case` | 用例编排：`AgentUseCase` + 责任链（Resolve → Collect），只做"解析→意图→投递→收集"的编排外壳 |
| `domain` | Agent 核心域：`ReactLoopAgent` 推理循环、工具体系、审批闸、会话事件溯源 |
| `infrastructure` | 持久化与网关：Repository / DAO / PO，MySQL（web）或 H2（standalone） |
| `api` / `types` | 对外契约：DTO 与接口定义 |

### 内核与插槽

主线是「**一切能力皆工具，一切扩展皆插槽**」：

- **稳定内核**：契约层、LLM 适配、ReAct 推理循环（Phase 状态机 + inbox 消息驱动 + SessionEventLog 事件溯源）、内置工具。不随场景变化。
- **统一插槽**：
  - `ToolRegistry`：fs / shell / web / mcp / lsp / terminal / skill 的统一注册与选择（`CompositeToolRegistry` / `AgentToolCatalog`），内核能力与插件能力在此汇流；
  - **Hook 链**：拦截工具调用前后，插件可注入审计、脱敏、风控；
  - **端口适配**：仓储、事件以端口暴露，`infrastructure` 可替换实现。
- **插件化扩展**：Java 插件经 ClassLoader + SPI 热插拔加载，与内核同 JVM。契约即 `AbstractHarnessPlugin` / `PluginContext` / `PluginHook`，启动时由 `PresetPluginLoader` 装载 `plugins/` 目录。

> 作者特意点明了三者的层级差异：Java 插件（同 JVM，零序列化、可注册 Hook、走事件总线） > 进程外 MCP / sidecar（跨进程） > 纯提示词 Skills（无代码能力）。

### 桌面端启动流程

Tauri 壳负责进程托管，以一条命令拉起 jar 子进程。四个设计点：

1. **进程托管**：壳层预先分配空闲端口、生成随机 API Key、管理子进程生命周期；后端随桌面端退出而关闭，不留孤儿进程。
2. **参数即架构声明**：一条启动命令把"远程服务端"切换为"本地自治进程"——H2 文件库替换 MySQL、动态端口避开冲突、随机 Key 保证本机安全，**服务端代码零改动**。
3. **健康握手**：壳层轮询 HTTP 可用性，服务就绪后才加载前端主界面，保证用户看到界面时服务一定可用。
4. **插件随启动装载**：`PresetPluginLoader` 在启动链末段装载 `plugins/` 预置插件。

![[ai-output/assets/dsh-java-agent-runtime-course/13.png]]
*原文配图 · 桌面端启动时序。启动命令形如 `java -jar` + `--spring.profiles.active=standalone` + `--server.port` / `--harness.auth.api-keys` / H2 数据源；随后由 `schema.sql` 建表迁移（`sql.init.mode=always`），`ApplicationReadyEvent` 处打印控制台地址、校验默认模型与 Provider 适配器、同步模型配置与表结构、装载 `plugins/` 预置插件；壳层轮询健康后再放行前端。此后所有请求经 `ApiKeyAuthInterceptor` 校验 `X-API-Key`（本机鉴权 D-04）。*

### 对话流程

入口在 `trigger` 层 `AgentController`（`/api/agent`）。四个要点：

- **双层结构**：`case` 层责任链只做编排外壳，ReAct 循环下沉到 `domain` 层 `ReactLoopAgent`，**编排与推理解耦**。
- **三重防护**：单 turn 最多 50 step、token 续接最多 4 次、取消信号即时中止。
- **人机协同**：危险操作走"审批挂起 / 唤醒"——Agent 挂起等待用户决议，而不是静默执行或直接拒绝。
- **可恢复性**：全量事件溯源落库，进程重启或会话中断后可从断点恢复，不从零开始。

![[ai-output/assets/dsh-java-agent-runtime-course/14.png]]
*原文配图 · 对话全链路时序（`POST /api/agent/stream`，X-ApiKey 鉴权）。责任链三段：**Resolve** 解析构建 AgentRun（可跨会话恢复）→ **Intent** 规则前置分类（CHAT / TASK / CLARIFICATION）→ **Dispatch** 意图裁决改写后投递 inbox 并唤醒 Agent。`ReactLoopAgent` 以 Phase 状态机跑 `runInside` 步循环（±50 步），每步"调模型 → 分块（正文 / 推理）"；模型要求工具时推 `SSE tool_result`（running 卡片），由 `ToolCallExecutor` 执行（shell / fs / web / lsp / mcp…，shell 先过危险命令守卫 + 校验）；非 FULL_OPEN 模式下生成 Pending 审批单，经 `POST approvals/{runtimeId}/resolve` 回填决议。工具结果以 `ToolCallResult` 事件回传，`stop` 返回 null 即走 `noFurtherContinuation` 结束；纯文本答复直接 `runEnd(Completed)`。收尾阶段 `SSE flush / done` → 落库 `Collect`（抽取等待恢复、写 SessionLog 事件）→ 返回 `AgentMessageResponseDTO`。用户点"停止"走 `POST /api/agent/{agentId}/cancel` 交互点中止。*

## 六、课程计划：12 Part、五个阶段

按 v0.1.8 分支制定。整体节奏：**先把内核立起来，再把插槽做成产品**。从冻结基线的 7 模块骨架（types / api / domain / case / trigger / app，加 `harness.yml` 双通道、standalone 切 H2）出发，最终交付一个与基线全量一致、零依赖可启动、可打包分发的完整 Agent 运行时。

![[ai-output/assets/dsh-java-agent-runtime-course/15.png]]
*原文配图 · 课程篇章规划总览：五个阶段从左到右、自上而下推进，底部收敛到"最终产品形态 = 与 v0.1.8 冻结基线全量一致、零依赖可启动、可打包分发"。每个 Part 都标了对应里程碑（M1–M6、M8）。*

### 阶段一 · 定语言、先能答（Part 01–02）

- **Part 01 契约层**（types + api）：Message / ToolCallBlock 消息与工具模型、插件 SPI 契约，沉淀 api 23 接口 + 55 DTO。
- **Part 02 LLM 适配**：DeepSeek 适配器、OpenAI 兼容 / Anthropic 路由工厂；顺带长出最小 HTTP/SSE 壳（阻塞式 message、SSE stream、模型设置热切换）。
- 达成 **M1 能答**：curl 问答、流式逐字。此后每节验证都走真实协议入口。

### 阶段二 · 会思考、会干活（Part 03–04）

- **Part 03 ReAct 循环**（全课程核心）：`ReactLoopAgent`、工具调用解析与结果回填、循环控制（步数/取消/超时）、SSE 事件协议、系统提示词装配、`CompactionEngine` 会话压缩。
- **Part 04 工具体系**："装上手臂"——`ToolRegistry`、`ToolCallExecutor`、fs 工具族、shell + 危险命令守卫、web 搜索抓取、`ask_user_question` 运行时提问、PRE/POST Hook 链。
- 达成 **M2 会思考**（自主多步推理）、**M3 会干活**（查资料→写文件一条龙）。

### 阶段三 · 有记忆、有约束（Part 05–06）

- **Part 05 持久化与事件溯源**：MyBatis 地基、`SessionEventFactory`、双事件存储（JSONL + JDBC）、Rebuilder / Projector 会话重建。达成 **M4 有记忆**（重启不丢会话、事件可回放）。
- **Part 06 任务与审批**：任务队列落库、权限矩阵评估、审批命令/查询、运行时审批网关（Shell 挂起）、Goal/Plan 与 Todo/Jobs。达成 **M5 受治理**。
- 叙事线索：内存版 → 落库版；"能力越强缰绳越紧，危险必审批"。

### 阶段四 · 成产品、可扩展（Part 07–10）

- **Part 07** 用例编排层：`CasePipeline` 策略树、终端五节点、任务链重构、Agent 消息编排四节点。
- **Part 08** 触发层与控制台：Controller 分层、统一响应、SSE 批处理、API Key 鉴权。达成 **M6 工程化**。
- **Part 09** Java 插件体系：加载器、`SpringPluginContext`、生命周期、事件总线、Hook、配置热更新、archetype 脚手架。
- **Part 10** 进程外扩展：MCP stdio/http、Node sidecar JSON-RPC 桥、子代理 Provider（Claude Code / Codex / ACP）。
- 主线：**先直连后抽象**，把最小壳长成产品形态。

### 阶段五 · 平台与收管（Part 11–12）

- **Part 11** 平台能力进阶（选修 5 节）：沙箱与执行边界、凭证管理与技能加载、计划任务与终端、工作流引擎、数字人与 A2A（AgentCard 可发现）。
- **Part 12** 完结：standalone 零依赖、Docker Compose、差量合入与全量对账（终态 = v0.1.8 冻结基线）。达成 **M8 可交付**：`package-local.sh` 产物在新机器跑通。

### 四条横向主线

| 主线 | 演进路径 |
| --- | --- |
| 契约 | 消息模型 → 对外接口 → SSE 事件协议 → 子代理契约 |
| 安全 | 危险命令守卫 → 权限矩阵 → 审批网关 → 沙箱边界 → API Key |
| 数据 | 设置内存版 → 建表 → 双事件存储 → 落库恢复 → 任务/插件落库 |
| 验证 | 最小 HTTP/SSE 壳 → 分层统一响应 → Web 控制台 → 打包分发 |

另有一套入门教程 **ToyAgent**：基于 DSH Java 拆分的最初上车课程，"一个类就是一个最小 MVP 版本的智能体"，每章只讲一个知识点。

![[ai-output/assets/dsh-java-agent-runtime-course/17.png]]
*原文配图 · ToyAgent 入门教程章节*

## 七、提炼与参考价值

**值得直接借鉴的四个设计**

1. **参数即架构**：同一条启动命令，靠参数把云端服务切成本地自治进程（H2 + 动态端口 + 随机 Key），服务端代码零改动。一套代码两形态，比自己维护两个分支干净得多。
2. **Jar 打进客户端 + 内置精简 JRE**：Java 桌面分发的标准解法，用户免装 JDK。Tauri 壳只做进程托管和健康握手，职责很薄。
3. **插件分三级**：同 JVM 热插拔 > 进程外 MCP/sidecar > 提示词 Skills。选型时显式分层，而不是所有扩展都塞进 MCP。
4. **只读优先的 Agent 权限范式**：27 个工具几乎全部限定"不写回、不删除、不代发、不 kill"，把破坏性操作全部交给审批挂起。这是能进生产环境的姿态。

**结构性观察**

- 编排（case）与推理（domain）解耦，`ReactLoopAgent` 用 Phase 状态机 + inbox 消息驱动 + 事件溯源，这套组合让"可恢复"和"可观测"同时成立——比常见的 while-loop + 内存会话稳。
- 三重防护（步数上限 / token 续接上限 / 取消信号）是任何 Agent 循环的必备项，缺一个都会出现失控或卡死。
- 74 个场景案例的真实价值不在"多"，而在于它把「业务系统 + 内嵌助手 + 原生插件」这个组合固化成可复制的仓库模板，降低了从 0 到 1 的启动成本。

**与我相关的点**

- 我的「考试 API 监控 + 微信推送」自动化属典型的**工具型 Agent 场景**；按它的分层，这类能力更适合做成进程外 sidecar 或纯 Skills，而不是塞进内核。
- 若要做 Java 侧的 Agent 运行时复用，`ToolRegistry` + Hook 链 + 事件溯源这三件套是最小可用骨架。

**在作者完整路线里的位置**

![[ai-output/assets/dsh-java-agent-runtime-course/16.png]]
*原文配图 · 小傅哥的 AI Agent 学习路线（通识 / 应用 / 项目三层，标注 15 个项目编号与三条架构方案分支）。DSH Java 落在"第 3 套架构方案 · Harness 马具方案"，接在 WaLiSSH、WaLiCode 这两套"AI Agent 脚手架 + 场景应用"之后，目标是做 1:1 复刻的运行时底座，再向下长出 DSH Plugin 智能客服、DSH Plugin 运维平台（MySQL）、DSH Java 桌面版（数字人）。*

这张图值得单独看一眼的原因：它把"学 Agent"拆成**通识（0）→ 应用（1–4）→ 项目（5–15）**三段，并给出两条推进路线（完整进阶 / 老板急发版），说明 DSH Java 并不是孤立的开源项目，而是一份商业课程体系里的第三层。判断是否值得投入时，这一点比技术细节更重要——**代码开源可读，课程付费**。

---
原文链接：https://mp.weixin.qq.com/s/e1gEo5JAinMEvU53tElsBA
项目仓库：https://github.com/deepseek-harness-java
官网：https://dsh-java.xiaofuge.cn/
