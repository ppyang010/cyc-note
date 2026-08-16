---
id: "2744189717"
title: "如何看待 Rust 的应用前景？"
author: "rribx"
type: zhihu-answer
source: "https://www.zhihu.com/question/30407715/answer/2744189717"
created: "2022-11-04 15:32"
updated: "2022-12-06 21:04"
collected: "2022-11-04 15:32"
downloaded: "2026-08-16"
---
说个小事, cloudflare用rust写了一个pingora代替nginx, 比nginx更快, 资源占用更小, 而且最神奇的是每次崩溃都发现不是pingora本身的问题, 是系统内核bug甚至硬件的错误, 所以in rust we trust真不是一句空话, 那些对运行效率、安全都要求极高的场景, 用rust绝对不会让你失望

* * *

另外一个值得关注的例子, 谷歌将安卓代码内存安全漏洞报告数量从2019的223个下降到2022的85个归结为rust使用比例的提升, rust在安卓13的新代码中占21%约150w行, 而在这些rust代码中发现的内存安全漏洞为0...... "谷歌提到, 这是一个重要发现, 因为过去安卓漏洞密度大于 1/kLOC, 也就是说, 每一千行程序代码至少会发现一个漏洞, 与历史资料相比, rust 可能已经阻挡成百上千个漏洞进入安卓"