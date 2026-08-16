---
id: "3395300720"
title: "程序中提升几毫秒、节省几 kB 的内存有必要吗？"
author: "VeroFess"
type: zhihu-answer
source: "https://www.zhihu.com/question/53606129/answer/3395300720"
created: "2024-02-13 20:52"
updated: "2024-11-08 12:58"
collected: "2024-02-13 20:52"
downloaded: "2026-08-16"
---
我把开源的openjdk稍微优化了一下，让他可以在热路径上生成更优的jit，大概每个函数能扣三五个到几百个周期

但是让mc服务端的tps从12直接升到了19.9

这就是每个扣一点的威力

  

更新：

好吧，看起来有朋友不太信，上用户反馈，如果觉得是我恶意截图，可以试试我放github的PalWorld Server Unoffical Fix的Patch 3和原版1.3.0的性能对比

![](images/294_001.jpg)

  

![](images/294_002.jpg)

  

![](images/294_003.jpg)

  

![](images/294_004.jpg)