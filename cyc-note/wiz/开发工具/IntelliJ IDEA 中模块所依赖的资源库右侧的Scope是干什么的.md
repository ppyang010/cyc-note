---
Title: "IntelliJ IDEA 中模块所依赖的资源库右侧的Scope是干什么的"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2021-12-22T21:07:23+08:00"
Cover: ""
Pinned: true
WizPinned: true
WizGuid: "b662d616-1ea6-41db-94d1-9d9ecb2c28be"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "ef51cf660711ba76e5ea4fc2413fced6"
Modified: "2021-12-22T21:07:58+08:00"
WizSyncedAt: "2026-07-22T16:05:38+08:00"
---

IntelliJ IDEA 中模块所依赖的资源库右侧的Scope是干什么的？

![[attachments/c924ad94-7304-462d-8455-a27c2b0e9bbb.png]]

类似maven中的scope

compile

compile表示被依赖项目需要参与当前项目的编译，当然后续的测试，运行周期也参与其中，是一个比较强的依赖。打包的时候通常需要包含进去。

test

scope为test表示依赖项目仅仅参与测试相关的工作，包括测试代码的编译，执行。比较典型的如junit。

runntime

runntime表示被依赖项目无需参与项目的编译，不过后期的测试和运行周期需要其参与。与compile相比，跳过编译而已，说实话在终端的项目（非开源，企业内部系统）中，和compile区别不是很大。比较常见的如JSR×××的实现，对应的API jar是compile的，具体实现是runtime的，compile只需要知道接口就足够了。oracle jdbc驱动架包就是一个很好的例子，一般scope为runntime。另外runntime的依赖通常和optional搭配使用，optional为true。我可以用A实现，也可以用B实现。

provided

provided意味着打包的时候可以不用包进去，别的设施(Web Container)会提供。事实上该依赖理论上可以参与编译，测试，运行等周期。相当于compile，但是在打包阶段做了exclude的动作。
