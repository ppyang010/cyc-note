---
id: "2062602323239736898"
title: "第 0 讲：为什么 Coding Agent 不是会写代码的聊天框？"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2062602323239736898"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 0
Created: "2026-07-20 18:38"
updated: "2026-08-04 11:43"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 0 讲：为什么 Coding Agent 不是会写代码的聊天框？

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2062602323239736898)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **君子欲讷于言而敏于行。——《[论语·里仁](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=%E8%AE%BA%E8%AF%AD%C2%B7%E9%87%8C%E4%BB%81&zhida_source=entity)》**

![Image 1](https://picx.zhimg.com/v2-0ba2e327b2fe83e14b73352d5b12bec4.jpg?source=25ab7b06)

Coding Agent = 模型 + Harness

大模型已经很会“说”：解释概念、分析报错、生成代码，都不难。

但 Coding Agent 真正要解决的，不是让 AI 说得更多，而是让它进入现场、使用工具、推进任务，并用结果证明自己做完了。

* * *

## 一、会背菜谱，不等于会做饭

看完做菜视频，不等于真会做菜。

视频里的步骤很清楚，真进厨房却会遇到油温、火候、顺序、调味和出锅判断。会背菜谱，只是知道怎么说；能把菜端上桌，才算完成任务。

AI 也是一样。

它可以告诉你哪里可能有 bug，也可以给出修改建议。但文件还没打开，测试还没运行，代码也没有真正改完。

```
聊天框让 AI 会回答问题； 
Coding Agent 让 AI 开始承担任务。
```

所以问题的关键不是“模型还能不能更聪明”，而是：**它怎样从会说，变成会做？**

代码正好提供了最清楚的观察窗口。

* * *

真实工程不是生成一段代码，而是面对一个项目：

```
需求可能不完整； 
代码分散在多个文件； 
旧逻辑不能破坏； 
测试可能失败； 
失败后还要继续定位； 
最后还要说明改了什么。
```

后面我们会一直使用一个小工程：

代码整体链接：[https://gitee.com/yege187/mini-coding-agent-course/repository/archive/main.zip](https://link.zhihu.com/?target=https%3A//gitee.com/yege187/mini-coding-agent-course/repository/archive/main.zip)

```
enhanced_project/   
  calculator.py   stats.py   formatter.py   
tests/     
  test_calculator.py     test_stats.py     test_formatter.py
```

这里有多处小问题。Agent 要读项目、跑测试、查源码、修改文件、回归验证，最后给出报告。

聊天框像坐在餐桌旁的顾问；Coding Agent 则要走进后厨，把任务推进到可以交付。

但模型不会因为改名叫 Agent，就自动拥有文件、终端、测试环境和权限。要让它真正进入现场，还需要一套工作支架。

* * *

## 三、Harness：让模型真正开始工作

`Coding Agent = 模型 + Harness`

Harness 常被简单理解成“工具调用”，但更准确的说法是：**工作支架**。

它不替模型思考，而是给模型提供完成工作的结构。

建筑支架不会替工人砌墙，却提供站立位置、施工通道和安全防护。后厨系统不会替厨师判断味道，却提供案板、锅灶、菜单、库存、流程和出餐检查。

Coding Agent 的 Harness 也是这样。

![Image 2](https://pic3.zhimg.com/v2-c6d176675db4f53e663061c1877473a8_1440w.jpg)

图 1：模型负责理解、判断和生成；Harness 把工具、记忆、权限、流程和检查组织起来。

它主要托住五件事：

*   **任务**：明确目标、约束和完成标准。
*   **现场**：接入文件、终端、搜索、测试和日志。
*   **边界**：通过权限、沙箱、确认和审计限制行为。
*   **闭环**：形成“计划—执行—观察—修正—验证”的过程。
*   **记忆**：保留目标、进度、失败原因和项目约定。

也可以压缩成三层：

```
能力支架：让模型能读、能查、能跑、能改； 
安全支架：让模型在权限和审计中工作； 
交付支架：让模型围绕测试和 Review 完成闭环。
```

因此，同一个模型放在不同产品里，表现可能完全不同。差别不只在模型，也在 Harness 是否把工作真正支起来。

有了 Harness，Agent 才能从“会回答”继续向“能负责”成长。

* * *

## 四、[AI 工程师](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=AI+%E5%B7%A5%E7%A8%8B%E5%B8%88&zhida_source=entity)不是一下子长成的

我们可以用 [L0～L5](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=L0%EF%BD%9EL5&zhida_source=entity) 描述这条成长线：

| 等级 | 角色 | 核心能力 |
| --- | --- | --- |
| L0 | 聊天顾问 | 会解释，但不在现场 |
| L1 | 代码副驾驶 | 会补全，能协助局部编码 |
| L2 | 项目助手 | 能读项目，能使用工具 |
| L3 | 任务执行者 | 能拆任务、验证并交付 |
| L4 | 工程队友 | 能协作、Review、[复盘](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=%E5%A4%8D%E7%9B%98&zhida_source=entity) |
| L5 | AI 工作者系统 | 能接入[组织流程](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=%E7%BB%84%E7%BB%87%E6%B5%81%E7%A8%8B&zhida_source=entity)，持续工作、被管理、可审计 |

![Image 3](https://pic3.zhimg.com/v2-95bcfa030a7a5462c288349e45b867aa_1440w.jpg)

图 2：从 L0 聊天顾问到 L5 AI 工作者系统，变化的是工作责任，而不只是界面。

从 L0 到 L5，真正变化的是三件事：

```
它能看到多大的工作现场； 
它能调用多完整的行动能力； 
它能承担多完整的交付责任。
```

但能力越强，边界也越重要。

* * *

## 五、Agent 不是魔法

Coding Agent 不是“全自动[替代工程](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=%E6%9B%BF%E4%BB%A3%E5%B7%A5%E7%A8%8B&zhida_source=entity)师”。

哪些操作可以自动完成，哪些需要人确认；哪些文件可以修改，哪些权限不能开放；哪些错误能自动修，哪些设计选择必须由人决定，都要事先规定。

“敏于行”不等于鲁莽行动。

成熟的 Agent 应该在目标清楚、权限明确、过程可追踪、结果可验证的前提下行动。

所以 Harness 不只让 AI 更能干，也让它更可控。

* * *

## 六、这套系列要做什么

后面的内容会围绕同一个修 bug 项目，逐步拆开 Coding Agent：

```
Task / Todo / Plan：任务怎样立起来； 
Agent Loop：任务怎样持续推进； 
Tools：模型怎样进入现场； 
Permission / Sandbox：行动边界怎样设置； 
Context / Memory：长任务怎样不忘、不乱； 
Review Loop：怎样证明任务真的完成； 
Skills / Hooks / MCP：能力怎样沉淀和扩展； 
Remote / Subagent：任务怎样委派和协作。
```

最后，我们会手写一个 Mini Coding Agent，把这些能力串起来：

`Task + Todo + Tools + State + Harness + Review`

它不会很复杂，但会完整走通“理解任务—进入现场—执行修改—验证结果”的[最小闭环](https://zhida.zhihu.com/search?content_id=279438319&content_type=Article&match_order=1&q=%E6%9C%80%E5%B0%8F%E9%97%AD%E7%8E%AF&zhida_source=entity)。

* * *

## 七、本讲小结

![Image 4](https://picx.zhimg.com/v2-2aa21ff6d74741e6b9c5f3f9a78e8c73.jpg?source=25ab7b06)

Coding Agent 不是更会聊天的模型，而是开始具备工作能力的 AI 系统。

```
模型负责理解、判断和生成； 
Harness 托住任务、现场、边界、闭环和记忆； 
两者结合，AI 才能从“会说”走向“会做”。
```

下一讲从最基础的一步开始：先把任务说清楚。

这就是 Task / Todo / Plan。