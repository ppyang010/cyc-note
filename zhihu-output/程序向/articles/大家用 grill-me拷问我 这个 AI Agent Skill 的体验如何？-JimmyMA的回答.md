---
id: "2066983895027934982"
title: "大家用 grill-me(拷问我) 这个 AI Agent Skill 的体验如何？"
author: "JimmyMA"
type: zhihu-answer
source: "https://www.zhihu.com/question/2054005413406946147/answer/2066983895027934982"
created: "2026-08-01 20:29"
updated: "2026-08-01 20:29"
collected: "2026-08-01 20:29"
downloaded: "2026-08-16"
---
### 快速决策（3 秒版）

| 你的情况 | 用这个 |
| ----- | ----- |
| 需求不清楚 | /grill-me or /grill-with-docs |
| 不熟悉领域 | /research |
| 快速原型 | /prototype |
| 开始实现 | /tdd |
| 东西坏了 | /diagnosing-bugs |
| 一天干不完 | /handoff |
| 大项目规划 | /wayfinder |

### 核心技能

-   /grill-me - 苏格拉底式访谈，压力测试想法，无文件产出
-   /grill-with-docs - 访谈 + 生成 CONTEXT.md 和 ADR，创建项目记忆
-   /research - 后台研究，查一手资料
-   /prototype - 快速原型验证
-   /tdd - 测试驱动开发
-   /wayfinder - 大规模工程规划
-   /handoff - 跨会话上下文传递
-   /diagnosing-bugs - 系统化 bug 诊断
-   /code-review - 双轴代码审查

### 辅助技能

-   /to-spec - 生成规范文档
-   /to-tickets - 分解任务
-   /implement - 实现任务
-   /domain-modeling - 领域建模
-   /codebase-design - 代码库设计

### 场景化工作流

### 需求模糊

**目标：** 澄清需求，建立共识

```text
/grill-me (快速对齐，无文档)
  或
/grill-with-docs (对齐 + 生成文档)
  ↓
决定下一步
```

### 不熟悉的领域

**目标：** 快速学习，补充知识

```text
/research (后台研究)
  ↓
阅读报告
  ↓
/grill-me (澄清理解)
```

### 熟悉的领域

**目标：** 快速实现

```text
/tdd (直接开始)
  ↓
/code-review (审查)
```

### 小项目（< 1 天）

**目标：** 快速交付

```text
/grill-me (5 分钟对齐)
  ↓
/tdd (实现)
  ↓
/code-review (审查)
```

### 大项目（> 1 周）

**目标：** 详细规划，分步实施

```text
/wayfinder (规划地图)
  ↓
逐个解决 tickets
  ↓
/tdd (实施每个任务)
```

### 一天干不完（需交接）

**目标：** 保存上下文，无缝继续

```text
工作到一半
  ↓
/handoff (压缩上下文)
  ↓
第二天用新会话加载
```

### 需求清楚 + 大项目

**目标：** 分解任务，逐步实现

```text
/to-spec (生成规范)
  ↓
/to-tickets (分解任务)
  ↓
/implement × N (逐个实现)
```

### 需求模糊 + 大项目

**目标：** 先澄清，再规划

```text
/grill-with-docs (澄清 + 文档)
  ↓
/wayfinder (规划地图)
  ↓
逐个解决 tickets
```

### 快速原型

**目标：** 快速验证想法

```text
/prototype (快速原型)
  ↓
验证想法
  ↓
决定：继续 or 放弃
```

### 修复 Bug

**目标：** 系统化诊断和修复

```text
/diagnosing-bugs (诊断)
  ↓
修复 + 回归测试
  ↓
/code-review (审查)
```

### 代码审查

**目标：** 检查代码质量

```text
/code-review (双轴审查)
  ↓
修复问题
  ↓
提交
```

### 完整工作流（从零到一）

**目标：** 从想法到交付

```text
/grill-with-docs (对齐)
  ↓
/research (学习)
  ↓
/wayfinder (规划)
  ↓
/to-spec → /to-tickets
  ↓
/implement × N
  ↓
/code-review
```

### 常用组合

| 组合名称 | 工作流 | 适用场景 |
| ----- | ----- | ----- |
| 快速对齐 | /grill-me → /tdd | 小项目，需求基本清楚 |
| 学习 + 实现 | /research → /grill-me → /tdd | 不熟悉的领域 |
| 大项目标准 | /wayfinder → tickets → /tdd | 大型项目 |
| 模糊大项目 | /grill-with-docs → /wayfinder → tickets | 需求模糊的大型项目 |
| 跨天工作 | 工作 → /handoff → 新会话继续 | 一天干不完 |
| Bug 修复 | /diagnosing-bugs → 修复 → /code-review | 修复 bug |

核心要点

1.  **不清楚就先问** - `/grill-me` 是你的第一步
2.  **不熟悉就先学** - `/research` 帮你补充知识
3.  **干不完就交接** - `/handoff` 保存上下文

* * *

### grill-me vs grill-with-docs

-   一次性讨论、不需要后续参考 → /grill-me
-   需要文档化、长期项目、团队协作 → /grill-with-docs

**grill-with-docs 会创建”项目记忆”：**

-   讨论中确定的术语 → 写入 `CONTEXT.md`
-   重要的架构决策 → 写入 `docs/adr/001-xxx.md`
-   后续会话可以读取这些文件，保持上下文连贯
-   团队成员可以参考这些文档，统一理解

相关资源

-   [Matt Pocock Skills 官方仓库](https://link.zhihu.com/?target=https%3A//github.com/mattpocock/skills)
-   [Superpowers 官方仓库](https://link.zhihu.com/?target=https%3A//github.com/obra/superpowers)