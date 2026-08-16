---
id: "3301173371"
title: "Spring Cloud各个微服务之间为什么要用http交互？难道不慢吗？"
author: "大大大呜呜呜"
type: zhihu-answer
source: "https://www.zhihu.com/question/270355472/answer/3301173371"
created: "2023-11-24 18:59"
updated: "2023-11-24 19:04"
collected: "2023-11-24 18:59"
downloaded: "2026-08-16"
---
先说结论，就是慢

这是一个防蠢防呆妥协的结果

1、Http基于socket，协议有开销，但是真的让写业务的同学写协议，风险更高

2、序列化和反序列化json/xml的开销恐怕比协议更大

3、硬件便宜，找牛逼的程序员折腾半年一年，可以买数十台服务器，足够抵消中小公司的性能损失。

另外，spring cloud 太臃肿复杂，已经在衰落，稍微有点规模的，还是考虑用k8s+istio+spring boot