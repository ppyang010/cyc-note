---
id: "2298574930"
title: "ZGC有什么缺点?"
author: "kimmking"
type: zhihu-answer
source: "https://www.zhihu.com/question/356585590/answer/2298574930"
created: "2022-01-05 14:00"
updated: "2022-01-05 14:00"
collected: "2022-01-05 14:00"
downloaded: "2026-08-16"
---
OpenJDK11下，目前不建议使用ZGC，主推G1，主要是基于几个考虑：

1）ZGC时Java进程占用三倍内存问题：由于ZGC着色指针把内存空间映射了3个虚拟地址，使得TOP/PS等命令查看占用内存时看到Java进程占用内存过大。此问题不影响操作系统，但是会影响到监控运维工具，需要注意。。

参考以下材料：

-   ZGC最大堆大小超过物理内存：[https://www.it1352.com/2281965.html](https://link.zhihu.com/?target=https%3A//www.it1352.com/2281965.html)
-   英文原文：[https://stackoverflow.com/questions/57899020/zgc-max-heap-size-exceed-physical-memory](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/57899020/zgc-max-heap-size-exceed-physical-memory)
-   《ZGC设计与实现》书里也有讲过：[https://gitee.com/laifengting/LFT-Note/blob/master/ZGC%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0.md#221%E5%A4%9A%E8%A7%86%E5%9B%BE%E6%98%A0%E5%B0%84](https://link.zhihu.com/?target=https%3A//gitee.com/laifengting/LFT-Note/blob/master/ZGC%25E8%25AE%25BE%25E8%25AE%25A1%25E4%25B8%258E%25E5%25AE%259E%25E7%258E%25B0.md%23221%25E5%25A4%259A%25E8%25A7%2586%25E5%259B%25BE%25E6%2598%25A0%25E5%25B0%2584)
-   Tencent Kona JDK11无暂停内存管理ZGC生产实践里也有提过：[https://mp.weixin.qq.com/s/BH7XAuSs4QsseIK-gMeD7A](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/BH7XAuSs4QsseIK-gMeD7A)

2）同样的应用ZGC内存占用会多一些

主要原因是ZGC借用了对象头，导致无法使用指针压缩功能。OpenJDK11+64位系统下，使用G1，默认UseCompressedOops是打开的，ZGC是false。不过内存够的情况下，这个影响不大。因为对于小于32G的堆，压缩oops能节省一部分内存，地址换算得多用一些CPU，同时只要垃圾能回收掉，都没啥影响。[https://docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html](https://link.zhihu.com/?target=https%3A//docs.oracle.com/javase/7/docs/technotes/guides/vm/performance-enhancements-7.html)

3）Metaspace区占用内存过多问题

OpenJDK11下ZGC不能实现Class Unloading，加上本来也不能使用指针压缩，所以内存占用量比G1要大，这个问题在OpenJDK12-15陆续有多个补丁修复。KonaJDK/DragonwellJDK已经把相关的补丁都backport到KonaJDK11，所以不存在这方面的问题。KonaJDK参见上面链接。Dragonwell参见：[https://developer.aliyun.com/article/789096](https://link.zhihu.com/?target=https%3A//developer.aliyun.com/article/789096)

4）吞吐量低于G1 GC。一般来说，可能会下降5%-15%。对于堆越小，这个效应越明显，堆非常大的时候，比如100G，其他GC可能一次Major或Full GC要几十秒以上，但是对于ZGC不需要那么大暂停。这种细粒度的优化带来的副作用就是，把很多环节其他GC里的STW整体处理，拆碎了，放到了更大时间范围内里去跟业务线程并发执行，甚至会直接让业务线程帮忙做一些GC的操作，从而降低了业务线程的处理能力。

**总结：在OpenJDK11版本，建议优先使用G1 GC。如果想使用ZGC，建议使用OpenJDK17版本，或者使用KonaJDK 11/Dragonwell JDK 11。**

ZGC在JDK16+版本（特别是当前LTS 17），还是推荐可以用的，修复了各类问题。特别是当前ZGC是不分代的，可以预期在下一个LTS版本，引入了分代处理，ZGC可以把STW停顿降低到1ms以内。

btw：官方各种GC的调优建议：

[https://docs.oracle.com/en/java/javase/11/gctuning/garbage-first-garbage-collector-tuning.html](https://link.zhihu.com/?target=https%3A//docs.oracle.com/en/java/javase/11/gctuning/garbage-first-garbage-collector-tuning.html)