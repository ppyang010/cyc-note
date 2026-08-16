---
id: "1711335242"
title: "我专业是软件工程，大二学校教的是java 2，但是现在不是都更新到java 14了吗？这没问题吗？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/419822191/answer/1711335242"
created: "2021-02-02 17:08"
updated: "2021-02-02 17:08"
collected: "2021-02-02 17:08"
downloaded: "2026-08-16"
---
你说的是这本吧？

[《Java 2实用教程（第5版）/高等学校Java课程系列教材》(耿祥义，张跃平)【摘要 书评 试读】- 京东图书](https://link.zhihu.com/?target=https%3A//item.jd.com/12179826.html)

我看了一下目录，其实不是java 2，里面用的jdk版本是5

5也的确有些太古老了，看了下出版时间，是2017年，2017年也不应该用5，5是2004年左右出来的，离现在都17年了……

不过这也多少能够理解，计算机技术的发展，会比教材发展的速度要快一点

那我们来看看，如何解决这个问题

基于5之后，你需要补充以下内容

1）java 8的lambda，用得非常多，无论如何要吸收进去，习惯用lambda，否则这么简单的特性看不懂就完蛋了，java的lambda还算是比较简单了，其他语言的多多少少都比java要复杂一点

2）java 9的jigsaw，模块化，学会拆装java的runtime，定制运行时，这个很重要，以后也会用得越来越多，目前已经有爆发的势头，我跟好几个开源的java库的作者建议过这个功能，尤其是native库，就是写c之类的库的作者

3）学会javafx，我看里面有说到组件，那多半是swing，swing真的已经快不用了，官方那个java主要开发负责人马克也说，将来会交给javafx，而不是swing，如果可以的话，作业想办法用javafx做

4）学会graal，这个跟前两个相辅相成，graal和jmod（jigsaw，javafx）等经常一起出现，还会被用在后端的aot编译上，学会用graal，而不仅仅是openjdk，graal应该是过去十年，java最重要的项目，包括james gosling本人，都在twitter上对graal，javafx等技术大加赞赏

5）其他语法上的差异可以看看project amber，因为这个对于写法有改变，比如var，yield，都开始出现在java源码中，这些特性难倒是不难，但是你得会，还有马上要来的record，sealed

6）多线程部分其实可以看看vert.x，但是这一块倒是不用太着急，因为大部分公司还在用spring，只是从国外反馈的趋势看，至少quarkus已经开始进入市场，而vert.x在aws上的使用率也在逐渐上升，vert.x特别适合创业公司，vert.x+flutter，一个人就可以把产品给搞出来，特别方便，但是这个你可以等到你创业的时候再来考虑，core java阶段可以先不了解vert.x这些

7）学会用idea，maven这些，idea自带有maven，不过这个应该是基操了，大部分公司都会了