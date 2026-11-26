---
title: "superpowers 目前 skills/ 目录下 14 个 skills 的逐个解读"
author: "猫咪不吃鱼"
source: "https://zhuanlan.zhihu.com/p/2039313824822636897"
site: "知乎"
published: 2026-05-17
created: 2026-11-26
summary_model: "gpt-6.2-sol"
tags:
  - 阅读笔记
  - Superpowers
  - AI编程
  - 软件工程
---

# Superpowers 14 项技能逐个解读

原文由猫咪不吃鱼于 2026 年 5 月 17 日发布。笔记根据文章所述的技能集整理。总结模型为 `gpt-6.2-sol`。[知乎原文](https://zhuanlan.zhihu.com/p/2039313824822636897) · [Superpowers 项目仓库](https://github.com/obra/superpowers)

## 目录

- [[#主流程]]
- [[#14 项技能速查]]
- [[#执行路径和并行条件]]
- [[#团队采用时的取舍]]
- [[#原文剪藏]]
  - [[#1. using-superpowers]]
  - [[#2. brainstorming]]
  - [[#3. writing-plans]]
  - [[#4. using-git-worktrees]]
  - [[#5. subagent-driven-development]]
  - [[#6. executing-plans]]
  - [[#7. test-driven-development]]
  - [[#8. systematic-debugging]]
  - [[#9. verification-before-completion]]
  - [[#10. requesting-code-review]]
  - [[#11. receiving-code-review]]
  - [[#12. dispatching-parallel-agents]]
  - [[#13. finishing-a-development-branch]]
  - [[#14. writing-skills]]
  - [[#这 14 个 skills 的关系图]]
    - [[#第一层：入口与规则]]
    - [[#第二层：需求到计划]]
    - [[#第三层：执行与质量控制]]
    - [[#第四层：调试、验证、收尾]]
  - [[#我建议你怎么用]]
    - [[#如果你用 Codex / Claude Code 做真实项目]]
    - [[#如果你是团队使用]]
  - [[#最终判断]]
  - [[#工作树清理附录]]

## 主流程

需求澄清 → 设计确认 → 计划拆解 → 隔离开发 → 测试驱动实现 → 代码审查 → 验证 → 分支收尾。

前一环节的产出是后一环节的依据。设计规格写明目标、边界和验收条件，实施计划把规格变成可逐步验证的任务。动手前确认隔离工作区和测试基线，完成时用本次运行的测试或构建结果证明交付状态。

## 14 项技能速查

| 技能 | 使用时机 | 要点 |
| --- | --- | --- |
| `using-superpowers` | 开始任务时 | 判断哪些技能适用，并先加载对应技能。 |
| `brainstorming` | 新功能、行为变化或需要明确方案时 | 查看项目上下文，逐个澄清问题，比较方案并确认设计，再写规格文档。 |
| `writing-plans` | 规格已确认、工作涉及多步时 | 写清文件路径、改动内容、测试命令和预期结果，逐项检查计划是否覆盖规格。 |
| `using-git-worktrees` | 准备开始实现时 | 检查当前是否已经隔离，优先使用平台的工作树能力，随后安装所需依赖并记录测试基线。 |
| `subagent-driven-development` | 已有计划且可用子代理时 | 每项任务用新的实现子代理，先查规格符合性，再查代码质量。修复发现的问题后复审。 |
| `executing-plans` | 由当前或独立会话执行书面计划时 | 先审查计划，再按任务逐项实施和验证，全部通过后进入收尾。 |
| `test-driven-development` | 实现新行为、修复缺陷或重构时 | 让测试先因预期原因失败，用最小实现让它通过，再在测试保持通过的情况下重构。 |
| `systematic-debugging` | 发现缺陷、构建失败或行为异常时 | 复现并追踪根因，对比正常模式，单独验证假设。连续三次修复失败时，重新评估架构假设。 |
| `verification-before-completion` | 声称完成、修复或通过前 | 运行能证明该结论的验证命令，读完整输出和退出码，再报告状态。 |
| `requesting-code-review` | 任务或主要功能完成、合并前 | 给审阅者明确的规格、变更范围和检查重点，按严重程度处理问题。 |
| `receiving-code-review` | 收到审查反馈时 | 对照代码库核实建议，澄清歧义后逐项修改和测试。 |
| `dispatching-parallel-agents` | 多个独立问题可同时推进时 | 每个问题域交给一名子代理，事先划清范围和写入边界。 |
| `finishing-a-development-branch` | 实现结束、准备交付时 | 先验证测试和基础分支，再决定本地合并、创建 PR、保留或放弃。放弃需要明确确认，清理前核实工作树归属。 |
| `writing-skills` | 创建或修改技能时 | 先用场景记录无技能时的表现，再写最小指令并复测。描述聚焦触发条件。 |

## 执行路径和并行条件

- **按计划分派**。`subagent-driven-development` 的分派单位是计划里的任务，每项任务都经历规格和质量两轮审查。由单一会话执行时，用 `executing-plans` 逐项验证进度。
- **按独立问题并行**。`dispatching-parallel-agents` 适用于问题可以各自复现、定位和修复，且写入范围互不冲突的情况。多个失败可能源于同一个问题、依赖同一份状态或涉及同一批文件时，先理清依赖关系。

## 团队采用时的取舍

作者建议在团队协作和生产代码中完整采用这条流程，在机械小改动或一次性探索中按任务选择。团队可以提前明确哪些改动需要设计确认、测试如何覆盖、规格和计划放在哪里，以及合并前需要哪些验证。只读分析可以在现有工作区直接完成。

另一篇阅读笔记梳理了技能加载机制与工作流。[[ai-output/Superpowers源码分析|Superpowers源码分析]]

## 原文剪藏

最核心的价值不是某个单独 skill，而是这条链路：

**需求澄清 → 设计确认 → 计划拆解 → 隔离开发 → TDD → review → 验证 → 收尾**

下面是对 obra/superpowers 目前 skills/ 目录下 14 个 skills 的逐个解读，以及我对“是否必须安装、是否必须使用”的判断。 [Superpowers](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=Superpowers&zhida_source=entity) 自己的定位是：给 coding agent 的完整软件开发方法论，由一组可组合 skills 和初始指令组成； **它的基本工作流是先澄清需求、写设计、写实施计划、TDD 实现、代码审查、验证、最后合并/PR/清理** 。

> 注意：要经常更新skills的代码版本和自己结合实际使用，将自己的经验和要求增加到skills，以便更好的编程和业务准确性，最好是将自身业务的要求单独作为skills引入到编程工具里；

---

**但如果你把 AI coding agent 当“长期工程助手”使用，我建议安装。** 尤其是你用 Claude Code、 [Codex CLI](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=Codex+CLI&zhida_source=entity) /App、Cursor、 [Gemini CLI](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=Gemini+CLI&zhida_source=entity) 、OpenCode、 [GitHub Copilot CLI](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=GitHub+Copilot+CLI&zhida_source=entity) 这类工具做真实项目开发时，Superpowers 的价值是把 AI 从“马上写代码”约束成“先理解、再设计、再计划、再 TDD、再 review、再验证”的流程。README 也明确说安装要按不同 harness 分别安装；例如 Claude Code、Codex、Cursor、Gemini、OpenCode、Copilot CLI 都有对应安装方式。([GitHub](https://github.com/obra/superpowers))

**是否必须使用？分三层看：**

| 层面 | 判断 |
| --- | --- |
| 技术层面 | 不必须。没有它，AI coding agent 也能写代码。 |
| 工程质量层面 | 对复杂项目，强烈建议。它强制 TDD、审查、验证，能减少“AI 自信但没验证”的问题。 |
| Superpowers 自身规则层面 | 一旦安装并启用，它的 using-superpowers 明确要求：只要有 1% 可能适用，就必须先调用相关 skill；README 也说这些是 mandatory workflows, not suggestions。(GitHub) |

我的建议是： **重项目安装，轻任务选择性使用；团队协作/生产代码建议默认启用；纯探索、一次性原型可以不用或显式绕开。**

---

### 1. using-superpowers

**作用：Superpowers 的入口规则。**

这个 skill 不是某个开发动作，而是“调度所有 skills 的总开关”。它要求 agent 在任何任务开始前先判断是否有相关 skill；只要有一点可能适用，就要先调用 skill，而不是凭经验直接干。它还规定了优先级：用户明确指令最高，Superpowers skills 其次，默认系统行为最低。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/using-superpowers/SKILL.md))

**它解决的问题：** AI 很容易觉得“这个很简单，不用流程”，然后跳过需求澄清、测试、验证。`using-superpowers` 专门防这种自我合理化。

**适合场景：**

- 每次打开 coding agent；
- 开始任何开发、调试、review、计划任务；
- 防止 agent 忘记用 TDD、debugging、verification 等流程。

**是否必须：** 如果你安装 Superpowers， **这个是事实上的必需入口** 。不用它，后面的 skills 很容易不会被触发。

**我的评价：** 它很强硬，但这正是 Superpowers 的核心价值：不是多给 agent 一些建议， **而是让 agent 形成“先查流程，再执行”的习惯** 。

---

### 2. brainstorming

**作用：写代码前做需求澄清和方案设计。**

它要求在任何创意/功能/行为修改之前，先理解项目上下文、逐个提问、提出 2–3 个方案、分段展示设计并获得用户确认，然后把设计写成 [spec](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=spec&zhida_source=entity) 文档，默认保存到 `docs/superpowers/specs/YYYY-MM-DD--design.md`。它明确禁止在设计获批前写代码或进入实现。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/brainstorming/SKILL.md))

**核心流程：**

1. 探索项目上下文；
2. 必要时提供视觉辅助；
3. 一次问一个澄清问题；
4. 给出多个方案和权衡；
5. 分段展示设计；
6. 写设计文档；
7. 自检 spec 是否有占位、矛盾、歧义；
8. 让用户 review；
9. 转入 `writing-plans`。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/brainstorming/SKILL.md))

**它解决的问题：**

- AI 还没理解需求就开始写代码；
- 用户以为自己说清楚了，但其实关键约束没说；
- 小需求里隐藏了大架构问题；
- agent 做了用户并不想要的东西。

**是否必须：** 对“新功能、行为变化、组件构建、复杂修改”非常值得用。 但对极小的机械修改，比如“把错别字改掉”“重命名一个变量”，可能太重。

**我的评价：** 这是 Superpowers 最有价值的 skill 之一。它牺牲一点速度，换来更少返工。尤其适合需求不确定、影响面较大的任务。

---

### 3. writing-plans

**作用：把已确认的 spec 变成可执行的详细实施计划。**

它要求计划足够细，假设执行者不了解代码库、测试品味也不可靠。因此计划必须包含：要改哪些文件、完整代码、测试命令、预期输出、每个任务的 2–5 分钟小步骤、TDD 步骤、频繁 commit。默认保存到 `docs/superpowers/plans/YYYY-MM-DD-.md`。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/writing-plans/SKILL.md))

**关键要求：**

- 每一步都要有具体内容；
- 不能写 `TBD`、`TODO`、“添加适当错误处理”这种空话；
- 代码步骤必须给完整代码；
- 测试步骤必须给命令和预期输出；
- 最后要自检 spec 覆盖率、占位符、类型一致性。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/writing-plans/SKILL.md))

**它解决的问题：**

- “实现这个功能”太宽泛，agent 执行时会乱跑；
- 计划没有文件路径和验证命令，无法可靠交给 subagent；
- 一次做太大，review 困难；
- 没有 TDD 节奏。

**是否必须：** 如果你要让 agent 做多步开发， **强烈建议必须用** 。 如果只是问一个概念、读一段代码，不需要。

**我的评价：** 这是把 AI coding 从“聊天式开发”变成“任务流水线”的关键。它的计划格式有点啰嗦，但非常适合 subagent 执行。

---

### 4. using-git-worktrees

**作用：开始实现前创建或确认隔离工作区。**

它的核心原则是：先检测是否已经在隔离 workspace；如果没有，优先使用平台原生 worktree 工具；没有原生工具时再用 `git worktree`。它还要求自动安装依赖、跑 baseline tests，确认起点干净。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/using-git-worktrees/SKILL.md))

**它解决的问题：**

- AI 直接在主分支上乱改；
- 当前工作区有用户未提交改动，被 agent 污染；
- 测试一开始就是坏的，后面分不清是原本坏还是 AI 改坏；
- 手动 `git worktree` 和平台原生隔离机制冲突。

**是否必须：** 对真实项目开发，尤其是多步实现、PR、实验性改动， **建议必须用** 。 对只读分析、解释代码、不改文件，不需要。

**我的评价：** 这是团队工程里非常实用的 skill。它不提升模型智能，但降低了“AI 把你的工作区搞乱”的风险。

---

### 5. subagent-driven-development

**作用：按照实施计划，每个任务派一个新 subagent 执行，并做两阶段 review。**

它适用于已经有 implementation plan，并且任务大多相对独立、希望在当前 session 连续执行的场景。每个任务先派 implementer subagent，然后派 spec reviewer 检查是否符合规格，再派 code quality reviewer 检查质量。它明确说不要在任务之间反复问用户“要继续吗”，除非遇到 blocker、真正的歧义，或者所有任务完成。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/subagent-driven-development/SKILL.md))

**核心模式：**

- 每个任务新鲜上下文；
- implementer 不继承主 session 的全部历史；
- 先 spec compliance review；
- 再 code quality review；
- reviewer 发现问题必须修复并复审；
- 所有任务完成后进入 `finishing-a-development-branch`。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/subagent-driven-development/SKILL.md))

**它解决的问题：**

- 一个长 session 上下文污染，agent 越做越偏；
- 没有 review，错误积累到最后才爆；
- 任务执行者既当开发又当 reviewer；
- 大任务中途频繁打断用户。

**是否必须：** 如果你的工具支持 subagent，比如 Claude Code 或 Codex 这类有子代理能力的环境， **这是 Superpowers 推荐的主执行方式** 。 如果没有 subagent，就用 `executing-plans`。README 的基本工作流也把 `subagent-driven-development or executing-plans` 放在计划之后。([GitHub](https://github.com/obra/superpowers))

**我的评价：** 这是 Superpowers 最“agentic”的部分。质量更高，但成本也更高，因为每个任务至少 [implementer](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=3&q=implementer&zhida_source=entity) + 两个 reviewer。

---

### 6. executing-plans

**作用：没有或不使用 subagent 时，按计划在当前或独立 session 中执行。**

它要求先读取计划、批判性审查计划，有问题先提出来；没问题就创建 todo，然后逐项执行、逐项验证。所有任务完成后必须使用 `finishing-a-development-branch`。它还提醒：如果有 subagent 支持，应优先用 `subagent-driven-development`。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/executing-plans/SKILL.md))

**它解决的问题：**

- 已经有计划，但 agent 不按计划执行；
- 执行中跳过验证；
- 遇到 blocker 继续猜；
- 做完以后没有正式收尾流程。

**是否必须：** 当你没有 subagent 能力，但已经有详细 implementation plan 时， **应该用它** 。 如果有 subagent，优先用 `subagent-driven-development`。

**我的评价：** 它是“低配但稳”的执行方案。没有两阶段 subagent review 那么强，但比无计划执行可靠很多。

---

### 7. test-driven-development

**作用：强制 TDD。**

这是 Superpowers 最硬核的 skill。它的铁律是： **没有先失败的测试，就不能写生产代码** 。如果已经先写了代码，它要求删除并从测试开始。它要求完整 RED-GREEN-REFACTOR：先写失败测试，确认它因为正确原因失败；再写最小实现，确认通过；再重构并保持绿色。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/test-driven-development/SKILL.md))

**适用范围：**

- 新功能；
- bugfix；
- refactor；
- 行为变化。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/test-driven-development/SKILL.md))

**例外：**

- 一次性原型；
- 生成代码；
- 配置文件。 但即便这些例外，也要求问 human partner。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/test-driven-development/SKILL.md))

**它解决的问题：**

- AI 写了看似正确但没测试的代码；
- 测试后补，结果只测试了实现而不是需求；
- bugfix 没有回归测试；
- 重构没有安全网。

**是否必须：** 对生产代码，我建议基本当成必须。 对 throwaway prototype 或纯探索，可以显式跳过，但要知道这是牺牲可靠性换速度。

**我的评价：** 它很教条，但这套教条是故意的。AI coding 最大问题之一就是“产出太快、验证太慢”，TDD skill 正好反过来约束它。

---

### 8. systematic-debugging

**作用：遇到 bug、测试失败、异常行为时，先找根因再修。**

它的铁律是： **没有根因调查，不许提出修复方案** 。流程分四阶段：根因调查、模式分析、假设与测试、实现修复。它特别强调读完整错误信息、稳定复现、检查最近变更、多组件系统加诊断日志、沿调用链追踪坏值来源。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/systematic-debugging/SKILL.md))

**它解决的问题：**

- “试试这个改动”的随机修 bug；
- 只修症状不修根因；
- 改一个地方坏另一个地方；
- 失败 3 次还继续硬试。

**特别重要的一点：** 如果连续 3 个修复都失败，它要求停止并质疑架构，而不是继续打补丁。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/systematic-debugging/SKILL.md))

**是否必须：** 遇到 bug、测试失败、构建失败、性能问题、集成问题时， **非常建议必须使用** 。 如果只是解释代码或做设计，不需要。

**我的评价：** 这是我认为最值得单独拿出来用的 skill。即使你不用整套 Superpowers，也可以学它的调试纪律：复现、证据、假设、最小实验、再修复。

---

### 9. verification-before-completion

**作用：在声称“完成、修好、通过”之前，必须新鲜验证。**

它的铁律是： **没有刚运行过的验证证据，就不能说完成** 。流程是识别哪个命令能证明这个 claim，运行完整命令，读完整输出和 exit code，然后再根据结果说真实状态。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/verification-before-completion/SKILL.md))

**它解决的问题：**

- AI 说“应该可以了”；
- agent 相信自己刚改完就是成功；
- 只跑了部分测试就说全部通过；
- 相信 subagent 的 success report，不自己验证；
- 提 PR 前没有跑测试。

**是否必须：** 对任何“完成/修复/测试通过/构建成功”的声明， **应该必须用** 。 这是 trust skill，不是 [coding skill](https://zhida.zhihu.com/search?content_id=275013538&content_type=Article&match_order=1&q=coding+skill&zhida_source=entity) 。

**我的评价：** 非常必要。AI 最大的信任问题不是不会写，而是会过早宣布成功。这个 skill 专门限制这件事。

---

### 10. requesting-code-review

**作用：在任务完成、重大功能完成、合并前，派 reviewer subagent 审查。**

它要求用精确上下文派出 code reviewer，而不是把整个 session 历史丢给 reviewer。必须在每个 subagent-driven task 后、重大功能后、merge 前 request review。反馈按 Critical / Important / Minor 处理；Critical 必须立即修，Important 继续前要修。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/requesting-code-review/SKILL.md))

**它解决的问题：**

- agent 自己写自己验；
- 小问题早期没发现，后期变大；
- reviewer 上下文太多，反而不聚焦；
- review 只是形式，没有按 severity 处理。

**是否必须：** 在 Superpowers 主工作流里，任务之间和合并前是必须的；README 的基本工作流也列出它会在任务之间激活，Critical issues 会阻塞进度。([GitHub](https://github.com/obra/superpowers))

**我的评价：** 如果你的环境支持 subagent，非常值得用。没有 subagent 的环境可以退化为让主 agent 做 checklist，但效果会弱很多。

---

### 11. receiving-code-review

**作用：收到 code review 反馈后，不盲从、不表演式同意，先技术验证。**

它要求先完整阅读反馈，理解并复述或澄清，再检查代码库现实，判断建议是否适合当前代码库，然后逐项实现和测试。它明确禁止 “You’re absolutely right!”、“Great point!” 这类表演性回应，也反对没验证就直接实现。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/receiving-code-review/SKILL.md))

**它解决的问题：**

- AI 看到 review 就无脑改；
- 外部 reviewer 不理解上下文，AI 却照做；
- 用户说“fix 1-6”，AI 只理解部分也先改；
- reviewer 建议“proper implementation”，AI 过度工程化。

**是否必须：** 当你给 agent review feedback，或者 GitHub/外部 reviewer 给了反馈时， **非常建议使用** 。 没有 review feedback 的时候不需要。

**我的评价：** 这个 skill 很成熟。它把 AI 从“讨好型助手”拉回“工程判断者”。对团队协作很有用。

---

### 12. dispatching-parallel-agents

**作用：遇到多个独立问题时，并行派多个 agent。**

它适合多个测试文件失败、多个子系统独立损坏、多个 bug 没有共享状态的情况。原则是一个 independent problem domain 一个 agent；不要把“修所有测试”这种宽泛任务丢给一个 agent。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/dispatching-parallel-agents/SKILL.md))

**适合场景：**

- 3 个不同测试文件分别失败；
- 多个互不相关的 bug；
- 不同子系统各自有问题；
- 每个问题可以独立理解和修复。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/dispatching-parallel-agents/SKILL.md))

**不适合场景：**

- 失败可能同根；
- 需要理解全局状态；
- agent 会改同一批文件；
- 需要共享状态或顺序依赖。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/dispatching-parallel-agents/SKILL.md))

**是否必须：** 不必须。它是提速工具，不是基础质量门。 但当你有多个独立失败时，很值得用。

**我的评价：** 这是“加速型 skill”。用对了非常省时间，用错了会制造冲突。关键判断是：这些问题是否真的独立。

---

### 13. finishing-a-development-branch

**作用：开发完成后的收尾流程。**

它要求先跑测试，测试不过就不能进入 merge/PR；然后检测环境是普通 repo、worktree、detached HEAD；确定 base branch；最后给用户结构化选项：本地 merge、创建 PR、保留分支、丢弃。丢弃必须要求用户输入确认。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/finishing-a-development-branch/SKILL.md))

**它解决的问题：**

- 测试没过就合并；
- 做完后不知道是 merge、PR、保留还是丢弃；
- worktree 清理错误；
- 意外删除分支或工作区；
- PR 后把仍需迭代的 worktree 清掉。

**是否必须：** 只要这次任务涉及真实分支/PR/合并， **建议必须用** 。 如果只是解释、设计、只读分析，不需要。

**我的评价：** 非常工程化。它不酷，但能防很多“最后一步翻车”的问题。

---

### 14. writing-skills

**作用：创建或修改 Superpowers-style skill。**

它把“写 skill”也当成 TDD：先设计 pressure scenario，让 agent 在没有 skill 的情况下失败；再写最小 skill；再验证 agent 有 skill 后是否遵守；如果发现新漏洞，再修改并复测。它也解释了 skill 的定位：skill 是可复用技术、模式、工具、参考指南，不是一次性经验叙事。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/writing-skills/SKILL.md))

**它关心的重点：**

- skill 的 description 只写触发条件，不总结流程；
- 避免 Claude 只看 description 就偷懒不读正文；
- 用关键词覆盖让 agent 能找到；
- skill 文档要精简；
- 每个 skill 修改都要测试；
- 不要批量写多个 skill 而不逐个验证。([GitHub](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/skills/writing-skills/SKILL.md))

**是否必须：** 只有你要创建、修改、维护 skills 时才需要。 普通使用 Superpowers 不需要它。

**我的评价：** 这是给框架作者和高级用户用的。普通开发者可以暂时忽略；但如果你想把团队规范沉淀成 AI 可执行流程，它很有价值。

---

### 这 14 个 skills 的关系图

可以理解成四层：

#### 第一层：入口与规则

- `using-superpowers`：决定什么时候加载其他 skills。

#### 第二层：需求到计划

- `brainstorming`：把想法变成设计；
- `writing-plans`：把设计变成可执行计划；
- `using-git-worktrees`：执行前隔离环境。

#### 第三层：执行与质量控制

- `subagent-driven-development`：有 subagent 时的主执行流；
- `executing-plans`：无 subagent 或 inline 执行流；
- `test-driven-development`：实现时的 TDD 铁律；
- `requesting-code-review`：主动请求 review；
- `receiving-code-review`：处理 review feedback；
- `dispatching-parallel-agents`：独立问题并行处理。

#### 第四层：调试、验证、收尾

- `systematic-debugging`：遇到 bug 先找根因；
- `verification-before-completion`：完成前必须验证；
- `finishing-a-development-branch`：合并/PR/保留/丢弃；
- `writing-skills`：扩展或维护 skills。

---

### 我建议你怎么用

#### 如果你用 Codex / Claude Code 做真实项目

建议完整安装并默认启用。README 明确说不同 harness 需要分别安装；Codex CLI/App、Claude Code、Cursor、Gemini CLI、OpenCode、Copilot CLI 都有对应方式。([GitHub](https://github.com/obra/superpowers))

#### 如果你是团队使用

建议把它当成“AI 工程规范模板”，但不要盲目接受所有默认强度。可以重点评估：

- 是否真的要求所有 feature 都 TDD；
- 是否允许小改动跳过 full brainstorming；
- spec 和 plan 文档保存在哪里；
- 是否强制 worktree；
- PR 前需要跑哪些测试；
- review feedback 是否由用户最终裁决。

---

### 最终判断

**Superpowers 不是“必须安装的工具”，而是“值得采用的 AI 编程纪律框架”。**

如果你的目标是：

> 快速让 AI 写点东西

那它可能太重。

如果你的目标是：

> 让 AI 更像一个守流程、会测试、会审查、会验证的工程师

那我认为它值得安装，而且应该认真使用。

最核心的价值不是某个单独 skill，而是这条链路：

**需求澄清 → 设计确认 → 计划拆解 → 隔离开发 → TDD → review → 验证 → 收尾**

这条链路正好针对 AI coding 最常见的失败模式： **过早实现、缺少测试、猜测修复、跳过验证、过早宣布成功** 。

### 工作树清理附录

原文的命令片段包含占位符，以下按页面上的文本收录。

~~~text
Then: Cleanup worktree (Step 6), then force-delete branch: `bash git branch -D <feature-branch> \`

### Step 6: Cleanup Workspace

**Only runs for Options 1 and 4.** Options 2 and 3 always preserve the worktree.

`bash GIT_DIR=<!--MATH_PH_3-->(git rev-parse --git-dir)\" 2>/dev/null && pwd -P) GIT_COMMON=<!--MATH_PH_4-->(git rev-parse --git-common-dir)\" 2>/dev/null && pwd -P) WORKTREE_PATH=<!--MATH_PH_5-->(git -C \"<!--MATH_PH_6-->MAIN_ROOT\" git worktree remove \"$WORKTREE_PATH\" git worktree prune # Self-healing: clean up any stale registrations \`

**Otherwise:** The host environment (harness) owns this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch | |——–|——-|——|—————|—————-| | 1. Merge locally | yes | - | - | yes | | 2. Create PR | - | yes | yes | - | | 3. Keep as-is | - | - | yes | - | | 4. Discard | - | - | - | yes (force) |

## Common Mistakes

**Skipping test verification** - Problem: Merge broken code, create failing PR - Fix: Always verify tests before offering options

**Open-ended questions** - Problem: \“What should I do next?\” is ambiguous - Fix: Present exactly 4 structured options (or 3 for detached HEAD)

**Cleaning up worktree for Option 2** - Problem: Remove worktree user needs for PR iteration - Fix: Only cleanup for Options 1 and 4

**Deleting branch before removing worktree** - Problem: git branch -d fails because worktree still references the branch - Fix: Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree** - Problem: Command fails silently when CWD is inside the worktree being removed - Fix: Always cd to main repo root before git worktree remove

**Cleaning up harness-owned worktrees** - Problem: Removing a worktree the harness created causes phantom state - Fix: Only clean up worktrees under .worktrees/, worktrees/, or ~/.config/superpowers/worktrees/

**No confirmation for discard** - Problem: Accidentally delete work - Fix: Require typed \“discard\” confirmation

## Red Flags

**Never:** - Proceed with failing tests - Merge without verifying tests on result - Delete work without confirmation - Force-push without explicit request - Remove a worktree before confirming merge success - Clean up worktrees you didn’t create (provenance check) - Run git worktree remove from inside the worktree

**Always:** - Verify tests before offering options - Detect environment before presenting menu - Present exactly 4 options (or 3 for detached HEAD) - Get typed confirmation for Option 4 - Clean up worktree for Options 1 & 4 only - cd to main repo root before worktree removal - Run git worktree prune after removal “
~~~
