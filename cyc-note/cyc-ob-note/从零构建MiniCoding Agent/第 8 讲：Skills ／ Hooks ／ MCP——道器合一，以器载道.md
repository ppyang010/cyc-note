---
id: "2063321155545698488"
title: "第 8 讲：Skills / Hooks / MCP——道器合一，以器载道"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2063321155545698488"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 8
Created: "2026-08-04 11:54"
updated: "2026-08-15 14:55"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 8 讲：Skills / Hooks / MCP——道器合一，以器载道

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2063321155545698488)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **道器合一，以器载道。**
> 
> 出处说明：本讲题眼化用《[周易·系辞上](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E5%91%A8%E6%98%93%C2%B7%E7%B3%BB%E8%BE%9E%E4%B8%8A&zhida_source=entity)》“形而上者谓之道，[形而下](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E5%BD%A2%E8%80%8C%E4%B8%8B&zhida_source=entity)者谓之器”。这里借“道”指方法、经验和原则，借“器”指工具、接口与[运行机制](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E8%BF%90%E8%A1%8C%E6%9C%BA%E5%88%B6&zhida_source=entity)。只有把方法落到具体载体上，能力才能真正生效。

前七讲解决了 Agent 怎样完成一次任务：

```
接任务；
拆步骤；
循环执行；
调用工具；
保存记忆；
独立复查；
管理长上下文。
```

但一个成熟系统不能每次都从零开始。

它还要回答三个问题：

```
做过的经验，怎样留下来？
关键事件发生时，怎样自动行动？
模型怎样发现并连接外部工具与数据？
```

对应的三个机制就是：

```
Skills：可复用的经验和方法；
Hooks：条件满足时自动触发的动作；
MCP：连接模型、工具、资源与服务的协议。
```

![Image 1](https://pic2.zhimg.com/v2-428de2a5d3ef750164f1d1edb9839d5d_1440w.jpg)

封面：方法是“道”，技能、触发器和协议是承载方法的“器”。

* * *

Agent 成功修过一次 Bug，不代表以后自然就会稳定复现这套方法。

要让经验真正留下来，需要把它整理成 Skill：

```
适用场景；
输入是什么；
标准步骤；
注意事项；
完成标准。
```

![Image 2](https://picx.zhimg.com/v2-972ec7884d85d4fae24b001bf12fce99_1440w.jpg)

图 1：Skills 像技能卡库，把经过验证的经验整理成可复用的方法。

例如，“修复测试失败”可以沉淀成一张技能卡：

```
适用场景：已有测试失败的 Python 项目；
步骤：复现 → 定位 → 最小修改 → 回归测试 → 检查 diff；
约束：不改正确测试，不做无关重构；
完成标准：全部测试通过且没有无关改动。
```

Skills 的价值是：

> **把偶然做对，变成下次还能稳定做对。**

* * *

## 二、Hooks：让[关键节](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E5%85%B3%E9%94%AE%E8%8A%82&zhida_source=entity)点自动触发动作

有些动作不应该依赖人一直盯着。

当某个事件发生或条件满足时，系统可以自动触发下一步：

```
测试失败 → 自动生成失败摘要；
文件修改完成 → 自动运行格式检查；
任务结束 → 自动进入 Review；
每天固定时间 → 自动生成进度报告。
```

![Image 3](https://pic3.zhimg.com/v2-e246e27fd78099523d00bfb387d79766_1440w.jpg)

图 2：Hooks 像后厨提醒铃，关键条件一到，系统自动触发相应动作。

Hook 通常包含三部分：

```
触发条件；
要执行的动作；
执行后的记录。
```

例如：

```
条件：测试命令返回失败；
动作：提取失败用例和错误栈；
记录：写入 Observation，并把 Todo 标记为需要继续修复。
```

Hooks 让流程少依赖人工提醒，也减少“忘了做下一步”的情况。

* * *

## 三、MCP：把模型和真实能力接起来

Skills 告诉 Agent 应该怎样做，Hooks 决定什么时候做。

但真正执行时，还需要把模型与文件、数据库、搜索、代码执行、[业务系统](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E4%B8%9A%E5%8A%A1%E7%B3%BB%E7%BB%9F&zhida_source=entity)等能力连接起来。

这就是 MCP（[Model Context Protocol](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=Model+Context+Protocol&zhida_source=entity)，模型上下文协议）在本讲中的位置。

![Image 4](https://pic1.zhimg.com/v2-096e92a31dd85aaee45d8ac780b4fcb0_1440w.jpg)

图 3：MCP 像统一工具站，让模型能够发现能力、调用能力并获得结构化结果。

可以先把 MCP 朴素地理解成：

```
工具怎样被描述；
模型怎样发现工具；
参数怎样传入；
结果怎样返回；
权限和错误怎样表达。
```

例如，模型不必知道数据库内部怎样连接，只需要知道有一个结构清楚的能力：

`search_orders(customer_id, date_range)`

通过协议，模型能够正确调用，并收到结构化结果。

### MCP 不是 Skill，也不是 Hook

| 机制 | 主要回答什么 |
| --- | --- |
| Skills | 这类任务应该怎样做？ |
| Hooks | 什么时候自动做？ |
| MCP | 怎样连接并调用外部能力？ |

一句话概括：

```
Skills 给方法；
Hooks 给时机；
MCP 给连接。
```

* * *

## 四、三者怎样组成[能力闭环](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E8%83%BD%E5%8A%9B%E9%97%AD%E7%8E%AF&zhida_source=entity)？

一个完整例子：

```
Skill：
定义“测试失败修复流程”。

Hook：
检测到 pytest 失败后自动启动该流程。

MCP：
连接文件读取、终端执行、代码编辑和测试工具。
```

最终形成：

```
事件发生
→ Hook 触发
→ Skill 提供方法
→ MCP 连接工具
→ Agent 执行
→ 结果写回 Memory
→ Review 检查
```

这就是“[道器合一](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=2&q=%E9%81%93%E5%99%A8%E5%90%88%E4%B8%80&zhida_source=entity)，以器载道”的工程化表达：

```
方法不能只停留在提示词里；
经验要封装；
时机要自动化；
工具要通过协议接入。
```

* * *

### 五、最小代码

```
skill = {
    "name": "修复测试失败",
    "steps": ["复现", "定位", "修改", "回归测试"],
}

hook = {
    "when": "pytest_failed",
    "run": skill["name"],
}

mcp_tool = {
    "name": "run_tests",
    "input": "command",
    "output": "test_result",
}

print(hook)
print(mcp_tool)
```

它表达的是：

```
经验要封装成 Skill；
事件要触发 Hook；
工具要通过统一协议被发现和调用。
```

* * *

### 六、这一讲让 Agent 成长到了哪里？

到了第 8 讲，Agent 不再只是完成一次任务，而开始形成可持续扩展的[能力系统](https://zhida.zhihu.com/search?content_id=279593727&content_type=Article&match_order=1&q=%E8%83%BD%E5%8A%9B%E7%B3%BB%E7%BB%9F&zhida_source=entity)：

```
经验可以复用；
动作可以自动触发；
外部工具可以统一接入；
工作流程可以被组织和组合。
```

这一步让 Agent 从“会做事的个体”，继续向“可扩展的 AI 工作者系统”成长。

* * *

## 本讲小结

```
Skills：���经验沉淀成可复用方法；
Hooks：在关键节点自动触发动作；
MCP：把模型、工具、数据和服务连接起来；
Skills 给方法，Hooks 给时机，MCP 给连接；
道器合一，能力才能真正落地。
```

下一讲：

> **Remote / Delegation——运筹帷幄，决胜千里。**