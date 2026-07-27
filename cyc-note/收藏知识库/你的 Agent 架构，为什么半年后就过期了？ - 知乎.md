[(99+ 封私信 / 84 条消息) 你的 Agent 架构，为什么半年后就过期了？ - 知乎](https://zhuanlan.zhihu.com/p/2064610816037540542) 

 JHOo | 训练数字工程师，也修炼真实的自己。

知乎：文章解读｜小红书：重点贴图｜B站：完整中文字幕｜抖音：精华剪辑 · 搜索 JHOo 或同名标题。

* * *

最近看了一场只有 19 分钟的演讲，标题非常扎心：

> Your Agent Architecture Has a Half-Life of 6 Months  
> 你的 Agent 架构，[半衰期](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%8D%8A%E8%A1%B0%E6%9C%9F&zhida_source=entity)只有六个月。

演讲者是 [Inngest](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=Inngest&zhida_source=entity) 联合创始人兼 CTO [Dan Farrelly](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=Dan+Farrelly&zhida_source=entity)。

这句话并不是说所有 Agent 项目半年后都会报废，而是在提醒我们：今天看起来很先进的模型、Prompt、工具协议和 Agent 编排方式，半年后很可能已经不是主流。如果[系统架构](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84&zhida_source=entity)与这些快速变化的部分深度绑定，[技术栈](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%8A%80%E6%9C%AF%E6%A0%88&zhida_source=entity)每升级一次，团队就要跟着重写一次。

我看完整场演讲后，最大的收获可以浓缩成一句话：

> 把变化最快的部分做成可替换组件，把最不能失败的部分做成稳定基础设施。

![](https://picx.zhimg.com/v2-bf84ae894a2c3e8ca113b85564a4b69b_1440w.jpg)

### 一、我们为什么总在重写 Agent？

回看过去一段时间，Agent 的热点几乎没有停过：

*   RAG、ReAct、[Prompt Chaining](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=Prompt+Chaining&zhida_source=entity)；
*   Function Calling、[MCP](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=MCP&zhida_source=entity)、CLI；
*   单 Agent、多 Agent、Sub-agent；
*   Coding Agent、Background Agent、Agent Factory；
*   云端 [Sandbox](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=Sandbox&zhida_source=entity)、本地执行环境、浏览器[自动化](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E8%87%AA%E5%8A%A8%E5%8C%96&zhida_source=entity)。

这些方案都可能有价值，问题在于它们变化得太快。

新模型出现后，旧 Prompt 可能失效；新的工具协议出现后，原有[调用链](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E8%B0%83%E7%94%A8%E9%93%BE&zhida_source=entity)可能要重构；当任务从一次对话变成运行数小时的后台流程时，原先围绕“请求—响应”设计的系统又会迅速触顶。

所以真正的问题不是“下一个框架应该选谁”，而是：

**当模型、工具和 Agent 形态继续变化时，系统中哪些部分应该跟着变，哪些部分必须保持稳定？**

### 二、把 Agent 系统拆成三层

Dan 把 Agent 系统分成三个概念层：计算层、上下文层和[执行层](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%89%A7%E8%A1%8C%E5%B1%82&zhida_source=entity)。

### 1\. [计算层](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=2&q=%E8%AE%A1%E7%AE%97%E5%B1%82&zhida_source=entity)：负责思考

计算层的核心是模型。它负责推理、规划、生成和判断。

但模型也是替换最频繁的组件之一。团队可能因为能力、成本、速度或上下文窗口，随时切换到新的模型，甚至在一次任务中[动态路由](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%8A%A8%E6%80%81%E8%B7%AF%E7%94%B1&zhida_source=entity)多个模型。

所以，模型应该提供智能，却不应该保存系统唯一的真实状态。

### 2\. 上下文层：负责让模型“知道什么、能做什么”

这一层包括：

*   System Prompt 和任务指令；
*   对话历史与[长期记忆](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E9%95%BF%E6%9C%9F%E8%AE%B0%E5%BF%86&zhida_source=entity)；
*   RAG 检索结果；
*   文件、代码和数据库信息；
*   API、MCP、CLI 等工具；
*   当前步骤的状态和前序结果。

上下文层非常重要，但同样变化很快。今天把全部历史塞进上下文，明天可能改成摘要加按需检索；今天使用 MCP，明天也可能改成 CLI 或直接调用 API。

因此，上下文层需要易于组合和替换。

### 3\. 执行层：确保事情真的做完

执行层负责的是那些不够“性感”、却决定 Agent 能否进入[生产环](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E7%94%9F%E4%BA%A7%E7%8E%AF&zhida_source=entity)境的能力：

*   状态[持久化](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%8C%81%E4%B9%85%E5%8C%96&zhida_source=entity)；
*   失败重试与[断点恢复](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%96%AD%E7%82%B9%E6%81%A2%E5%A4%8D&zhida_source=entity)；
*   延时、定时和事件调度；
*   暂停、取消与人工审批；
*   [并发控制](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%B9%B6%E5%8F%91%E6%8E%A7%E5%88%B6&zhida_source=entity)和任务队列；
*   子 Agent 的派发与结果汇总；
*   [幂等](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%B9%82%E7%AD%89&zhida_source=entity)、去重和超时；
*   全链路可观测与审计。

模型会变，Prompt 会变，工具会变，Sandbox 也会变，但这些可靠执行能力不会消失。

![](https://pic4.zhimg.com/v2-098dc47f736926b76654de79ee6ac623_1440w.jpg)

### 三、Sandbox 是“手”，执行层才是“脑”

现在很多 Agent 产品会给模型配一个 Sandbox，让它能够执行代码、操作文件、安装依赖和调用工具。

Sandbox 很适合充当 Agent 的“手”，却不适合成为整个系统的“脑”。

原因很直接：

*   Sandbox 可能被销毁或回收；
*   本地文件未必可靠持久化；
*   进程可能因为超时、崩溃或升级而中断；
*   单个 Sandbox 很难掌握跨任务、跨 Agent 的全局状态；
*   把恢复逻辑写进 Sandbox，会让[业务逻辑](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E4%B8%9A%E5%8A%A1%E9%80%BB%E8%BE%91&zhida_source=entity)和基础设施紧密耦合。

更合理的边界应该是：

```text
执行层
  ├─ 保存任务状态
  ├─ 决定和调度下一步
  ├─ 失败后恢复任务
  └─ 记录完整运行轨迹
        │
        ▼
Sandbox
  ├─ 执行命令
  ├─ 修改文件
  ├─ 调用工具
  └─ 返回结果
```

一句话概括：**Sandbox 可以替换，任务状态不能丢。** 

![](https://picx.zhimg.com/v2-a391d84699c62d02380e56142da954e9_1440w.jpg)

### 四、Agent 的基本单位，不该是一次回复

传统 LLM 应用通常围绕一次 Prompt 和一次 Response 展开。但生产级 Agent 更像一个循环：

```text
接收目标
  → 获取上下文
  → 模型判断
  → 调用工具
  → 观察结果
  → 更新状态
  → 再次判断
  → 达成目标或退出
```

这个循环可能运行几分钟，也可能运行几个小时；可能发起数百次工具调用；没有用户一直盯着它；而且几乎可以确定，中间至少会有一步失败。

因此，Agent 的基本单位不应只是“某次模型回复”，而应该是一次从目标开始、直到结果落地的完整运行（Run）。

每次 Run 至少应该记录：

*   初始目标和唯一标识；
*   使用的模型、Prompt 和工具版本；
*   每一步输入、输出和状态变化；
*   错误、重试及恢复过程；
*   最终结果；
*   后续真实业务效果。

这也是为什么只记录聊天消息远远不够。聊天记录告诉我们 Agent “说了什么”，运行轨迹才能告诉我们它“做了什么”。

### 五、把决策交给模型，把边界留给代码

Agent 需要灵活决策，但灵活不等于把所有事情都交给模型。

适合交给模型的部分包括：

*   理解模糊目标；
*   制定或调整计划；
*   选择工具；
*   分析非结构化信息；
*   根据反馈修正方向。

适合由确定性代码和执行层控制的部分包括：

*   [权限边界](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%9D%83%E9%99%90%E8%BE%B9%E7%95%8C&zhida_source=entity)；
*   输入输出校验；
*   重试、退避和超时；
*   并发及成本限制；
*   [幂等控制](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%B9%82%E7%AD%89%E6%8E%A7%E5%88%B6&zhida_source=entity)；
*   高风险操作审批；
*   审计与合规要求。

我很认同这里隐含的一个原则：

> 让模型在受控范围内做判断，让基础设施保证这些判断能够安全、可靠地落地。

### 六、Agent 评估不能只看“回答得像不像”

Agent 的价值往往发生在外部世界中，而不只是最终生成的一段文字。

例如：

*   编程 Agent 是否真的创建了可合并的 PR？
*   PR 是否通过测试和审查，最终被合并？
*   研究 Agent 的报告是否被团队采用？
*   客服 Agent 是否真正解决了问题？
*   运营 Agent 是否正确修改了目标系统中的数据？
*   长流程任务失败后，是否仍然最终完成？

因此，评估至少应该分为三个层次：

1.  **步骤质量**：工具和参数选择是否合理；
2.  **运行质量**：任务是否可靠、合规、低成本地完成；
3.  **业务结果**：最终结果是否真正被接受和使用。

而且真实结果经常延迟出现。PR 可能几天后才被合并，[研究报告](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E7%A0%94%E7%A9%B6%E6%8A%A5%E5%91%8A&zhida_source=entity)可能一周后才被引用。评估系统必须能把这些后续事件重新关联到最初那次 Agent Run。

![](https://pic1.zhimg.com/v2-f3b9369e54b11299679e3abf30424fa2_1440w.jpg)

### 七、这套观点也要批判性地看

Dan 是 Inngest 的联合创始人，而 Inngest 本身提供持久执行、队列、[流量控制](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%B5%81%E9%87%8F%E6%8E%A7%E5%88%B6&zhida_source=entity)和可观测等能力。所以这场演讲天然会强调执行层的重要性，也与其产品定位一致。

但这并不意味着观点没有价值。我们需要区分：

1.  **普遍的架构原则**：把可靠执行与快速变化的模型、Prompt 和工具解耦；
2.  **具体的产品选择**：使用 Inngest、自建[工作流引擎](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E5%B7%A5%E4%BD%9C%E6%B5%81%E5%BC%95%E6%93%8E&zhida_source=entity)，还是采用其他持久执行平台。

对于简单、低风险、失败后可以快速重跑的 Agent，一整套持久执行平台可能太重；对于跨多个系统、运行时间长、会产生真实副作用的 Agent，执行层通常会很快成为必要基础设施。

### 八、一个实用的落地检查表

如果正在做 Agent 系统，可以先问自己这些问题：

*   每次 Run 是否有唯一标识，步骤状态是否持久化？
*   进程或 Sandbox 被销毁后能否继续？
*   工具调用是否幂等，重试会不会产生重复副作用？
*   是否支持超时、取消和人工介入？
*   子 Agent 的任务、依赖和结果是否可追踪？
*   高风险动作是否有确定性的校验或审批？
*   是否能查看一次 Run 的完整时间线？
*   更换模型、工具协议或 Sandbox，需要改动多少核心代码？
*   评估是在测“回答质量”，还是在测“任务结果”？

如果这些问题大多没有答案，那么系统可能只是一个好看的 Demo，还不是一个可靠的 Agent 产品。

### 最后的感受

这场演讲最打动我的，不是它推荐了哪个框架，而是它提供了一种判断[架构边界](https://zhida.zhihu.com/search?content_id=279827722&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E8%BE%B9%E7%95%8C&zhida_source=entity)的方法：

*   模型提供智能；
*   上下文提供信息和工具；
*   Sandbox 提供执行环境；
*   执行层提供连续性和可靠性；
*   结果评估判断系统是否真正创造价值。

我们无法预测半年后最流行的模型、协议和 Agent 范式，但可以提前设计好边界，让变化只发生在应该变化的地方。

一个架构能否活过下一轮技术浪潮，取决的不是它有没有猜中未来，而是它有没有把最容易变化的部分隔离出去。

* * *

原演讲：Dan Farrelly，Inngest 联合创始人兼 CTO  
视频标题：Your Agent Architecture Has a Half-Life of 6 Months  
原始来源：[https://www.youtube.com/watch?v=X1kp-ABIIxQ](https://link.zhihu.com/?target=https%3A//www.youtube.com/watch%3Fv%3DX1kp-ABIIxQ)

本文为个人学习整理与中文解读。演讲视频及画面版权归原发布方所有。