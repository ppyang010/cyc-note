---
Title: "atom 插件"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-08-30T11:05:00+08:00"
Cover: ""
WizGuid: "40e26afb-9b8a-40df-9aa8-6762db23d557"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "9f31e489d5b3f2f9af4a0bdb1dd7429d"
Modified: "2017-02-08T17:52:59+08:00"
WizSyncedAt: "2026-07-21T15:18:27+08:00"
---

1. Emmet — 用过都说好,神器;有个别快捷键会和Markdown preview快捷键冲突,改下就好了
2. autoprefixer — 用来补充css前缀的,会自动生成多个浏览器的前缀
3. color-picker — 取色器,太赞了有木有,,比sublime那个好用,不卡,启动超快
4. linter — 这货默认可以识别多门语言的错误,但是不细致,属于主插件,可以针对性的安装更细致的检查插件(太多,不一一列出,下面是前端可能用到的)
  - **linter-jshint**, for JavaScript and JSON, using jshint
  - **linter-coffeelint**, for CoffeeScript, using coffeelint
  - linter-tslint, for Typescript, using tslint
  - linter-php, for PHP using php -l
  - linter-pylint, for Python, using pylint
  - **linter-scss-lint**, for SASS/SCSS, using scss-lint
  - **linter-less**, for LESS, using less
  - **linter-csslint**, for CSS, using csslint
  - linter-stylint, for Stylus, using stylint
  - linter-stylus, for Stylus, using stylus
5. minimap — 用过Sublime Text的友友们都知道有一个很实用的功能,就是内部编辑那里有一个小小的代码图,这货就是补全atom这个功能的,支持高亮代码,还可控哦!!具体看内部设置
6. open-last-project ”记住上一次打开的目录”
7. 浏览器预览 对于前端开发来说,浏览器预览功能必须要有的有木有!!!不然每次都要自己手动拖拉文件到浏览器不是N烦!! **插件:RIB - run in browser** 插件简介: Run in Browser will open the current pane in the default web browser. 这货有默认的用法,看下面 Command Palette: rib — 命令面板搜索rip Keymap: ctrl + alt + r — 默认快捷键(和我一些安装的插件有冲突,也用不惯这么多按键,我直接改F12调用了) the current pane must be a .html or .htm file — 该插件目前支持在html和htm后缀名使用 个人RIB自定义按键修改–仅供参考 'atom-text-editor': 'f12':'rib:run-in-browser' 'ctrl-shift-space':'autocomplete:toggle'
8.

open-in-browser 右键可以选择在浏览器打开 指定默认浏览器

通过命令行安装插件（插件介绍可看文末链接）

apm install emmet //前端常用

apm install atom-beautify //格式化

apm install minimap //代码地图

apm install autoclose-html //自动闭包

apm install linter //lint检查

apm install linter-jshint//js检查

apm install file-icons //文件视图图标

apm install run-in-browser //使用浏览器预览

插件:atom-html-preview

官方描述:A live preview tool for Atom Editor.

简言之:Atom编辑器内实时预览的工具

Docblockr  注释工具

atom-ternjs js代码提示很强大，高度定制化。
color-picker 取色器（必备插件）

pigments 颜色显示插件 （必装）

react  提示插件

快捷键

默认快捷键 : CTRL + P 调用 ,会和内置核心插件冲突(切换文件那个) — 非常不好

修改版快捷键: CTRL + F12(感觉方便使用且没有冲突的快捷键)

#实时浏览器调用快捷键

'atom-text-editor':

'ctrl-F12':'atom-html-preview:toggle'

Highlight Selected   双击变量  高亮

主题

monokai-flat

### 自用atom 插件集合

参考[https://github.com/shery15/awesome-atom-packages/blob/master/README-zh.md](https://github.com/shery15/awesome-atom-packages/blob/master/README-zh.md)

2017年2月8日

docblockr 注释插件

atom-ternjs

ES5, ES6, ES7, Node.js, jQuery, Angular 等等 js 代码自动补全

emmet

快速手写 HTML, CSS, Sass / SCSS / LESS
