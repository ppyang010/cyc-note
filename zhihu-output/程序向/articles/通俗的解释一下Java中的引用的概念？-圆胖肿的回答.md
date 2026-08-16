---
id: "3386251139"
title: "通俗的解释一下Java中的引用的概念？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/55323413/answer/3386251139"
created: "2024-02-03 22:44"
updated: "2024-02-03 22:47"
collected: "2024-02-03 22:44"
downloaded: "2026-08-16"
---
嗯，今天有人说起引用，我突然想到了这个说法

这个说法是非常misleading，误导的

而且非常不利于理解

确切地说，java里面的应该是引用类型，reference type，而非引用

引用这个词汇应该被彻底废弃，因为非常不利于理解，而且很误导

我给个更加直观的说法，用官方的文档来解释

因为java正在做值类型，所以它要区分引用类型和值类型

以下内容截取自官方的jeps，也就是java enhanced proposal，java增强提案[^1]

In Java, every object that is created is given a unique identity, distinguishing it from any other object in the system. The `Object.toString` method hints at this unique identity, and the `==` operator compares objects by their identities, as illustrated in JShell:

```text
jshell> new Object()
$1 ==> java.lang.Object@b1bc7ed

jshell> new Object()
$2 ==> java.lang.Object@30dae81

jshell> new Object() == new Object()
$3 ==> false
```

翻译一下，就是说 java 对于每一个生成的对象，都会赋予一个id，就是唯一标识，这个id跟你在数据库表设计中的那个id是一个意思，id是identity的缩写，identity翻译过来，就是身份，但是这个说法有点模糊，更确切地说就是唯一标识的意思，国内每个人都有身份证，就是id证，我们身份证号，就是我们的id，一人一号，到了国外，鬼佬说，出示你的id，那你就可以用护照，驾照等证件来展示你的id

这个id不能直接通过方法获取，但是你可以用缺省的tostring方法，拿到对象的类型（class）和id组合的字符串，上面那个new object之后，jshell给出了tostring的结果

java.lang.Object@b1bc7ed

@前面是对象的类型，后面就是它的id了，也就是b1bc7ed

实际上 java 里面 == 比较的，就是这个 id

这个 id 一样，就一样，不一样，就不一样

但是注意，这个id，只有reference type，引用类型才有，值类型，== 就是 equals，比较的是值是否相等，引用类型才比较这个 id 是否一样

所以之前的很多说法，估计就是根据这个，把 id 说成了引用，值类型比较值，引用类型比较引用，这样显得工整和对仗

但引用有指针指向的地址的意思，一般认为，引用类型，会把heap堆里面的地址，存入stack栈中

所以很多文章会说，比较的是这个引用的地址

其实这个是错的

**id是唯一标识，但其值不是内存地址**

这个用常识判断就行了，因为java对象在heap堆中的地址，是会变的，gc之后，java会移动对象，所以有些对象如果没有被gc掉，它会移动到另外一个地址中去，这个时候，引用的地址就发生了改变

难不成你以为这个时候id也跟着改变了？

当然不是，这个id跟这个对象是绑定的

对象在内存中被移动了，id可不会变，要不然移动一下对象，它就变成另外一个对象，那搞什么

所以你不需要知道什么是引用，你只需要知道

java的对象，有一个id，就行了

所谓的引用，其实说的就是这个id

更确切一点说，应该是java中的引用类型的对象，都有一个id

值得注意的是，java中除了普通类的对象以外，还有值类型，目前的值类型仅仅是原始数据类型那8个，后续等value关键字出来之后，所有被标记为value的class的对象，都是值类型，值类型跟引用类型的区别就在于，值类型没有id

所以值类型的==比较的就是值是否相等，==其实就是equals

但是引用类型的==比较的是id是否相当，而用equals来比较值是否相等，当然缺省的equals就是==，教材上建议你要自己去实现equals比较值是否相等就是这个原因，因为java没给你做这事，当然equals的实现你可以让ide自动帮你生成

[^1]: [1] https://openjdk.org/jeps/401