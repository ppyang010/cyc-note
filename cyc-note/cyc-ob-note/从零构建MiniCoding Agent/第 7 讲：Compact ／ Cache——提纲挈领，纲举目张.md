---
id: "2063318674673554071"
title: "第 7 讲：Compact / Cache——提纲挈领，纲举目张"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2063318674673554071"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 7
Created: "2026-07-22 17:53"
updated: "2026-08-15 14:55"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 7 讲：Compact / Cache——提纲挈领，纲举目张

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2063318674673554071)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **提纲挈领，纲举目张。**

第 5 讲让 Agent 学会记忆，第 6 讲让它学会复查。

但任务继续变长以后，新的问题会出现：

```
对话越来越长；
测试输出越来越多；
已经失效的推测还留在上下文里；
真正重要的目标、进度和下一步反而被淹没。
```

这时，光有 [Memory](https://zhida.zhihu.com/search?content_id=279592826&content_type=Article&match_order=1&q=Memory&zhida_source=entity) 还不够。

Agent 还要学会两种“做减法”的能力：

```
Compact：把长上下文提炼成一份可继续工作的提纲；
Cache：把稳定、常用、代价较高的结果存起来，避免重复计算。
```

![Image 1](https://pica.zhimg.com/v2-a8065251a15b2ecc3c7bd11cc830f028_1440w.jpg)

封面：任务越长，越要先抓住主线，再按需取回细节。

* * *

Compact 常被理解成“把内容缩短”。

但工程里的 Compact 不是机械删字，而是从长上下文中保留下一轮真正需要的工作骨架：

```
目标是什么；
已经完成什么；
当前发现了什么；
还有哪些约束；
下一步做什么。
```

![Image 2](https://pic2.zhimg.com/v2-5fd06249ee608b3a6c93a8a8203e38ed_1440w.jpg)

图 1：Compact 像把一张冗长菜谱提炼成主料、关键步骤和出餐要求。

### Compact 不应该丢掉什么？

至少不能丢掉：

```
任务目标；
关键结论；
尚未解决的问题；
用户约束；
下一步行动。
```

如果压缩以后只剩一句“继续修 Bug”，那不是 Compact，而是把任务压没了。

* * *

## 二、Cache：已经算清楚的，不必每次重来

Compact 解决的是“上下文太长”。

Cache 解决的是“同一结果被反复计算或反复读取”。

适合缓存的内容通常具有三个特点：

```
比较稳定；
会重复使用；
重新获取有成本。
```

例如：

```
项目目录结构；
固定测试命令；
已经验证过的搜索结果；
稳定的工具说明；
常用模板和配置。
```

![Image 3](https://pica.zhimg.com/v2-75e96e3615fa27f76da6c5ab46d73714_1440w.jpg)

图 2：Cache 像后厨的常用食材架，已经准备好的内容可以直接复用。

例如，Agent 已经确认测试命令是：

`python -m pytest -q`

只要项目配置没有变化，就不必每一轮重新阅读 README 才得到同一个结论。

### Cache 不是 Memory

两者容易混淆，但职责不同：

| 能力 | 主要保存什么 | 解决什么问题 |
| --- | --- | --- |
| Memory | 目标、进度、发现、约定 | 防止长任务失忆 |
| Cache | 可复用的结果、配置和中间产物 | 避免重复计算和重复读取 |
| Compact | 当前长上下文的精炼提纲 | 防止信息过载、主线丢失 |

一句话概括：

```
Memory 记住任务；
Compact 提炼任务；
Cache 加速任务。
```

* * *

## 三、Compact 与 Cache 怎样配合？

长任务里，最稳妥的做法是：

```
主线放在 Compact 里；
关键事实放在 Memory 里；
常用结果放在 Cache 里；
真正需要时再取回细节。
```

![Image 4](https://pic1.zhimg.com/v2-560fff97f3589468b1d85dc420a491b8_1440w.jpg)

图 3：提纲负责抓主线，缓存负责保存可复用细节，两者协同才能让长任务不乱。

可以把它想象成后厨：

```
墙上的今日菜单：Compact；
厨师的工作记录：Memory；
已经备好的高汤和酱料：Cache。
```

三者各司其职，Agent 才不会一边做菜，一边重新翻遍所有旧记录、重新熬同一锅高汤。

* * *

## 四、最小代码

```
compact = {
    "goal": "修复 4 个 Bug",
    "progress": "已完成 2/4",
    "remaining": ["median", "division by zero"],
    "next": "先修 median",
}

cache = {
    "test_command": "python -m pytest -q",
    "project_tree": "已缓存",
}

print(compact["next"])
print(cache["test_command"])
```

这段代码只表达两个思想：

```
Compact 保存可继续工作的主线；
Cache 保存可重复使用的结果。
```

* * *

## 五、这一讲让 Agent 成长到了哪里？

到了第 7 讲，Agent 开始具备处理长任务的“节奏感”：

```
信息多了，会先整理；
上下文长了，会先压缩；
结果稳定了，会缓存复用；
需要细节时，再按需取回。
```

它不再靠把所有东西堆在眼前来维持工作，而是开始学会管理信息。

* * *

## 本讲小结

```
Compact 不是简单删字，而是保留任务骨架；
Cache 不是长期记忆，而是复用稳定结果；
Memory 记住任务，Compact 提炼任务，Cache 加速任务；
提纲挈领，才能纲举目张。
```

下一讲：

> **Skills / Hooks / MCP——道器合一，以器载道。**