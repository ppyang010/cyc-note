---
id: "2053058800718964733"
title: "ai agent的架构好像都差不多啊?有啥比较特别的吗？"
author: "wxz131"
type: zhihu-answer
source: "https://www.zhihu.com/question/1959742114519844109/answer/2053058800718964733"
created: "2026-06-24 10:16"
updated: "2026-06-24 10:16"
collected: "2026-06-24 10:16"
downloaded: "2026-08-16"
---
**结论：骨架确实趋同了，**生产级 Harness 的12个组件（编排循环、工具、记忆、上下文管理、提示词构建、输出解析、状态管理、错误处理、护栏、验证循环、子Agent编排……）每个框架都在做。ReAct 循环本质上就是一个 while loop——“笨循环”里所有智能住在模型这边（Anthropic 原话）。**真正的分化发生在三个维度，而不是组件清单维度。**

* * *

## 维度一：记忆的”写”触发机制——谁在决定该记什么？

这是最隐蔽但最关键的差异。

**普通 Agent：** 记忆是被动存储——用户说”记住这个”，它就写。没有主动提炼。

### Hermes：Nudge Engine（催促引擎）

双计数器机制：

-   **Memory 计数器**：每10个用户回合触发一次审查（因为记忆来自用户输入）
-   **Skill 计数器**：每10次工具迭代触发一次（因为经验来自执行过程）
-   后台 Fork 一个 review agent（独立线程，输出静默到 /dev/null，最多8次迭代），共享主 Agent 的 Memory 存储
-   当 Agent 主动调用 memory 工具时，计数器归零——已经在反思了就不用再催

### Claude Code：Turn Stop Hook

每次交互结束后，Fork 一个后台 Agent（复用 KV Cache），判断哪些信息值得保存，并更新到 Markdown 文件中。

### OpenAI：Dreaming

后台综合用户与 ChatGPT 的所有聊天记录，提炼出”你是谁、你喜欢什么、你最近在忙什么”，然后把这些信息注入每次新对话。

### OpenHuman：三层树

-   **源树**（Source Tree）：每个数据来源一棵（Gmail、Slack……）
-   **主题树**（Topic Tree）：按人物/项目/话题聚合（”张三”在多个来源中的信息合并）
-   **全局树**（Global Tree）：每日摘要→每周摘要→每月→每年自动压缩

### 关键分歧

记忆不仅仅是”存”的问题，更是**“什么时候写、写什么、淘汰什么”**的问题：

| 方案 | 写入触发 | 淘汰策略 | 核心成本优化 |
| ----- | ----- | ----- | ----- |
| Hermes Nudge | 计数器+后台审查 | 2200/1375字硬上限强制淘汰 | 后台线程，用户无感 |
| Claude Code | Turn Stop Hook | 模型判断选择性保存 | KV Cache 复用 |
| OpenAI Dreaming | 跨会话定时 | 系统自动提炼压缩 | 面向普通用户 |
| OpenHuman | 每日凌晨定时 | 多级时间尺度压缩 | 按实体聚合去重 |

* * *

## 维度二：能力增长路径——技能是”写死”还是”长出来”？

### 普通框架

工具/技能是预定义的——给 Agent 一堆 tool schema，它只能调用这些。

### Hermes：Skill 系统（程序性记忆）

**定位：** Skill 是”程序性记忆”（知道怎么做），Memory 是”陈述性记忆”（知道什么）。

**创建触发：**

-   复杂任务成功（5+次工具调用）
-   克服错误后
-   用户纠正的方法有效
-   发现非平凡工作流
-   用户要求记住某个流程

**修补机制（最特别的设计）：**

当按已有 Skill 执行踩到新坑时，完成任务后做**模糊匹配局部补丁**（`_patch_skill`），不是全量重写：

关键设计点：

-   **模糊匹配**：即使 Agent 提供的 `old_string` 与原文有格式差异也能匹配
-   **原子写入**：避免写入中途出错导致文件损坏
-   **安全扫描+回滚**：写入后立即安全检查，不通过自动恢复

**渐进式加载：** 上下文里只放名字+一句话描述的轻量索引，用到了才加载完整文件：

```text
Available skills:
devops:
- flask-k8s-deploy: Deploy a Flask app to Kubernetes with health checks
- nginx-reverse-proxy: Configure Nginx reverse proxy with SSL
software-development:
- fix-pytest-fixtures: Debug and fix pytest fixture scope issues
```

**Prompt 引导自动修补：**

```text
# tools/skill_manager_tool.py:681-701
SKILL_MANAGE_SCHEMA = {
    "name": "skill_manage",
    "description": (
        "Manage skills (create, update, delete). Skills are your procedural "
        "memory — reusable approaches for recurring task types.\n\n"
        "Create when: complex task succeeded (5+ calls), errors overcome, "
        "user-corrected approach worked, non-trivial workflow discovered, "
        "or user asks you to remember a procedure.\n"
        "Update when: instructions stale/wrong, OS-specific failures, "
        "missing steps or pitfalls found during use. "
        "If you used a skill and hit issues not covered by it, "
        "patch it immediately with skill_manage(action='patch') "
        "— don't wait to be asked.\n\n"
        "After difficult/iterative tasks, offer to save as a skill. "
        "Skip for simple one-offs."
    ),
}
```

* * *

## 维度三：上下文腐烂对抗——怎么处理”窗口越大越蠢”？

Chroma 研究显示：**关键内容落在上下文中间时，模型性能下降超过30%**（被斯坦福”Lost in the Middle”论文印证）。

### 各家策略对比

| 策略 | 谁在做 | 做法 |
| ----- | ----- | ----- |
| 摘要压缩 | Claude Code | 接近上限时压缩对话，保留架构决策和未解决 bug |
| 观察屏蔽 | JetBrains Junie | 隐藏旧工具输出，保留工具调用可见 |
| 即时检索 | Claude Code | 用 grep/glob/head/tail 替代加载完整文件 |
| 子Agent委托 | Anthropic | 每个 sub-agent 做大范围探索，只返回 1-2k token 压缩摘要 |
| 提示词缓存优化 | Hermes | 固化 MEMORY/USER 快照在前缀，最大化 Prompt Caching 命中 |

### Hermes 的提示词组装顺序（极其讲究）

```text
[0] 默认智能体身份
[1] 工具使用行为指南
[2] Honcho 集成模块（可选）
[3] 可选系统消息
[4] 固化的 MEMORY.md 快照    ← 关键：稳定前缀
[5] 固化的 USER.md 快照      ← 关键：稳定前缀
[6] 技能索引
[7] 上下文文件（AGENTS.md, SOUL.md 等规则文件）
[8] 日期/时间 + 平台信息
[9] 对话历史
[10] 当前用户消息
```

把稳定内容放前面，是为了最大化供应商的 Prompt Caching 收益——**这是一个”用架构适配基础设施”的设计决策，不是单纯的代码组织习惯。**

> 参考来源：

[Agent-Harness 工程经验总结](https://zhuanlan.zhihu.com/p/2021529299576988417)