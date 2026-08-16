---
id: "36932325263"
title: "java 可以跨平台的原因是什么？"
author: "kimmking"
type: zhihu-answer
source: "https://www.zhihu.com/question/573490785/answer/36932325263"
created: "2024-11-21 11:36"
updated: "2024-11-21 11:36"
collected: "2024-11-21 11:36"
downloaded: "2026-08-16"
---
我们对比一个东西就可以了，那就是chrome浏览器。

MacOS/Linux/Windows上的Chrome浏览器，那么对于HTML/CSS/JS的渲染效果都一样的。

我们就可以认为Chrome+HTML/CSS/JS是跨平台的。

这里面，HTML/CSS/JS是不变的的，对于一个网页，它就一份。

但是在不同的操作系统上，Chrome 程序其实是不一样的。

然后用这些不一样的Chrome程序，来渲染同一份HTML/CSS/JS，实现同样的效果。

HTML/CSS/JS 是代码or程序，Chrome是代码运行的平台，也叫运行时Runtime。

同样的，对于Java来说，也有两个东西。

Java代码以及编译后的字节码，class文件或其打包的jar文件。

以及运行class或jar的容器，Java虚拟机，也叫JRE运行时。

不同操作系统平台上安装的JRE是不一样的。

但是给他们同样的一个class或者Jar文件，这些不同的虚拟机需要屏蔽差异，像Chrome运行HTML/CSS/JS一样，执行Java程序的效果最后是一样的。

这就是跨平台的原因，有一层用来承上启下的事儿，对上做抽象提供统一的调用方式和执行结果，对下屏蔽下层平台或操作系统的差异性，封装起来。

用一句最简单的话来说，不同平台的差异性由一个虚拟层来屏蔽掉了。

实际上，这个思路被用在各个地方，比如Linux操作系统跨不同的硬件平台。

再比如，Java的Swing和eclipse的swt/jface都可以做跨MacOS/Linux/Windows的桌面UI程序。

但是Swing和SWT/jface的方式又有非常大的差异。

Swing是完全自己重新画一套虚拟的界面出来，这样UI就全部统一了，缺点是效率低一点，优势是不管什么平台都是完全一致的。

SWT/jface则是直接复用当前操作系统原生或者某个native的UI，然后封装一层统一的操作模型，这样的优势是效率高一些，一个明显的缺点是，不同平台上明显效果是差异较大的。