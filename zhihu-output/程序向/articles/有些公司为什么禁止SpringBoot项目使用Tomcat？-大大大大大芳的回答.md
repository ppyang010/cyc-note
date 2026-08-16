---
id: "2930943568"
title: "有些公司为什么禁止SpringBoot项目使用Tomcat？"
author: "大大大大大芳"
type: zhihu-answer
source: "https://www.zhihu.com/question/588619979/answer/2930943568"
created: "2023-03-11 08:28"
updated: "2023-03-11 12:55"
collected: "2023-03-11 08:28"
downloaded: "2026-08-16"
---
你告诉我是哪个大厂，等我去那边干几天看看是不是这个情况。

  

第一现在都是嵌入式tomcat，之前都是启动一个tomcat然后upload代码，这不代表不用tomcat。

tomcat类似还有一大堆

比如jboss，weblogic，websphere**，**glassfish

叠加了各种功能。

  

为啥现在看不到tomcat了，也看不到这些容器了，因为微服务架构，每一个微服务只要基础的web功能就够了，屏蔽底层方便开发。

你能想象100个微服务启动100个tomcat然后，重新粘贴依赖依赖到tomcat lib目录，然后部署100次？

直接java -jar启动才是最方便的，是吧。

  

第二 不使用tomcat而使用undertow？

请测试对比一下这两者关系，我反正测试过了。

低并发，小内存环境下tomcat吊打undertow

不管是响应速度，稳定性都是吊打。

tomcat存在这么多年，姜还是老的辣。

  

高并发大内存环境下undertow才有优势。

但大多数情况下，2者差距不大。

你有5000并发1w并发，10w，100w并发解决方案并不是tomcat换成undertow就能解决的。

—————

当然，在公司别这么说，问就是undertow牛逼，我建议换。