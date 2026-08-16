---
id: "1505609987"
title: "既然 GraalVM 支持多语言且能 AOT 编译 Java，它能否用来 AOT 编译 TS？"
author: "圆胖肿"
type: zhihu-answer
source: "https://www.zhihu.com/question/423945328/answer/1505609987"
created: "2020-10-03 20:49"
updated: "2020-10-03 21:02"
collected: "2020-10-03 20:49"
downloaded: "2026-08-16"
---
理论上什么都可以编译成native

但是graal并不官方支持typescript，目前支持的是javascript，which向java买了版权，js里面的java就是那个java，而不是很多人嘴里说的跟java毫无关系，js当然跟java有很深的关系，不仅有，而且js的版权也在oracle手里[^1]，现在oracle就是打算把js做成java的script，js的很多改版都变得越来越像java，比如加上class

java并不需要graal就能做aot编译，openjdk里面就有jaotc，虽然最初技术来自graal项目

graal做的是native image，而不仅是aot，是把整个runtime做了剪裁，把相关联的部分全部给放到一起，做成image

> GraalVM Native Image allows to ahead-of-time compile Java code to a standalone executable, called a **native image**. This executable includes the application classes, classes from its dependencies, runtime library classes from JDK and statically linked native code from JDK.

而且这个需要把依赖也给塞进去，那这个就比较麻烦了

最早graal出来的时候，glavo就试了下，发现javafx编译不过，于是就过去提了一个issue，说编译不过，然后引起重视，然后用了两年多时间，在graal和javafx两个组的努力下，今年九月才刚刚把javafx编译成native，算是一个小进步，但是这一个小进步，付出的代价真的不少，整整两年时间，我看johan vos就在忙这个了

现在可以用maven项目来直接编译生成win，安卓和ios上的app了，native image，这是start页面，我们群里几个小伙伴都成功做出了win上，安卓上还有iOS上的native image/app，而且还不支持交叉编译，你要编译安卓app，目前还只能用linux

[Gluon Start](https://link.zhihu.com/?target=https%3A//start.gluon.io/)

js那个就比较诡异了，因为js的依赖比较麻烦，如果只是看后端用的npm，那还好说

但是有很多npm是前端用的，依赖的是浏览器上下文，那样你要是想用这些东西，那就需要把整个浏览器也给拆了，或者是干脆把整个浏览器塞入你的应用

你确定要这么做？这是我之前在群里问latte的问题

![](images/305_001.jpg)

latte写的vproxy已经用上了graal做native image，还有jlink那些

讲真，你要是把整个浏览器塞进去，你还不如换个语言呢，这一点看dart和swift做的，尤其是dart/flutter做的那样，恐怕那才是app的正途，虽然理论上你也可以在里面塞入一个webview，怎样怎样，但是gui开发有那么难？

让程序员换个语言开发比你去拼命优化浏览器上下文的依赖要容易得多

从当前的进度看，下一个能够被native image的应该是python，因为scipy和numpy这些没依赖浏览器的，所以要native image的话，相对会简单一点

用的话，现在应该都可以尝试，当然会有一大堆问题，而且并不是所有问题都有人会去解决，就像vert.x的多语言，总有人说，为什么没有vertx-lang-python，但是每次都是说到：有谁愿意贡献啊？就都没声音了，所以这就是搞笑的点，伸手党很多，有能力去贡献的比较少，真正愿意投入去贡献的，就更少了

绝大多数人只是看个热闹，所以这事很容易就不了了之

这一点上看，javafx用了两年时间，用graal把gui（javafx）的native iamge给做了出来，相当不容易，相比之下awt还不行，awt不行swing也就不行[^2]，所以java也还有一小部分不支持native image，其他的就更要慢慢等了

当然，话说回来，你有本事，你应该去贡献

![](images/305_002.png)

[^1]: "JavaScript" is a trademark of Oracle Corporation in the United States https://tsdr.uspto.gov/#caseNumber=75026640&caseType=SERIAL_NO&searchType=statusSearch
[^2]: [native-image] Windows with a swing application #1327 https://github.com/oracle/graal/issues/1327