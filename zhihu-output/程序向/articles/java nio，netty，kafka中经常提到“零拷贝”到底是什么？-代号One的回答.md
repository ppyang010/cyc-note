---
id: "3323668096"
title: "java nio，netty，kafka中经常提到“零拷贝”到底是什么？"
author: "代号One"
type: zhihu-answer
source: "https://www.zhihu.com/question/634419059/answer/3323668096"
created: "2023-12-13 09:20"
updated: "2023-12-13 09:20"
collected: "2023-12-13 09:20"
downloaded: "2026-08-16"
---
Java中的零拷贝指的是 数据只从内核拷贝到了jvm的堆外内存，不再拷贝到jvm堆。

Linux中也有零拷贝 指的是从文件系统直接通过内核将数据发送给网络设备不再经过Linux用户态中转一次

另外还有一种零拷贝 mmap，直接将文件系统里面的文件内容映射到用户态内存上，避免了内核的拷贝。

以上来说其实都不是零，只是和其他技术相比减少了内存拷贝的操作