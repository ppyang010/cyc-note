---
Title: "topic"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-11-03 19:46:48"
Cover: ""
WizGuid: "fde5639d-9c46-4752-904c-22890d92d69e"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "3291b90433984ce7254717ea97451bb7"
Modified: "2017-11-09 18:29:17"
WizSyncedAt: "2026-07-29 15:36:28"
---

1.关于数字签名的

概念

[http://blog.csdn.net/zhangdaiscott/article/details/49690741](http://blog.csdn.net/zhangdaiscott/article/details/49690741)

我们系统中

主要使用

com.dxy.platform.sdk.openapi.OpenApi

这个类

类中的get（）  post（）方法会构建http请求最后返回一个通用的结果实体

![[attachments/72374922.png]]

主要逻辑应该在这里

其中this.sign().sign() 方法会将所有需要签名的 参数进行拼接  诚xx=xx的形式然后做sha1加密 这个加密后的值作为request 中参数名为 sign的参数的参数值

最终发起http请求的地方应该是

getRestTemplate().getForObject(this.buildGetRequestUrl(), String.class)

以上是发送请求的过程

现在需要看代码分析

简单定位在

@PlatformRestGet

这方面还需要看

2.将汇率变更的事情作为一个案例进行讲解
