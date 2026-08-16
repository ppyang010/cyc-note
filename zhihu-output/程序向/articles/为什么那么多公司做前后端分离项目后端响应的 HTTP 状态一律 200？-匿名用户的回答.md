---
id: "2641575729"
title: "为什么那么多公司做前后端分离项目后端响应的 HTTP 状态一律 200？"
author: "匿名用户"
type: zhihu-answer
source: "https://www.zhihu.com/question/513865370/answer/2641575729"
created: "2022-08-23 18:22"
updated: "2022-08-23 18:22"
collected: "2022-08-23 18:22"
downloaded: "2026-08-16"
---
注意语义！注意分层！

现在服务端不管三七二十一，只要请求成功一律返回 2xx，代表这个 API endpoint 有效。

对应前端的处理，如果访问某个 API endpoint 的 http 状态码为 404，那表示这个 endpoint 不存在。如果访问这个 endpoint 的 http 状态码为 200，但内容中的 status = 404，则表示这个 endpoint 找不到你想要的内容，而非 endpoint 不存在。这里服务端对资源的定义只是复用了 http 状态码定义，是为了降低学习和沟通成本。

跟连接有没有被劫持没关系。如果你担心http请求被劫持了，那就https。防劫持应该是 session 层该干的事，不应该由 presentation 层负责。