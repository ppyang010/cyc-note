---
id: "656301417"
title: "Java 21：最新进展一览"
author: "InfoQ"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/656301417"
created: "2023-09-15 15:35"
updated: "2023-09-15 15:35"
collected: "2023-09-15 15:35"
downloaded: "2026-08-16"
---
作者 | Michael Redlich

译者 | 明知山

策划 | 丁晓昀

  
Oracle Java 平台组首席架构师[Mark Reinhold](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/markreinhold)[宣布](https://link.zhihu.com/?target=https%3A//mail.openjdk.org/pipermail/jdk-dev/2023-August/008059.html)[JDK 21](https://link.zhihu.com/?target=https%3A//openjdk.java.net/projects/jdk/20/)（继[JDK 17](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2021/09/java17-released/)之后的下一个长期支持(LTS)版本）已经进入初始发布候选阶段。主线源码库（在 2023 年 6 月初（Rampdown Phase One）fork 到 JDK[稳定代码库](https://link.zhihu.com/?target=https%3A//github.com/openjdk/jdk21)） 定义了 JDK 21 的特性集合。一些关键错误，如回归或严重的功能问题，可能得到了修复，但这些修复必须通过[Fix-Request](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/3%23Fix-Request-Process)流程审批。根据[发布时间表](https://link.zhihu.com/?target=https%3A//openjdk.org/projects/jdk/21/%23Schedule)， JDK 21 将于 2023 年 9 月 19 日正式发布。  
  
最终确定的 15 个新特性按照[JEP](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/0)的形式分为四类：**核心 Java 库**，**Java 语言规范**，**HotSpot** 和**安全库**。  
  
被归入为**核心 Java 库**的 6 个新特性：

-   JEP 431：[序列集合](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/431)  
    
-   JEP 442：[外部函数和内存API(第三次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/442)  
    
-   JEP 444：[虚拟线程](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/444)  
    
-   JEP 446：[作用域值(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/446)  
    
-   JEP 448：[Vector API(第六次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/448)  
    
-   JEP 453：[结构化并发(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/453)  
    

  
被归入 **Java 语言规范**的 5 个新特性：

-   JEP 430：[字符串模板(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/430)  
    
-   JEP 440：[记录模式](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/440)  
    
-   JEP 441：[switch模式匹配](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/441)  
    
-   JEP 443：[未命名模式和变量(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/443)  
    
-   JEP 445：[未命名类和实例主方法(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/445)  
    

  
被归入 **HotSpot** 的 3 个新特性：

-   JEP 439：[分代ZGC](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/439)  
    
-   JEP 449：[弃用Windows 32位x86移植](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/449)  
    
-   JEP 451：[准备禁止动态加载代理](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/451)  
    

  
最后，归入**安全库**的 1 个新特性：  

-   JEP 452：[密钥封装机制API](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/452)  
    

值得注意的是，JEP 404（[分代Shenandoah(实验特性)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/404)），最初是针对 JDK 21 的）已正式从 JDK 21 的最终特性集中[移除](https://link.zhihu.com/?target=https%3A//mail.openjdk.org/pipermail/jdk-dev/2023-June/007959.html)。这是由于“在审查过程中发现了确定性的风险，并且没有足够的时间来进行针对大量代码改动所需的评审。”Shenandoah 团队决定“尽他们所能提供最好的分代 Shenandoah”，并将 JDK 22 作为发布目标。  
  
我们研究了其中的一些新特性，以及它们所属的 4 个主要 Java 项目——[Amber](https://link.zhihu.com/?target=https%3A//openjdk.java.net/projects/amber/)、[Loom](https://link.zhihu.com/?target=https%3A//wiki.openjdk.java.net/display/loom)、[Panama](https://link.zhihu.com/?target=https%3A//openjdk.java.net/projects/panama/)和[Valhalla](https://link.zhihu.com/?target=https%3A//openjdk.java.net/projects/valhalla/)——这些项目旨在孵化一系列组件，并最终包含在 JDK 中。  
  
**Project Amber  
**  
JEP 445（[未命名类和实例主方法(预览版)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/445)），也就是之前的\_灵活的主方法和匿名主类(预览)\_和\_隐式类和增强的主方法(预览)\_，提议“让新手可以很容易地编写他们的第一个 Java 程序，而无需知道那些为大型程序而设计的语言特性。”Oracle Java 语言架构师[Brian Goetz](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/briangoetz/)在 2022 年 9 月撰写了博文[Paving the on-ramp](https://link.zhihu.com/?target=https%3A//openjdk.org/projects/amber/design-notes/on-ramp)进一步推进了这一 JEP。Oracle 技术咨询委员会成员[Gavin Bierman](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/gavin-bierman-a0173075/)已[发布](https://link.zhihu.com/?target=https%3A//mail.openjdk.org/pipermail/amber-dev/2023-May/008065.html)[规范文档](https://link.zhihu.com/?target=https%3A//cr.openjdk.org/~gbierman/jep445/jep445-20230502/specs/unnamed-classes-instance-main-methods-jls.html)初稿，供 Java 社区评审。关于 JEP 445 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/05/beginner-friendly-java/)中找到。  
  
JEP 440（[记录模式](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/440)）最终确定，并根据前两轮的[预览](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/12)反馈进行了改进：在 JDK 20 中发布的 JEP 432（[记录模式(第二次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/432)）和在 JDK 19 中发布的 EP 405（[记录模式(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/405)）。这个特性通过\_记录模式\_来解构记录值。记录模式可以与\_类型模式\_结合使用，实现“强大的、声明式和可组合的数据导航和处理形式”。类型模式在`switch`中得到了进一步采用：在 JDK 18 中发布的 JEP 420（[switch模式匹配(第二次预览)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/420)）和在 JDK 17 中发布的 JEP 406（[switch模式匹配(预览)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/406)）。JEP 432 最重要的变化是删除了对出现在增强的`for`语句头中的记录模式的支持。关于 JEP 440 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/05/java-gets-boost-with-record/)中找到。  
  
JEP 430（[字符串模板(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/430)）提出了用\_字符串模版\_（包含嵌入表达式的字符串字面量）来增强 Java 编程语言，这些表达式将在运行时进行验证和求值。关于 JEP 430 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/04/java-gets-a-boost-with-string/)中找到。  
  
**Project Loom  
**  
JEP 453（[结构化并发(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/453)）结合针对前两轮孵化的反馈：在 JDK 19 中发布的 JEP 428（[结构化并发(孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/428)）和在 JDK 20 中发布的 JEP 437（[结构化并发(第二轮孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/437)）。最新的重大变化包括：`TaskHandle`接口被重命名为[\`Subtask\`](https://link.zhihu.com/?target=https%3A//cr.openjdk.org/~alanb/sc/api/java.base/java/util/concurrent/StructuredTaskScope.Subtask.html)；修复了`handleccomplete()`方法的通用签名；修改了取消子任务时的状态和行为；在[\`Threads\`](https://link.zhihu.com/?target=https%3A//cr.openjdk.org/~alanb/sc/api/jdk.management/com/sun/management/Threads.html)类中定义了一个新的`currentThreadEnclosingScopes()`方法，该方法返回一个包含当前结构化上下文描述的字符串；[\`StructuredTaskScope\`](https://link.zhihu.com/?target=https%3A//download.java.net/java/early_access/loom/docs/api/jdk.incubator.concurrent/jdk/incubator/concurrent/StructuredTaskScope.html)类的`fork()`方法返回一个`Subtask`（之前前的`TaskHandle`）实例而不是[\`Future\`](https://link.zhihu.com/?target=https%3A//docs.oracle.com/en/java/javase/20/docs/api/java.base/java/util/concurrent/Future.html)，因为老的`TaskHandle`接口的`get()`方法被重构为行为与`Future`接口的`resultNow()`方法相同。关于 JEP 453 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/06/structured-concurrency-jdk-21/)中找到。  
  
JEP 446（[作用域值(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/446)），也就是之前的\_扩展局部变量（孵化器）\_，现在是 JEP 429（[作用域值(孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/429)，在 JDK 20 中发布）之后的一个[预览](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/12)特性。这个 JEP 建议在线程内部和线程之间共享不可变数据。这比线程局部变量更可取，特别是在使用大量虚拟线程时。  
  
JEP 444（[虚拟线程](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/444)）根据前两轮的预览进行特性的确定：在 JDK 20 中发布的 JEP 436（[虚拟线程(第二次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/436)）和在 JDK 19 中发布的 JEP 425（[虚拟线程(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/425)）。该特性为 Java 平台提供虚拟线程，可以显著减少编写、维护、观察高吞吐量并发应用程序的工作量。来自 JEP 436 的最重要的变化是虚拟线程现在完全支持[线程局部变量](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8303683%23Thread-local-variables)，取消了不使用这些变量的选项。关于 JEP 444 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/04/virtual-threads-arrives-jdk21/)和 Oracle Java 平台组 Java 开发者布道师[José Paumard](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/jos%25C3%25A9-paumard-2458ba5/)的[JEP Café](https://link.zhihu.com/?target=https%3A//inside.java/2022/06/08/jepcafe11/)中找到。  
  
**Project Panama  
**  
JEP 448（[Vector API(第六次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/448)）结合了对前五轮孵化反馈的增强：在 JDK 20 中发布的 JEP 438（[Vector API(第五次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/438)）、在 JDK 19 中发布的 JEP 426（[Vector API (第四次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/426)）、在 JDK 18 中发布的 JEP 417（[Vector API (第三次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/417)）、在 JDK 17 中发布的 JEP 414（[Vector API (第二次孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/414)）、在 JDK 16 中作为[孵化器模块](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/11)发布的 JEP 338（[Vector API (孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/338)）。此功能建议增强 Vector API，以便可以从外部函数和内存 API 定义的[\`MemorySegment\`](https://link.zhihu.com/?target=https%3A//docs.oracle.com/en/java/javase/14/docs/api/jdk.incubator.foreign/jdk/incubator/foreign/MemorySegment.html)中加载和存储 Vector。  
  
JEP 442（[外部函数和内存API(第三次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/442)）基于之前的反馈进行了改进，并提供第三次预览：在 JDK 20 中发布的 JEP 434（[外部函数和内存API(第二次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/434)）、在 JDK 19 中发布的 JEP 424（[外部函数和内存API(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/424)），以及相关的孵化——在 JDK 18 中发布的 JEP 419（[外部函数和内存API(第二孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/419)）和在 JDK 17 中发布的 JEP 412（[外部函数和内存API(孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/412)）。这个特性为 Java 应用程序提供了一个 API，可以通过有效地调用外部函数和安全地访问不受 JVM 管理的外部内存与 Java 运行时之外的代码和数据进行互操作。来自 JEP 434 的更新包括：在`Arena`接口中集中管理本地段的生命周期、增强的布局路径，使用新元素来解引用地址布局、移除`VaList`类。  
  
开发人员可能会有兴趣了解外部函数和内存 API 所带来的性能提升，这个 API 预计将成为 JDK 22 的最终特性。Oracle 技术咨询委员会成员[Per-Åke Minborg](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/minborg/)发表了一篇[博文](https://link.zhihu.com/?target=http%3A//minborgsjavapot.blogspot.com/2023/08/java-22-panama-ffm-provides-massive.html)，他在文章中提供了一个关于字符串转换的基准测试，他使用这个 API 在 JDK 21（JEP 442）和 JDK 22（JEP Draft 8310626）中与旧的 Java 本地接口(JNI)调用进行了比较。  
  
**HotSpot  
**  
JEP 439（[分代ZGC](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/439)）“通过扩展 Z Garbage Collector(ZGC)来为年轻代和老年代象维护单独的代来提高应用程序性能”。这将使 ZGC 能够更频繁地回收早就成为垃圾的年轻代对象。”关于 JEP 439 的更多细节可以在 InfoQ 的[报道](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/07/java-enhance-zgc/)中找到。  
  
**JDK 22  
**  
目前还没有针对计划于 2024 年 3 月发布的[JDK 22](https://link.zhihu.com/?target=https%3A//jdk.java.net/20/)的 JEP。然而，根据一些 JEP 候选和草案，特别是那些已经提交的，我们可以推测出哪些额外的 JEP 有可能包含在 JDK 22 中。  
  
[Project Amber](https://link.zhihu.com/?target=https%3A//openjdk.org/projects/amber/)的 JEP 447（[super()前置语句](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/447)）提议：允许构造函数中不引用正在创建的实例的语句出现在`this()`或`super()`调用之前，并保留现有的安全性和初始化保证。Oracle 技术咨询委员会成员[Gavin Bierman](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/gavin-bierman-a0173075/)提供了该 JEP 的[初始规范](https://link.zhihu.com/?target=https%3A//cr.openjdk.org/~gbierman/jep447/jep447-20230420/specs/statements-before-super-jls.html)，供 Java 社区评审和反馈。  
  
JEP 435（[异步堆栈跟踪虚拟机API](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/435)），一个特性 JEP，提议定义一个有效的 API，用于从包含 Java 和本地帧信息的信号处理程序获取异步调用跟踪信息。  
  
JEP 401（[Null-Restricted值对象存储(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/401)，之前的\_原始类(预览)\_，属于 Project Valhalla），引入了开发人员声明的原始类（Primitive Classes）——由值对象 API 定义的特殊类型的值类——它们定义了新的原始类型。  
  
**JEP 草案 8307341**（[为限制JNI使用做准备](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8307341)），提议限制使用不安全的 Java 本地接口(JNI)，并在外部函数和内存(FFM)API 中使用受限制的方法，[这预计将成为JDK 22的最终特性](https://link.zhihu.com/?target=https%3A//mail.openjdk.org/pipermail/jdk-dev/2023-August/008061.html)。从 JDK 22 开始，Java 运行时将会显示关于使用 JNI 的警告，除非 FFM 用户通过命令行启用不安全的本地访问。预计在 JDK 22 之后的版本中，使用 JNI 将抛出异常而不是警告。  
  
**JEP 草案 8310626**（[外部函数和内存API](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8310626)），建议经过两轮孵化和三轮预览之后成为最终特性：在 JDK 17 中发布的 JEP 412（[外部函数和内存API(孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/412)）、在 JDK 18 中发布的 JEP 419（[外部函数和内存API(第二孵化器)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/419)）、在 JDK 19 中发布的 EP 424（[外部函数和内存API(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/424)）、在 JDK 20 中发布的 JEP 434（[外部函数和内存API(第二次预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/434)），以及即将在 JDK 21 中发布的 JEP 442（[外部函数和内存API(第三预览版)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/442)）。自上一个版本以来的改进包括：一个新的`Enable-Native-Access` MANIFEST 属性，允许可执行 JAR 包中的代码调用受限制的方法，不需要使用`——Enable-Native-Access`标志；允许客户端以编程方式构建 C 函数描述符，避免使用特定于平台的常量；改进对本地内存可变长度数组的支持；本机字符串多字符集支持。  
  
**JEP 草案 8288476**（[模式、instanceof和switch中的原始类型(预览)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8288476)），提议“允许在所有模式上下文中使用原始类型模式，将原始类型模式的语义与 instanceof 对齐，并允许将原始常量作为 switch 的 case 标签。”  
  
**JEP 草案 8277163**（[值对象(预览)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/8277163)），Project Valhalla 的一个特性 JEP，提议提供值对象——可以指定其实例行为的无标识值类。该草案与仍处于**候选**状态的 JEP 401（[原始类(预览)](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/401)）相关。  
  
**JEP 草案 8313278**（[Java虚拟机的提前编译](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8313278)），提议“让 Java 虚拟机加载编译成本地代码的 Java 应用程序和库，以实现更快的启动和基线执行。”  
  
**JEP 草案 8312611**（[计算常量](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8312611)），引入了\_计算常量\_的概念，持有不可变值，最多可被初始化一次。它具备`final`字段的性能和安全优势，同时在初始化时间方面提供了更大的灵活性。该特性将作为[预览](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/12) API 首次亮相。  
  
**JEP 草案 8283227**（[JDK源代码结构](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8283227)），一个信息类 JEP，用于描述 JDK 源代码和 JDK 代码库中相关文件的总体布局和结构。该 JEP 建议帮助开发人员适应 JEP 201（[模块源代码](https://link.zhihu.com/?target=https%3A//openjdk.java.net/jeps/201)，在 JDK 9 中发布）所描述的源代码结构。  
  
**JEP 草案 8280389**（[ClassFile API](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8280389)），提议提供一个用于解析、生成和转换 Java 类文件的 API。这个 JEP 最初将作为[ASM](https://link.zhihu.com/?target=https%3A//asm.ow2.io/)（Java 字节码操作和分析框架）的内部替代方案，并计划将其作为公共 API 开放出来。Java 语言架构师[Brian Goetz](https://link.zhihu.com/?target=https%3A//www.linkedin.com/in/briangoetz)称 ASM 为“带有大量遗留包袱的旧代码库”，并提供了关于该草案将如何演进并最终取代 ASM 的相关信息。  
  
**JEP 草案 8278252**（[JDK打包和安装指南](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8278252)，一个信息类 JEP，提议为构建 macOS、 Linux 和 Windows 的 JDK 安装程序提供指南，以降低在安装不同 JDK 供应商提供的 JDK 时出现冲突的风险。其目的是通过形式化安装目录名称、包名称和可能导致冲突的其他元素，为安装 JDK 更新版本提供更好的体验。  
  
我们预计 Oracle 很快就会提供 JDK 22 将包含的 JEP。  
  
**原文链接**：  
[https://www.infoq.com/news/2023/09/java-21-so-far/](https://link.zhihu.com/?target=https%3A//www.infoq.com/news/2023/09/java-21-so-far/)

  

**本文转载来源：**

[Java 21：最新进展一览\_编程语言\_Michael Redlich\_InfoQ精选文章](https://link.zhihu.com/?target=https%3A//www.infoq.cn/article/QB87kOkWjf6jXxODkd9T)