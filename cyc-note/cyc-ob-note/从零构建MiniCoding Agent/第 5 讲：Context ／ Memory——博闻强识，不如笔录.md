---
id: "2062976957806122678"
title: "第 5 讲：Context / Memory——博闻强识，不如笔录"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2062976957806122678"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 5
Created: "2026-07-21 19:12"
updated: "2026-07-27 21:21"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 5 讲：Context / Memory——博闻强识，不如笔录

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2062976957806122678)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **[博闻强识](https://zhida.zhihu.com/search?content_id=279516753&content_type=Article&match_order=1&q=%E5%8D%9A%E9%97%BB%E5%BC%BA%E8%AF%86&zhida_source=entity)，不如笔录。**

![Image 1](https://picx.zhimg.com/v2-a783b151cccecc5f93110ab466f40445.jpg?source=25ab7b06)

前几讲里，Agent 已经会接任务、会循环、会用工具，也知道要守边界。

但任务一长，它很容易出现另一种问题：

```
忘了用户原来的要求；
重复已经失败的尝试；
记得做过，却说不清做到哪里；
上下文越堆越长，反而找不到重点。
```

所以，第 5 讲要给 Agent 配一本真正的后厨工作本。

![Image 2](https://pic2.zhimg.com/v2-d92274984d2c53133f194a0a628501eb_1440w.jpg)

封面：Context 是眼前案板，Memory 是跨轮次保存的后厨工作本。

* * *

### 一、Context：这一轮眼前要看什么？

Context 是 Agent 当前这一步真正能看到的信息，例如：

```
当前文件；
刚刚的测试结果；
正在处理的 Todo；
用户最新的要求。
```

它像厨师眼前的案板。

案板太空，做不了事；案板堆满所有食材、旧盘子和废纸，也一样会乱。

![Image 3](https://pic3.zhimg.com/v2-04294c6b5040dec12a53243602fd77ec_1440w.jpg)

图 1：Context 只放当前工作需要的信息：当前文件、测试结果和当前步骤。

所以 Context 管理的原则不是“越多越好”，而是：

> **当前要做什么，就先拿什么。**

* * *

### 二、Memory：哪些事情必须跨轮次记住？

Memory 不是把整段对话原封不动存下来，而是记录以后还会影响行动的关键事实。

最少应保存四类信息：

```
目标：最终要完成什么；
进度：已经做到哪里；
发现：哪些结论已经被验证；
约定：哪些边界和规则不能忘。
```

![Image 4](https://pic1.zhimg.com/v2-6c7708b7b779db7ebdb6da44a5c10e4e_1440w.jpg)

图 2：Memory 像后厨工作本，目标、进度、关键发现和项目约定都要记下来。

继续用 `enhanced_project` 的四 [Bug 案例](https://zhida.zhihu.com/search?content_id=279516753&content_type=Article&match_order=1&q=Bug+%E6%A1%88%E4%BE%8B&zhida_source=entity)：

```
目标：让 10 个测试全部通过；
已完成：add() 已修复；
当前结果：3 failed, 7 passed；
关键发现：mean() 没处理空列表；
约定：不修改正确测试期望。
```

这样下一轮 Agent 就不用重新猜，也不会把已经确认的结论弄丢。

* * *

### 三、记忆要经历“写入—整理—读取”

记忆系统不是一个只进不出的仓库。

真正可用的 Memory 要完成三件事：

```
写入：把重要结果记下来；
整理：按目标、进度、发现和约定分类；
读取：下一步只取真正需要的内容。
```

![Image 5](https://pic1.zhimg.com/v2-ff2f99341b4427d27b1aac6825fa95b4_1440w.jpg)

图 3：该记的记下来，该用的再拿出来；不是把所有历史重新塞进上下文。

如果什么都保存，Memory 会变成杂物间；如果什么都不存，Agent 每一轮都像失忆。

好的[记忆系统](https://zhida.zhihu.com/search?content_id=279516753&content_type=Article&match_order=2&q=%E8%AE%B0%E5%BF%86%E7%B3%BB%E7%BB%9F&zhida_source=entity)，追求的是：

```
少而关键；
结构清楚；
随任务更新；
需要时能快速取回。
```

* * *

### 四、最小代码

```
memory = {
    "goal": "修复 4 个 Bug",
    "progress": "已修复 add()",
    "finding": "mean() 未处理空列表",
    "next": "补充边界测试",
}

print(memory["next"])
```

这段代码只表达一个思想：

> **每做一步，都要留下能支持下一步的记录。**

* * *

### 五、这一讲让 Agent 长到了哪里？

有了 Context / Memory，Agent 才开始具备长任务能力：

```
不忘目标；
不丢进度；
不重复踩坑；
能从上一次停下的地方继续。
```

它开始从一次性的任务执行者，向能够持续协作的工程队友靠近。

* * *

### 本讲小结

```
Context 管“这一轮看什么”；
Memory 管“跨轮次记什么”；
记忆要写入、整理、按需读取；
博闻强识还不够，关键工程信息必须笔录。
```

下一讲：

> **Review Loop——三省吾身，精益求精。**