---
id: "572519795"
title: "运行时（runtime）是什么意思？应该怎样深入且直观地理解？"
author: "haveto上班"
type: zhihu-answer
source: "https://www.zhihu.com/question/20607178/answer/572519795"
created: "2019-01-12 23:19"
updated: "2020-02-24 00:37"
collected: "2019-01-12 23:19"
downloaded: "2026-08-16"
---
我也不太明白这个问题, 不过在 Stack Overflow 上有相关的讨论:

[What is "runtime"?](https://link.zhihu.com/?target=https%3A//stackoverflow.com/questions/3900549/what-is-runtime)

算是拾人牙慧吧, 我在这里把上面的一些回答翻译一下.

* * *

## 提问者: 什么是 runtime?

我听说过 "C Runtime", "Visual C++ 2008 Runtime", ".NET Common Language Runtime", 等等.

-   "runtime" 确切地是什么?
-   它是由什么构成的?
-   它和我的代码有什么相互影响? 或者更确切地说, 我的代码是怎样被它控制的?

当我在 Linux 上编写汇编语言时, 我可以使用 INT 指令来进行系统调用. 所以, runtime 只是一堆预制函数将低级函数包装成更抽象和更高级别的函数吗? 但是这不是更像 "库" 的定义, 而非 "运行时" 吗?

"runtime" 和 "runtime library" 是否是两个不同的东西?

ADD1:

这些天来, 我思考了一下, 也许 Runtime 与虚拟机有一些共同之处, 比如 JVM. 这是导致整个想法的引文:

> 这个编译过程非常复杂，可以分成几个抽象层，这些过程通常涉及三个转换器：编译器，虚拟机实现和一个汇编器。 This compilation process is sufficiently complex to be broken into several layers of abstraction, and these usually involve three translators: a compiler, a virtual machine implementation, and an assembler. --- [The Elements of Computing Systems](https://link.zhihu.com/?target=https%3A//www.amazon.com/dp/0262640686/)(Introduction, The Road Down To Hardware Land)

这本 [Expert C Programming: Deep C Secrets](https://link.zhihu.com/?target=https%3A//www.amazon.com/dp/0131774298) 的第 6 章 Runtime Data Structures 是一个有用的参考.

* * *

## Answer1:

Runtime 描述了 软件/指令 在你的程序运行的时候是如何执行的, 尤其是你没有明确地写出来, 却对于正确执行代码是必须的那些指令.

低级语言, 例如 C 只有很小的 runtime. 更多复杂语言, 例如 Objective-C, 允许动态的消息通过, 拥有大得多的 runtime.

你所说的 "runtime 代码是库代码" 是正确的, 但是库代码是一个更通用的术语, 描述了任何由库所生成的代码. "runtime 代码" 则特指实现语言本身特性所需要的代码.

## Answer2:

Runtime 是一个通用术语, 指代任何你的代码所运行的库, 框架或平台.

C 和 C++ 的 runtime 是函数的集合.

.NET 的 runtime 包含了一个 [通用中间语言](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Common_Intermediate_Language) 解释器, 垃圾收集器以及其他.

* * *

根据以上的回答, 虽然我也是刚谷歌这个概念, 请允许我做出一些不负责任的推测与类比:

runtime 就是一个语言实现的基础, 就好像一个人类最基本的心跳, 呼吸技能一样. runtime 和 库 的区别, 类似于 人类本身 与 人类后天增加的装备 的区别。

更新 2020 2 24。runtime 一般和 compile time 相对，他们在时间上，分别代表运行期和编译期两个时期；在代码上，runtime 代表程序能正常运行所必需的基础代码。对于解释型语言，它的解释器就是 runtime；对于编译型语言，它的 runtime 可以理解为标准库和系统库中不可或缺的那一部分。

比如 c 语言对 glibc，python 对 cpython。但有些语言的标准库的作用除了提供 runtime 之外还提供常用方法的官方实现，并非少了它们整个程序就运行不了了。对于这些并非必要的部分，一般不把它们当做语言的 runtime。

runtime 本身是一个相当混淆的概念，不需要分那么清。对于不同层级的应用，其 runtime 的含义不同。一个编程语言的 runtime 概念范围比用它写的某个应用程序的要小；另一个基于此应用的应用程序的 runtime 包含了前者。

总之， runtime 的意思大概就是 「运行期所必需的东西」。