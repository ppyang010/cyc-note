---
id: "3315996913"
title: "Netty到底是个啥？"
author: "八舞耶俱矢"
type: zhihu-answer
source: "https://www.zhihu.com/question/607575828/answer/3315996913"
created: "2023-12-06 21:57"
updated: "2023-12-07 12:29"
collected: "2023-12-06 21:57"
downloaded: "2026-08-16"
---
曾经用Netty写过几个fq的小工具，可以说：**Netty是一个从概念上来说外光鲜亮丽，但内部略显肮脏的网络处理框架。**

Netty的精髓就在于其链式调用handler来处理协议中的每一层，将middleware思想引入了网络协议的处理中。

在fq的工具的实现中，我可以从最底层的raw socket写起，对于tcp或者udp协议可以任意且随时进行切换，上层的加密协议也可以动态进行替换，甚至于可以无限套娃下去，写起来无比的爽快。

甚至对于一层协议中的每一个阶段，都可以将Handler的加载和卸载，作为一个状态机进行处理。比如说将socks5协议的某种认证方法，在一个handler中单独实现，当握手检测到对应的认证方法时，直接将挂载链上，待到认证完毕后，再卸载掉，后面的数据就无需再经过认证的Handler了。这个过程非常自然且顺畅。

而且在协议的处理过程中，基本上能做到将数据zero-copy的传递到下一层级（排除加解密等操作）。

但一旦到了具体Handler实现，就显得有些糟糕了。很多时候，Handler细分到一定程度无法细分了，就不得不在Handler手撸一个状态机，手撸状态机的结果就是，不得不再一个Handler里维护多个状态，导致一个Hander内部实现得复杂。

另一个糟糕之处就在于对于ByteBuf的使用，ByteBuf带来的zero-copy固然美好，但各种奇怪的Bytebuf，其生命周期的转移和维护，也是一个及其糟糕和麻烦的事情，一不留神就带了各种奇怪的内存泄漏的问题，是各种中间件和大数据组件的噩梦。

* * *

**下面是胡言乱语时间：**

如果让我改进Netty，我会考虑以下几点

首先，使用Handler分层的大思想应该是不变的，但Handler应该允许嵌套，可以灵活的进行加载和组装。

其次：虚拟线程走起，java.nio给我滚开，Netty就是给这坨东西擦屁股的。

然后，没了java.nio，ByteBuf就可以被简化了，不仅方法被简化，而且各种奇怪的也应该删掉，什么pooled/unpool，direct/Heap，safe/unsafe滚开，只要pooled/unpool+Heap就够了，是觉得zgc回收不够快么。

如果让我改进C#或者Kotlin里实现一个等价于Netty的东西，我还会考虑以下改进：

Handler里的channelRead和channelWrite应该是一个可挂起的函数，在一个Handler的生命周期中，应该只运行一次。