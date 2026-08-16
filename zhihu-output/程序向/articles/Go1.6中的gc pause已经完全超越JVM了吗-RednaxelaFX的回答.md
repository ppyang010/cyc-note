---
id: "94460053"
title: "Go1.6中的gc pause已经完全超越JVM了吗?"
author: "RednaxelaFX"
type: zhihu-answer
source: "https://www.zhihu.com/question/42353634/answer/94460053"
created: "2016-04-09 16:40"
updated: "2016-04-11 07:55"
collected: "2016-04-09 16:40"
downloaded: "2026-08-16"
---
**Go的GC完胜JVM GC？**

作为在2TB的GC堆上能维持在< 10ms GC暂停时间的Azul Systems的Zing JVM…

而且Zing JVM的C4 GC是一种完全并发的、会整理堆内存的GC（Fully Concurrent Mark-Compact GC），不但mark阶段可以是并发的，在整理（compaction）阶段也是并发的，所以在GC堆内不会有内存碎片化问题；而Go 1.5/1.6GC是一种部分并发的、不整理堆内存的GC（Mostly-Concurrent Mark-Sweep），虽然实现已经做了很多优化但终究还是能有导致堆内存碎片化的workload，当碎片化严重时Go GC的性能就会下降。

简短回答是：不，Go 1.6的GC并没有在GC pause方面“完胜”JVM的GC。

我们有实际客户在单机十几TB内存的服务器上把Zing JVM这2TB GC堆的支持推到了极限，有很多Java对象，外带自己写的基于NIO的native memory内存管理器，让一些Java对象后面挂着总共10TB左右的native memory，把这服务器的能力都用上了。在这样的条件下Zing JVM的GC还是可以轻松维持在< 5ms的暂停时间，根本没压力；倒是Linux上自带的glibc的ptmalloc2先“挂”了——它不总是及时归还从OS申请来的内存，结果把这没开swap的服务器给跑挂了…

（注意上面的单位都是TB。）

Zing JVM的C4 GC跟其它JVM GC相比，最大的特征其实还不是它“不暂停”（或者说只需要暂停非常非常短的时间），而是它对运行的Java程序的特征不敏感，可以对各种不同的workload都保持相同的暂停时间表现。这样要放在前面强调，因为下面的讨论就要涉及workload了。

后面再补充点关于Zing JVM的GC的讨论。先放几个传送门：

-   [Azul Systems 是家什么样的公司？ - RednaxelaFX 的回答](https://www.zhihu.com/question/24938498/answer/36055851)  
    
-   [Java 大内存应用（10G 以上）会不会出现严重的停顿？ - RednaxelaFX 的回答](https://www.zhihu.com/question/35109537/answer/61379522)  
    
-   [C++ 短期内在华尔街的买方和卖方还是唯一选择吗？ - RednaxelaFX 的回答](https://www.zhihu.com/question/31602530/answer/53044262)  
    

要跟JVM比GC性能的话不要光看HotSpot VM啊。

**Go的低延迟GC的适用场景和实际性能如何？**

其实很重要的注意点就是：每种GC都有自己最舒服的workload类型——Zing的C4 GC是少有的例外。

题主给的那张演示稿没有指出这benchmark测的是啥类型的workload，也没有说明这个workload运行了多长时间，这数据对各种不同情况到底有多少代表性还值得斟酌。最公平的做法是把benchmark用的Go程序移植到Java，然后用HotSpot VM的CMS GC也跑跑看，对比一下。

作为一种CMS（**Mostly**\-Concurrent Mark-Sweep）GC实现，Go的GC最舒服的应用场景是当程序自身的分配行为不容易导致碎片堆积，并且程序分配新对象的速度不太高的情况。

**而如果遇到一个程序会导致碎片逐渐堆积，并且/或者程序的分配速度非常高的时候，Go的CMS就会跟不上，从而掉进长暂停的深渊。**这就涉及到低延迟模式能撑多久多问题。

具体怎样的情况会导致碎片堆积大家有兴趣的话我回头可以来补充。主要是跟对象大小的分布、对象之间的引用关系的特征、对象生命期的特征相关的。

这里让我举个跟Go没关系的例子来说明讨论这类问题时要小心的陷阱。

要评测JVM/JDK性能，业界有几个常用的标准benchmark，例如SPECjvm98 / SPECjvm2008，SPECjbb2005 / SPECjbb2013，DaCapo等。其中有不少benchmark都是，其声称要测试的东西，跟它实际运行中的瓶颈其实并不一致。

SPECjbb2005就是个很出名的例子。JVM实现者们很快就发现，这玩儿实际测的其实是GC暂停时间——如果能避免在测试过程中发生full GC，成绩就会不错。于是大家一股脑的都给自己的GC添加启发条件，让JVM实现们能刚刚好在SPECjbb2005的测试时间内不发生full GC——但其实很多此类“调优”的真相是只要在多运行那么几分钟可能就要发生很长时间的full GC暂停了。

所以说要讨论一个GC的性能水平如何，不能只靠看别人说在某个没有注明的workload下的表现，而是得具体看这个workload的特征、运行时间长度以及该GC的内部统计数据所表现出的“健康程度”再来综合分析。

**Go CMS GC与HotSpot CMS GC的实现的比较**

Go GC目前的掌舵人是Richard L. Hudson大大，是个靠谱的人。

他之前就有过设计并发GC的经验，设计了Sapphire GC算法。

Sapphire: Copying GC Without Stopping the World

ftp://ftp.cs.umass.edu/pub/osl/papers/sapphire-2003.pdf

设计了并发Copying GC的他在Go里退回到用CMS感觉实属无奈。虽然

[未来Go可能会尝试用能移动对象的GC](https://link.zhihu.com/?target=https%3A//github.com/golang/go/issues/12416)

，在Go 1.5的时候它的GC还是不移动对象的，而外部跟Go交互的C代码也多少可能依赖了这个性质。要不移动对象做并发GC，最终就会得到某种形式的CMS。

Go的CMS实现得比较细致的地方是它的pacing heuristics，或者说“并发GC的启动时机”。这是属于“策略”（policy）方面做得细致。HotSpot VM的CMS GC则这么多年来都没得到足够多的关爱，其实尚未发挥出其完全的能力，还有不少改进/细化的余地，特别是在策略方面。

而在“机制”（mechanism）方面，Go的CMS GC其实与HotSpot VM的CMS GC相比是非常相似的。都是只基于incremental update系write-barrier的**Mostly**\-Concurrent Mark-Sweep。两者的工作流程中最核心的步骤都是：

1.  Initial marking：扫描根集合
2.  Concurrent marking：并发扫描整个堆
3.  Re-marking：重新扫描在(2)的过程中发生了变化/可能遗漏了的引用
4.  Concurrent sweeping

具体到实现，两者在上述核心工作流程上有各自不同的扩展/优化。

两者的(1)都是stop-the-world的，这是两者的GC暂停的主要来源之一。

HotSpot VM的CMS GC的(3)也是stop-the-world的，而且这个暂停还经常比(1)的暂停时间要更长；Go 1.6 CMS GC则在此处做了比较细致的实现，尽可能只一个个goroutine暂停而不全局暂停——只要不是全局暂停都不算在用户关心的“暂停时间”里，这样Go版就比HotSpot版要做得好了。

（无独有偶，Android Runtime（ART）也有一个CMS GC实现，而它也选择了把上述两种暂停中的一个变为了每个线程轮流暂停而不是全局暂停，不过它是在(1)这样做的，而不是在(3)——这是Android 5.0时的状况。新版本我还没看）

HotSpot版CMS对(3)的细化优化是，在真正进入stop-the-world的re-marking之前，先尝试做一段时间的所谓并发的“abortable concurrent pre-cleaning”，尝试并发的追赶应用程序对引用关系的改变，以便缩短re-marking的暂停时间。不过这里实现得感觉还不够好，还可以继续改进的。

有个有趣的细节，Go版CMS在(3)中重新扫描goroutine的栈时，只需要扫描靠近栈顶的部分栈帧，而不需要扫描整个栈——因为远离栈顶的栈帧可能在(2)的过程中根本没改变过，所以可以做特殊处理；HotSpot版CMS在(3)中扫描栈时则需要重新扫描整个栈，没抓住机会减少扫描开销。Go版CMS就是在众多这样的细节上比HotSpot版的更细致。

再举个反过来的细节。目前HotSpot VM里所有GC都是分代式的，CMS GC在这之中属于一个old gen GC，只收集old gen；与其配套使用的还有专门负责收集young gen的Parallel New GC（ParNew），以及当CMS跟不上节奏时备份用的full GC。分代式GC很自然的需要使用write barrier，而CMS GC的concurrent marking也需要write barrier。HotSpot VM就很巧妙的把这两种需求的write barrier做在了一起，共享一个非常简单而高效的write barrier实现。

Go版CMS则需要在不同阶段开启或关闭write barrier，实现机制就会稍微复杂一点点，write barrier的形式也稍微慢一点点。

从效果看Go 1.6的CMS GC做得更好，但HotSpot VM的CMS GC如果有更多投入的话也完全可以达到一样的效果；并且，得益于分代式GC，HotSpot VM的CMS GC目前能承受的对象分配速度比Go的更高，这算是个优势。

（待续）