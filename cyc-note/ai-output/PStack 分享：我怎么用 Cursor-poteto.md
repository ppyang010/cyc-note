---
title: "PStack 分享：我怎么用 Cursor"
author: "poteto（@poteto）"
zhihu_author: "出发向未来"
source: "https://zhuanlan.zhihu.com/p/2091544982477878358"
original_source: "https://x.com/poteto/status/2058975157503570132"
published: 2026-10-08T18:17:00+08:00
original_published: 2026-08-23
created: 2026-10-14
type: "文章阅读笔记"
summary_model: "gpt-6.1-sol"
tags:
  - AI/Agent
  - AI/Coding
  - Cursor
  - 多模型协作
  - 工程实践
aliases:
  - "PStack 与深度优先 Agent 编排"
  - "先建立信任，再扩大 Agent 并行"
---

# PStack 分享：我怎么用 Cursor

> [!info] 来源与整理说明
> - **原作者**：[@poteto](https://x.com/poteto)；**知乎发布者**：出发向未来。译者未在正文中单独署名，不将发布者直接认定为译者。
> - **阅读来源**：[知乎文章](https://zhuanlan.zhihu.com/p/2091544982477878358)，页面显示发布于 2026-10-08 18:17。
> - **原文日期**：中文译文说明标注为 2026-08-23；[X 原文链接](https://x.com/poteto/status/2058975157503570132)为文章所列，本次未另行读取核验。
> - **整理日期**：2026-10-14；**总结模型**：`gpt-6.1-sol`。
> - **笔记范围**：前半部分为 AI 整理，后半部分保留知乎页面可见文章正文、引用链接与 6 张本地化配图；移除了知乎自动生成的术语搜索跳转和重复列表符号，原文措辞及代码示例保留。

## 目录

- [[#核心结论]]
- [[#核心观点]]
  - [[#从命令行工具到面向任务的界面]]
  - [[#多 Agent 优先钻深，而不是铺广]]
  - [[#工程纪律是建立信任的基础]]
- [[#PStack 技能速查]]
  - [[#入口与核心模式]]
  - [[#常用技能与适用场景]]
  - [[#调试的基本方法]]
- [[#Benny 的软件维护闭环]]
  - [[#反馈分诊与证据收集]]
  - [[#复现、修复、验证与评审]]
  - [[#自动化的前置条件]]
- [[#可复用实践清单]]
  - [[#任务开始前]]
  - [[#执行与验收时]]
  - [[#任务结束后]]
- [[#阅读边界与个人启发]]
  - [[#哪些内容不能当成普遍结论]]
  - [[#对日常 Agent 编程的启发]]
- [[#关键摘录]]
- [[#延伸资源]]
- [[#关联笔记]]
- [[#原文剪藏]]
  - [[#开篇与 Cursor 使用体验]]
  - [[#用 Cursor 做 Cursor]]
  - [[#想快，先深]]
  - [[#禅与软件维护艺术]]
  - [[#原文引用链接]]

## 核心结论

> [!abstract] 一句话概括
> **Agent 编程的瓶颈不是生成代码，而是验证代码；先用严谨的工程流程建立单任务交付的可信度，再用多模型与多 Agent 扩大深度和自动化程度。**

1. **优先提高单个问题的解决质量，而不是同时开更多任务。** 多 Agent 更适合对同一问题探索不同解法、独立复现、交叉审查。
2. **把失败模式沉淀成可执行的方法。** Rule、skill、工具和长期记忆是补充 Agent 工程能力的手段，不应只靠临时提醒。
3. **没有验证闭环，就没有可信的自动化。** 必须能确认问题真实存在、修复确实生效，并留下便于人审阅的证据。
4. **代码越容易生成，维护、评审和人的注意力越可能成为瓶颈。** 并行有成本，不能仅用 Agent 数量或代码行数衡量产出。

## 核心观点

### 从命令行工具到面向任务的界面

作者原先偏爱 Claude Code，后来在 Cursor 面试与日常工作中，认可了三个体验：

- **多模型协作方便**：可按任务切换模型，并使用不同模型的子代理。例如，作者以 Opus 做前端、Codex 做系统层为自己的使用方式。
- **上下文压缩体验更顺畅**：作者主观认为 Cursor 的压缩更快，减少了对上下文用量的持续关注。
- **GUI 提供额外交互能力**：内置浏览器、Design Mode 等让运行中的应用与设计修改更直观，而非单纯把多个终端装进窗口。

更深层的问题是：大量人在 CLI 外再造编排工具，说明有未被满足的编排需求；但**更好的编排不只是同时展示更多 Agent，而是让人能放心地把更完整的任务交出去**。

### 多 Agent 优先钻深，而不是铺广

作者提倡的“深度优先”不是取消并行，而是把并行投入到一个或少数几个问题上。

| 并行方式 | 主要目的 |
| --- | --- |
| 同题多解、N 选一 | 对比方案，选择较优解或组合各自优点 |
| 不同模型对抗式评审 | 挑战假设、发现遗漏与错误 |
| 多 Agent 独立尝试复现 | 确认问题是否真实、稳定，以及触发条件 |
| 按任务特点选模型 | 利用模型之间不同的长处与短处 |

相反，同时让很多 Agent 分别推进互不相关的任务，会把状态追踪、上下文切换和验收压力集中到人身上。**如果每个 Agent 都不可信，增加并行度只是更快地产生需要检查和维护的代码。**

### 工程纪律是建立信任的基础

作者把 Agent 类比为能力强、但容易遗忘和犯错的新同事。需要教给它的不是“多写一点”，而是：

- 先理解代码库和工作方式，再开始修改。
- 先建立假设和收集证据，而不是凭感觉猜解法。
- 用测试、运行时观测、性能分析、实际产品操作验证结果。
- 把反复出现的失败模式转化为 skill 和 playbook，持续改进。

PStack 的目标由此不是最大化代码量，而是**用尽可能少的代码取得最大的有效成果**。

## PStack 技能速查

### 入口与核心模式

- 原文将 PStack 描述为作者开源的 skill 与工程原则集合。
- 插件入口：[Cursor Marketplace](https://cursor.com/marketplace/cursor/pstack)。
- 文章给出的安装命令如下；**本次仅记录，未安装或执行**：

```text
/add-plugin pstack
```

核心入口 `/poteto-mode` 会根据任务选择适用的 playbook。原文覆盖的场景包括：skill 编写与评测、自主工作、bug 修复与运行时取证、功能开发、视觉对齐与原型。

### 常用技能与适用场景

以下含义均按文章描述整理，未逐项核验当前插件实现。

| 技能 | 适用场景 |
| --- | --- |
| `/poteto-mode` | 根据任务选择严谨的执行方法，作为统一模式入口 |
| `/how` | 理解某个子系统实际上如何运行 |
| `/why` | 结合版本控制、工单、文档、聊天和可观测数据追溯设计原因 |
| `/architect` | 跨函数边界开发前，先明确类型和数据结构 |
| `/arena` | 对同一任务并行尝试多种方案，比较并择优 |
| `/interrogate` | 使用不同模型做对抗式评审 |
| `/tdd` | 修 bug 时先写失败测试，再实施修复 |
| `/unslop` | 清理 AI 生成文字，使表达更自然 |
| `/reflect` | 长对话后复盘，持续改进 skill |
| `/figure-it-out` | 为不常见任务设计严谨、可审计的执行方法 |
| `/show-me-your-work` | 将决策记录为可审阅的 TSV 留痕 |
| `/automate-me` | 从近期对话中提炼个人工作方式，起草自定义模式 |
| `/orchestrate` | 通过 Cursor SDK 递归组织 Agent，处理复杂任务；见 Benny 案例 |

### 调试的基本方法

原文提出的调试思路可以概括为：

1. 对可能原因提出若干假设。
2. 有条理地排除假设，像二分查找一样缩小问题空间。
3. 难以复现时，设计条件主动触发问题。
4. 加入必要的插桩或日志，观察程序运行状态。
5. 找到根因后修复，再验证原问题确实消失。

这是一套应被编码进 playbook 的工程方法，而不是让 Agent 不断尝试“看起来可能有用”的补丁。

## Benny 的软件维护闭环

### 反馈分诊与证据收集

Benny 是作者在 Cursor 内部探索的软件维护机器人，依赖定时或事件触发的 Cloud Agents。

第一阶段不是立即写代码，而是让问题变得可调查：

- 收集员工反馈，理解图片和视频附件。
- 复现步骤不清楚时，向报告人追问。
- 查看代码与 Git 历史，寻找可能引入回归的变更。
- 检索 Slack 中的相关反馈，以及 Notion 中的设计与产品决策。
- 区分真正的 bug 与原本就如此设计的行为，整理调查结果并形成工单。

### 复现、修复、验证与评审

第二阶段由另一个 Benny 接手，通过 `/orchestrate` 组织子任务：

```text
用户反馈
  → 补齐信息与调查分诊
  → 形成带证据的工单
  → 在真实运行环境中复现
  → 稳定复现后实施修复
  → 多个 worker 验证修复与验收标准
  → 录制修复前后的视频
  → 提交附带证据的 PR，交给人评审
```

其中最重要的证据包括：

- **行为问题**：在可操作的产品环境中复现，并进行修复前后对比。
- **性能问题**：对比修复前后的 CPU trace 和堆快照。
- **最终验收**：对照原工单确认问题被解决，不只相信 worker 的完成声明。

### 自动化的前置条件

文章强调：只有能够放心地让一个 Agent **从头到尾负责一个问题，包含验证**，才有条件将这一环自动化，再逐步放大规模。

作者明确说明 Benny 仍在开发中，因此这里展示的是实践案例与演进方向，不是已经解决所有维护问题的成熟方案。

## 可复用实践清单

> [!tip] AI 整理的行动建议
> 以下是根据文章提炼的实践清单，不是作者原文逐字列出的规定。

### 任务开始前

- [ ] 明确现象、预期行为、环境、复现步骤和验收标准。
- [ ] 确认 Agent 具备观察与操作真实运行环境的工具，而不只是读取代码。
- [ ] 先判断单 Agent 是否足够；如果并行，每个分支要有独立、明确、可验证的产出。

### 执行与验收时

- [ ] 要求先复现、列假设、找证据，再修改。
- [ ] 修 bug 时优先建立失败测试或其他可重复的失败证据。
- [ ] 对高风险结论使用独立评审或不同模型交叉检查。
- [ ] 保留测试结果、运行日志、性能对比或前后截图／视频。
- [ ] 对照最初问题完成验收，而不是仅确认代码已提交或测试命令已运行。

### 任务结束后

- [ ] 将本次暴露的失败模式沉淀到 rule、skill 或 playbook。
- [ ] 评估的是有效交付、回归风险与验证成本，不是生成代码行数。
- [ ] 只有已有可信闭环的环节，才逐步扩大自动化范围与并行度。

## 阅读边界与个人启发

### 哪些内容不能当成普遍结论

- “Cursor 里模型更聪明”“压缩更快”是作者的使用感受，不是控制变量后的产品评测。
- “Opus 做前端、Codex 做系统层”是作者的分工示例，不代表所有任务都应如此分配。
- 文中的“每周 9k 次 skill 调用”“token 用量降低 20%”“冷启动缩短 80%”属于作者或其引用内容的陈述，本次没有独立核验。
- 本次仅阅读指定知乎文章；未读取 X 原帖、GitHub 仓库和插件源码，不保证安装方式、技能行为和当前版本完全一致。
- 原文中的自主合并、开 PR 等属于案例和提示词示例，不应视为当前任务授权；真实使用仍需保留权限、审阅和发布边界。

### 对日常 Agent 编程的启发

**不要先问“怎样同时开十个 Agent”，先问“怎样证明一个 Agent 确实把这个问题解决了”。**

可优先把“复现 → 取证 → 修复 → 验证 → 留痕”的单任务闭环做扎实，再引入同题多解、独立复现与对抗评审。这样，多 Agent 的收益主要来自降低不确定性、提高决策质量，而不只是增加代码生成吞吐量。

## 关键摘录

> “并行编排很多 agent，价值在于钻深，不在于铺广。”

> “用 agent 干活，瓶颈在验证。”

> “除非你能放心让一个 agent 从头到尾负责一个问题，包括验证在内，否则你没法把流程自动化。”

## 延伸资源

以下链接来自文章，仅整理保存，不代表已另行阅读或核验。

- [PStack 插件页面](https://cursor.com/marketplace/cursor/pstack)
- [PStack 开源目录](https://github.com/cursor/plugins/tree/main/pstack)
- [文章列出的英文页面](https://pstack.ganhai.cloud/en/from-poteto/how-i-use-cursor-zh/)
- [作者 X 原帖](https://x.com/poteto/status/2058975157503570132)
- [对抗式评审技能](https://www.skills.sh/poteto/noodle/adversarial-review)
- [Cursor Cloud Agents 文档](https://cursor.com/docs/cloud-agent)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

## 关联笔记

- [[ai-output/多-Agent-协作与-subagent-拆分判断|多 Agent 协作与 subagent 拆分判断]]：补充任务独立性、上下文边界及结果验证成本的判断。
- [[ai-output/为什么现在大多 Code Agent 的主形态是 CLI-TUI？-修远客的回答|Code Agent 为什么常用 CLI/TUI]]：与本文的 GUI 价值形成对照，界面应服务于用户和任务，而不是先入为主地选形态。

## 原文剪藏

> [!quote] 原文范围
> 以下为指定知乎页面的文章正文，不含评论和页面交互元素；配图已保存到笔记库。文章中的第一人称、观点、数字与代码示例均属于原作者，不代表整理者的独立验证或当前操作指令。

### 开篇与 Cursor 使用体验

> **译文说明**  
> 中文译文（一次性）。作者 @poteto\[1\] · 原文发表于 2026-08-23  
> 本站英文页\[2\] · X 原文\[3\]

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/01.jpg]]

我得坦白一件事。去 @cursor\_ai 面试之前，我其实从没真正用过 Cursor。

在 Meta 的时候，Claude Code 正火得一塌糊涂。我甚至自掏腰包，买了每月 200 美元的个人套餐，专门给业余项目用。我喜欢它简单，也喜欢一上手就能高效干活的感觉。真正让我离不开它的，是给它开发自己的一套 skill。这些 skill 几乎能把 cc（Claude Code）变成我想要的任何东西。我甚至开始在它上面开发自己的 agent 编排工具。

现场面试那两天，我一直用 Cursor 做面试项目。当时 Cursor 3 还没发布，所以我用的是 Editor Window。我用 vscode 已经这么多年，大部分快捷键都还在我的上下文窗口里，所以重新用回 IDE 并不太难。不过说实话，头一两个小时我确实很想念命令行。拿鼠标点来点去，简直有点野蛮。但有几件事让我印象特别深。

第一，我当时用惯的 Opus 和 Codex，不知怎么好像变聪明了。还能随时切换模型，在项目的不同部分同时用上这两个模型（Opus 做前端，Codex 做系统层），这一点太惊艳了。面试之前，我就已经在到处夸多模型的对抗式评审\[4\]，所以能直接在界面里这么做，感觉顺理成章。更棒的是，还能拉起不同模型的子代理，一次对话里就能同时拿到两边的长处。

第二，compaction（上下文压缩）快得离谱。用 cc 的时候，我早就习惯了一次 compaction 要好几分钟，所以总是提心吊胆地盯着上下文和套餐用量。因此 Cursor 的速度让我大吃一惊。快到我基本再也不用去看上下文用了多少。它就是好用。反观 cc，compaction 之后我常觉得模型一下子变得特别笨。

第三，我发现 GUI 能比 TUI（终端里的文本界面）多给出很多东西。直接在 Cursor 的浏览器里打开自己的应用，再用 Design Mode 改设计，感觉很直观。这也让我开始琢磨，专门打造的界面能让 agent 编程高效多少。

### 用 Cursor 做 Cursor

三月底入职以后，我主要在做 Cursor 3 的 Agent Window，平时也拿它当主力工具。我仍然觉得 cc 是个很酷的产品，团队也很棒。但我发现，正因为它简单，大家总想在它外面再包一层自己的抽象。在上一份工作里，感觉每周都有人发布一个基于 cc 的新内部编排工具。

@bcherny 经常讲「latent demand」（潜在需求）这个概念：

> 「做产品有个很老的概念，叫 latent demand……你把产品做得能随便改，足够开放，让大家能把它滥用到别的用途上。然后你看大家怎么滥用，再照着去做。」

说的就是这个！大家不约而同地去做编排工具，正好暴露了 latent demand 在哪：用命令行的时候，编排者就是你这个人。

但我用过的每一种 agent 工作流，重点都放错了。在 GUI 里同时跑好几个命令行工具，完全没抓住要害。我感兴趣的做法，是建立对 agent 的信任。

我以前当过工程经理，很快就意识到，管理 agent 跟组建一支真人工程团队很像。新人入职要有人带，让他们熟悉代码库，也熟悉活是怎么干的。他们入职时就已经预训练好了，身上带着从过往经历里学来的技能。随便举几个：怎么调试，怎么写高质量的代码和测试，怎么沟通。

而 agent 就像永远失忆、永远犯傻的新人。你跟它们说过的话，它们记不住，也从来没真正学会过什么新东西。但我们可以给它们配上 rule、skill、工具和长期记忆，大致补上这一块。它们能干，但也蠢，而且非常好教。在我看来，它们的每一种失败模式都是机会，让我把自己懂的那套深入、严谨的工程做法全教给它们。

因为一旦没有严谨，agent 就会一味讨好你，不择手段地写出你要的代码。而且好家伙，它能写，也真会写，一写就是一大堆。简单粗暴地并行，只会让它们更快地产出 slop（粗制滥造的代码）。

> 我越来越确信，并行编排很多 agent，价值在于钻深，不在于铺广。你要在一个或少数几个问题上钻得更深，才能把拿到好结果的机会拉到最大：

- N 选一的赛跑，挑出最好的解法
- 对抗式评审
- 让多个 agent 一起尝试复现报上来的问题
- 不同类型的活交给不同的模型

> 借 @mattpocockuk 的话说，「代码并不便宜」。  
> 这比让一堆 agent 分头处理 10 个不同的问题、自己在它们之间来回切换上下文要强。瓶颈还是在我身上。我得记住每个 agent 在干什么，还得把这些都装在自己的上下文窗口里。我觉得以后会有更好的界面来解决这个问题。  
> 还有信任这个因素。信任越多，你在视角的梯子上就能爬得越高。信任很少的时候，你只能对每一个 agent 都事无巨细地盯着。能放手了，你就能把更多事交出去。这跟管人一模一样！  
> 原帖：@poteto\[5\]

### 想快，先深

我确实觉得，agent 编排是能做出成效的。但我们得按深度优先的路子来。

我把 pstack\[6\] 开源了。这是我个人的一套 skill 和工程原则，我每天开发 @cursor\_ai 都在用。这些 skill 的早期版本，是我在业余项目里开始写的，之后一直在打磨。

在这里获取： [cursor.com/marketplace/](https://cursor.com/marketplace/cursor/pstack)

```
/add-plugin pstack
```

这些 skill 已经是 Cursor 团队最常用的一批了，所以能分享给大家，我很兴奋。

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/02.jpg]]

*Cursor 公司内部的排行榜。这周我的 skill 用了 9k 次！*

pstack 用多个模型，教 agent 变得更严谨。我把自己观察到的所有失败模式，都做成了 skill。这个插件的核心是 /poteto-mode。它是一个高阶 skill，会针对手头的任务，给 agent 挑一份该照着走的 playbook。目标不是把代码行数堆到最多，恰恰相反，是用最少的代码做出最大的成效。

要做到严谨，就要像有经验的工程师那样处理问题。比如调试，一个很好的办法是对问题空间做二分查找。你先对可能出了什么事提几个假设，再有条理地逐个排除，直到越来越接近真正的根因。如果问题难以复现，可以想办法人为地逼这个 bug 出现。也可以加插桩或 console 日志，在程序运行时查看它的状态。

这些步骤合起来就是一份 playbook，agent 可以照着它彻底排查问题，而不是瞎猜。你要是由着它们，它们很乐意瞎猜。pstack 自带很多 skill 和 playbook，让你用同样的严谨程度做软件工程。我目前有这些方面的 playbook：

- skill 编写与评测
- 自主工作
- bug 修复与运行时取证
- 功能开发
- 视觉对齐与原型
- 还有更多

需要严谨的时候，就在提示词前面加上 /poteto-mode。例如：

```
/poteto-mode this pr has a subtle bug where the scroll drifts every 750ms even when idle. repro first, then fix and verify.
/poteto-mode a big list takes a second or two to load even though we virtualize. run a cpu trace and tell me why.
/poteto-mode build a small feature behind a feature flag. verify it really works.
/poteto-mode build two prototypes of the markdown renderer so we can compare. spawn an agent for each.
/poteto-mode open source these skills as a plugin. nothing internal leaks, work in a temp dir, show me the dependency graph first.
/poteto-mode i'm going to bed. land the stack even if ci flakes. i want everything merged by morning.
/poteto-mode the row spacing is too tall when this flag is on. the second image is correct. repro and fix until it matches.
```

其他 skill 你也可以按需调用：

- /how：你想有人带你走一遍，弄清某个子系统实际是怎么运作的。
- /why：你想知道某样东西为什么做成这样。它会用你手头可用的 MCP，并行查询每一类证据（版本控制、问题跟踪、长文档、即时聊天、基础设施可观测性、错误追踪、分析数据仓库）。
- /architect：你要写的代码会跨越函数边界，想先把类型和数据结构定下来。
- /arena：你想对同一件事并行做 N 次尝试，再从每一份里挑出最好的部分。
- /interrogate：你想让几个不同的模型对某样东西做对抗式评审。
- /tdd：你在修 bug。先写一个会失败的测试，再写修复。
- /unslop：你在清理任何一种 AI 写出来的文字。它会让这些文字说人话。
- /reflect：长对话之后，你想持续改进自己的 skill。
- /figure-it-out：要做点不寻常的事？它会为这个任务设计一份严谨、可审计的 playbook。
- /show-me-your-work：你想留下一条可供审阅的决策 trail（留痕记录）。它把决策记进一个 tsv 文件，你可以直接把这个文件提交进仓库。

最后，你还可以用 /automate-me 做一个自己的 mode skill。它会挖掘你最近的对话记录，按你的工作方式起草一个 your-mode skill，底层走的仍然是 pstack。

pstack 能用在任何 agent 编程工具里，但在 Cursor 这类多模型工具里效果尤其好。很多 skill 都用多模型工作流，利用每个模型各自独特的长处和短处。这也是 agent 编排，只不过走的是深度优先，而不是广度优先。

用 agent 干活，瓶颈在验证。它们能很快写出大量代码。可要确认这些代码全都正确，难度极高。等你能做到这一步，真正的 agent 并行才有可能实现，就像软件行业的黑灯工厂那样。

但首先，我们得往深里走，做到严谨。我觉得，要走到那一步，靠的是把信任一点点调高。

试试 pstack\[7\]，告诉我你的想法。

### 禅与软件维护艺术

有了这些 skill，我写代码时更有底气。但现在所有代码都由 agent 来写，维护代码成了一场噩梦。bug、性能问题、功能需求，照样得花时间一个个处理。而且现在要处理的东西多太多了！

我在 Cursor 内部大量使用 Cursor automations。它们是 cloud agent，可以定时运行，也可以由事件触发，比如 Slack 频道里来了新消息。我的机器人 Benny 就是一个例子。我给他装上了和 pstack 里一样的 skill。

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/03.jpg]]

*Benny 的各种化身*

Benny 还在开发中，但我的设想是，把软件维护流程尽可能多地自动化。思路是这样的：既然我们已经有信心靠 pstack 把大多数问题「一次搞定」，而且相当确定 PR 质量很高，那反馈这一环肯定也能自动化。

这座工厂的第一道工序是 triage（分诊），也就是向员工收集 bug 报告的相关信息。我们自己大量 dogfood（自家产品自己先用）Cursor，所以每个候选发布版都会收到很多员工反馈。Benny 看得懂图片和视频附件，会用 pstack 的 skill 探索代码库。如果复现步骤不清楚，他还会找报告人聊，问清楚怎么复现。

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/04.jpg]]

*Benny 在追问更多信息*

这是 bug 报告流程里很重要的一环。没有清楚的复现步骤，也不知道到底哪里坏了，agent 就只能瞎猜解法。我们得让它们清楚地知道，问题到底坏在哪里、是怎么坏的。

triage 完成后，Benny 会建一张工单，写上他的 finding（调查结果）。他会看代码，翻 git 历史找最近引入的回归，在 Slack 里找关于同一个 bug 的其他消息，甚至去 Notion 查设计和产品上的决策，看这个功能本来该怎么工作。这到底是 bug，还是本来就设计成这样？

工单建好后，另一个 Benny 机器人会接手，用的是我做的另一个 skill，叫 /orchestrate。

> 推出 /orchestrate。这个 skill 用 Cursor SDK 递归地拉起 agent，帮你攻克最有野心的任务。  
> 我们已经用它：

- 对内部 skill 做 autoresearch（让 agent 自动跑实验、反复改进），token 用量降低 20%，评测成绩还提高了
- 把内部后端的冷启动时间缩短了 80%

原帖：@cursor\_ai\[8\]

首先，他会直接操控电脑，试着复现问题。Cursor 的 Cloud Agents\[9\] 能在云端运行 Cursor 本身，在那里操作桌面、点击界面、发送键盘输入。背后用的是我做的另外一些 skill。它们用 CDP\[10\] 这类协议或其他等效手段，以编程方式控制我们的产品。

这样我们就能证明，这份 bug 报告到底能不能复现。如果能稳定复现，他接着就会尝试修复。如果是性能问题，Benny 可以在修复前后各抓一份 CPU trace 和堆快照。子规划 agent 会再拉起更多 worker，用 pstack 的 skill 验证修复，并对照工单检查问题是不是真的修好了。

这一次运行还会拉起更多 worker，录下修复前后的视频。最后由一个 worker 开 PR 提交评审，描述里附上视频。

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/05.jpg]]

*最近一次运行，问题成功复现并修好了*

这一切都还在开发中，要做的事还多得很。但想到有一支 agent 团队，能在我睡觉或忙别的事时帮我有把握地修 bug，我就很兴奋。让代码评审跟得上规模，是另一个大方向。我觉得 Cursor 接下来会推出一些很酷的功能来帮忙。

但要搭建你自己的软件工厂，关键在于信任。除非你能放心让一个 agent 从头到尾负责一个问题，包括验证在内，否则你没法把流程自动化。pstack 这类插件能让 agent 有更深的工程功底。用它们把信任调高，你就可以开始攻克更有野心的问题。对还信不过的 agent 搞并行，是在大把浪费 token，还会往代码库里塞进更多 slop。

感谢阅读！

顺便提醒一句，如果你在意花费：同时用多个 agent，尤其是 frontier（最前沿的那一档）模型，会烧掉大量昂贵的 token。

我希望以后的 Composer 能改变这一点。又快又便宜，还很强

### 原文引用链接

`[1]` @poteto: *[x.com/poteto](https://x.com/poteto)*  
`[2]` 本站英文页: *[pstack.ganhai.cloud/en/](https://pstack.ganhai.cloud/en/from-poteto/how-i-use-cursor-zh/)*  
`[3]` X 原文: *[x.com/poteto/status/205](https://x.com/poteto/status/2058975157503570132)*  
`[4]` 对抗式评审: *[skills.sh/poteto/noodle](https://www.skills.sh/poteto/noodle/adversarial-review)*  
`[5]` @poteto: *[x.com/poteto/status/204](https://x.com/poteto/status/2048092593087721736)*  
`[6]` pstack: *[github.com/cursor/plugi](https://github.com/cursor/plugins/tree/main/pstack)*  
`[7]` pstack: *[cursor.com/marketplace/](https://cursor.com/marketplace/cursor/pstack)*  
`[8]` @cursor\\\\\_ai: *[x.com/cursor\_ai/status/](https://x.com/cursor_ai/status/2052432778743210127)*  
`[9]` Cloud Agents: *[cursor.com/docs/cloud-a](https://cursor.com/docs/cloud-agent)*  
`[10]` CDP: *[chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/)*

![[ai-output/assets/pstack-how-i-use-cursor-2091544982477878358/06.jpg]]