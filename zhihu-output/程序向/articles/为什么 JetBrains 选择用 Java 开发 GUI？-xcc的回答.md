---
id: "1645771823"
title: "为什么 JetBrains 选择用 Java 开发 GUI？"
author: "xcc"
type: zhihu-answer
source: "https://www.zhihu.com/question/31373671/answer/1645771823"
created: "2020-12-26 00:04"
updated: "2020-12-26 00:04"
collected: "2020-12-26 00:04"
downloaded: "2026-08-16"
---
我想说swing仅仅是一个库而已，gui拼速度在窗口层面只有用gpu还是不用gpu的情况下有区别，（从运行效率角度上看）。

java界标准窗口应用的基础只有一个就是awt。好多人搞错了awt扮演的角色，你可以用它来直接写应用，但你也可以用它来先写个框架！

做个不恰当的比喻，awt相当于java界opengl，只不过它只面向二维窗口应用。swing才是游戏引擎。如果你感觉swing不好用重新写个引擎就是了。但你要直接用opengl api做游戏那我也没话说...这必须得麻烦死。

awt本应该是vendor提供用来适配各种设备接口，哪怕嵌入式设备。这样java就达到了跨平台和写一次到处跑的目的。

**你甚至可以把浏览器和一个web server拼起来当成一个awt设备，让机器A的浏览器显示机器B运行的awt（or swing）程序。idea 的projector项目已经实现了这个。**