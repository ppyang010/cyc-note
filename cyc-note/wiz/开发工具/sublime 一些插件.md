---
Title: "sublime 一些插件"
Url: "http://www.cnsecer.com/460.html"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-06-29T11:06:39+08:00"
Cover: ""
WizGuid: "7a3a4efc-9d6e-44c4-a928-9b38cd4c6b4b"
WizType: ""
WizLocation: "/开发工具/"
WizDataMd5: "adeaa649f8ea7cedab4cbfbbba76eb52"
Modified: "2016-09-10T15:27:20+08:00"
WizSyncedAt: "2026-07-21T15:18:27+08:00"
---

使用Package Control组件安装

也可以安装package control组件，然后直接在线安装：

- 按Ctrl+`调出console（注：安装有QQ输入法的这个快捷键会有冲突的，输入法属性设置-输入法管理-取消热键切换至QQ拼音）

- 粘贴以下代码到底部命令行并回车：

import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())

- 重启Sublime Text 3。

- 如果在Perferences->package settings中看到package control这一项，则安装成功。

用Package Control安装插件的方法：

- 按下Ctrl+Shift+P调出命令面板

- 输入install 调出 Install Package 选项并回车，然后在列表中选中要安装的插件。

不爽的是，有的网络环境可能会不允许访问陌生的网络环境从而设置一道防火墙，而Sublime Text 2貌似无法设置代理，可能就获取不到安装包列表了。

好，方法介绍完了，下面是本文正题，一些有用的Sublime Text 插件：

Bracket Highlighter　　用于匹配括号，引号和html标签。对于很长的代码很有用。安装好之后，不需要设置插件会自动生效

Emmet(Zen Coding)　　快速生成HTML代码段的插件，强大到无与伦比，不知道的请自行google

JS Format    一个JS代码格式化插件。   不好用

Sublime CodeIntel  代码自动提示  需要配置  配置文件已放群中   打开个js文件，按ctrl+shift+space

Better Completion jq代码提示

JSLint是一个Javascript代码质量检测工具。它可以告诉你代码的什么地方需要改进。虽然你也可以在网上检测，但这个插件能让你不打开浏览器，直接在Sublime里面检测。 快捷键为ctrl+l

DocBlockr可以自动生成PHPDoc风格的注释。它支持的语言有Javascript, PHP, ActionScript, CoffeeScript, Java, Objective C, C, C++。

SideBar Enhancements 这个插件改进了侧边栏，增加了许多功能：将文件移入回收站，在浏览器中浏览，将文件复制到剪切板。

LiveReload自动刷新插件

ColorPicker  内置调色盘
