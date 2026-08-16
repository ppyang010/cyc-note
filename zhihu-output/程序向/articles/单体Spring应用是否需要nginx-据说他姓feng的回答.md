---
id: "3476937926"
title: "单体Spring应用是否需要nginx?"
author: "据说他姓feng"
type: zhihu-answer
source: "https://www.zhihu.com/question/609079086/answer/3476937926"
created: "2024-04-24 13:43"
updated: "2024-04-27 23:00"
collected: "2024-04-24 13:43"
downloaded: "2026-08-16"
---
工程上说，有必要。

  

nginx对流量管理、静态缓存等更好设置。

  

还有一个更重要的原因，spring用root账号跑80端口，总给我感觉非常不放心。

  

最安全的办法，是nginx、应用都用普通user跑，用root配一个端口转发。