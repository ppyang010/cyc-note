---
id: "3309405677"
title: "Spring Cloud各个微服务之间为什么要用http交互？难道不慢吗？"
author: "iyacontrol"
type: zhihu-answer
source: "https://www.zhihu.com/question/270355472/answer/3309405677"
created: "2023-12-01 13:55"
updated: "2023-12-02 11:01"
collected: "2023-12-01 13:55"
downloaded: "2026-08-16"
---
先说慢不慢？的确慢。

从工程维度来看的话， [@kimmking](https://www.zhihu.com/people/65a81f15a574f659bfbe9042a71b6c5a) 已经讲的非常清晰了。

我补充一下选择http的优势：

-   基于标准协议来实现。可以充分享受到标准协议的生态。
-   调试和问题排查简单。

> 关于标准协议的好处，我可以分享一个案例。21年，我在一家公司负责落地服务网格，RPC主要是thrift。由于thrift在envoy中不是一等公民，所以我们就需要大量的投入去增强Envoy对thrift的支持。假如RPC协议是HTTP1.1/HTTP2/gRPC，开发量基本上会大量减少。

半导体界有个牧本定律，它认为半导体产品的发展,总是在标准化和定制化之间左右摇摆,大概每隔10年波动一次。牧本定律的背后,则是性能、功耗和开发效率之间的平衡。

其实软件工程，也是在效率、性能、安全等维度trade-off。

![](images/332_001.png)

所以综合来看，Spring Cloud 在当时选择HTTP，也是一个不错的选择。

站在上帝的视角，今天我们重新开发一个微服务框架，大概率是基于HTTP2或是基于gRPC来实现。