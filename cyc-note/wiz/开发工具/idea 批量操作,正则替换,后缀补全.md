---
Title: "idea 批量操作,正则替换,后缀补全.md"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2021-09-10T15:04:38+08:00"
Cover: ""
WizGuid: "c3a684fa-450a-486c-946f-5d9c8330f167"
WizType: "TemplateNote"
WizLocation: "/开发工具/"
WizDataMd5: "7b39d11348d5929e93c12e99852d837d"
Modified: "2021-09-10T15:05:02+08:00"
WizSyncedAt: "2026-07-22T16:05:38+08:00"
---

> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [zhuanlan.zhihu.com](https://zhuanlan.zhihu.com/p/145138904)

批量操作

----

多光标操作，是一款优秀的编辑器的基本职能。

在 idea 中利用_Alt_键可以轻松的一次性拉取多行进行多点编辑操作：

![](https://pic3.zhimg.com/v2-6d46bc200a3fad0ed9d2726be8268d72_r.jpg)

如果需要按点选择，则可以按_Alt_+_Shift_选择编辑：

![](https://pic2.zhimg.com/v2-3cfab4c7e9cc926fb0409bc585194fc1_r.jpg)

_Ctrl_+_Alt_+_Shift_则包揽了行选择和点选择的功能：

![](https://pic4.zhimg.com/v2-40e93ee6390e533ea5a13bba2e924863_r.jpg)

组合其他快捷键使用可以完成相对复杂的操作，例如将原有类变量的行注释，变更为段注释。

这里用到了_Ctrl_ + _Alt_ +_Shift_ + _J_ 和 _Ctrl_+_W_。

前者可以选中当前文件中所有相同的内容，如果光标没有选择范围则默认为附近的一个词。

而后者则可以选中当前光标附近的词。

![](https://pic1.zhimg.com/v2-46915f4a2997ac9515d282564df62eb0_r.jpg)

利用_Ctrl_+_W_可以轻易找到多个编辑点内容开头结尾

![](https://pic1.zhimg.com/v2-0e01cf25e53cb15f33d5305374530c30_r.jpg)

正则替换

----

idea 文本替换功能支持所有的标准正则表达式，利用正则表达式可以完成很多复杂的功能。

使用正向和反向预查正则可以仅替换满足指定条件的文本，这个表达式可以替换被

包裹的中文：

```

(?<=<li>)[\u4e00-\u9fa5]*(?=</li>)

```

![](https://pic1.zhimg.com/v2-763a9d5adf20389306cbc252c1c62878_r.jpg)

idea 支持使用小括号对正则进行分组，然后进行取值替换，上面将行注释变更的功能使用分组替换也可以完成：

```

\/\/ ([\u4e00-\u9fa5]*)

```

![](https://pic1.zhimg.com/v2-8b9746e91367b04c1237416ad73cafa0_r.jpg)

利用复杂的正则表达式可以简便的完成数据库方言的替换。

例如时间格式化字符串在 Oracle 中是_yyyymmddHH24miss_而在 mysql 中却是_%Y%m%d%H%i%s_。

替换正则：

```

(yyyy)(-|/)*?(mm)(-|/)*?(dd)(\s)*?(HH24)(:*?)(mi)(:*?)(ss)

```

替换为:

```

%Y$2%m$4%d$6%H$8%i$10%s

```

![](https://pic2.zhimg.com/v2-b53d2c846da5bb6018673b1623e04ce1_r.jpg)

用好正则替换功能将会给代码重构带来极大的便利。

除了标准的正则表达式外，idea 还支持在替换时修改替换文本的大小写属性（该功能不支持全局替换）。

| 表达式 | 含义 | | :----: | :------------------------------------: | | \l | 将替换文本的首字母置为小写 | | \u | 将替换文本的首字母置为大写 | | \L | 将替换文本置为小写，可以使用 \ E 标记停止 | | \U | 将替换文本置为大写，可以使用 \ E 标记停止 |

![](https://pic3.zhimg.com/v2-86cb6889e8a2f84d4a203aaf63a1b0ca_r.jpg)

后缀补全

----

对对象使用调用符_._时 idea 除了会弹出调用方法的提示，还会弹出一些预定义的后缀模板，利用这些后缀模板可以大幅减少移动光标的次数：

![](https://pic3.zhimg.com/v2-f72fc909f5a12d8953e3afb762e533ce_r.jpg)

官网预定义的模板可以满足大部分场景，但有些调用 Api 并不满足需要，在_2018.01_版本后的 idea 允许自定义后缀模板（旧版本可以使用插件_Custom Postfix Templates_）。

按_Ctrl_+_Shift_+_A_搜索 postfix completion 或者 Setting=>General=>PostFix Completion 打开 postfix completion 编辑页面。

这里允许自定义后缀模板：

![](https://pic1.zhimg.com/v2-621f2a5c229cb9ed4e2f9ae17ca56d74_r.jpg)

定义的模板中可以配置关键词，语言版本，适用的变量类型等，这里为任意对象定义一个 Optional.orElse 的模板：

![](https://pic2.zhimg.com/v2-9c5cf379c1c0b7de99fcb4e6249da541_r.jpg)

_$EXPR$_模板生效后变量将处在的位置，_$END$_则标记了光标最后处在的位置：

![](https://pic4.zhimg.com/v2-0dd15db3c078bca27f6c200b64a5dfe3_r.jpg)

唯一遗憾的一点是官方文档中并未说明多任务光标要如何定义，期待官方后续版本能够开发这个设置。

![](https://pic4.zhimg.com/v2-9e1cb7f968ee3ede9cb362c2bd7cd26f_r.jpg)

以上为本文全部内容。

![](https://pic4.zhimg.com/v2-20541e7ac61d0f39531b198971f090eb_r.jpg)

毛胚公众号弱弱的求一波大佬关注。
