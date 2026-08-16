---
id: "1936965432"
title: "MySQL已经可以干大部分事情了，还有必要使用商业数据库或者PostgreSQL吗？"
author: "木风"
type: zhihu-answer
source: "https://www.zhihu.com/question/21793412/answer/1936965432"
created: "2021-06-12 20:12"
updated: "2021-06-12 20:23"
collected: "2021-06-12 20:12"
downloaded: "2026-08-16"
---
前阿里员工可以很负责的说一句，去IOE的事迹内部宣传很多次了，就是为了省钱，仅此而已。如果Oracle免费，你看互联网大厂会用MySql还是Oracle？

不管是性能，架构，对SQL标准的支持度，还是代码质量，Oracle，pgsql 都是甩MySql 好几条街的。

互联网的特点是业务逻辑简单，但是并发量大，那么养一个牛逼的中间件团队做好横向扩容就行了，同时尽量不使用复杂和嵌套的sql。某种程度上讲，已经在NoSql化了，比如为了提高读性能进行的各种denormalization。

至于pgsql能做而mysql不能做的，有很多，随便说一个：条件索引。

再次编辑，再说一个，一条插入语句插入n行数据，并返回所有插入行的主键，用mysql自增主键生成器，怎么做？做不到的。

再加一条，将非主键索引建为 clustered index，mysql压根都不支持。

我差不多在10几秒内就能想到这么多mysql没法做的事情，怎么会叫mysql都能支持呢。