---
id: "1921337597340422399"
title: "IntelliJ IDEA 中有什么让你相见恨晚的技巧？"
author: "江小北"
type: zhihu-answer
source: "https://www.zhihu.com/question/300830746/answer/1921337597340422399"
created: "2025-06-25 22:42"
updated: "2025-06-25 22:42"
collected: "2025-06-25 22:42"
downloaded: "2026-08-16"
---
**结构化搜索与替换（Structural Search and Replace，简称 SSR）**

这玩意儿不是普通的 Ctrl+R，是语法级别的搜索。比如你要找所有 `List<X>` 里用了 `add(null)` 的地方，SSR 可以精准匹配，不靠正则瞎蒙，直接搜代码结构，效率爆炸。用法：`Edit -> Find -> Replace Structurally`，自带模板能玩出花。

  

> **IDEA 2025**的最新版本，参考我这篇亲测激活教程，都可以激活成功，如果不行，过来踢我  
> **新版本新增了AI功能，快来试试吧：免费激活教程**

[【2025最新版】IDEA 2025.1.2 安装与永久激活教程（激活码+破解补丁）](https://link.zhihu.com/?target=https%3A//ilovemn.cn/jetBrains/idea-1-2.html)

### **Evaluate Expression（调试时的“万能计算器”）**

调试断点时点一下 “Evaluate Expression”（快捷键 `Alt+F8`），输入任意表达式直接运行，连私有字段、内部类都能搞。这功能救过我无数次，尤其是排那种复杂对象嵌套的问题，一步步打印太慢，直接 evaluate 一波全明白。

### **Live Templates 动态代码片段**

你提到了模板，这里我补一嘴：除了 `sout` 这些常用的，还有 `iter`, `itco`, `itar`, `psvm` 之类的循环/主函数模板都能自定义。再高级点可以加变量占位符，比如 `${EXCEPTION}`，还能触发自动补全。用得顺了，真的是写代码像开挂。

### **Database Tools 中的 Diagram View**

你项目连了数据库的话，右键点击表名 → **Diagrams → Show Visualization**，直接一张 ER 图甩出来，主外键关系一目了然，不用再开 PowerDesigner 那种工具了。配合 SQL Console，边写边看，效率拉满。

### **Code With Me 协同编程**

这功能疫情那会儿用得多，现在也挺香。你远程带新人、Code Review 或调试线上 bug，开个“Code With Me”，一秒把 IDEA 分享出去，语音 + 编辑 + 跳转全支持。远程 pair-programming 直接原地起飞。

### **External Tools 外部工具集成**

IDEA 可以配置外部脚本/命令，比如我经常把阿里 Java 代码规约扫描（p3c）集成进去，写完代码点一下菜单就能跑规则扫描；也可以绑定自己写的 Shell 脚本，自动清理缓存、重启服务，自己想怎么玩都行。

### **Scopes + Favorites（作用域与收藏）**

这个不常被提，但对大项目特别香。你可以自定义 Scope，比如“只看 service 层”，“只扫 test 包下的代码”等，然后配合代码检查、搜索、版本控制过滤都方便。写完功能还能加到 Favorites 里，方便后续查阅或 Review。

### **Quick Documentation（Ctrl+Q）+ External Doc 配置**

想看某个方法的注释、参数、返回值？直接 `Ctrl+Q`，不用点进去。更牛的是你可以配置外部文档（比如 Java 官方文档或你们公司内部的 Wiki），F1 一按直接跳转，查接口一秒钟。

### **Code Cleanup + Save Actions**

写完代码就交？不行，得清理一波。`Code → Reformat Code` 配合 `Optimize Imports + Rearrange Code`，再配合 `Save Actions` 插件，保存时自动执行这套操作，保证提交前干干净净。

### **插件推荐一波**

-   **Key Promoter X**：帮你记快捷键，点一次鼠标它就提醒一次。
-   **String Manipulation**：大小写转换、驼峰转下划线，全靠它。
-   **Rainbow Brackets**：括号层级颜色区分，避免括号地狱。
-   **Grep Console**：控制台输出加高亮，加关键字提醒。
-   **Presentation Assistant**：讲课直播时显示快捷键操作，极香。