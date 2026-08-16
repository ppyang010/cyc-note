---
id: "3388503835"
title: "JavaWeb项目放弃jsp？为什么要前后端解耦？为什么要前后端分离？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/636046855/answer/3388503835"
created: "2024-02-06 00:27"
updated: "2024-02-06 00:27"
collected: "2024-02-06 00:27"
downloaded: "2026-08-16"
---
java web并没有放弃jsp

jsp是j2ee的一个标准

实际上到现在jsp依旧在被遵照执行

你看tomcat这个项目是不是还在积极地维护着呢？

什么时候tomcat这个项目彻底放弃了，那你可以说，jsp被放弃了

但现实是，支持 jsp 的 tomcat 已经还在被 apache 积极维护并开发着

你要用还是可以用的，所以并没有被放弃

其次呢，为什么要做分离啊

我觉得最重要一个理由，就是当时的 jsp 容器，比如 tomcat

对于异步 api 的支持比较差，在 java 21 下发生产之后，这个局面才会改观

而在 tomcat 支持 21 之前很长一段时间

tomcat 的并发量，是不如 node.js 的

虽然 node.js 写起来很变扭，在没有 await 之前，一堆 callback 搞死人

但是性能好啊

所以很多互联网公司在并发量上来之后，tomcat 就撑不住了，所以需要用 node.js 来支持这种大并发的访问量

后来 node.js 的变扭的代码书写方式，被 go 那种简单实用的代码编写方式所超过，所以很多互联网公司后来又用了go，然后node.js也采用了await和async的语法糖来优化代码书写

再然后 java 21 下发生产，tomcat 升级，之后 tomcat 就可以既像go一样简单书写，又享有高性能的服务

但到了这时候，对于互联网高性能访问的需求那阵风也已经过去了

所以这种互相碾压式的借鉴和抄袭带来的结果就是，大量从业人员过剩

但这也没办法，因为技术的进步不可阻挡