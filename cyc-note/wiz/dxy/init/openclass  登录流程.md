---
Title: "openclass  登录流程"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2019-02-27 14:39:52"
Cover: ""
WizGuid: "26d63bb4-d7dd-4924-9c76-6c00301dfa07"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "d9d41d9c04c67029bb8237e0364511c8"
Modified: "2019-03-04 10:11:50"
WizSyncedAt: "2026-07-29 15:36:28"
---

openclass 登录流程

1.点击 openclasshost/login?done=来源url

2.后台转发到 ssologinUrl?service=(openclasshost/index.do?done=来源url) 这个就是sso的输入账号和密码的页面

3.输入账号密码后登录,ssoh会回调openclass的index.do 接口 带上ticket 参数

4.openclass 根据ticket 参数去sso验证 验证通过在参数中写一个cookie 包含用户信息等
