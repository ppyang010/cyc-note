---
id: "1940059139746300426"
title: "目前最具性价比的全栈路线是啥？"
author: "momo"
type: zhihu-answer
source: "https://www.zhihu.com/question/594662421/answer/1940059139746300426"
created: "2025-08-16 14:35"
updated: "2025-08-21 13:11"
collected: "2025-08-16 14:35"
downloaded: "2026-08-16"
---
首先排除nextjs。

  

remix，tanstack会轻很多，是前端开发的唯二选择。

目前tanstack start是beta，不过tanstack query可是成熟的不行了，可以自己用turborepo做全栈开发，不被框架捆绑是真正的自由。

前端：tanstack query + tanstack router + bun

后端：hono + bun

这套无论是 性能 还是 灵活性 都碾压nextjs

  

从开发体验讲:

  

1\. nextjs老奶奶般的构建速度，nextjs 一个 / 页面都给我编译三秒五秒，vite 几十ms就解决了，我甚至可以边开发边build，nextjs敢想吗，能把turbopack累死。

  

2\. 打包方面，nextjs构建产物要拖家带口一大堆node\_module，再配合一个最小node的docker，随随便便一个demo页面一百多MB......

而自己搓的前后端，没有那么多黑魔法，底层做的什么自己都清楚，打包出来都是轻的不得了，一个bun就能启动（同样的demo，我这套前端构建产物3MB , 后端0.5MB) 。

  

总结：  
1\. web用tanstack全家桶，无痛复用到rn

2\. 后端用hono + bun，通信用tRPC，全部都包到一个turborepo里，开发体验非常舒适，看着Copilot杀穿前后端，在workspace之间穿梭的感觉非常爽，根本不用打开第二个IDEA，全面拥抱tRPC，代替Restful，我新增接口只需要在dto package里新增类型，重新编译，前后端直接就可以拿到新增的强类型了

  

  

  

  

* * *

贪快？

不要说什么开箱即用，现在ai时代，你开箱还是ai开箱？ vite那么也集成了各种前端脚手架，哪个不是一分钟启动项目。