---
id: "2071307778770187299"
title: "第 9 讲：Remote / Delegation——运筹帷幄，决胜千里"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2071307778770187299"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 9
Created: "2026-08-13 18:52"
updated: "2026-08-15 14:54"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 9 讲：Remote / Delegation——运筹帷幄，决胜千里

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2071307778770187299)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **[运筹帷幄之中](https://zhida.zhihu.com/search?content_id=281283710&content_type=Article&match_order=1&q=%E8%BF%90%E7%AD%B9%E5%B8%B7%E5%B9%84%E4%B9%8B%E4%B8%AD&zhida_source=entity)，决胜千里之外。**
> 
> 出处说明：语出《[史记·高祖本纪](https://zhida.zhihu.com/search?content_id=281283710&content_type=Article&match_order=1&q=%E5%8F%B2%E8%AE%B0%C2%B7%E9%AB%98%E7%A5%96%E6%9C%AC%E7%BA%AA&zhida_source=entity)》。本讲借它来说明：Agent 的能力不只来自“自己在本地执行”，还来自远程调度与任务委派。

前八讲里，我们一直在训练一个 Agent 怎样把事情做好。

但任务继续扩大以后，单个 Agent 会遇到新的限制：

```
本地环境不适合执行；
任务需要更长时间；
不同步骤需要不同资源；
主控不应该亲手处理所有细节。
```

于是 [Harness](https://zhida.zhihu.com/search?content_id=281283710&content_type=Article&match_order=1&q=Harness&zhida_source=entity) 还要学会两件事：

```
Remote：把任务放到远程环境或独立执行点完成；
Delegation：把合适的子任务交给合适的执行者。
```

![Image 1](https://picx.zhimg.com/v2-622c5fd991b111b11c336ad45220399b_1440w.jpg)

封面：主控负责统筹全局，远程执行点负责完成被分配的具体工作。

* * *

Remote / Delegation 的核心问题是：

```
这项工作由谁执行？
应该在哪里执行？
要交付什么结果？
主控怎样知道执行到哪一步？
```

它更像一位主厨站在中央指挥台，把备菜、烹饪、清洁和装盘分别交给不同工作站。

![Image 2](https://pic4.zhimg.com/v2-37671dffd7bb60bda5611f832de63e61_1440w.jpg)

图 1：Delegation 的重点，是把合适的工作交给合适的执行者，而不是让主控亲手完成每一步。

主控仍然负责：

```
理解总目标；
拆分子任务；
选择执行者；
明确验收标准；
回收并检查结果。
```

执行者负责：

```
在授权范围内完成子任务；
按约定格式汇报进度；
返回结果、证据和异常。
```

* * *

## 二、Remote：不在同一个“灶台”，也能协同推进

远程执行不只是“换一台电脑”。

它可能意味着：

```
在云端跑长时间测试；
在专用环境里构建项目；
在另一台机器上使用特殊依赖；
把耗时任务放到独立工作区执行。
```

![Image 3](https://picx.zhimg.com/v2-4236fc750ebede5167ba688e9eb5d221_1440w.jpg)

图 2：Remote 把任务分布到不同执行地点，主控负责统一调度和掌握全局进度。

继续用 `enhanced_project` 来举例：

```
主控：
明确目标是修复四个 Bug，并要求全部测试通过。

远程执行点 A：
运行完整测试，收集失败报告。

远程执行点 B：
检查 stats.py 的边界条件。

主控：
汇总返回结果，决定下一步修改。
```

远程的价值在于：

```
隔离不同环境；
并行利用资源；
让主控保持清晰；
避免把所有执行细节塞进同一个上下文。
```

* * *

## 三、Delegation 不是“一扔了之”

低质量委派往往只有一句：

`你去把这个问题解决一下。`

这会带来四个问题：

```
目标不清；
边界不清；
进度不可见；
结果无法验收。
```

真正的 Delegation 应该形成闭环：

```
1. 任务拆分；
2. 明确目标与约束；
3. 下放执行；
4. 中途回报；
5. 结果验收；
6. 汇总复盘。
```

![Image 4](https://pic1.zhimg.com/v2-1d1ca1da1df4cf36c4d2773ef8f2fa5a_1440w.jpg)

图 3：任务下放后还要追踪进度、纠正偏差、回收并验收结果。

一个合格的委派单至少应包含：

```
任务：要完成什么；
输入：可以使用哪些资料；
权限：允许做什么；
输出：以什么格式返回；
完成标准：满足什么条件才算完成；
回报机制：何时汇报进度和异常。
```

* * *

## 四、第 9 讲与第 10 讲有什么区别？

两讲都可能出现“多个 Agent”，但关注点不同：

| 章节 | 核心问题 | 主要结构 |
| --- | --- | --- |
| 第 9 讲 Remote / Delegation | 谁去执行、在哪里执行、结果怎样回收 | 主控 → 执行点 |
| 第 10 讲 Subagent / Multi-agent | 多个角色怎样互补思考、协调判断 | 多角色 ↔ 协商 ↔ 共识 |

一句话概括：

```
第 9 讲偏“组织执行”；
第 10 讲偏“组织认知”。
```

第 9 讲可以只有一个主控和一个远程执行者；

第 10 讲即使所有角色都在同一台机器上，也仍然属于[多智能体协作](https://zhida.zhihu.com/search?content_id=281283710&content_type=Article&match_order=1&q=%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E5%8D%8F%E4%BD%9C&zhida_source=entity)。

* * *

## 五、最小代码

```
task = {
    "name": "运行完整测试",
    "worker": "remote_test_worker",
    "done_when": "返回完整测试结果",
}

result = {
    "worker": task["worker"],
    "status": "done",
    "output": "4 failed, 6 passed",
}

print(result)
```

它表达的是：

```
任务要有执行者；
执行要有状态；
结果要能回传和验收。
```

* * *

## 六、这一讲让 Agent 长到了哪里？

到了第 9 讲，Agent 开始从“自己做事”升级为“组织别人做事”：

```
会拆分；
会委派；
会远程调度；
会追踪进度；
会回收结果。
```

它越来越像一个真正的工程负责人，而不只是一个执行脚本。

* * *

## 本讲小结

```
Remote 解决“在哪里执行”；
Delegation 解决“交给谁执行”；
主控负责目标、拆分、权限、追踪和验收；
任务下放不是结束，结果闭环才是完成。
```

下一讲：

> **Subagent / Multi-agent——集思广益，群策群力。**