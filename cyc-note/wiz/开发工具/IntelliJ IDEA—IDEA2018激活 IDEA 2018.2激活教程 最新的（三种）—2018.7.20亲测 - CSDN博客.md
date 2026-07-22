---
Title: "IntelliJ IDEA—IDEA2018激活 IDEA 2018.2激活教程 最新的（三种）—2018.7.20亲测 - CSDN博客"
Url: "https://blog.csdn.net/HALEN001/article/details/81137092"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2018-08-29 10:28:52"
Cover: ""
WizGuid: "87bddb27-9ee9-41d1-a329-75d237fe7d67"
WizType: ""
WizLocation: "/开发工具/"
WizDataMd5: "6daf443ad9e0baeaabf9e3ff7c1ab8e9"
Modified: "2018-08-29 10:28:52"
WizSyncedAt: "2026-07-21 17:35:17"
---

版权声明：本文为博主原创文章，未经博主允许不得转载。 https://blog.csdn.net/HALEN001/article/details/81137092

![[attachments/20180720171540379.jpg|这里写图片描述]]

# IntelliJ IDEA 2018.2（Ultimate Edition）激活方法

本因博主Windos10系统上IDEA 2017会出现自带输入法候选框不跟随光标的问题，故更新了IntelliJ IDEA 2018，当时官方发布虽然还是Beta版本，但是迫于输入中文累死眼睛的窘态下，更新了2018版本，So,我想说的是什么呢？2018版本解决了以上bug……
 **言归正传**

### 一、第一种激活方式：破解补丁（此方式有效期到2100年）

**1、 下载破解补丁文件 JetbrainsCrack-2.9-release-enc.jar，路径为：百度云链接：[https://pan.baidu.com/s/1rfOdn3suqyP2RUtIsZqbkQ](https://pan.baidu.com/s/1rfOdn3suqyP2RUtIsZqbkQ) 密码：etr5（失效）**

###### 2018.8.1更新最新破解补丁JetbrainsCrack-2.10-release-enc.jar，百度云下载地址：[https://pan.baidu.com/s/1qgXrr8yHBhAI9gcqRsxrbA](https://pan.baidu.com/s/1qgXrr8yHBhAI9gcqRsxrbA) 密码：9nrg （失效）

###### 2018.8.15更新最新破解补丁JetbrainsCrack-3.1-release-enc.jar百度云下载地址：[https://pan.baidu.com/s/1hcoSMVfdQD3UzvCaGUCK3w](https://pan.baidu.com/s/1hcoSMVfdQD3UzvCaGUCK3w) 密码：x56a

**2、将补丁放在安装包的/bin路径下，如图中放置在最后的jar文件，并且 分别 对本文件夹(bin)下的idea.exe.vmoptions和idea64.exe.vmoptions这两个文件进行修改，打开文件在末尾添加如下配置指令：**

```
windows版：-javaagent:D:/indea/bin/JetbrainsCrack-3.1-release-enc.jar

Mac版：-javaagent:../bin/JetbrainsCrack-3.1-release-enc.jar123
```

**说明：D:/indea/bin/ 是你IDEA的安装位置**

**3、保存编辑后的文件后，到 [http://idea.lanyus.com](http://idea.lanyus.com/) 网站中 ，点获取注册码，拷贝注册码**
 **4、打开IDEA，进入激活窗口此时需要选择 激活码(Activation code) 的激活方式，并输入刚刚拷贝激活码进行激活**
 **5、激活完成**
 ![[attachments/20180720183351951.png|这里写图片描述]]

---

### 二、第二种激活方式：License Server

**1、将地址 [http://idea.autoseasy.cn/heihei](http://idea.autoseasy.cn/heihei) 或者 [http://active.chinapyg.com/](http://active.chinapyg.com/) 或者 [http://idea.toocruel.net](http://idea.toocruel.net/) 任意一个复制到License Server中**
 **说明**
 1. 激活有问题的，查看版本是否对应
 **2、激活完成**

---

### 三、第三种激活方式：Activation code (支持JetBrains旗下所有集成开发工具)

**1、C:\Windows\System32\drivers\etc目录下找到 *hosts* 文件**
 **2、打开hosts文件将 *0.0.0.0 account.jetbrains.com* 添加到文件末尾**
 **3、到 [http://idea.lanyus.com](http://idea.lanyus.com/) 网站中 ，点获取注册码，拷贝注册码**
 **4、将注册码输入Activation code 中**
 **5、激活完成**
 **说明**
 1. 如果没有此文件 尝试查看文件是否被隐藏
 2. 修改后无法保存的话进行如下修改权限操作
 ![[attachments/20180720174808306.png|这里写图片描述]]
 ![[attachments/20180720174819620.png|这里写图片描述]]

### 四、JetBrains系列激活成果图

![[attachments/2018082210143671.png|这里写图片描述]]
 ![[attachments/20180822101447304.png|这里写图片描述]]
 ![[attachments/20180822101456181.png|这里写图片描述]]
