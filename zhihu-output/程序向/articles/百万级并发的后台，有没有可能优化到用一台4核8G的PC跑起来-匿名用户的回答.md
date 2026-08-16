---
id: "3006566899"
title: "百万级并发的后台，有没有可能优化到用一台4核8G的PC跑起来?"
author: "匿名用户"
type: zhihu-answer
source: "https://www.zhihu.com/question/524930170/answer/3006566899"
created: "2023-04-29 23:18"
updated: "2023-04-29 23:18"
collected: "2023-04-29 23:18"
downloaded: "2026-08-16"
---
这个问题在HTTP/3的时代已经意义不大了。

采用HTTP/3，基于UDP，没有连接的概念了。

对于需要密集交互的用户，HTTP/3轮询效率完全没有问题。

对于低频用户，websocket长连接维持着，有消息了就激活HTTP/3交换下数据。如果websocket没连上，也没啥。