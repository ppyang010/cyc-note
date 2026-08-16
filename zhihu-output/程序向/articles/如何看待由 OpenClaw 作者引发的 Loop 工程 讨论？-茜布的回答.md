---
id: "2049537011460182357"
title: "如何看待由 OpenClaw 作者引发的 \"Loop 工程\" 讨论？"
author: "茜布"
type: zhihu-answer
source: "https://www.zhihu.com/question/2048003050531558553/answer/2049537011460182357"
created: "2026-06-14 17:01"
updated: "2026-06-14 17:01"
collected: "2026-06-14 17:01"
downloaded: "2026-08-16"
---
## 如果你认真观察过去半年 Claude Code、Codex、Cursor Agent、OpenHands、OpenAI Agent SDK、Anthropic Harness、Trellis、OpenClaw 这些项目的发展方向，会发现它们正在不约而同地向同一个终点收敛：

-   Prompt → Goal
-   Chat → State
-   Context → Memory
-   Agent → Controller
-   Workflow → Reconciliation Loop
-   Human Operator → Loop Designer

而这个终点，Kubernetes 社区在十几年前已经到过一次。

下面这篇文章，我会沿着这个角度展开。

* * *

## AI Coding 正在重新发明 Kubernetes：从 Loop Engineering 到下一代软件工程

### 引子：为什么最近大家突然都在讨论 Loop Engineering

过去两年，AI Coding 圈子经历了三个明显阶段。

### 第一阶段：Prompt Engineering（2023–2024）

大家都在研究：

-   Prompt 怎么写
-   System Prompt 怎么设计
-   Few-shot 怎么组织
-   Chain of Thought 怎么引导

那时候一种普遍的信念是：

> Prompt 是 AI 时代最重要的技能。

后来发现不是。因为模型越来越强，Prompt 的边际收益越来越低。

* * *

### 第二阶段：Context Engineering（2024–2025）

大家逐渐意识到：真正决定 Agent 效果的，不是 Prompt，而是 Context。

于是研究方向转向了：

-   RAG
-   Memory
-   MCP
-   Tool Calling
-   Context Compression
-   Context Window Management

Anthropic 后来甚至公开表态：

> Context Engineering 比 Prompt Engineering 更重要。

这是一次实质性的认知升级。因为大家的关注点变了：问题不再是如何说服模型，而是如何构造模型所处的环境。

* * *

### 第三阶段：Loop Engineering（2026）

然后大家又发现了一个新问题：即使 Context 解决了，Agent 仍然不稳定。

为什么？

因为软件开发本质上不是一次推理，而是一个持续反馈过程。

真实的开发流程是这样的：

```text
看代码
  ↓
修改代码
  ↓
编译
  ↓
测试
  ↓
发现问题
  ↓
重新修改
  ↓
再次测试
  ↓
Review
  ↓
修复
  ↓
部署
```

这是一个循环，不是一次调用。

于是行业的发展轨迹变成了：

```text
Prompt
  →
Prompt + Context
  →
Goal + Loop
```

这就是 Loop Engineering 的来由。

* * *

### 起源：从一行 Bash 到一个范式

Loop Engineering 这个词虽然新，但它的工程直觉已经酝酿了很久。

最早可以追溯到 2025 年 7 月，开发者 Geoffrey Huntley 提出了一个名为 **Ralph**（Ralph Wiggum）的极简循环。它最纯粹的形态只有一行 bash：

```text
while :; do cat PROMPT.md | claude-code ; done
```

精髓在于它的自嘲——“这技术在一个不确定的世界里，确定性地很烂”。每一轮循环都用全新的上下文窗口，状态不靠对话历史，而是靠文件系统、git 历史和一个 `fix_plan.md` 计划文件来传递。社区后来把这条原则浓缩成一句话：**Agent 会忘，仓库不会忘。**

2026 年 6 月，这个方向被引爆了。导火索是 Anthropic 旗下 Claude Code 负责人 Boris Cherny 的一句话：

> “我已经不给 Claude 写 prompt 了。我有一堆循环在跑，它们去给 Claude 写 prompt、自己琢磨该干什么。我的工作就是写循环。”

几乎同时，开发者 Peter Steinberger 发了一条被疯传的推文——“你不该再给编码 Agent 写 prompt 了，你该设计能给 Agent 写 prompt 的循环”——而 Google 的 Addy Osmani 随即发布博客，正式把这个现象命名为 **Loop Engineering**，并给了它一个定义：

> “Loop engineering 就是把‘给 Agent 写 prompt 的那个人’——也就是你自己——替换掉。你转而去设计那个替你写 prompt 的系统。这里的‘循环’可以理解为一个递归目标：你定义一个目的，AI 就一直迭代直到完成。”

注意这几个关键词：**递归目标**、**迭代直到完成**、**声明一个想要的结果，然后交给一个会自己观察、自己行动、自己判断“做完没有”的系统。**

如果你熟悉后端基础设施的工程范式，此刻应该已经感觉到一种强烈的既视感——因为这正是 Kubernetes 的世界观。

### 一个循环的工程骨架

那么，构成一个 Loop Engineering 系统的零件是什么？Osmani 总结了五个积木加一层记忆，目前主流工具（Claude Code、OpenAI Codex）已经收敛到同一套原语：

-   **Automations（自动触发）**：定时器、cron、webhook、GitHub Actions——给循环一个“心跳”，让它不是人工按按钮才跑。
-   **Worktrees（Git 工作树）**：让多个并行 Agent 各自拥有独立的工作空间，互不踩踏对方的修改。
-   **Skills（SKILL.md）**：把项目知识、编码规范、领域约定写成结构化的文档，Agent 每轮都能读到——这就是“把人类的 prompt 技巧固化进系统”。
-   **Plugins / Connectors（MCP）**：连到真实的工具链、issue 系统、数据库、CI/CD，让 Agent 不只是在沙箱里自嗨。
-   **Sub-agents（子 Agent）**：把“写代码的”和“检查的”拆成不同的 Agent（maker / checker），避免模型给自己打分太宽容。
-   **Memory / State（记忆）**：用 Markdown 文件、Linear issue、git 提交信息把进度记录在对话之外——循环可以随时被杀死重启，但状态不会丢。

## 一个惊人的发现

当我第一次认真研究 Loop Engineering 的时候，脑子里冒出的第一个词不是 Agent，而是 Kubernetes。

因为两者长得太像了。

* * *

### Kubernetes 真正的核心是什么

很多人以为 Kubernetes 是容器编排平台。其实不是。

Kubernetes 真正伟大的地方在于：**它把控制论（Cybernetics）带进了软件工程。**

K8s 的核心只有一句话：

```text
Desired State
    ↓
Observe
    ↓
Compare
    ↓
Act
    ↓
Repeat
```

也就是 Reconciliation Loop. Controller 永远在干同一件事：

```text
实际状态 = 期望状态 ？
```

如果不是，就继续调节。

这其实就是恒温器的逻辑：

```text
当前温度 = 18°  →  目标温度 = 22°  →  继续加热
当前温度 = 21°  →  目标温度 = 22°  →  继续加热
当前温度 = 22°  →  目标温度 = 22°  →  停止
```

Kubernetes 本质上是**一个由无数控制循环组成的系统**。Deployment Controller 是循环，ReplicaSet Controller 是循环，HPA 是循环，Operator 也是循环。

* * *

## 它们共享同一棵家谱树：控制论的两条分支

上面这个类比如果只是事后附会，那就不值一提。但有意思的是，**两边的奠基文献都在显式地引用控制论。**

Kubernetes 官方用恒温器解释 controller，这已经成了分布式系统的经典比喻。而另一边，Martin Fowler 和 Birgitta Böckeler（Thoughtworks）在 2026 年发表的《Harness engineering for coding agent users》中，直接用**前馈控制（feedforward）+ 反馈控制（feedback）**这套控制论术语来拆解 AI 编码的脚手架：

-   **Guides（前馈控制）**：在 Agent 动作\*之前\*引导它——规范文档、Skills、提示约束——提前告诉它“什么不能做、应该怎么想”。
-   **Sensors（反馈控制）**：在 Agent 动作\*之后\*观测并纠偏——测试结果、类型检查、lint 报告、LLM 裁判——把偏差检测出来并喂回下一轮。

恒温器、PID 控制器、Reconciliation Loop、Agentic Loop——它们是同一棵家谱树上的不同分支。Loop Engineering 不是凭空发明的新范式，而是控制系统思想在“代码生成”这个被控对象上的又一次投影。

### K8s 和 Loop Engineering 共享的核心工程智慧

Kubernetes controller 不依赖“我有没有收到那个事件通知”。它每轮都会重新读取集群当前真实状态，然后和期望状态做 diff。错过一个事件、进程崩溃重启、网络抖动丢了一条消息——都无所谓，下一轮照样能收敛。这正是 K8s 容错能力的根源：**不信任易失的事件流，只信任可重复观测的持久状态。**

Loop Engineering 正在独立地发现完全相同的原则。Ralph 循环的每一轮都丢弃上下文窗口、从仓库重新读取现状。社区的口号——“Agent 会忘，仓库不会忘”——翻译成 K8s 黑话就是：不信任易失的对话历史（边沿触发的隐患），只信任可重新观测的持久状态（etcd / git）。这就是教科书级的 level-triggered reconcile。

也正因为如此，Loop Engineering 天然容忍单轮失败、崩溃和跑偏——它靠重复迭代收敛，而不是靠“每一轮都必须做对”。

值得注意的是，AI 编程的整体趋势正是从“长对话”往“状态进仓库、每轮重读”演进——也就是说，它在主动朝 K8s 那套调谐模型靠拢。这个类比不是越用越牵强，而是越来越贴。

### Plant Model：一道无法跨越的鸿沟

但这里同时也暴露了 Loop Engineering 最根本的困境。

控制论有一个前提概念叫**被控对象模型（Plant Model）**——你得大致知道“推一下，系统会怎么动”。Kubernetes 有这个东西：创建一个 Pod、删除一个 Pod、修改一个 Deployment——每个动作的结果都是确定、可预测的。

而 LLM 循环的“被控对象”是一团概率云。同样一句“修复支付系统的并发问题”，Claude 今天可能这样写，明天可能那样写；GPT 和 Claude 可能给出完全不同的方案。你是在用一个噪声极大、模型极模糊的执行器做控制。

这就是为什么 K8s Operator 可以做到**可证明收敛**，而 Agent Loop **至今无法证明收敛**。这不是工程水平的差距，而是被控对象性质的鸿沟，这可能是未来需要研究的方向。

## AI Coding 为什么越来越像 K8s

如果我们把 Claude Code 的执行过程画出来，会看到：

```text
读取代码库
  ↓
理解目标
  ↓
修改代码
  ↓
运行测试
  ↓
分析结果
  ↓
再次修改
  ↓
重新测试
  ↓
直到通过
```

这不就是：

```text
Observe → Diff → Act → Repeat
```

吗？

也就是说，Agent Loop 和 Reconciliation Loop 在结构上几乎完全一致。

* * *

### Prompt 正在变成 Spec

这是我认为最重要的变化。

传统开发是命令式的（Imperative）——你把步骤告诉 Agent：

```text
打开文件 A
修改函数 B
新增测试 C
运行命令 D
```

而 Loop Engineering 是声明式的：

```text
修复支付系统中的并发问题，确保测试全部通过。
```

结束。Agent 自己想办法。

这和 Kubernetes 的写法本质上是一样的：

```text
replicas: 3
```

你不会告诉 Controller “启动 Pod1、启动 Pod2、启动 Pod3”。你只告诉它：我要三个副本。

Prompt 正在演变成 Spec。

* * *

## 真正重要的不是 Agent，而是 Controller

很多人还在讨论 Claude 厉害还是 GPT 厉害。这个问题越来越不重要了，因为未来模型会趋同。

真正决定系统能力的，是 Loop。

K8s 社区早就证明了一件事：Controller 比 Pod 更重要。因为 Pod 会死，Controller 不会。

AI Coding 的未来也是如此。模型只是执行器，Loop 才是大脑。

未来的软件工程团队很可能长这样：

```text
Agent A — 负责编码
Agent B — 负责测试
Agent C — 负责 Review
Agent D — 负责安全扫描
Agent E — 负责架构检查

Loop Controller — 负责协调
```

这已经非常接近 Kubernetes 的架构了。

* * *

## 为什么状态外置如此重要

最近一个很有意思的趋势是：大家开始把状态从上下文窗口里搬出来。

比如：

-   AGENTS.md
-   SKILL.md
-   memory.md
-   task.md
-   progress.md

很多人以为这是为了省 Token。其实不是。

根本原因在于：**Agent 的记忆不可靠。**

这不是工程上的小毛病，而是架构层面的根本缺陷。LLM 的对话历史本质上是易失的——换一个模型、重启一个 session、上下文窗口溢出，之前的“记忆”就全丢了。

Kubernetes 早就解决过这个问题。Controller 可以随时被杀掉，为什么没关系？因为状态在 etcd 里。Controller 本身是无状态的——它不“记住”上一轮做了什么，每一轮都从 etcd 重新读取当前状态，和期望状态做 diff，然后行动。

Agent 未来也一样。一个 Agent 崩溃、重启、换模型、换供应商——都没关系。只要状态还在，循环就能继续。但前提是：**状态不在对话里，而在仓库里。**

于是：

```text
etcd
  变成了
Git / Markdown / Issue / Task Board / Vector DB
```

而且这一映射比表面看起来更精确。K8s controller 除了读 spec 和 observed state，还会把观测结果写回 **status 子资源**——这是下一轮 reconcile 的起点。Loop Engineering 里的 `progress.md`、`task.md` 就是同样的东西：循环必须在每轮结束时把“我现在在哪”写回磁盘，否则下一轮无从读起。这正是 K8s 社区在十几年前就内化的一条经验：**一个没有 status 的 controller 是半成品。**

本质完全一致。

* * *

## 为什么 Loop Engineering 还远远不如 Operator：五组关键差异

这里才是最有意思的地方。表面上两者结构同构，但一旦深究“你到底在控制什么东西”，五组本质差异就暴露出来——而且正是这些差异解释了为什么 Loop Engineering 现在这么难、为什么还离不开人。

### 差异一：执行器——确定性 vs 随机性

上文已经讲了 Plant Model 的鸿沟，这里不再展开。只补充一点：LLM 不但随机，而且**非幂等**。K8s controller 调一次 API 创建一个 Pod，调十次还是那一个 Pod。而 Agent 对同样的输入可能输出不同的代码——可能更好，可能更差，可能完全跑偏。你是在用一个噪声极大、模型极模糊的执行器做控制。

### 差异二：收敛保证

写对的 reconcile loop 是**可证明收敛、有界**的——K8s 社区有成熟的形式化验证工具链。而 LLM 循环**没有收敛保证**：它可能震荡（改过去又改回来）、可能卡死（反复报同一个错但不会换思路）、可能谎称完成（给自己打满分，但代码根本跑不通）。

这一差异直接催生了一个 K8s 里不存在的设计——**maker/checker 分离**：写代码的 Agent 和判断“是否完成”的 Agent 必须是不同的模型，因为模型给自己打分太宽容。Claude Code 和 Codex 都内置了 `/goal` 这类原语，用一个独立的小模型来裁定循环是否该停。K8s 不需要这层，因为它判定收敛只需要一句话：`observed == desired`。

### 差异三：完成判定——不可机器判定

K8s 的期望状态是精确、机器可校验的 spec，diff 几乎零成本。AI 循环的“完成”常常**不可机器判定**，要靠测试、类型检查、甚至 LLM-as-judge——**而裁判本身还会错。**

于是冒出一个 K8s 里没有的哲学问题：**谁来监督监督者？** Maker/checker 的答案是用独立模型评审（给 checker 换一个比 maker 更强的模型），用强制测试套件做硬门槛，用静态分析做旁路验证——本质上全都是在给一个不可靠的判定函数打补丁。

Operator 只能在**受约束的 API** 里增删改已知资源——建 Pod、删 Pod、改 ConfigMap，blast radius 可控。编码 Agent 的动作空间近乎**无界**——它可以写任意代码、执行任意 shell、修改任意文件。一个跑飞的 reconcile 顶多把集群搞乱；一个跑飞的编码循环可能把你的代码库、甚至生产环境推下悬崖。

这是实践层面最大的区别。**K8s Operator 一旦写好、被信任，就全自主运行，正常情况下没有人在环。** K8s 用了近二十年、靠确定性和形式化测试，才挣到“无人值守”的信任。

而 Loop Engineering 的所有严肃倡导者都在说同一句话。Osmani 的原话：

> “循环改变了工作，但没有把你从工作里删掉……验证仍然是你的责任。一个无人值守跑着的循环，也是一个无人值守犯错的循环。”  
> “去搭这个循环。但要像一个打算继续当工程师的人那样去搭它，而不是只负责按下‘开始’的人。”

他甚至给两种新的失败模式起了名字：

-   **理解债（comprehension debt）**：交付了自己从未真正读懂的代码。循环跑完了，功能上线了，但没有人知道它到底写了什么、为什么那样写——这在一个出问题时需要人类介入的系统里是致命的。
-   **认知投降（cognitive surrender）**：工程师逐渐放弃理解循环在做什么，变成纯粹的“开始键操作员”——这是对工程能力的慢性侵蚀。

换个角度说：**Loop Engineering 现阶段就是一个“还没挣到自主权”的 Operator 模式。** 同样的调谐循环架构，但因为执行器不可靠、收敛无保证、判定会出错，所以上面必须再套一层人类监督回路。

这也决定了未来十年 AI Coding 最大的研究方向——不是更强的模型，而是：

> 如何让概率系统在工程上表现得像一个确定性系统。

* * *

## Maker-Checker 本质上是 Admission Controller

这是我最近一个有趣的观察。为什么大家都在做 Maker Agent + Checker Agent？

因为大家发现：模型会骗自己。Claude 说“任务完成”，不代表真的完成了。于是需要第二个 Agent 来审查。

Kubernetes 里其实有类似的思想。Admission Controller、Validating Webhook——它们本质上都在干同一件事：

> 不要相信执行器。

未来 Agent 系统一定会越来越多层：

```text
Maker
  ↓
Checker
  ↓
Reviewer
  ↓
Policy Engine
  ↓
Human
```

这其实就是 AI 世界里的 Control Plane。

* * *

## K8s 二十年经验能教 Loop Engineering 什么

如果把这个类比当成工程工具来用，K8s 社区踩了二十年的坑几乎可以逐条映射成 Loop Engineering 的设计原则。这不是“借鉴灵感”，而是同构系统间的直接经验迁移：

-   **幂等性 → “每轮只做一件事” + 全新上下文。** K8s reconcile 的核心要求是幂等可重入——跑一次和跑十次结果一样。Ralph 循环的“one item per loop”就是在用工程纪律逼近同样的性质：每轮只推进一个明确任务，状态落盘后再进下一轮，不让混沌叠加。
-   **Status 子资源 → 进度笔记与记忆文件。** K8s controller 不只在 etcd 里读 spec，还会把观测结果写回 status 子资源——这是下一轮 reconcile 的起点。Loop Engineering 里的 `progress.md`、`task.md` 就是同样的设计：循环必须在每轮结束时把“我做到了哪、卡在了哪”写回磁盘，否则下一轮无从读起。
-   **Requeue + 指数退避 → 循环节奏与心跳。** K8s controller 出错后不是立刻重试，而是带指数退避地重新入队。Loop Engineering 同样需要节奏控制——用 cron / webhook 给循环一个“心跳”，用明确的退出条件防止空转和死循环。一个没有终止条件的循环不是工程系统，是资源泄漏。
-   **CRD 扩展领域知识 → Skills + MCP。** 两者都是“把通用引擎特化到你的领域”的机制。K8s 用 CRD 把通用 controller 变成数据库 Operator、消息队列 Operator；Loop Engineering 用 `SKILL.md` 和 MCP 连接器把通用 Agent 变成“你项目的专属工程师”。
-   **Reconcile Storm 教训 → Worktree 隔离。** K8s 社区很早就知道并发 controller 会互相踩踏——多个 controller 同时修改同一个资源会导致 reconcile storm。Loop Engineering 用 git worktree 让并行 Agent 各自拥有独立工作空间，本质上是同一类问题的同一类解法。

反过来，Loop Engineering 也能回馈 K8s。它对“独立 checker、外部验证、对‘宣称完成’保持怀疑”的执念，对那些动作本身不确定、依赖外部云 API 的 Operator 同样有借鉴价值——当你的执行器开始变得不那么确定时，你就会需要一个 maker/checker。

## 从结构相似到本质相似：为什么真正的核心不是 Loop，而是 Goal 和 Evaluation

前面花了很大篇幅论证 Loop Engineering 和 Kubernetes Operator 在结构上的同构。但如果只停留在结构相似，这篇文章就还没有触达最深的那个洞察。

事实上，看完 Anthropic、OpenAI、Claude Code、OpenHands、Trellis、OpenClaw 以及最近各种 Loop Engineering 实践之后，我越来越觉得：

> **Loop Engineering 的本质不是设计 Loop，而是设计 Goal 和 Evaluation.**

甚至可以说：

> Prompt Engineering → Context Engineering → Loop Engineering → **Goal Engineering**

后面真正决定上限的，根本不是 Agent，也不是 Loop，而是：

```text
Goal
  ↓
Evaluation
  ↓
Loop
  ↓
Model
```

很多人把注意力放在最下面一层。实际上最重要的是最上面两层。

### Kubernetes 真正的成功学：Desired State 被严格定义了

很多人以为 K8s 成功是因为 etcd、CRD、Operator、Scheduler。其实不是。

Kubernetes 最大的成功只有一件事：**Desired State 被数学化了。**

```text
replicas: 3
```

什么叫完成？没有歧义——`actual_replicas == 3`，结束。再比如：

```text
available_replicas: 3
ready_replicas: 3
```

完成。没有模糊空间，没有审美，没有主观判断，没有“我觉得差不多了”。Goal 和 Evaluation 被彻底形式化了，所以 Controller 才能收敛，所以全自主运行才成为可能。

这是 K8s 世界最被低估的一条经验：**不是 Controller 设计得有多好，而是它要逼近的那个目标足够清晰。**

### AI Coding 最大的问题恰好在这里

Goal 根本不明确。

比如：“帮我优化支付系统。”什么意思？性能？稳定性？代码质量？可维护性？安全性？成本？不同工程师理解完全不同。

再比如：“重构用户系统。”完成了吗？没人知道。

所以 AI Coding 的问题从来不是 Agent 不够聪明，而是 **Goal 无法精确定义**。你连“做完”是什么意思都说不清楚，Agent 怎么可能收敛？

而更致命的是第二层——即使 Goal 勉强定义了，**Evaluation 仍然很难。**

“修复这个 Bug”——什么叫修复成功？很多团队停留在“测试通过”，实际上远远不够。可能测试覆盖不全、引入了性能回退、埋下了安全问题、增加了架构债务、制造了未来 Bug。

真正的 Evaluation 会变成：

```text
单元测试 + 集成测试 + E2E 测试 + 性能测试 + 静态分析 + 安全扫描 + Code Review
```

你会发现，这里越来越不像 Prompt，而越来越像 **Benchmark System**。

这也是为什么 OpenAI 和 Anthropic 都在疯狂投入 Evals 团队——不是因为他们喜欢做测评，而是因为**没有 Evaluation 就无法优化 Agent.** 控制论里有一个最基本的公式：

```text
Control = Goal − Observed State
```

如果你测不出 Observed State，控制本身就不存在。

### 一个很多人忽略的公式

我现在越来越喜欢用这个公式来表达 Agent 的能力上限：

```text
Agent Capability = Model × Context × Loop × Evaluation
```

很多人在优化 Model，少部分人在优化 Context，极少数人在优化 Loop。但真正的天花板其实在 **Evaluation**。因为没有 Evaluation，Loop 无法收敛——模型再强、上下文再丰富、循环设计得再精巧，都只是在随机游走。

### 为什么很多 Agent 跑着跑着就废了

原因特别简单：没有 Termination Condition.

K8s 的停止条件是一行代码：`actual == desired`。Agent 呢？是“继续修还是停？”——不知道。

于是两种经典死法：要么修好了继续修，最后修坏了；要么根本没修好，却说完成了。本质原因只有一个：Evaluation 不够好。

很多人脑中的 Loop 是：

```text
Goal → Agent → Done
```

实际上应该是：

```text
Goal → Agent → Evaluation → Score → Feedback → Agent → Evaluation → Score → ...
```

这已经不是 Loop。这是一个 **Optimization System**——它和强化学习已经开始共享同一套骨架。

我甚至怀疑，未来不会出现大量的 Prompt Engineer，而会出现 **Goal Engineer** 和 **Evaluation Engineer**。

因为 Prompt 越来越不重要，Goal 越来越重要。

一个 Goal Engineer 写出来的东西不是“帮我开发一个支付系统”，而是：

```text
goal:
  latency_p99: < 100ms
  availability: > 99.99%
  test_coverage: > 90%
  critical_vulnerability: 0

evaluation:
  - unit_test
  - integration_test
  - benchmark
  - security_scan
```

这时候 Agent 才知道该往哪个方向努力，Loop 才知道什么时候可以停。

### 四层理解：从结构到本质

到这里，我们可以总结出理解 AI Coding 和 Kubernetes 关系的四个层次：

**第一层理解**：Loop Engineering ≈ Operator——这是结构相似。

**第二层理解**：Agent ≈ Controller——这是实现相似。

**第三层理解**：Goal ≈ Spec, Evaluation ≈ Status——这才是本质相似。

**第四层理解**（也是最重要的一层）：**AI Coding 不是自动化写代码，而是自动化逼近目标。** 而一切自动化逼近目标的系统，最终都会回到控制论。

控制论里面最重要的从来不是执行器，而是三件事：目标是否清晰、状态是否可观测、反馈是否准确。

行业关注点会逐渐从“哪个模型更强”转向——Goal 如何表达，Evaluation 如何量化，Benchmark 如何构建，Agent 如何收敛。因为当 Goal 和 Evaluation 被定义清楚以后，模型只是一个可替换组件。

就像 Kubernetes 世界里，你真正关心的从来不是某个 Pod，而是：**Spec 是否定义正确，Status 是否真实反映系统状态，以及 Controller 是否持续把两者拉近。**

这也恰恰是 AI Coding 从“好玩的工具”变成“可靠的工程系统”必须跨过去的那道坎。

## 我认为未来真正会出现的东西

我甚至怀疑，未来会出现类似 Kubebuilder 和 Operator SDK 这样的 Agent Operator Framework——但和上文 YAML 示例不同，它的核心不再是声明“用什么模型、怎么检查”，而是声明 **Goal 的量化指标和 Evaluation 的验证矩阵**：

你只需要声明：

```text
goal:
  description: "修复支付系统的并发问题"
  metrics:
    correctness:
      unit_test_pass_rate: "100%"
      integration_test_pass_rate: "100%"
    performance:
      latency_p99: "< 100ms"
      throughput: ">= 1000 tps"
    safety:
      critical_vulnerability: 0
      data_race: 0

evaluation:
  layers:
    - unit_test
    - integration_test
    - e2e_test
    - benchmark
    - static_analysis
    - security_scan
  judge:
    model: "independent-checker"
    threshold: "all_layers_pass"

loop:
  max_iterations: 20
  strategy: "exponential_backoff"
```

然后自动生成整个 Agent Loop——Agent 自己想办法逼近 Goal，Evaluation 层判定它是否到了，Loop 负责节奏和收敛。

那时候，大家不再写 Prompt，而是写 Agent CRD。而 Agent CRD 里最重要的字段不是 `maker` 和 `checker` 选什么模型——**而是** `goal.metrics` **和** `evaluation.layers`**。**

听起来很科幻。但如果你观察 Claude Code、Codex、OpenHands、OpenAI Agent SDK、Anthropic Harness、Trellis 这些项目，会发现行业已经在朝这个方向移动。

* * *

## AI Native 软件工程团队会是什么样

很多人以为 AI 会替代工程师。我不这么看。

我觉得 AI 会让工程师越来越像 SRE——但不止于此。

过去，工程师写代码。未来，工程师设计循环。而再往后一步，工程师设计的是**目标与验证系统**。

过去你思考的是：函数怎么写。未来你思考的是：

-   目标怎么定义——把模糊的“优化支付系统”翻译成 `latency_p99 < 100ms, availability > 99.99%`
-   验证怎么设计——构建多层的 Evaluation Pipeline，让“完成”可以机器判定
-   状态怎么管理——让 Agent 的记忆不在脑子里而在仓库里
-   Agent 怎么协作——Maker、Checker、Reviewer 的权责边界在哪
-   循环怎么收敛——Termination Condition 怎么定义、Feedback 怎么喂回

我甚至怀疑，未来会分化出两个新角色：**Goal Engineer**（负责把业务意图翻译成 Agent 可收敛的形式化目标）和 **Evaluation Engineer**（负责构建 Benchmark、Sensor、判定标准，让 Agent 知道自己什么时候算“做完了”）。Prompt Engineer 会消失，不是因为 Prompt 没用，而是因为写 Prompt 这件事会被自动化——而定义 Goal 和 Evaluation 不会被自动化。

这是更高层次的工程问题，也是 Kubernetes 社区过去十几年一直在研究的问题。区别只在于，K8s 控制的是 Pod 的副本数，而你控制的是软件本身的正确性、性能、安全性和可维护性。

* * *

## 结语：AI Coding 的终点可能不是程序员，而是控制系统工程师

如果让我用一句话总结最近半年 AI Coding 的变化，我会这样说：

> Prompt Engineering 解决的是如何和模型说话，Context Engineering 解决的是如何给模型信息，Loop Engineering 开始解决真正的工程问题——如何让一个不可靠的执行器，在持续反馈中稳定地逼近目标。而再往前一步，Goal Engineering 要解决的是比这一切都更根本的问题：你那个“目标”本身，到底能不能被精确地定义和测量。

这也是为什么我越来越觉得，Loop Engineering 并不是一个新概念。它更像是控制论、状态机、反馈系统、Kubernetes Controller、Operator Pattern 这些老思想，在 AI Coding 时代的一次重新复活。

展开来看，理解这场变革有四个层次：第一层看到结构相似（Loop ≈ Operator），第二层看到实现相似（Agent ≈ Controller），第三层看到本质相似（Goal ≈ Spec，Evaluation ≈ Status），第四层——也是最重要的一层——意识到 **AI Coding 不是自动化写代码，而是自动化逼近目标**。一切自动化逼近目标的系统，无论叫 Controller 还是 Agent，最终都会回到控制论。

很多 AI 从业者觉得自己正在探索全新的世界。但如果你同时熟悉 Kubernetes、Operator、分布式系统和控制理论，你会发现一种强烈的既视感：

**AI Coding 正在重走 Kubernetes 过去十几年的演化路径。**

区别仅仅在于：Kubernetes 控制的是 Pod，而下一代 Loop Engineering 控制的，将是软件本身。而再往深处看，控制 Pod 和控制软件，它们的核心挑战其实是一样的——**Spec 是否定义正确，Status 是否真实反映系统状态，以及 Controller 是否持续把两者拉近。**

这也是为什么我觉得，AI Coding 最激动人心的未来，不是 Prompt Engineer 遍地开花，而是会出现一批 **Goal Engineer** 和 **Evaluation Engineer**——他们不再研究怎么跟模型说话，而是研究怎么把模糊的人类意图翻译成可收敛的形式化目标，以及怎么构建让 Agent 无法自我欺骗的验证系统。

而真正值得研究的问题，也许不是“哪个模型更强”，而是：

> 当软件开始自己修改自己时，我们该如何设计那个负责约束它、验证它、纠正它、最终信任它的控制循环——而这一切的前提是，我们得先想清楚：**“做完了”到底是什么意思。**

这个问题，可能才是未来十年 AI Native 软件工程最核心的问题。