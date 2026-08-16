---
id: "1935109247735148892"
title: "为什么很多 SpringBoot 开发者放弃了 Tomcat，选择了 Undertow?"
author: "小黄瓜的忧郁"
type: zhihu-answer
source: "https://www.zhihu.com/question/623790275/answer/1935109247735148892"
created: "2025-08-02 22:46"
updated: "2025-08-02 22:55"
collected: "2025-08-02 22:46"
downloaded: "2026-08-16"
---
我要开始暴论输出了，不接受批判！

如果要我放弃springboot，我会去直接用netty，其他第三方库怼到启动和退出函数里面，绝对直观好用，又轻量。什么模式，什么重型框架都是面向老板和管理人员，以牺牲性能和效率，来换取可维护性和招人高性价比（八股文白痴），这些辣鸡，吾视之如草芥。netty上Promise，结合reactorCore，再结合第三方的reactive库，如此这般，如果这样io型的任务性能还有问题，或许已经不是你的问题，无脑怼产品和业务。