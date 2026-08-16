---
id: "2277460421"
title: "为什么 electron 不做成独立的 runtime？"
author: "Belleve"
type: zhihu-answer
source: "https://www.zhihu.com/question/505356140/answer/2277460421"
created: "2021-12-19 15:14"
updated: "2022-07-13 08:14"
collected: "2021-12-19 15:14"
downloaded: "2026-08-16"
---
然而 .NET 现在也开始鼓励程序自带了…

主要是两点：

1.  公用 Electron（或者其他任何的 runtime）可能会导致更新 Electron 的时候 break 掉某些下游软件。你**不能**假设所有人写程序的时候都会认真读文档。
2.  普通用户还是比较喜欢「下载一个安装器 / 点 Store 里面一个按钮」搞定安装。

当然，最理想的方法是，软件作者仍然发布带依赖的软件包，OS 等平台则实现一些减少磁盘占用 / 降低下载所用流量的措施（比如如公用文件只存在一份、下载一次），这样就可以把好处两头都占了。