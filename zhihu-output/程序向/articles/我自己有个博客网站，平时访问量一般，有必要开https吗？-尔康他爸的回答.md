---
id: "2979770937"
title: "我自己有个博客网站，平时访问量一般，有必要开https吗？"
author: "尔康他爸"
type: zhihu-answer
source: "https://www.zhihu.com/question/548068171/answer/2979770937"
created: "2023-04-12 10:08"
updated: "2023-04-12 10:08"
collected: "2023-04-12 10:08"
downloaded: "2026-08-16"
---
开吧，很简单也不花钱的。

首先你的反向代理一般都是nginx吧，建议直接安一个 Nginx Proxy Manager

然后一键打开ssl就可以了，他会自动申请免费的ssl证书 开启https

![](images/468_001.jpg)

  

  

我用很久了 很稳定，而且过期了会自动申请新的

[https://www.mcaoyuan.com/](https://link.zhihu.com/?target=https%3A//www.mcaoyuan.com/)