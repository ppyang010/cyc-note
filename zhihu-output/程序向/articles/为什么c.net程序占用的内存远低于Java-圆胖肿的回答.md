---
id: "3153637237"
title: "为什么c#(.net)程序占用的内存远低于Java?"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/615720475/answer/3153637237"
created: "2023-08-07 09:23"
updated: "2023-08-07 09:24"
collected: "2023-08-07 09:23"
downloaded: "2026-08-16"
---
你写的hello world内存占用的优化，这个我之前在twitter上看到过javafx作者johan vos曾经讲过，如何通过模块化，进一步优化java.base等模块，把java启动占用内存缩小到几m，但是嘛，似乎对此感兴趣的人非常少，最后也就不了了之

java好像从来没有关注过在启动时候内存占用的优化，甚至java并不是特别看重内存优化，总体而言，java社区大概有这么一个思路，就是内存是拿来用的，不是拿来看的，所以java程序经常是饥渴滴占用内存，你给它多少，它就用多少，大概这种思路

但是即便如此，也还是有一些方式，能够让你运行中的java内存占用更小，依次列举

1.  xmx参数，可以设置java最大的内存占用，zgc测试时候从2m到2t都测试过，所以你可以试试直接把xmx设置成2m
2.  client mode，现在java启动大部分是以server mode形式启动，但是在早期，java是可以以client mode启动，client mode更加看重内存的占用小等，但是现在分发的jdk，包括openjdk，大部分都已经干掉了client mode，所以如果你能找到有client mode提供的jdk，那么用client mode启动，会有收获
3.  project liliput，小人国项目，这个是red hat正在推进的一个项目，立志要把启动时间和内存占用缩小，以适配aot和jit之间的一种场景，这个好像有一些成果出来了，但是我没怎么关注，有兴趣可以看看：[https://wiki.openjdk.org/display/lilliput](https://link.zhihu.com/?target=https%3A//wiki.openjdk.org/display/lilliput)，但是一般red hat做的这些side project，都不会被并入openjdk，尤其是会被oracle的openjdk给删了，比如shenandoah就被oracle的open jdk给删了，以后要是打算用这个，需要用其他公司提供的openjdk build
4.  zgc，zgc会把gc来的内存还给操作系统
5.  aot，aot可以减少内存占用
6.  值类型，明年3月就会下panama，也就是java的加强版ffi，值类型的value object的jep也已经开始提供preview了，不知道22还是23会开始preview，用值类型可以减少内存占用

大概这些，但是总体而言，java并没有真的很看重启动时候的内存占用，甚至整个运行过程中的内存占用都不是非常看重，虽然有项目可以对这方面有帮助性贡献

如果你非常在意内存大小的话，那就别用java了