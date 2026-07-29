---
Title: "vpn 线上日志"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2026-01-04 09:35:41"
Cover: ""
Pinned: true
WizPinned: true
WizGuid: "8265b6dd-3a9b-443c-95c0-faa453c5bacc"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "1c44d0ca9abd028b0446f727d22cde84"
Modified: "2026-03-27 13:36:49"
WizSyncedAt: "2026-07-29 15:36:28"
---

HI 各位：

VPN 查看线上日志已开通了，但是要通过跳板机，方法如下：

先执行下面命令，添加自己的私钥

ssh-add

然后用下面的命令登录跳板机

ssh -p 7311 -A  {username}@192.168.202.203

登录后，可以开始ssh到你需要的测试机上了。

ssh caicy@192.168.201.99
