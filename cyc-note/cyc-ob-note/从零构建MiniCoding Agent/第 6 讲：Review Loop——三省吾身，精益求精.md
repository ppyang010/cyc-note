---
id: "2062980779085500655"
title: "第 6 讲：Review Loop——三省吾身，精益求精"
author: "二哥慈悲"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2062980779085500655"
column: "从零构建MiniCoding Agent"
column_id: "c_2071555890440827912"
lesson: 6
Created: "2026-07-22 16:39"
updated: "2026-07-27 21:24"
downloaded: "2026-09-01"
tags:
  - 知乎/专栏
  - AI/Agent
  - Coding-Agent
  - MiniCoding-Agent
---

# 第 6 讲：Review Loop——三省吾身，精益求精

> [!info] 来源信息
> - 专栏：从零构建MiniCoding Agent
> - 作者：二哥慈悲
> - 来源：[知乎专栏文章](https://zhuanlan.zhihu.com/p/2062980779085500655)
> - 抓取日期：2026-09-01
> - 说明：专栏中的纯视频条目未导入；本文正文保留文章内的图片、代码和文本链接。


> **三省吾身，精益求精。**
> 
> 出处说明：“三省吾身”出自《[论语·学而](https://zhida.zhihu.com/search?content_id=279517403&content_type=Article&match_order=1&q=%E8%AE%BA%E8%AF%AD%C2%B7%E5%AD%A6%E8%80%8C&zhida_source=entity)》“吾日三省吾身”。“精益求精”取意于《论语·学而》所引“如切如磋，如琢如磨”，[朱熹](https://zhida.zhihu.com/search?content_id=279517403&content_type=Article&match_order=1&q=%E6%9C%B1%E7%86%B9&zhida_source=entity)注释为“治之已精，而益求其精也”。

![Image 1](https://picx.zhimg.com/v2-e305f9247d268d154819d2a81df7497d.jpg?source=25ab7b06)

Review Loop——三省吾身，精益求精

Agent 最危险的一句话，往往不是“我不会”，而是：

`“我已经完成了。”`

代码改完了，不代表问题真的解决；某一次测试通过，也不代表没有新问题。

所以 [Harness](https://zhida.zhihu.com/search?content_id=279517403&content_type=Article&match_order=1&q=Harness&zhida_source=entity) 还需要一道独立的 Review Loop。

![Image 2](https://pic3.zhimg.com/v2-6ec2421f14ec321ba8f88720767123ec_1440w.jpg)

封面：执行者负责做完，Review 负责判断能不能交付。

* * *

### 一、“做完”不等于“通过”

做完，只说明动作结束了。

通过，则必须有证据：

```
测试是否全部通过；
目标是否真正满足；
有没有无关改动；
有没有违反权限和项目约定。
```

![Image 3](https://pic1.zhimg.com/v2-a81ae8f661caeec3c3d24098150cbeb6_1440w.jpg)

图 1：完成只是候选结果，检查通过以后才算真正完成。

在[四 Bug 案例](https://zhida.zhihu.com/search?content_id=279517403&content_type=Article&match_order=1&q=%E5%9B%9B+Bug+%E6%A1%88%E4%BE%8B&zhida_source=entity)中，不能只看“改了四个函数”，而要看：

```
10 passed；
git diff 只有必要修改；
正确测试没有被改；
修复报告和真实结果一致。
```

* * *

### 二、Review 要换一个视角重新看

执行者容易相信自己的判断，这就是“当局者迷”。

Review 要重新对照一遍：

```
需求有没有遗漏；
测试有没有漏跑；
边界条件有没有覆盖；
有没有顺手改了无关内容。
```

![Image 4](https://pic3.zhimg.com/v2-ab689073309bba53712f904d4aad1ad4_1440w.jpg)

图 2：三省吾身，不是反复自责，而是用清单重新检查目标、结果和边界。

Review 可以由另一个模型完成，也可以由同一个模型切换到独立检查模式；关键在于：

> **不能只是重复执行阶段原来的思路。**

* * *

### 三、精益求精不是无限修改

Review 不是为了没完没了地挑毛病。

它需要明确的停止标准：

达到标准，就允许交付；没有达到，就回到 Agent Loop 继续修。

![Image 5](https://pic2.zhimg.com/v2-dbd66fd3af6d9ced3646c3a77813e725_1440w.jpg)

图 3：不通过就回到修改—测试—复审；通过以后才允许交付。

完整闭环是：

```
执行
→ 测试
→ Review
→ 不通过：继续修改
→ 再测试、再 Review
→ 通过：允许交付
```

* * *

### 四、最小代码

```
def review(tests_pass, goal_met, no_extra_diff):
    return all([tests_pass, goal_met, no_extra_diff])

print("允许交付" if review(True, True, True) else "返回修改")
```

它表达的是：

> **完成不是一句话，而是一组同时满足的证据。**

* * *

### 五、这一讲让 Agent 长到了哪里？

到了第 6 讲，Agent 不仅会执行任务，还开始对质量负责：

```
结果可以验证；
过程可以复盘；
失败会回到循环；
通过后才允许交付。
```

这正是从“任务执行者”向“工程队友”迈进的关键一步。

* * *

### 本讲小结

```
做完不等于完成；
Review 要检查目标、测试、边界和回归；
三省吾身，是换视角重新核验；
精益求精，是不通过就改，通过后才交付。
```

下一讲：

> **Compact / Cache——提纲挈领，纲举目张。**