---
id: "3063470673"
title: "虚拟机是怎么实现的？"
author: "ScratchLab"
type: zhihu-answer
source: "https://www.zhihu.com/question/20848931/answer/3063470673"
created: "2023-06-07 19:52"
updated: "2023-06-07 19:52"
collected: "2023-06-07 19:52"
downloaded: "2026-08-16"
---
我写了一个小项目桃花源（英文名为 peach），该项目是一个迷你虚拟机，用于学习 Intel 硬件虚拟化技术。学习该项目可使读者对 CPU 虚拟化、内存虚拟化技术有个感性、直观的认识，为学习 KVM 打下坚实的基础。peach 实现了如下功能：

-   使用Intel VT-x技术实现CPU虚拟化
-   使用EPT技术实现内存虚拟化
-   支持虚拟x86实模式运行环境
-   支持虚拟CPUID指令
-   支持虚拟HLT指令，Guest利用HLT指令关机

代码仓库如下：

```text
https://gitee.com/pandengyang/peach.git
https://github.com/pandengyang/peach.git
```

可做参考。