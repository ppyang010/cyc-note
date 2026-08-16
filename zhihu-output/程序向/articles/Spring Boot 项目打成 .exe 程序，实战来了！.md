---
id: "666687158"
title: "Spring Boot 项目打成 .exe 程序，实战来了！"
author: "代码小咖"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/666687158"
created: "2023-11-14 08:21"
updated: "2023-11-14 08:21"
collected: "2023-11-14 08:21"
downloaded: "2026-08-16"
---
近期做了一个前后端合并的spring boot项目，但是要求达成exe文件，提供给不懂电脑的小白安装使用，就去研究了半天，踩了很多坑，写这篇文章，是想看到这篇文章的人，按照我的步骤走，能少踩坑。

  

**准备**

  

准备工作：

-   一个jar包，没有bug能正常启动的jar包
-   exe4j，一个将jar转换成exe的工具
-   inno setup，一个将依赖和exe一起打成一个安装程序的工具

  

**开始**

  

以我为例子，我将jar包放在了桌面

  

![](images/337_001.png)

  

打开安装好的exe4j

![](images/337_002.jpg)

直接下一步进入界面，选择JAVA转EXE

![](images/337_002.jpg)

然后点下一步，输入名称和输出路径

![](images/337_003.jpg)

继续点击下一步，选择启动模式

![](images/337_004.jpg)

下方有个选项，需要设置打包后的程序兼容32和64位系统

  

![](images/337_005.jpg)

  

进来后勾选上

  

![](images/337_006.jpg)

  

然后一直下一步，一直出现如下界面，开始选择jar包以及配置

在VM参数配置的地方加上：-Dfile.encoding=utf-8

  

![](images/337_007.jpg)

  

  

![](images/337_008.jpg)

  

  

![](images/337_009.jpg)

  

  

![](images/337_010.jpg)

  

点击下一步，配置JRE

  

![](images/337_011.jpg)

  

下拉框点击后进入如下界面

![](images/337_012.jpg)![](images/337_013.jpg)

照着这个样子写的目的是，最终会把本地jre目录和exe一起打包，让exe文件自己去根据路径去查找一起打包的jre，可不用再安装jdk

  

![](images/337_014.jpg)

接着下一步，选择Client VM

  

  

![](images/337_015.jpg)

  

然后一直下一步，最终出现如下界面

  

![](images/337_016.jpg)

  

这个时候你会发现桌面多了一个demo.exe文件，这个时候先别着急点开，接下来就是将jre和exe文件再打个包合并，达到在没有jdk电脑环境下也能运行。

打开inno setup，左上角File - New

  

![](images/337_017.jpg)

  

直接点下一步，填写配置，应用名称，版本等，随意

  

![](images/337_018.jpg)

  

然后点击下一步，这个地方默认就行，直接下一步

  

![](images/337_019.jpg)

  

接着选择生成好的exe文件

  

![](images/337_020.jpg)

  

然后下一步，进入这个界面保持默认，直接下一步

![](images/337_021.jpg)

依旧下一步，不用管

![](images/337_022.jpg)

继续下一步，这里是选择语言

  

![](images/337_023.jpg)

  

然后就是选择输出路径和填写安装程序的名字了

![](images/337_024.jpg)

然后下一步，直接点Next，然后结束.

配置到最后一步了，脚本文件，到这里会弹出问你是否马上编译，选择否，先把脚本写好再自己编译：

![](images/337_025.jpg)

然后到了最后一步了，把本地的JRE写进脚本

![](images/337_026.jpg)![图片](images/337_027.jpg)![](images/337_027.jpg)

Source: "自己本地JRE路径\*"; DestDir: "{app}{#MyJreName}"; Flags: ignoreversion recursesubdirs createallsubdirs

然后直接编译就好了，会提示保存当前脚本，随便起个名字，下个还可以继续用

![](images/337_028.jpg)![](images/337_029.jpg)

然后等待绿色滚动条结束

![](images/337_030.jpg)

当绿色滚动条结束后，桌面会多了一个setup.exe文件

![](images/337_031.jpg)

也同时会跳出一个安装的，因为程序帮你自动启动生成的安装程序了，安装就可以了，安装的时候记得勾选创建快捷方式

![](images/337_029.jpg)

这个就是最后的程序了，双击运行就可以看到结果了，把setup.exe文件给别人安装，就都可以看到自己的程序了！