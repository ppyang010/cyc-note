---
id: "2305680702"
title: "java设计request body为什么设计成只允许读取一次???"
author: "Ivony"
type: zhihu-answer
source: "https://www.zhihu.com/question/400797045/answer/2305680702"
created: "2022-01-10 23:46"
updated: "2022-01-10 23:46"
collected: "2022-01-10 23:46"
downloaded: "2026-08-16"
---
别人上传1T的文件，然后Java先全部读取到内存，服务器直接就挂了……

所以不确定最大能多大的东西，默认都是流式处理，要缓存反复读，你自己写代码就完了，这都写不出来还写什么程序？