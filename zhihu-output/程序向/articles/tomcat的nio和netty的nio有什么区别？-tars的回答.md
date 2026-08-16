---
id: "36585340516"
title: "tomcat的nio和netty的nio有什么区别？"
author: "tars"
type: zhihu-answer
source: "https://www.zhihu.com/question/618365639/answer/36585340516"
created: "2024-11-20 23:01"
updated: "2024-12-18 09:19"
collected: "2024-11-20 23:01"
downloaded: "2026-08-16"
---
tomcat 和netty的区别

主要在事件驱动吧

tomcat 不分事件 连接进来就给你线程 没有线程了拒绝连接

netty 区分连接和数据接收 连接你只管来 只要还有建立fd 就给你连 有数据来我就处理数据 所以netty能支持高并发

tomcat虽然并发不行 但是前面加个nginx 后面多搞几个tomcat也就行了