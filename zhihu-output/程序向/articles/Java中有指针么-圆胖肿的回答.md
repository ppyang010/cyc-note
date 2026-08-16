---
id: "3396362860"
title: "Java中有指针么?"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/597994094/answer/3396362860"
created: "2024-02-14 23:34"
updated: "2024-02-14 23:35"
collected: "2024-02-14 23:34"
downloaded: "2026-08-16"
---
这个话题最近被翻出来，我估计是 java 22 一个重要特性 project panama a.k.a. ffm，即将下发生产的缘故，实际上 22 的第一个 rc 也就是release candidate已经放出来了，github action上已经可以下到不带-ea后缀的 jdk 22 build了，这个其实就已经是正式版了，除非发现有重大bugs（可能性极低）否则这个跟真正release时候的第一个版本不会有什么区别

[JEP 454: Foreign Function & Memory API](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/454)[https://jdk.java.net/22/](https://link.zhihu.com/?target=https%3A//jdk.java.net/22/)

ffm就是java中像c一样操作内存的功能，直接取代之前的 jni 和 unsafe，后者在使用时候，会抛出非安全警告，如果想关闭警告，则需要用户在启动 java 程序的时候，加入一个 option 以开启非安全操作，在该option中用户需要明确具体unsafe操作的模块名称，这样才能真正关闭warning警告

很多类似问题下面的回答都说到 java 有指针，说的就是 unsafe，那 unsafe（还有jni）的继任者 ffm 已经在下发生产过程中了，所以如果你能接受这个就是 java 的指针的话，也就是用代码操作内存，这个就是你想要找的东西，它可以用代码画出堆外内存，并指定该内存快是否由gc管理，或者干脆你自己手动处理，后者也就是unsafe的功能，因为这种操作的不安全的特性，所以会有warning和option授权这些东西

* * *

我觉得有个回答说得很好

> 你以为的好工具：把所有的能用的都暴露出来，让用户自行选择用哪个  
> 而真正的好工具其实是：让傻子也能用来解决问题

比如 c++ 就是前者的代表，而 java 是后者的代表

其实你认真看 java 的特性，没有的东西多得去了

比如它只有有栈的纤程，而没有无栈的协程，所以它没有 async 和 await

比如它只有 gc，而没有 arc，所以它没有 weak

但是，java的特点就是简单，因为它没有 async，await，weak，指针这些玩意

那么我在工作中，就不需要费劲跟人去解释什么是 async/await，什么时候应该标记 weak，还有\*(int\*)&addr 这种看起来花里花哨的玩意是啥，实际上这个我都不确定写没写对

* * *

正规说起来，java中并没有指针

或者说，java并不要求你在学习的过程中，理解什么是指针，它不会跟你解释和讨论这个概念，你不懂也没关系，懂了也不一定好，因为半懂不懂的，对真正掌握这个工具未必有好处

指针应该被认为是实现java中某些概念，比如引用的一种手段

但其实我感觉，所谓的引用，也随着一些概念的引入，正在被逐步规范化，是不是被淘汰掉，不好说，因为以后会开始强调普通对象和值对象差别，这两者的差别其实是普通对象有 id，而这个东西，java specification并没有讲得很清楚，id和引用，地址这些概念在spec.里面有些乱，但是我相信，随着value class这个特性的发展并最终下发生产，这一块会有比较大的改变，并最终将其规范起来，就看到时候怎么讲会比较清楚了，这一块有逐渐向 swift 类似概念看齐的可能，实际上 java 的一些seminar，也就是座谈会，java 开发组参加，java当前的主架构马克就说，java当前正在向 node.js，go和swift等语言学习和借鉴一些特性，前两者比较容易理解，比如虚拟线程，就是充分参考了 node.js 和 go 的设计，而 java 对于 swift 的参考，是不是一直都没看到？直到值类型的出现，当 java 开始强调引用类型和值类型区别，而且说这两者区别是有没有 id 的时候，swift 的痕迹就出现了