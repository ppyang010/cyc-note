---
Title: "分布式事务seata分享"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2023-03-09 22:57:12"
Cover: ""
WizGuid: "956afea3-ae50-4627-a66e-43d3ce22fbdb"
WizType: "document"
WizLocation: "/dxy/init/"
WizDataMd5: "5d17eed35502fc39a6f90a0f62231412"
Modified: "2023-03-29 22:19:53"
WizSyncedAt: "2026-07-29 15:36:28"
---

参考资料:

分布式事务中间件 Seata 的设计原理

[https://seata.io/zh-cn/blog/seata-at-mode-design.html](https://seata.io/zh-cn/blog/seata-at-mode-design.html)

再有人问你分布式事务，把这篇扔给他 - 掘金

[https://juejin.cn/post/6844903647197806605#heading-7](https://juejin.cn/post/6844903647197806605#heading-7)

本地事务 | 凤凰架构

[http://icyfenix.cn/architect-perspective/general-architecture/transaction/local.html](http://icyfenix.cn/architect-perspective/general-architecture/transaction/local.html)

什么是XA协议？它跟2PC有什么关系？ - 梯子教程网

[https://www.tizi365.com/question/4830.html](https://www.tizi365.com/question/4830.html)

对比7种分布式事务方案，还是偏爱阿里开源的Seata，真香！(原理+实战)_51CTO博客_分布式事务 阿里开源

[https://blog.51cto.com/zhongmayisheng/5219677](https://blog.51cto.com/zhongmayisheng/5219677)

---

官网博客

分布式事务 Seata 及其三种模式详解

[https://seata.io/zh-cn/blog/seata-at-tcc-saga.html](https://seata.io/zh-cn/blog/seata-at-tcc-saga.html)

分布式事务如何实现？深入解读 Seata 的 XA 模式

[https://seata.io/zh-cn/blog/seata-xa-introduce.html](https://seata.io/zh-cn/blog/seata-xa-introduce.html)

详解 Seata AT 模式事务隔离级别与全局锁设计

[https://seata.io/zh-cn/blog/seata-at-lock.html](https://seata.io/zh-cn/blog/seata-at-lock.html)

---

seata (图解_秒懂_史上最全)_40岁资深老架构师尼恩的博客-CSDN博客

[https://blog.csdn.net/crazymakercircle/article/details/120521772](https://blog.csdn.net/crazymakercircle/article/details/120521772)

分布式事务（ 图解 + 秒懂 + 史上最全 ） - 疯狂创客圈 - 博客园

[https://www.cnblogs.com/crazymakercircle/p/13917517.html#autoid-h3-3-1-4](https://www.cnblogs.com/crazymakercircle/p/13917517.html#autoid-h3-3-1-4)

----

原理分析

深入了解分布式事务组件 Seata ：AT 模式（二） - 腾讯云开发者社区-腾讯云

[https://cloud.tencent.com/developer/article/1553985](https://cloud.tencent.com/developer/article/1553985)

Seata实战-AT模式分布式事务原理、源码分析_hosaos的博客-CSDN博客

[https://blog.csdn.net/hosaos/article/details/89403552](https://blog.csdn.net/hosaos/article/details/89403552)

Seata-AT模式 原理 - 掘金

[https://juejin.cn/post/6969550082152595464#heading-11](https://juejin.cn/post/6969550082152595464#heading-11)

----

全局锁

详解 Seata AT 模式事务隔离级别与全局锁设计 - 腾讯云开发者社区-腾讯云

[https://cloud.tencent.com/developer/article/1928386](https://cloud.tencent.com/developer/article/1928386)

Seata AT模式的全局锁GlobalLock - hongdada - 博客园

[https://www.cnblogs.com/hongdada/p/16796704.html](https://www.cnblogs.com/hongdada/p/16796704.html)

-----

xa tcc 隔离性

干货｜一篇文章带你学习分布式事务-阿里云开发者社区

[https://developer.aliyun.com/article/597305](https://developer.aliyun.com/article/597305)

-------

由Seata看分布式事务取舍_拉丝的裤衩的博客-CSDN博客

[https://blog.csdn.net/qq_31457665/article/details/106128707](https://blog.csdn.net/qq_31457665/article/details/106128707)

从零开始写一个分布式事务框架(一) | 佑祺's Blog

[http://blogxin.cn/2020/02/16/Distributed-Transaction-1/](http://blogxin.cn/2020/02/16/Distributed-Transaction-1/)

-------------

一、

什么是事务ACID，事务隔离级别

什么是分布式事务

为什么要分布式事务

二、

分布式事务主流解决方案介绍AT，XA，TCC，SAGA，（MQ本地消息表）

三、

Seata的架构介绍

四、

seata主推AT模式的大致实现原理解析（带自己的思考与seata的对比）

五(？)、

AT模式脏读问题

-----------------------

1背景介绍 ->演进过程+理论基础

1.1 为什么会有分布式事务

1.2 理论基础 ->

acid ,cap, 一致性,base=

2技术方案调研和对比

XA,2pc,3pc,

事务补偿型(TCC)

异步确保型

最大努力型

框架对比

ByteTCC、TCC-transaction、EasyTransaction,Seata

3核心功能

Seata 是一款开源的分布式事务解决方案，致力于提供高性能和简单易用的分布式事务服务。Seata 将为用户提供了 AT、TCC、SAGA 和 XA 事务模式，为用户打造一站式的分布式解决方案。

4架构原理

AT原理

TCC原理

------

分布式事务发展时间线

cap -> base ->OTP XA 2pc 3pc ->tcc ->saga ->seata AT

2pc 3pc  (XA的是两阶段提交)

XA是一套语言无关的通用规范  ---->

Java 中专门定义了JSR 907 Java Transaction API，基于 XA 模式在 Java 语言中的实现了全局事务处理的标准，这也就是我们现在所熟知的 JTA。JTA 最主要的两个接口是：

事务管理器的接口：javax.transaction.TransactionManager。这套接口是给 Java EE 服务器提供容器事务（由容器自动负责事务管理）使用的，还提供了另外一套javax.transaction.UserTransaction接口，用于通过程序代码手动开启、提交和回滚事务。

满足 XA 规范的资源定义接口：javax.transaction.xa.XAResource，任何资源（JDBC、JMS 等等）如果想要支持 JTA，只要实现 XAResource 接口中的方法即可

但现在Bittronix、Atomikos和JBossTM（以前叫 Arjuna）都以 JAR 包的形式实现了 JTA 的接口

并且需要数据库支持

-----

XA规范定义了一组API，应用程序可以使用这些API来管理分布式事务。

XA规范主要涉及到以下三个角色：

- 应用程序（Application Program）：执行业务逻辑，并发起或参与分布式事务。
- 事务管理器（Transaction Manager）：负责管理分布式事务的整个生命周期，包括事务的提交、回滚和恢复等。
- 资源管理器（Resource Manager）：管理事务处理过程中涉及到的各种资源，如数据库、消息队列等。

在XA规范中，应用程序使用XA API与事务管理器进行交互，而事务管理器使用XA API与各个资源管理器进行交互。XA规范定义了一组标准的接口函数，包括开始全局事务、结束全局事务、提交全局事务、回滚全局事务等。通过这些接口函数，应用程序可以实现分布式事务的提交和回滚，从而保证事务的一致性和可靠性。

总的来说，XA规范为应用程序和数据库提供了一套通用的接口，使得分布式事务处理变得更加容易和可靠。各大数据库厂商都实现了XA规范，因此应用程序可以在不同的数据库系统之间进行无缝的移植。

(应用程序和数据库都需要按照XA规范设计接口)

两段式提交”（2 Phase Commit，2PC）协议  ->追求数据一致性的协议

XA在Java中的实现是JTA

JTA在提交事务的时候为了保证一致性 是通过2pc的方式提交事务的

2pc的使用还有其它地方 例如mysql的日志提交

2pc是追求强一致性的的方案,但是不是所有情况都能保证强一致性  有前提

--

刚性事务和柔性事务

-----

chatgpt

事务（Transaction）指的是数据库管理系统（DBMS）中的一个基本操作单元，它是由一系列的操作语句组成的逻辑单位。事务的目的是将一组相关的数据库操作（例如插入、修改、删除等）视为一个不可分割的整体，保证这些操作要么全部执行成功，要么全部失败回滚。

在执行事务时，DBMS需要遵守ACID原则，即原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）和持久性（Durability）。原子性表示事务中的所有操作要么全部执行成功，要么全部失败回滚；一致性表示事务执行前后数据库中的数据必须符合预设的规则；隔离性表示多个并发执行的事务之间应该相互隔离，互不影响；持久性表示一旦事务提交，所做的更改应该永久保存在数据库中。

事务的使用可以保证数据库操作的正确性和完整性，并且可以避免数据丢失和损坏等问题。事务在企业级应用系统中得到了广泛的应用。

-----

public void buyBook(PaymentBill bill) { userTransaction.begin(); warehouseTransaction.begin(); couponTransaction.begin(); try { userAccountService.pay(bill.getMoney()); warehouseService.deliver(bill.getItems()); couponService.update(bill.getCouponCode()); userTransaction.commit(); warehouseTransaction.commit(); couponTransaction.commit(); } catch(Exception e) { userTransaction.rollback(); warehouseTransaction.rollback(); couponTransaction.rollback(); } }

```
xxxxxxxxxx
```

21

1

```
public void buyBook(PaymentBill bill) {
```

2

```
    userTransaction.begin();
```

3

```
    warehouseTransaction.begin();
```

4

```
    couponTransaction.begin();
```

5

```

```

6

```
    try {
```

7

```
        userAccountService.pay(bill.getMoney());
```

8

```
        warehouseService.deliver(bill.getItems());
```

9

```
        couponService.update(bill.getCouponCode());
```

10

```

```

11

```
        userTransaction.commit();
```

12

```
        warehouseTransaction.commit();
```

13

```
        couponTransaction.commit();
```

14

```
    } catch(Exception e) {
```

15

```
        userTransaction.rollback();
```

16

```
        warehouseTransaction.rollback();
```

17

```
        couponTransaction.rollback();
```

18

```
    }
```

19

```
}
```

20

```

```

21

```

```

---------

Mysql的XA事务分为外部XA和内部XA

外部XA用于跨多MySQL实例的分布式事务，需要应用层作为协调者，通俗的说就是比如我们在PHP中写代码，那么PHP书写的逻辑就是协调者。应用层负责决定提交还是回滚，崩溃时的悬挂事务。MySQL数据库外部XA可以用在分布式数据库代理层，实现对MySQL数据库的分布式事务支持，例如开源的代理工具：网易的DDB，淘宝的TDDL等等。

内部XA事务用于同一实例下跨多引擎事务，由Binlog作为协调者，比如在一个存储引擎提交时，需要将提交信息写入二进制日志，这就是一个分布式内部XA事务，只不过二进制日志的参与者是MySQL本身。Binlog作为内部XA的协调者，在binlog中出现的内部xid，在crash recover时，由binlog负责提交。(这是因为，binlog不进行prepare，只进行commit，因此在binlog中出现的内部xid，一定能够保证其在底层各存储引擎中已经完成prepare)。

-----

分布式系统中通用的问题有哪些

单点问题?

-----

分布式

原子性和持久性那张可以考虑删除

隔离性->最简单就是加锁-->也就是串行化 ->>但是性能问题 所以提供了多种隔离级别->>取平衡

什么是seata

at模式简单使用

at模式原理
