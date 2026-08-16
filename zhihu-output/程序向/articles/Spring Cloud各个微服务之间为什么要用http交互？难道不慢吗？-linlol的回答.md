---
id: "2812005842"
title: "Spring Cloud各个微服务之间为什么要用http交互？难道不慢吗？"
author: "linlol"
type: zhihu-answer
source: "https://www.zhihu.com/question/270355472/answer/2812005842"
created: "2022-12-22 18:18"
updated: "2022-12-22 18:19"
collected: "2022-12-22 18:18"
downloaded: "2026-08-16"
---
**gRPC用HTTP2**

  

http 肯定不会比你自己往死里优化来得快，但是http标准通用，每个语言都有无数的支持方式，《重构》里教过我们先把功能实现，再一点点优化

  

讲个我最近闹的笑话，我们有需求是一个python进程a在内网里调用另外一个python进程b，把b里面的pandas dataframe （类似excel的数据） 传输给a

  

既然我们走http，那标准的思路肯定是把一个dataframe 转化成JSON，然后走http，走标准的json返回体返回给进程a，然后a再把json重新变回pandas dataframe

  

但是我们都知道，转化成JSON会生成很多遍没有用的header，而市面上有开源高效的标准解决方案apache arrow，于是我实现了一版方案在b里面把dataframe 变成parquet 字节流，然后在http里传输流，a直接把流反序列化成dataframe

  

最后发现parquet 方案生成的体积只有json方案的三分之一，但是耗时还增加了大概十毫秒...原因是我们的网速很快，但是在dataframe小的情况下（比如说几千行\*几十列），pandas 默认的parquet的序列化/反序列化比json慢，我估计是因为压缩的耗时...然后我默默的把我写了半天的《parquet转换》，《字节流传输》全删了...

  

在现实中所谓的“优化”更多要先有一个具体的“优化目标”，没有优化目标的情况下，为了优化去牺牲通用性和简单性是不值得的