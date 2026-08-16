---
id: "2387500784"
title: "关于Java的Panama project一些问题?"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/521680078/answer/2387500784"
created: "2022-03-13 19:36"
updated: "2022-03-13 19:38"
collected: "2022-03-13 19:36"
downloaded: "2026-08-16"
---
先让我不厚道滴笑一下，2年，这个时间跨度在java的项目中，根本排不上号，而且panama也不是才做了2年，而是

**8年**

从2014年，也就是java 8发布之后，就立项了panama项目，一直做到现在

而且这个在java的相关项目中，不算是特别久的，graal做了快20年，前后换了三个名字，才在2018年真正发出来，光graal这个项目，就做了8年，现在还在做，前面还有maxine（05-12）和klein（99-05）

所以panama的时长，充其量也就是个中规中矩，谈不上特别久

不过人生可没多少个8年，好在这个漫长的等待，已经开始接近尾声了，总算java的几个重要项目，panama，valhalla和loom，都要开始准备preview了

按照现在jcp的流程，任何一个jep，只要开始preview了，那么正常情况下，也就是只要不出现大的设计问题，那么一年之后，也就是2nd preview之后，就会正式下版本

比如19开始preview，那么20就是2nd preview，21正式下

除非说，像之前的\`的那个设计一样，出现比较多的反对声音，那么会重新设计，改成"""后，再次preview，那就要多等一两年这样子，但是这种比较少，属于特殊情况

在preview之前，是incubator或者experimental阶段，那panama的两个重要jep，已经经过了好多次incubator了，分别是  
  
[JEP 338: Vector API (Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/338)  
[JEP 414: Vector API (Second Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/414)  
[JEP 417: Vector API (Third Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/417)  
[JEP 370: Foreign-Memory Access API (Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/370)  
[JEP 383: Foreign-Memory Access API (Second Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/383)  
[JEP 393: Foreign-Memory Access API (Third Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/393)  
[JEP 389: Foreign Linker API (Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/389)  
[JEP 412: Foreign Function & Memory API (Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/412)  
[JEP 419: Foreign Function & Memory API (Second Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/419)

你看这么多incubator，这些是已经下了版本的jeps，然后经过前面这么多铺垫，总算

[JEP 424: Foreign Function & Memory API (Preview)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/424)

424开始preview了，那你只需要看，这个preview什么时候开始纳入版本，就大概能推测出下生产的时间了，现在按照在jcp的邮件交流以及twitter等社交媒体上看，应该是19会开始preview，所以差不多是21下

21就是明年9月，也就是说，今年9月开始preview，明年9月正式下发生产，而且21正好是一个lts，也就是长期支持版本，所以应该是21下，也就是明年9月

然后panama是一个大的项目，它拆成两个部分，然后科技树的依赖是这样

foreign function & memory api -> vector api

而且vector api同时会依赖valhalla的一些进展，valhalla的科技树依赖是这样

value object -> primitive class -> universal generics

vector api需要至少value object，所以vector api在foreign function & memory api下生产之前，还会继续保持在incubator的状态，所以你会看到，forth incubator以及将来还会出现的fifth incubator等vector api的jeps出现，比如

[JEP draft: Vector API (Fourth Incubator)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/8280173)

这个就能回答你，panama大概什么时候下的问题了，当然对于多数人而言，vector api可能用到的不是很多，最重要的还是直接用panama调用c等native api，就是foreign function & memory api了

以及对应的，根据c的h头文件，extract萃取出java interface的jextract项目

那这个应该是就是看什么时候开始preview了

而且话说回来，看现在的jep列表，18之后，候选的jeps已经很少了，剩下的，全部都是panama，valhalla和loom的jeps，不上这些项目，就没东西可上了

刚前面解释了panama和valhalla的科技树，那loom的科技树也说一下，是

virtual thread -> scope local -> structure concurrency

当然对于多数人而言，最重要的是第一个，virtual thread，也就是java的goroutine，纤程，fiber这些，但是java的命名是，虚拟线程，因为api跟线程thread的api是一样的，这样做方便类库升级

然后现在这三个大项目，panama，valhalla和loom的第一个preview，都已经给出jeps了

分别是：

[JEP 424: Foreign Function & Memory API (Preview)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/424)  
[JEP draft: Virtual Threads (Preview)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/8277131)  
[JEP draft: Value Objects (Preview)](https://link.zhihu.com/?target=http%3A//openjdk.java.net/jeps/8277163)

你看，现在的状态全部都是preview了，那只要开始preview，前面说了，一年之后，就下生产

那就看，这几个具体什么时候开始preview了

panama的这个424按照目前各个渠道流出的消息，这个排到19里面去，问题不大

其他两个preview嘛，也就是java的虚拟线程和值类型

但是就算不是19，那也是20排进去，差个半年下生产

所以这就能回答你的第一个问题

* * *

第二个问题，弥补科学计算和gui的缺陷

科学计算的缺陷，这个可能valhalla也就是java的值类型放出来之后，可以做的会更多，用c去写科学计算嘛

当然也不是没有，国内一堆技术不行的，学谭浩强老师的c语言出身的，比较有可能这么干，但是国外一般flink，spark什么都算是比较成功的案例了，其实就算真要这么干，科学计算的高复杂度，也就是cpu密集型应用，graal那边有sulong，还有gcuda，其实都可以做到类似的效果，并不是一定要等panama不可

[https://github.com/NVIDIA/grcuda](https://link.zhihu.com/?target=https%3A//github.com/NVIDIA/grcuda)

而且graal还能用r，不比panama简单？

gui上的话，其实jni现在也能用，javafx就是主要用jni，而且graal对于javafx的支持，也已经很先进了

比如可以对javafx的项目，做各种平台上的native image，比如linux还有windows，mac当然不在话下了，我最近写的项目，就利用github action，对树莓派和windows做了native image/aot编译

在这里

[https://github.com/vertx-china/ShallVTalk/actions/workflows/aot.yml](https://link.zhihu.com/?target=https%3A//github.com/vertx-china/ShallVTalk/actions/workflows/aot.yml)

那个启动是超级快的说，一点就开

所以光gui，其实也没有那么迫切

对于现有的工具而言，其实他们都已经做到了native化，当然你说，panama是不是有正面积极的影响，那显然还是有的，panama无论如何，都比jni要快，只是这个快，对于这些简单的调用而言，并没有那么明显的促进作用

比较有意义的，应该是游戏领域，尤其是3d游戏，这个在社区里面，经常可以看到，老外在提议，意思就是，我要用java做游戏，3d游戏，panama和valhalla什么时候出来

因为3d游戏在gpu和cpu之间的数据交换，比较密集，比较吃性能，经常需要自己手动去写shader之类的函数，那目前opengl和vulkan两个跨平台的渲染管道，提供的都是c的api，metal提供的是c++，那苹果会优化swift和c++之间的调用，最近刚立项了，除开苹果平台，其他的平台上，主要就是c了，panama对于这个领域，会有比较大的促进作用

* * *

第三个问题，对于普通人会有什么影响

可能最直接的利好，就是你用c写的类库，以后会更加简单

我很怀疑，以后maven central上，会出现大量的c等语言写的native依赖

其实现在已经越来越多了

当然这个对于普通用户而言，是透明的，就你不写类库的话，可能你未必感受得到

对于普通用户而言，将来调用这些native类库啊（dylib，so，dll）就跟调用jar一样简单方便

这个可能是panama对于java普通用户的最直接的影响