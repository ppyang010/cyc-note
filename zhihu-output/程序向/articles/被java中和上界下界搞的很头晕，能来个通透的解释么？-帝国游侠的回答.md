---
id: "37542771130"
title: "被java中<? extends T>和<? super T>上界下界搞的很头晕，能来个通透的解释么？"
author: "帝国游侠"
type: zhihu-answer
source: "https://www.zhihu.com/question/4685225699/answer/37542771130"
created: "2024-11-22 01:50"
updated: "2024-11-22 01:50"
collected: "2024-11-22 01:50"
downloaded: "2026-08-16"
---
不知道你哪方面头晕，简单讲讲

<? extends T>：？扩展了T，所以？是T的子类，这里没问题吧？

假设有List<? extends T> list1，T1和T2都是T的子类

那么这个list1到底表示什么呢？或者说list1有什么特性？

A、list1可以同时装入T1和T2的实例

B、list1要么是List<T1>、要么是List<T2>，不可能同时装入T1和T2的实例（这里忽略正好是List<T>本身的情况）

正确答案是B（很狗吧？）

不要问为什么，问就是“就这么定义的”（狗头）

好了，那么这个list1可能是List<T1>、也可能是List<T2>，那么在不能确定的情况下、为了保证类型安全，肯定不能往里面add东西了，强行add编译器会报错的。

有一个例外，就是null可以add进去

list1只能做get、forEach等读取操作，而且get、forEach出来的元素类型是T，因为不管是T1还是T2，都可以用T来引用，这没问题吧？

* * *

好了，聪明如你肯定能想到了，既然List<? extends T>不能写入、只能读取，那么List<? super T>就是正好反过来：只能写入、不能读取呢？

只能说基本正确吧

假设R和S都是T的父类，List<? super T>可能是List<R>、也可能是List<S>，但不确定

所以，你可以放心往里面放T的子类T1和T2，因为不管是T1还是T2，都是R和S的子类

但是你说读取嘛，因为不确定里面的元素到底是t1、还是t2，也有可能是r或s（当然t本身也是可能的），甚至是R再往上的父类，所以读取的时候，只能保险点、读取出Object了

* * *

《Java Effective》这本书对上述特性有个缩写是：PECS（发音类似pigs）

Producer Extends, Consumer Super

生产者（可以读取出来，所以叫生产者），就用 ? extends T

消费者（消费T的，意味着要吃进T），就用 ? super T

不过我个人更喜欢另外一个记忆方法：

我们日常生活中有个很常见的单词Exit，几乎在所有的大厦、地铁等室内空间都能看到

Exit是出去的意思，exit和extends比较接近，所以用extends的时候表示只能出去（读出去）

super，首字母s想到“塞进去”，所以用super的时候表示只能往里放（当然也能读，但读出来就是Object了）