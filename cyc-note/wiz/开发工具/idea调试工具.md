---
Title: "idea调试工具"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2022-03-19T15:21:38+08:00"
Cover: ""
WizGuid: "1f15788f-c842-4e37-bdc0-2bbb993fc387"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "05023431cecc477f9bab9e205d1d8371"
Modified: "2022-04-28T17:24:45+08:00"
WizSyncedAt: "2026-07-21T17:35:17+08:00"
---

断点

## 2.断点类型与设置

#### **行断点（line breakpoints)**

在到达设置断点的代码行时暂停程序。这种类型的断点可以设置在任何可执行的代码行上。该类型断点的图标：

![[attachments/b348c010-fd70-40f4-80f6-de328f22884d.jpg]]

#### **字段断点（field breakpoints）**

当指定的字段被读取或写入时暂停程序。这允许你对与特定实例变量的交互作出反应。例如，如果

在一个复杂的过程结束时，你的某个字段出现了明显的错误值，设置一个字段观察点可能有助于确

定故障的来源。该类型断点的图标：

![[attachments/1fa8a152-8cbb-42fd-aeb4-f2a9a98a8b87.png]]

鼠标右键点击该断点图标 ，弹出该断点配置，会有Field access和Field modification选项，此选项是字段类型断点特有的，分别对应访问该字段或修改该字段触发断点，两项同时选中，则访问与修改该字段都会触发断点。

![[attachments/8b65b833-8c21-4567-a1d4-3a393df6873a.png]]

#### **方法断点（method breakpoints）**

在进入或退出指定的方法或其实现之一时暂停程序，允许你检查该方法的进入/退出条件。

该类型断点的图标： ![[attachments/bcf80f63-6523-4a10-bf6a-06bd69dd52d1.png]]

![[attachments/7079eeba-9437-4c25-a40a-44bbececb2ee.png]]

当断点加在class类名这一行，且该类中没有编写构造函数（只有默认无参构造函数），当调用默认

无参构造函数时会触发此断点，程序挂起，故该断点虽然图标是行断点类型图标，但实际上属于方

法类型断点。

![[attachments/c2a5f861-3497-44db-a3f5-5f4d2fb6b7bf.png]]

-鼠标右键点击该断点图标 ，弹出该断点配置，会有Emulated、Method entry、Method exit选项，此选项是方法类型断点特有的。Emulated

勾选中，会将方法断点优化成方法中第一条和最后一条语句的行断点，这样会优化调试的性能，因此在IDE中会默认选中，

-通过匹配符批量添加方法断点，在断点列表页

![[attachments/18356c0b-ff00-4102-b10c-7d0fa48afede.png]]

![[attachments/94d9236b-d357-4a08-b130-a839f6359930.png]]

#### 异常断点（Exception breakpoints）

- 异常断点分为两种，一种是Any Exception，任意Throwable异常被捕获或未被捕获就会触发断点，另一种是指定类型的异常及其该异常子类被捕获或未被捕获会触发断点，该类型断点图标   ![[attachments/21bb33cc-8764-4e54-96a8-9c8c50368f89.png]]

- 鼠标右键点击该断点图标 ，弹出该断点配置，会有Caught exception和Uncaught exception选项，此选项是字段类型断点特有的，Caught exception选项选中时，当指定的异常被捕获时，触发断点程序挂起，Uncaught exception选中时，当指定的异常未被捕获时，触发断点程序挂起

## ![[attachments/d8fc6f1e-f162-4250-9b67-7c2ab275c322.png]]

## 断点属性配置

打开配置窗口的方式

方式1 鼠标操作：右键断点：More(Ctrl+Shift+F8)

![[attachments/6b937020-3d76-4bc0-b473-5568f3dbb070.png]]

方式2 快捷键：Ctrl+Shift+F8

方式3 快捷键：光标所在行 Alt+Enter

![[attachments/2291b93f-8267-447a-9fdd-f936fc5853b7.png]]

#### Enabled

表示是否启用该断点，选中表示启用，取消选中表示不启用。

#### Supend

- 当断点的 Suppend 属性被勾选，触发该断点时，会触发程序挂起，当该属性未选中时，程序触发该断点时，程序不会挂起，常用于输出一些表达式结果日志。
- 当断点的 All 属性被勾选，触发该断点时，会挂起所有线程
- 当断点的 Thead 属性被勾选，触发该断点时，只会挂起触发该断点的那个线程，不影响其他线程 .实际生产实践中，可用于调试多线程并发的问题

当需要在不暂停程序的情况下记录一些表达式时（例如，需要知道一个方法被调用了多少次时），或者需要创建一个主断点，在击中后启用附属断点时，非暂停性断点是非常有用的。(Suppend 属性 不被勾选的情况)

#### Condition

- 可以输入一段能获得true或false的表达式，程序运行到断点处，且表达式条件为true才会触发断点

#### Log

下面三个属性选项经常配合 Suppend 属性一起使用，用于在不挂起的情况下，输出一些想要的日志信息

- Breakpint hit message ：控制台输出触发端点的日志信息，类似如： Breakpoint reached at ocean.Whale.main(Whale.java:5)
- Stack trace ：输出触发断点时的堆栈信息
- Evaluate and log ：计算表达式结果并输出表达式结果到控制台，表达式的计算基于断点所在行的上下文，表达式的语句可以是字符串字面量，如 "我是字符串" ,也可以是方法调用，如users.size() ，也可以是多行语句块，表达式的结果取自return语句，如果没有return语句，会取表达式中的最后一行语句。

![[attachments/3bafa75a-a9b4-4242-8249-79e153c311c7.png]]

#### Remove once hit

是否在断点触发后移除该断点. 在管理面板中移除,需要重新设置断点

#### Disable until hitting the following breakpoint

指定在另一个断点触发后，该断点才启用，若该断点启用后，并且被触发，触发后是否继续启用由Disable again和Leave enabled指定，Disable again表示触发后不再启用,后面不会触发,例如在循环中，

Leave enabled表示触发后继续启用。

场景：当只需要在某些条件下或某些操作后暂停程序时，这个选项很有用。在这种情况下，触发断点通常不需要停止程序的执行，而是做成非暂停状态。

#### Filters

前边说的大都数属性，都只针对方法程序运行上下文。此属性更多关注通过过滤掉类、实例和调用者方法来微调断点操作，只在需要时暂停程序。，有如下几种过滤方式：

- Catch class filters ：此选项只对异常类型的断点可用，可以让程序只在指定类和子类中抛出的异常才会触发断点或者不在指定的类和子类中触发断点（即排除一些类，排除通常以 - 开始，例如 -pacakge.ClassName ），
- Instance filters ：只有指定实例id号可以触发断点，多个实例id号以逗号隔开，实例id号可以在Variables和Memory面板中查看
- Class filters ：可以让程序只在指定类和子类中才会触发断点或者不在指定的类和子类中触发断点（即排除一些类）。例如:断点设置在父类指定子类才进入断点
- Caller filters ：根据调用者来进行过滤，需指定方法的全限定名（包含方法签名），例如mypackage.MyObject.addString(Ljava/lang/String;)V

![[attachments/f5e429a0-202b-47ce-9e82-7c02cea65d85.png]]

#### Pass count

- 勾选中并输入一个正整数N，N>=1，那么程序会每N次命中断点才会触发挂起，如果同时设置了condition 与 pass count 属性，ide会优先判断 condition 表达式，再判断 pass count 是否满足，下例中， pass count 中传入的是15，每15次命中断点才会触发断点(例如第15次,第30次....)，挂起程序

![[attachments/2adaa087-1b73-4213-af05-ac93b22f67ad.png]]

## 5.断点状态

![[attachments/05c3d3b2-ea7a-4ab9-9c38-43ddf9cf66d7.png]]

![[attachments/901dcdd1-9e41-4430-a1d5-a1ea27b26bff.png]]

## 9.生产力建议

**#### 使用断点进行 "printf "调试**

使用非暂停的日志断点，而不是在代码中插入打印语句。这为处理调试日志信息提供了一种更灵活和集中的方式。

场景：所有需要打印的地方. 如果生产上禁止 System.out.print();就可以使用这种方式减少不合规的代码

#### 调试无响应的应用程序

如果你的应用程序挂起，暂停会话，让调试器获得关于其当前状态的信息。然后你可以检查程序的状态并找出问题的原因。

场景：项目启动卡死等处理

#### 计算保留的大小

对于每个类的实例，你可以计算它的保留大小。保留大小是指对象本身和它所引用的所有对象以及没有被其他对象引用的对象所占据的内存量。

这在估算重型单体或从磁盘上读取的数据（例如，复杂的JSON）的内存占用时，可能很有用。另外，在决定使用哪种数据结构时（例如，ArrayList与LinkedList），这也很有用。

在运行应用程序之前，确保在设置/首选项|构建、执行、部署|调试器中启用附加内存代理选项。

在查看类的实例时，右键单击一个实例并单击计算保留大小。

![[attachments/8332d464-a762-4627-82da-f20205701f75.png]]

![[attachments/5620d0e6-6fb6-49cb-85e3-9d10c93e5762.png]]

----

## debug技巧

drop frame

作用 丢弃当前方法的栈帧 返回上一个方法 (java每次方法调用丢失会创建栈帧)

![[attachments/450b67a2-363d-468e-9bce-b06ec9f00d03.png]]

run to cursor

作用程序处于断点调试时 可以让程序一口气执行到指定行 而不是一行一行的执行

指定行(光标所在的行,或者直接在目标行右键执行run to cursor  )

![[attachments/cd71201f-adf7-450a-815f-85be989a89a6.png]]
