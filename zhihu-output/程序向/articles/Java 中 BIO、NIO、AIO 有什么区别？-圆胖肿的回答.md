---
id: "3327315149"
title: "Java 中 BIO、NIO、AIO 有什么区别？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/570649003/answer/3327315149"
created: "2023-12-16 00:47"
updated: "2023-12-18 14:21"
collected: "2023-12-16 00:47"
downloaded: "2026-08-16"
---
啊，java中没有aio，这个是中国人造的名词，不信你Google一下java aio，搜索出来的全都是中文网页，什么乱七八糟的，估计是一些英语很糟糕的中国程序员一知半解瞎说的东西，个人建议，你要有基本的英语阅读能力，就别看国内这些东西了，看不懂不说，看出一堆中国人造的错误概念才是真要命

**java只有bio，nio和nio 2**

bio全称是basic io，都放在[http://java.io](https://link.zhihu.com/?target=http%3A//java.io)这个包下面，这里面的操作大部分都是阻塞（blocking）的，会阻塞调用线程

nio全称是non blocking io，就放在java.nio这个包下面，里面操作大部分是非阻塞的，不会阻塞调用线程

nio2在nio的基础上，新增了一个文件操作的java.nio.file包，让你操作文件时候也能像操作网络io一样不会阻塞调用线程

再次强调，没有aio，异步和非阻塞其实是同义词，不存在说nio同步，nio2/aio异步的情况，记得中文网站上流传甚广的关于异步和非阻塞的对比的那个文章，列举了什么同步非阻塞和异步非阻塞的区别

**那个感觉是错误的**，因为我并没有看到老外强调异步和非阻塞的差别，反正java这里不强调也没有aio这个概念，nio里面所有的api本身就是异步的api，也不会阻塞调用线程，同步非阻塞可能说的是loom也就是虚拟线程毕业之后，vert.x 5里面实现的那种future.await的方法，但是java的nio2也就是java.nio.file包真的不是同步的写法，一样也是异步的写法

* * *

一开始我只是觉得java没有aio这回事，后来发现，java不仅没有aio，java也没有blocking io和non blocking io这几个，这是某个特定操作系统，比如posix也就是unix-like操作系统的几类api

具体在这里：[https://en.wikipedia.org/wiki/Asynchronous\_I/O](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Asynchronous_I/O)

但是java中没有这个概念，java只有io和new io

而io的实现可能在posix操作系统上是用blocking io实现的，所以这个如果认为是bio，还算合理

但是new io，就不一定都是non blocking io实现的了，可能也有async io实现的

所以应该说，这个问题是把操作系统的api生搬硬套到java上去，这是十分错误的

我重新写了个回答，在这里：[AIO 在 java 中有哪些应用场景？](https://www.zhihu.com/question/560021953/answer/3329859080)