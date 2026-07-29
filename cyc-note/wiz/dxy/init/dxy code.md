---
Title: "dxy code"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2018-07-27 20:50:17"
Cover: ""
WizGuid: "6c7f8869-391b-4147-b702-15726766e4cf"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "d3b42b7782f25b3bec28d8e7b7c50de6"
Modified: "2018-07-27 20:50:31"
WizSyncedAt: "2026-07-29 15:36:28"
---

// 发布事件通知(包括短信通知以及微信模板消息通知)
         CoreUtil.publishEvent(new OpenclassPayOrderEvent(order));
         //更新收益
         Utils.execute(() -> walletManageService.completeIncome(order.getCode()));
