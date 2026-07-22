---
Title: "Itellij idea 插件"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-07-28 20:04:41"
Cover: ""
WizGuid: "a1a3fdb6-899d-4c53-b2c0-ca0ba9a96866"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "cf3be2f18bc1d883c82d68602a4dd914"
Modified: "2020-04-20 10:41:39"
WizSyncedAt: "2026-07-21 17:35:17"
---

ignore   gitignore编写插件   [http://blog.csdn.net/qq_34590097/article/details/56284935](http://blog.csdn.net/qq_34590097/article/details/56284935)

Key promoter  （快捷键提示插件）     [https://plugins.jetbrains.com/plugin/4455-key-promoter](https://plugins.jetbrains.com/plugin/4455-key-promoter)

bashsupport  shell文件执行

Rainbow Brackets   彩色 括号

RESTfultoolkit

一套 RESTful 服务开发辅助工具集。

1.根据 URL 直接跳转到对应的方法定义 ( Ctrl \ or Ctrl Alt N );

maven-helper

maven 扩展

gsonformat

FindBugs

alibaba-java-coding-guidelines

阿里巴巴代码规约

Lombok

IntelliJ IDEA提供了CamelCase很方便的工具插件，使用快捷键shift+alt+u。

按住shift+alt再不停的按U,会把选中内容的单词的下划线转驼峰转大写等，不停的转换，直到你想要的。

[https://zhuanlan.zhihu.com/p/99354824](https://zhuanlan.zhihu.com/p/99354824)

## 2.2 jclasslib bytecode viewer

下面要隆重介绍的是一款可视化的字节码查看插件：[jclasslib](https://link.zhihu.com/?target=https%3A//plugins.jetbrains.com/plugin/9248-jclasslib-bytecode-viewer) 。

大家可以直接在 IDEA 插件管理中安装（安装步骤略）。

[https://plugins.jetbrains.com/plugin/9248-jclasslib-bytecode-viewer](https://plugins.jetbrains.com/plugin/9248-jclasslib-bytecode-viewer)

**使用方法**：

1. 在 IDEA 打开想研究的类。
2. 编译该类或者直接编译整个项目（ 如果想研究的类在 jar 包中，此步可略过）。
3. 打开“view” 菜单，选择“Show Bytecode With jclasslib” 选项。
4. 选择上述菜单项后 IDEA 中会弹出 jclasslib 工具窗口。
![[attachments/931d1ef0-ae4f-4b6c-b0b4-a4f03cfd7d88.jpg]]

那么有自带的强大的反汇编工具 javap 还有必要用这个插件吗？

这个插件的**强大之处**在于：

1. 不需要敲命令，简单直接，在右侧方便和源代码进行对比学习。
2. 字节码命令支持超链接，**点击其中的虚拟机指令即可跳转到 jvms 相关章节**，超级方便。

该插件对我们学习虚拟机指令有极大的帮助。

详细安装和介绍参考另外一篇手记：[https://www.imooc.com/article/296257](https://link.zhihu.com/?target=https%3A//www.imooc.com/article/296257)

## 2.3 Codota

另外一个不得不说的就是专栏中提到的辅助开发神器: [Codota](https://link.zhihu.com/?target=https%3A//www.codota.com/code)。

可以点击下图所示“Add Codota to you IDEA” 了解安装步骤。

![[attachments/dfe6caf2-307c-4059-8aae-bf658276ee52.jpg]]

该插件的强大之处在于：

1. 支持智能代码自动提示，该功能可以增强 IDEA 的代码提示功能。
2. 支持 JDK 和知名第三方库的函数的使用方法搜索，可以看到其他知名开源项目对该函数的用法。

当我们第一次使用某个类，对某个函数不够熟悉时，可以通过该插件搜索相关用法，快速模仿学习。

![[attachments/81d1d9ad-bd12-48f6-82f4-fca30f931f45.jpg]]

如上图所示，我们想了解 `Stream` 类中 `flatMap` 函数的用法，可以使用该插件查看知名开源项目的用法。

插件窗口顶部还给出了该类最常用的函数，可以点击查看相关用法案例，每个案例右侧的 "view source"可以跳转到该片段对应的开源项目的源码中。

## 2.4 Auto filling Java call arguments

开发中，我们通常会调用其他已经编写好的函数，调用后需要填充参数，但是绝大多数情况下，传入的变量名称和该函数的参数名一致，当参数较多时，手动单个填充参数非常浪费时间。

该插件就可以帮你解决这个问题。

安装完该插件以后，调用一个函数，使用 Alt+Enter 组合键，调出 "Auto fill call parameters" 自动使用该函数定义的参数名填充。

## 2.5 GenerateO2O、**GenerateAllSetter**

我们定义好从 A 类转换到 B 类的函数转换函数后，使用这两个插件可以自动调用 Getter 和 Setter 函数实行自动转换。

实际开发中还有一个非常常见的场景： 我们创建一个对象后，想依次调用 Setter 函数对属性赋值，如果属性较多很容易遗漏或者重复。

![[attachments/15512c73-f728-4790-911d-c233f69db57f.jpg]]

可以使用这 GenerateAllSetter 提供的功能，自动调用所有 Setter 函数（可填充默认值），然后自己再跟进实际需求设置属性值。

## 2.10 SequenceDiagram

[SequenceDiagram](https://link.zhihu.com/?target=https%3A//plugins.jetbrains.com/plugin/8286-sequencediagram/)可以根据代码调用链路自动生成时序图，超级赞，超级推荐！

这对研究源码，梳理工作中的业务代码有极大的帮助，堪称神器。

安装完成后，在某个类的某个函数中，右键 --> Sequence Diagaram 即可调出。

如下图是 Netty 的源码，可以通过该插件绘制出当前函数的调用链路。

![[attachments/7c68f2bb-c008-4720-91d0-9b659cb076e6.jpg]]

双击顶部的类名可以跳转到对应类的源码中，双击调用的函数名可以直接调入某个函数的源码，总之非常强大。

## 2.11 Stack trace to UML

[Stack trace to UML](https://link.zhihu.com/?target=https%3A//plugins.jetbrains.com/plugin/10749-stack-trace-to-uml/) 支持根据 JVM 异常堆栈画 UML时序图和通信图。

打开方式 *Analyze > Open Stack trace to UML plugin* + Generate UML diagrams from stacktrace from debug

![[attachments/99ac3566-bbdd-46a6-876f-4591257c0b71.jpg]]

## 2.12 Java Stream Debugger

Stream 非常好用，可以灵活对数据进行操作，但是对很多刚接触的人来说，不好理解。

那么 [Java Stream Debugger](https://link.zhihu.com/?target=https%3A//plugins.jetbrains.com/plugin/9696-java-stream-debugger/) 这款神器的 IDEA 就可以帮到你。它可以将 Stream 的操作步骤可视化，非常有助于我们的学习。

![[attachments/93ad2924-81bd-48ed-9ab7-c969a961942e.jpg]]![[attachments/f8478f94-a52a-4825-b840-eb2ff82a4401.jpg]]

## 2.13 JOL Java Object Layout

[https://plugins.jetbrains.com/plugin/10953-jol-java-object-layout](https://link.zhihu.com/?target=https%3A//plugins.jetbrains.com/plugin/10953-jol-java-object-layout)

查看对象布局和大小的插件，非常赞。

![[attachments/593aa509-070e-454a-b55b-bfcbb58f1c69.jpg]]

### 3.9 Git Commit Template

老是有人吐槽你提交的 **Git** 不规范？你可以试试这个插件。它提供了很好的 **Git** 格式化模版，你可以按照实际情况格式化你的提交信息。

![[attachments/a9eb00bb-8fa5-4195-a017-94985db98d32]]
GitToolBox
[https://plugins.jetbrains.com/plugin/7499-gittoolbox](https://plugins.jetbrains.com/plugin/7499-gittoolbox)

![[attachments/38443308.png]]
