---
title: "怎么成为一个 ai agent 工程师？"
author: "AIKS"
source: "https://www.zhihu.com/question/1936375725931361485/answer/2109298205322224155"
site: "知乎"
published: 2026-11-26
created: 2026-11-26
summary_model: "gpt-6.2-sol"
tags:
  - 阅读笔记
  - AI智能体
  - SpringAI
  - 工程实践
---

# 怎么成为一个 AI Agent 工程师？

原文是 AIKS 于 2026 年 11 月 26 日发布的知乎回答。总结模型为 `gpt-6.2-sol`。[知乎原文](https://www.zhihu.com/question/1936375725931361485/answer/2109298205322224155)

## 目录

- [[#从后端转 Agent 先练什么]]
- [[#Spring AI 2.0.2 的重试实测]]
- [[#延伸阅读]]
- [[#原文剪藏]]

## 从后端转 Agent 先练什么

把大模型当作有延迟、调用成本和限流约束的下游服务。先选一个真实业务场景，把工具调用、流式返回和会话记忆串起来。然后用模拟服务分别返回 HTTP 429、HTTP 500 或延迟响应，观察调用次数、等待时间、最终错误和用户收到的流式输出。练习的验收点是能说明模型故障、响应慢或限流时，系统会如何处理。

## Spring AI 2.0.2 的重试实测

- AIKS 用模拟服务持续返回 HTTP 429。把旧的 `spring.ai.retry.max-attempts` 设为 1 或 10，观察到的都是 4 次请求。作者将这一行为归因于 Spring AI 2.0 的 OpenAI 模块改用官方 SDK 处理重试。
- 原文示例中的 `spring.ai.openai.max-retries=2` 配置的是首次请求之后的重试次数，`spring.ai.openai.timeout=30s` 配置的是单次请求超时。核对总耗时时还需计入重试间隔。
- 模拟服务返回 `Retry-After: 60` 时，作者观察到 SDK 每次约等 8 秒，三次重试都落在限流窗口内，约 25 秒后失败。这是回答中该版本和场景的实测结果。

## 延伸阅读

作者另有一篇文章对照 Spring AI 1.1 和 2.0 在 429、500、超时和流式场景中的重试行为，并讨论备用模型注册成 Bean 后的主模型选择问题。[Spring AI 调大模型报 429 怎么办](https://zhuanlan.zhihu.com/p/2104513081422492387)

[[ai-output/AI Agent 学习路线|AI Agent 学习路线]]

## 原文剪藏

从后端转过去的话，最该补的不是提示词，而是把大模型当成一个又慢、又贵、还会限流的下游服务来对待。会调 API 写个 demo 的人很多，能把限流、超时、重试、流式输出、上下文这几件事兜住的人少，差距在这里。

举一个我在 Spring AI 2.0.2 上用假服务测过的例子。很多人照着老文档配 `spring.ai.retry.max-attempts`，配 1 次、配 10 次，模型返回 429 时都一样发了 4 次请求，因为 2.0 起 OpenAI 模块的重试交给了官方 SDK，真正生效的是这两个：

```
# Spring AI 2.0 OpenAI 模块：重试次数（不含第一次，默认 3）和单次超时（默认 60 秒，超时也会重试）
spring.ai.openai.max-retries=2
spring.ai.openai.timeout=30s
```

还有更隐蔽的：服务商返回 `Retry-After: 60` 让你等一分钟，SDK 每次只等 8 秒左右，3 次重试全撞在限流窗口里，25 秒后照样失败。这些问题 demo 里看不出来，上了生产才会冒出来。

所以路线可以这样走：先拿一个真实业务场景做完整的 agent（工具调用、流式返回、会话记忆），再逐个把上面这些异常情况用假服务复现一遍。能讲清楚”模型挂了、慢了、限流了，我的系统会怎样”，就够格叫 agent 工程师了。

1.1 和 2.0 两个版本对 429、500、超时、流式的重试行为对比表，以及备用模型注册成 Bean 会把主模型顶掉的坑，都在这篇： [Spring AI 调大模型报 429 怎么办](https://zhuanlan.zhihu.com/p/2104513081422492387) 。这些实测都在这个号里持续更新，感兴趣可以关注。

你现在做 agent 主要用哪套：A. Spring AI；B. [LangChain](https://zhida.zhihu.com/search?content_id=806118571&content_type=Answer&match_order=1&q=LangChain&zhida_source=entity) / [LangGraph](https://zhida.zhihu.com/search?content_id=806118571&content_type=Answer&match_order=1&q=LangGraph&zhida_source=entity) ；C. 直接调各家 SDK？
