---
Title: "intellj 入门使用小结  project structure"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags:
  - "blog"
Created: "2017-07-29T19:32:32+08:00"
Cover: ""
WizGuid: "5572c49f-47a7-46bb-a5ec-f112f45314b1"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "f877aab5cb742f3b2b7a1a09af859d86"
Modified: "2017-07-30T00:22:23+08:00"
WizSyncedAt: "2026-07-21T17:35:17+08:00"
---

参考

[http://www.cnblogs.com/JMLiu/p/6020959.html](http://www.cnblogs.com/JMLiu/p/6020959.html)

[http://www.cnblogs.com/zadomn0920/p/6196962.html](http://www.cnblogs.com/zadomn0920/p/6196962.html)

# project structure（项目结构）说明

左侧面板

![[attachments/bd55cbaa-bb29-4dd3-8293-f66ddb60f5a0.png]]

在说明如何填写之前，先说说这些项都代表什么，包含Project、module、library、artficat和facet。project就是这个工程，下面有很多module。

这里project和module的关系类似于Visual Studio中的解决方案和项目之间的关系，project对应于解决方案，module对应于项目（没错，就是这样，project就是顶层，不要看英文翻译）。library就是要包含的library，这个有点像VS里的程序集的概念。artifact是打包用的，这是maven里的概念，就是这个资源包含了哪些内容，当用package时，生成相应的jar或war，用instal(maven里用于发布资源)时，这个包会连同其它必要的文件（如.pom文件），最后放在repository（maven的仓库）中。facet是为了确认信息，比如源码在哪里放、相关资源（图形等）在哪里放、java web程序的root路径等等。

使用基于IntelliJ的IDE，都会对project和module的关系比较糊涂。用简单的一句话来概括是：

IntelliJ系中的Project相当于Eclipse系中的workspace。

IntelliJ系中的Module相当于Eclipse系中的Project。

IntelliJ中一个Project可以包括多个Module

Eclipse中一个Workspace可以包括多个Project

![[attachments/fa94a7b5-dc56-4deb-8edb-5ccd10ef698e.png]]

公司项目一般是一个parent统领若干module，parent 统一项目自身版本、依赖版本、插件版本等，module对应不同服务，可作为数据存取服务、service服务、api服务、restful服务、客户端服务等。在Intellij idea 中，一个project对应一个eclipse workspace，每个eclipse 窗口对应一个workspace，对比得知：intellij idea 中一个project 对应一个窗口。

Intellj idea 中的global library集中管理，避免各个module中相同的lib冗余。

## 1.project

![[attachments/7528ef28-86a1-43aa-a700-a240034412e8.png]]

## 2.Modules

![[attachments/0.9082557444238761.png]]

### Sources面板

![[attachments/0.0755794845144453.png]]

### Paths面板

![[attachments/0.7731202812412061.png]]

### dependencies面板

![[attachments/0.5304273870350777.png]]

## Libraries

这里时全局jar管理 可以给jar分组

![[attachments/0.7539709977645848.png]]

![[attachments/0.832893208280808.png]]

![[attachments/0.43374390627791337.png]]

## Facets

![[attachments/0.22565223692530045.png]]

## artifacts

![[attachments/0.7078010558215246.png]]

##
