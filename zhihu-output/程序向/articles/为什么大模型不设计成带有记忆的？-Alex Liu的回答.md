---
id: "2017720943145939816"
title: "为什么大模型不设计成带有记忆的？"
author: "Alex Liu"
type: zhihu-answer
source: "https://www.zhihu.com/question/2015214268652474918/answer/2017720943145939816"
created: "2026-03-18 21:56"
updated: "2026-03-18 21:56"
collected: "2026-03-18 21:56"
downloaded: "2026-08-16"
---
这个问题触及了LLM架构的核心矛盾。简单来说，不让模型"记住一切"是因为**技术限制**和**经济考量**，但下一代架构必然会改变这一点。

  
从技术角度看，当前Transformer的attention机制要求每次推理都要重新处理全部历史，这导致计算复杂度随对话长度呈平方增长。如果模型内置持久记忆，就会面临训练时梯度消失和推理时检索效率的双重挑战。更根本的是，该领域长期缺乏一个理论框架来量化"记忆容量"应该如何随模型规模变化。最近发表在 [Beyond scaling laws: Understanding transformer performance with associative memory](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2405.08707) 中的研究试图解决这个难题。

  
这项研究发现，Transformer和记忆系统应该分工而非融合。Transformer擅长的是短期模式匹配和推理，而长期知识存储应该交给专门的associative memory模块。这就像人类大脑：工作记忆容量有限但处理快速，长期记忆容量巨大但需要主动检索。强行让Transformer"记住所有历史"，就像试图让工作记忆承担长期记忆的功能，既低效又不合理。

  
当前的RAG方案（外部数据库检索+LLM生成）其实是工程上的折中：简单、灵活、可升级。但这种方法有根本缺陷——检索和推理是分离的，模型无法主动控制"该记什么、该忘什么"。上述研究给出了未来神经记忆架构的scaling law：总性能是Transformer处理能力加上associative memory容量的函数，而非单纯依赖参数量。

  
所以大模型现在不"带记忆"不是因为不想，而是因为还不知道如何正确地做。答案不是让context window无限延长（那只是在逃避问题），而是设计出能与推理系统深度融合的神经记忆模块，这正是该领域正在努力的方向。