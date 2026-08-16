---
id: "3529724637"
title: "为什么都在用ollama而lm studio却更少人使用?"
author: "黑风寨大债主"
type: zhihu-answer
source: "https://www.zhihu.com/question/654357364/answer/3529724637"
created: "2024-06-13 23:59"
updated: "2024-10-22 10:21"
collected: "2024-06-13 23:59"
downloaded: "2026-08-16"
---
我的体会：

1\. ollama用起来和docker一样的感觉，pull模型，run模型，ls看模型，ps看运行。非常顺手丝滑，入手无门槛。

2\. 另外，ollama支持很多主流LLM，什么Llama2/3，谷歌的gemma，mistral，国内的qwen，deepseek，llama的中文，微调各种chat，code，够用。而且都是量化好的，随拉随用，4090就跑的起来。尤其是在国内拉模型速度极快，我的环境最高可达15m/s，比起背墙的某h网站，方便很多。

3\. 还有一点，ollama是llama.cpp实现模型推理，模型小，速度快。

4\. 还有，ollama提供11434端口的web服务，重要的是还兼容openai的端点接口，可以和各种前端配合，比如ollama自己open webui，国产的chatbox，连后端带界面，一套搞定

5\. ollama是系统服务形式（也能容器运行），前后端分离（ 严格来说没有前端，只有命令行入口），耦合小，搭配灵活。

很好用，越用越好用，尤其对于linux用户。现在的主要问题是并发多模型不太好，将来会慢慢进的。

lm studio看界面很不错，功能也多。不过和界面耦合，最主要是拉模型太难了。

  

\--2024/10/22更新--

ollama的迭代很快，现在多模型并发的问题已经解决了