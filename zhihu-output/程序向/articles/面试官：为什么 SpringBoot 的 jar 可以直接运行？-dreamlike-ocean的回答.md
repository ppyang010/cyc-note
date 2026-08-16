---
id: "3016210229"
title: "面试官：为什么 SpringBoot 的 jar 可以直接运行？"
author: "dreamlike-ocean"
type: zhihu-answer
source: "https://www.zhihu.com/question/598680332/answer/3016210229"
created: "2023-05-06 22:56"
updated: "2023-05-06 22:56"
collected: "2023-05-06 22:56"
downloaded: "2026-08-16"
---
![](images/488_001.jpg)

这是什么问题 你指定一下main不就跑起来了?

不会是离了springboot插件就不会打uber-jar了吧

得亏quarkus不火 要是火了肯定有人会问为什么我的quarkus代码没写main函数怎么跑起来的，肯定是生成了一个打进去的啊

甚至exec插件也是走的他的main函数 再调用的你的入口方法

所谓的web框架不都是listen一下开非守护线程读请求 你的处理代码丢到他的请求处理器里面吗？

前两天在v2ex看到一个帖子"做Java程序员 不要做spring程序员" 送给提问者