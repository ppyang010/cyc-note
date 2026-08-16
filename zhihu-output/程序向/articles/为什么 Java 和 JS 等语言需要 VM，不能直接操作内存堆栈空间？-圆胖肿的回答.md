---
id: "1838749872"
title: "为什么 Java 和 JS 等语言需要 VM，不能直接操作内存堆栈空间？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/449995754/answer/1838749872"
created: "2021-04-16 18:42"
updated: "2021-04-16 18:42"
collected: "2021-04-16 18:42"
downloaded: "2026-08-16"
---
第一个，java现在已经不再强调jvm的概念，如果你还在学习所谓的jvm，那你的知识需要更新一下了

以前是这样，jvm是跨平台所需要部分的最小子集，也就是主要用来封装操作系统差异用的，每一个操作系统，都给弄一个jvm，这样暴露给上层的接口就统一了

在jvm的基础之上，加上一些常见的类库，工具，就做成了jre，也就是java的运行时runtime

然后再在jre的基础之上，添加一些编译器等工具，这就是java的sdk了，简称jdk

所以jdk是jre的超集，jre是jvm的超集，反过来，jvm是jre的子集，jre是jdk的子集

一般而言，jvm是native代码，通常用c或者c++编写而成，以前bea的jrockit就是c写的，但是现在用的openjdk和oraclejdk都是hotspot，c++写的，作者叫做lars bak，这个人很重要，记住这个人，等下会说，然后在jvm的基础上，以前再加上java写的rt.jar，就是jre了，过去java会提供jre和jdk两个下载，如果只是运行java的字节码，jar那些的话，你下载jre安装就行了，不需要安装jdk，只有开发者才需要jdk

而java在9的jigsaw之后，就不再使用jvm的概念，因为jre也就是java的运行时可以被定制了，jvm和jre被拆成了一个又一个的模块，你自己可以根据需要，删减或者加入自己编写的模块，我这两天刚做完steamworks sdk的java包装模块，然后我就把steam sdk给加入到我自己的java运行时里面去了，所以我的jre跟你的jre，是不一样的，我的jre支持steam sdk

所以为什么不再强调jvm的概念，就是这个原因，因为java的运行时可以被定制，就不再是以前  
jre = jvm+rt.jar  
那种搞法了，而是jmods以及其他模块化jars的自由组合，一个常见的会放进去的jmod就是javafx的那些jmods

那几乎所有语言都是runtime运行时，包括c，c++和rust，从这一点上说，java跟c等语言，没有什么本质上的不同，都是运行时

第二个，刚才说的java的vm+runtime部分的做法，其实lars bak也用在了其他地方，比如flutter用的dartvm，然后你说的js，多半指的是v8吧，那这个也是lars bak做的

所以为什么你会觉得，怎么概念都比较接近，因为最开始都是一个人做的，但并不是所有的语言，它都是这样，现在不怎么强调vm虚拟机这个概念，而普遍转向runtime运行时的概念，跟大多数语言保持一致

第三个，java访问内存，当然可以，只是以前java还不行，但是java将会可以这么做，这就是java的panama巴拿马项目正要做的事，比如访问堆外内存[^1]

```java
MemorySegment segment = MemorySegment.allocateNative(100);
```

只是说java相对而言，对于内存管理，封装得比较好，就不允许用户轻易访问内存

你真要做，用c写一个，然后用jni包装一层，哪有什么做不了的，以前一大堆人用unsafe，但是不安全，你看这名字就知道了，容易写错

以前就是挑剔gc比较慢嘛，那有问题解决问题，gc现在都被优化到1ms以内，平均是0.1-0.2ms的暂停了[^2]，这个前提下，你就不需要太过于关心gc带来的问题，而可以享受gc带来的内存管理的便捷，是吧，你自己去写，一大堆bugs，直接用不是很好，何必给自己找麻烦？

第四个，编译器

编译器是无所谓你用什么语言写的，但是在一个编程语言还没诞生之前，要实现该语言的编译器，那就只能用其他语言来实现，所以c的第一款编译器，多半是汇编或者介于汇编和c之间的一个语言写出来的，但是现在c的编译器应该已经全部是c自己写的了，还有其他语言写的了

java也是一样，java最早的编译器是c（jrockit）或者c++（hotspot）写的，但是现在出现了java自己写的java编译器，那就是java的圣杯graal[^3]，graal是法语圣杯的意思，graal就是java写的多语言的编译器，它不仅可以编译java，还可以编译其他语言，比如ruby，python那些东西

第五个，编译产物

虽然现在java代码多数还是运行在jre上，也就是java的运行时上，但是，graal出现之后，java可以被编译成native代码，这就跟c很像了，其实之前就有很多技术可以对java做aot，只是一直没有进入主流视野，graal之后算是官方产品，如果你的目标是把产品送上比如app store这种渠道的话，你应该会对这些功能比较熟悉

现在流行的是jit和aot双功能，jit用来开发测试时候使用，真正release的时候，再做aot，也就是编译成native代码，包括但不限于dart/flutter，swift和java，这些都朝着同时支持jit和aot的方向前进

[^1]: [1] https://github.com/openjdk/panama-foreign/blob/foreign-jextract/doc/panama_memaccess.md
[^2]: [2] https://wiki.openjdk.java.net/display/zgc/Main
[^3]: [3] https://www.graalvm.org/