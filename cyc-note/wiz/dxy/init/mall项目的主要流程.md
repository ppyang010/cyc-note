---
Title: "mall项目的主要流程"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-11-07 19:30:57"
Cover: ""
Pinned: true
WizPinned: true
WizGuid: "401762e7-151a-40f3-aabb-53a3314fecf5"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "264920765dfccbf4c10fa4e440008586"
Modified: "2017-12-06 11:48:32"
WizSyncedAt: "2026-07-29 15:36:28"
---

前台

首页（各个栏位的划分）

商品详情（商品 规格 库存之间的关系） 商品及商品信息的各个数据的关系  如商品和一组图片的关系

购买流程

提交订单

[http://mall.dxy.net/japi/platform/110820004](http://mall.dxy.net/japi/platform/110820004)

提交订单返回订单号

[http://mall.dxy.net/japi/platform/110820012](http://mall.dxy.net/japi/platform/110820012)

获取支付渠道和支付url

[http://mall.dxy.net/japi/platform/110820013?orderNo=3242818946216269548](http://mall.dxy.net/japi/platform/110820013?orderNo=3242818946216269548)

轮询判断是否支付

添加商品

[http://mall.dxy.net/japi/platform/110720005](http://mall.dxy.net/japi/platform/110720005)

后台

未支付订单过时流程

这里是用定时器没秒在跑

Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G36 dxyapp_name/drugs dxyapp_version/4.6 dxyapp_system_version/9.3.5 dxyapp_client_id/77c403d127a9926e1e734e1567d4d7f6a9e61f54udidfor7

模拟app的ua

可以借鉴学习的点

分页的实体类

统一返回的实体类

RestTemplate（项目中是使用openapi 调用的）

HandlerInterceptor  （拦截  openapi 接收端验证）

各个包装类型的工具类  （在module-tool）

webutil、obj、int、str

CORS等网络安全
