---
Title: "怎么成为一个 ai agent 工程师？ - 面叔 的回答"
Url: "https://www.zhihu.com/question/1936375725931361485/answer/2077692587385922329"
Author: "面叔面叔AI｜中小企业 AI 落地​ 关注"
Origin: "知乎回答"
Description: "我觉得如果你已经有 6 年后端经验，不要把自己当成“转行 AI 的新人”。你真正要做的是：把原来的工程能…"
Tags:
  - "人工智能"
  - "工程师"
  - "Agent"
Created: "2026-08-31 10:55:48"
Cover: "https://picx.zhimg.com/v2-98f2e73c0d32161569ee7beb5b58ad55_l.jpg?source=c8b7c179"
---

[谢邀 @Zarvis](https://www.zhihu.com/people/092b4cee739823f87bfb494f4a275b99)

我觉得如果你已经有 6 年后端经验， **不要把自己当成“转行 AI 的新人”。**

你真正要做的是：

> **把原来的工程能力，升级成“能把大模型接进真实业务”的能力。**

现在很多人学 Agent 的路线是：

Prompt → RAG → LangChain → MCP → 各种框架……

最后懂了一堆名词，但给他一个真实业务流程，还是不知道怎么做。

我会反过来。

先做一个完整的小项目，例如：

**客户询盘 → AI识别需求 → 查询资料 → 调用工具 → 生成结果 → 人工确认 → 写入系统**

然后在这个过程中缺什么补什么。

需要企业资料，就学 RAG；

需要操作外部系统，就学 Tool Calling / MCP；

需要多步骤执行，就学 Workflow / Agent；

开始跑生产以后，再解决日志、重试、权限、缓存、评估、成本和人工接管。

其实到了最后，你会发现：

**Agent 工程师很大一部分工作，仍然是工程。**

只不过以前你处理的是确定性的程序，现在你需要把一个具有不确定性的大模型，包进一个稳定的系统里。

所以后端经验不是包袱，反而是优势。

如果是我，我会把学习目标从：

> “半年学完 AI Agent 技术栈”

改成：

> **“90 天做出一个真的有人能使用的 Agent 系统。”**

做到这一点，再去补各种框架，速度会快很多。

而且企业最终真正愿意付钱的，也不是你会多少 Agent 框架。

而是：

**你能不能把 AI 接进业务，让它稳定干活。**

[发布于2026-08-31 09:41](https://www.zhihu.com/question/1936375725931361485/answer/2077692587385922329) ・广东

如果没基础的话可以先看微软的《AI Agents for Beginners》 - GitHub 5万+星，12课时左右就能很快入手，而且有完整的中文教程 [github.com/microsoft/ai](https://github.com/microsoft/ai-agents-for-beginners)

把Agent基础概念、工具调用、记忆系统、多Agent协作这些基本都覆盖完了，不需要网上找那些卖课的，来付费学习课程。

Hugging Face也有免费的《Agents Course》，但是更偏实践性。

[huggingface.co/learn/ag](https://huggingface.co/learn/agents-course)

生产部署，smolagents、LangGraph这些，如果要在自己的简历上添加做agent的项目经历，根据这里面的课程做几个小demo可能更好。

agent重要的其实是状态图、持久化、复杂工作流编排这些。学会这些，进行封装是可以手搓一个agent框架的，但是如果想快速部署，比如立刻做一个agent应用，也可以推荐几个框架。

一个是LangGraph。官方文档在 [langchain-ai.github.io/](https://langchain-ai.github.io/langgraph/)

社区教程是 [github.com/langchain-ai](https://github.com/langchain-ai/langgraph)

还有AutoGen，微软的

[Redirecting...](https://microsoft.github.io/autogen/)

[github.com/microsoft/au](https://github.com/microsoft/autogen)

CrewAI

[docs.crewai.com/](https://docs.crewai.com/)

[github.com/crewAIInc/cr](https://github.com/crewAIInc/crewai)

---

还是推荐手搓比较好，手搓可以推荐Datawhale《Hello-Agents》，从零入手直接手搓agent框架，没有任何库依赖。

[github.com/datawhalechi](https://github.com/datawhalechina/hello-agents)

一天一小时需要一个月，刷完 [anthropic.skilljar.com/](https://anthropic.skilljar.com/claude-with-the-anthropic-api) 这个 Claude 的官方教程，你就算是入门了。这是我目前看到的最好的基础教程，整个流程和各个知识点都会讲到，了解整个 ai agent 的工作原理。

之后就可以有针对性的进行深入学习了。

[西藏日喀则吉隆口岸发生泥石流 382 万](https://www.zhihu.com/search?q=%E8%A5%BF%E8%97%8F%E6%97%A5%E5%96%80%E5%88%99%E5%90%89%E9%9A%86%E5%8F%A3%E5%B2%B8%E5%8F%91%E7%94%9F%E6%B3%A5%E7%9F%B3%E6%B5%81&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 热

[个人房贷最长不超过 40 年 320 万](https://www.zhihu.com/search?q=%E4%B8%AA%E4%BA%BA%E6%88%BF%E8%B4%B7%E6%9C%80%E9%95%BF%E4%B8%8D%E8%B6%85%E8%BF%87+40+%E5%B9%B4&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 热

[女排 朱婷 311 万](https://www.zhihu.com/search?q=%E5%A5%B3%E6%8E%92+%E6%9C%B1%E5%A9%B7&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 新

[Zhihu CLI 功能上新 306 万](https://www.zhihu.com/search?q=Zhihu+CLI+%E5%8A%9F%E8%83%BD%E4%B8%8A%E6%96%B0&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 热

[出发吧！看山 305 万](https://event.zhihu.com/travel-game/) 活动

[吉隆泥石流痕迹有 20 层楼高 304 万](https://www.zhihu.com/search?q=%E5%90%89%E9%9A%86%E6%B3%A5%E7%9F%B3%E6%B5%81%E7%97%95%E8%BF%B9%E6%9C%89+20+%E5%B1%82%E6%A5%BC%E9%AB%98&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 新

[中国女排憾负泰国无缘直通奥运会 304 万](https://www.zhihu.com/search?q=%E4%B8%AD%E5%9B%BD%E5%A5%B3%E6%8E%92%E6%86%BE%E8%B4%9F%E6%B3%B0%E5%9B%BD%E6%97%A0%E7%BC%98%E7%9B%B4%E9%80%9A%E5%A5%A5%E8%BF%90%E4%BC%9A&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 新

[比尔盖茨万字长文示警AI时代 301 万](https://www.zhihu.com/search?q=%E6%AF%94%E5%B0%94%E7%9B%96%E8%8C%A8%E4%B8%87%E5%AD%97%E9%95%BF%E6%96%87%E7%A4%BA%E8%AD%A6AI%E6%97%B6%E4%BB%A3&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content)

[孙宇晨重仓资产被欧盟英国制裁 283 万](https://www.zhihu.com/search?q=%E5%AD%99%E5%AE%87%E6%99%A8%E9%87%8D%E4%BB%93%E8%B5%84%E4%BA%A7%E8%A2%AB%E6%AC%A7%E7%9B%9F%E8%8B%B1%E5%9B%BD%E5%88%B6%E8%A3%81&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content) 热

[新版《国防动员法》10 月 1 日实施 277 万](https://www.zhihu.com/search?q=%E6%96%B0%E7%89%88%E3%80%8A%E5%9B%BD%E9%98%B2%E5%8A%A8%E5%91%98%E6%B3%95%E3%80%8B10+%E6%9C%88+1+%E6%97%A5%E5%AE%9E%E6%96%BD&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content)