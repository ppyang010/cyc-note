---
Title: "VSCode 实现可以右键打开文件和文件夹的解决方案"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2019-12-29T23:30:52+08:00"
Cover: ""
WizGuid: "df098d42-e34a-46f2-a017-bba822f92859"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "37a63d2e3416b760f99e43cdff6c723f"
Modified: "2019-12-29T23:31:04+08:00"
WizSyncedAt: "2026-07-21T17:35:17+08:00"
---

**VSCode 实现可以右键打开文件和文件夹的解决方案：**

**A.添加右键打开文件**
1,    Win+R 打开运行，输入regedit，打开注册表，找到HKEY_CLASSES_ROOT\*\shell分支，如果没有shell分支，则在*下点击右键，选择“新建－项”，建立shell分支。
2,    在shell下新建“VisualCode”项，在右侧窗口的“默认”键值栏内输入“用VSCode打开文件”，这是右键上显示值，也就是文字。其事可以随便写，只是为了方便记忆和分辨。
3,    在“VisualCode”下再新建Command项，在右侧窗口的“默认”键值栏内输入程序所在的安装路径，我的是："D:\Program Files (x86)\VSCode\code.exe" "%1"。其中的%1表示要打开的文件参数。
4,    关闭注册表，即可生效。

**B.添加右键打开文件夹**
以上方法可以在选中文件时右键在菜单栏中显示："用VSCode打开文件夹"，但当右键文件夹时仍然不能显示此选项，所以还要进行下面的操作：

打开注册表，找到HKEY_CLASSES_ROOT\Directory\shell，按照上面2、3的方法添加即可。

添加Icon，也就是文字前面的图标
在原有的VisualCode项上新建可扩充字符串值，命名为Icon，像一个键值对那样把"D:\Program Files (x86)\Microsoft VS Code\code.exe"放进去就可以了。

来源： [http://www.dalbll.com/Group/Topic/OtherTool/8753](http://www.dalbll.com/Group/Topic/OtherTool/8753)
