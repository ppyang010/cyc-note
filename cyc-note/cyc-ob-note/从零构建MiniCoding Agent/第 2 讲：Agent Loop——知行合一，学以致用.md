---
id: "2062952305662615669"
title: "第 2 讲：Agent Loop——知行合一，学以致用"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2062952305662615669"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 2
Created: "2026-07-21 17:42"
updated: "2026-07-27 21:05"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 2 讲：Agent Loop——知行合一，学以致用

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2062952305662615669)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


![Image 1](https://pica.zhimg.com/v2-0d45b53b980e5bb3d4790ef8be30b226.jpg?source=25ab7b06)

第 1 讲里，我们给 Agent 准备了 [Task](https://zhida.zhihu.com/search?content_id=279510336&content_type=Article&match_order=1&q=Task&zhida_source=entity)、Todo 和 [Plan](https://zhida.zhihu.com/search?content_id=279510336&content_type=Article&match_order=1&q=Plan&zhida_source=entity)。

它已经知道：

```
最终要完成什么；
有哪些步骤；
现在应该先做哪一步。
```

但知道下一步，不等于真正完成下一步。

就像厨师看完菜单和备菜清单以后，还要拿起刀、开火、尝味道，再根据结果继续调整。

这个不断重复的过程，就是 **Agent Loop（智能体行动循环）**。

![Image 2](https://pic1.zhimg.com/v2-de8642aae0c512b05f97ff8c8143e1ea_1440w.jpg)

图 1：Agent Loop 不是一直思考，而是读取任务、执行一步、观察结果、更新状态，再进入下一轮。

* * *

### 一、Agent Loop 到底是什么？

最小的 Agent Loop 可以写成一句话：

`选择下一步 → 执行动作 → 读取结果 → 更新状态 → 再选择下一步`

对应到后厨：

```
看清当前工序；
开始洗菜或下锅；
看看实际结果；
记录缺什么、做到了哪里；
决定下一步继续做什么。
```

对应到 Coding Agent：

```
读取 Task 和 Todo；
选择当前 Action；
调用工具执行；
获得 观察值；
更新任务状态；
判断继续还是停止。
```

![Image 3](https://pic3.zhimg.com/v2-59e4d73d5cdd1ef8912f828b8b666b30_1440w.jpg)

图 2：行动循环的核心不是循环次数，而是每一轮都用新的 观察值 修正下一步。

* * *

### 二、为什么不能只想一次？

[软件工程](https://zhida.zhihu.com/search?content_id=279510336&content_type=Article&match_order=1&q=%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B&zhida_source=entity)里的现场信息，不会在任务开始前一次性全部出现。

例如，用户说：

`把 enhanced_project 修好。`

Agent 第一次并不知道四个错误分别在哪里。

它只能逐步推进：

```
先运行测试；
看到 4 failed, 6 passed；
阅读第一个失败；
修改对应代码；
重新运行测试；
看到剩余失败；
继续下一轮。
```

如果没有循环，Agent 很容易出现三种问题：

```
只生成一份计划，却没有真正执行；
修改一次以后，不检查结果；
看到新问题以后，仍然沿用旧判断。
```

![Image 4](https://pic3.zhimg.com/v2-48c02ca844cf598ade160630ba9c1082_1440w.jpg)

图 3：没有循环，Agent 容易“一通乱炒”；有了循环，才能根据每次结果继续推进。

* * *

### 三、贯穿案例：修复四个 Bug

本系列的故障项目初始状态是：

`4 failed, 6 passed`

一次合理的循环大致是：

```
第 1 轮：
运行测试
→ 发现 add() 结果错误
→ 修改 calculator.py
→ 记录 观察值

第 2 轮：
重新运行测试
→ 剩余 3 个失败
→ 发现 mean() 没处理空列表
→ 修改 stats.py

第 3～4 轮：
继续读取失败
→ 修复 median() 和除零问题

最后一轮：
重新运行全部测试
→ 10 passed
→ 任务满足 Done when
→ 输出报告并停止
```

这里最重要的不是“四轮”，而是：

> **每一轮都必须根据工具返回的新结果，决定下一步。**

* * *

### 四、Agent Loop 不是一个裸 while True

第 2 讲不需要实现完整工具系统。

先看最小骨架：

```
for step in range(10):
    action = choose_next_action(state)
    observation = execute(action)
    state = update_state(state, observation)

    if is_done(state):
        break
```

四行分别对应：

```
choose_next_action：现在做什么；
execute：真正执行；
update_state：把结果写回任务本；
is_done：判断是否已经满足完成标准。
```

会循环不难。真正难的是让循环 **有目标、有反馈、有边界、能停止**。真实 Agent 还会加入：

```
最大轮数；
失败处理；
权限检查；
工具超时；
人工确认；
最终 Review。
```

但无论系统多复杂，核心循环都没有变。

* * *

### 五、从 L2 到 L3：Agent 开始持续行动

第 1 讲结束时，Agent 已经像一个项目助手：

```
能接住任务；
能拆分步骤；
能知道当前下一步。
```

第 2 讲加入 Agent Loop 后，它开始向 L3 任务执行者迈进：

```
读取状态；
执行一步；
观察结果；
更新判断；
继续推进；
满足条件后停止。
```

它不再只是拿着菜单和清单站在灶台前，而是真的开始做菜，并且会尝味道、看火候、改下一步。

* * *

### 本讲小结

Agent Loop 可以记成五个词：

`选择 → 执行 → 观察 → 更新 → 继续`

下一讲，我们会把循环里的 执行 拆开，看 Agent 怎样真正接入文件、终端和测试。

> **第 3 讲：Tools——欲善其事，先利其器**