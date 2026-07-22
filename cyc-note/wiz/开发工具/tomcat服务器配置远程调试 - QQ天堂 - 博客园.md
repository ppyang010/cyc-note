---
Title: "tomcat服务器配置远程调试 - QQ天堂 - 博客园"
Url: "http://www.cnblogs.com/QQParadise/articles/1639831.html"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-07-06 16:13:19"
Cover: ""
WizGuid: "ce3783b7-f15c-4cee-8496-0f4f8b9ee249"
WizType: ""
WizLocation: "/开发工具/"
WizDataMd5: "127738e42928669b767f94890778f3f7"
Modified: "2016-07-06 16:13:19"
WizSyncedAt: "2026-07-21 15:18:27"
---

[返回主页](http://www.cnblogs.com/QQParadise/)

# [QQ天堂](http://www.cnblogs.com/QQParadise/)

## QQ天堂的BLOG(每天灌水一点点，长此以往，大海将会出现！)

- [博客园](http://www.cnblogs.com/)
- [首页](http://www.cnblogs.com/QQParadise/)
- [新随笔](http://i.cnblogs.com/EditPosts.aspx?opt=1)
- [联系](http://msg.cnblogs.com/send/QQ%E5%A4%A9%E5%A0%82)
- [管理](http://i.cnblogs.com/)
- [订阅](http://www.cnblogs.com/QQParadise/rss) [订阅](http://www.cnblogs.com/QQParadise/rss)

随笔- 30  文章- 282  评论- 46

# [tomcat服务器配置远程调试](http://www.cnblogs.com/QQParadise/articles/1639831.html)

对于新入门的人而言，调试跟踪对于你理解程序和查找错误是很有利的一种方法。通常情况下如果jsp页面出现了异常或servlet中的程序有错误，光凭你的一双肉眼凡胎来解决问题是一件颇费神的事情。下面告诉大家怎么配置tomcat服务器的远程调试。

首先到tomcat/bin/目录下找到 catalina.bat文件.然后在该文件中加入如下设置:SET CATALINA_OPTS=-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5888

当然SET CATALINA_OPTS 变量应该在使用它之前。这是在tomcat启动时设置一些虚拟机参数，使服务器允许远程连接功能，address=5888表示远程连接的端口号，可以设置成任意其他不冲突端口。其他的应用服务器比如weblogic也应该可以设置这些参数，不过我没试过
SET CATALINA_OPTS 变量应该在使用它之前指的是(在clatalina.bat文件中看到有
rem-----Execute The Requested  Command ------------------的一行内容
把上面的设置放在这一行的上面就可以了。)

重启动tomcat,可以直接独立启动，而不用在eclipes的插件中启动。打开eclipse中的debug设置窗口，选择Remote Java Application ，新建一个debug项，输入服务器IP(如果是本机就输入localhost或127.0.0.1)和刚才设置端口号，点ok就可以进入debug状态了。

不过要注意在Linux下，有一点点差异，是要编辑catalina.sh文件。
而且要改成这样：CATALINA_OPTS="-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5888"
     也就是把SET去掉，后面加双引号引起来，因为在Linux下，是没有SET这个语法的。大家有兴趣的可以去试一下

分类: [JAVA](http://www.cnblogs.com/QQParadise/category/150258.html)

[好文要顶](#) [关注我](#) [收藏该文](#) ![[attachments/icon_weibo_24.png]] ![[attachments/wechat.png]]

![[attachments/u38368.jpg]]

[QQ天堂](http://home.cnblogs.com/u/QQParadise/)
 [关注 - 0](http://home.cnblogs.com/u/QQParadise/followees)
 [粉丝 - 76](http://home.cnblogs.com/u/QQParadise/followers)

[+加关注](#)

1

0

(请您对文章做出评价)

[«](http://www.cnblogs.com/QQParadise/archive/2009/06/12/1501906.html) 上一篇：[什么是负载均衡？](http://www.cnblogs.com/QQParadise/archive/2009/06/12/1501906.html)
[»](http://www.cnblogs.com/QQParadise/archive/2011/01/27/1946078.html) 下一篇：[B2B，B2C和C2C的区别](http://www.cnblogs.com/QQParadise/archive/2011/01/27/1946078.html)

posted @ 2010-01-05 18:42 [QQ天堂](http://www.cnblogs.com/QQParadise/) 阅读(10626) 评论(0)  [编辑](http://i.cnblogs.com/EditArticles.aspx?postid=1639831) [收藏](http://www.cnblogs.com/QQParadise/articles/1639831.html#)

[刷新评论](#)[刷新页面](http://www.cnblogs.com/QQParadise/articles/1639831.html#)[返回顶部](http://www.cnblogs.com/QQParadise/articles/1639831.html#top)

注册用户登录后才能发表评论，请 [登录](#) 或 [注册](#)，[访问](http://www.cnblogs.com/)网站首页。

**最新IT新闻**:
 · [微软准备推出DirectX 12更新 更好地支持多显卡](http://news.cnblogs.com/n/548805/)
 · [视频和有线化敌为友：Netflix成为有线机顶盒的一个频道](http://news.cnblogs.com/n/548804/)
 · [第一版刚亮相3周后，苹果四大操作系统面向开发者推出第二个测试版](http://news.cnblogs.com/n/548803/)
 · [2016上半年手机趋势观察：回归线下 乱局求生](http://news.cnblogs.com/n/548802/)
 · [全球最薄柔性光伏电池韩国诞生 厚度为人类头发直径百分之一](http://news.cnblogs.com/n/548801/)
» [更多新闻...](http://news.cnblogs.com/)

**最新知识库文章**:

· [抽象：程序员必备的能力](http://kb.cnblogs.com/page/544641/)
 · [编程同写作，写代码只是在码字](http://kb.cnblogs.com/page/213197/)
 · [遇见程序员男友](http://kb.cnblogs.com/page/207265/)
 · [设计师的视觉设计五项修炼](http://kb.cnblogs.com/page/511529/)
 · [我听到过的最精彩的一个软件纠错故事](http://kb.cnblogs.com/page/514193/)

» [更多知识库文章...](http://kb.cnblogs.com/)

昵称：[QQ天堂](http://home.cnblogs.com/u/QQParadise/)
园龄：[7年10个月](http://home.cnblogs.com/u/QQParadise/)
粉丝：[76](http://home.cnblogs.com/u/QQParadise/followers/)
关注：[0](http://home.cnblogs.com/u/QQParadise/followees/)

[+加关注](#)

| \| [<](#) \| 2016年7月 \| [>](#) \|<br>\| --- \| --- \| --- \| |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| [<](#) | 2016年7月 | [>](#) |  |  |  |  |
| 日 | 一 | 二 | 三 | 四 | 五 | 六 |
| 26 | 27 | 28 | 29 | 30 | 1 | 2 |
| 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 17 | 18 | 19 | 20 | 21 | 22 | 23 |
| 24 | 25 | 26 | 27 | 28 | 29 | 30 |
| 31 | 1 | 2 | 3 | 4 | 5 | 6 |

### 搜索

### 常用链接

- [我的随笔](http://www.cnblogs.com/QQParadise/p/)
- [我的评论](http://www.cnblogs.com/QQParadise/MyComments.html)
- [我的参与](http://www.cnblogs.com/QQParadise/OtherPosts.html)
- [最新评论](http://www.cnblogs.com/QQParadise/RecentComments.html)
- [我的标签](http://www.cnblogs.com/QQParadise/tag/)
- [更多链接](http://www.cnblogs.com/QQParadise/articles/1639831.html#)

### 我的标签

- [Explain](http://www.cnblogs.com/QQParadise/tag/Explain/)(1)
- [MySQL](http://www.cnblogs.com/QQParadise/tag/MySQL/)(1)
- [执行计划](http://www.cnblogs.com/QQParadise/tag/%E6%89%A7%E8%A1%8C%E8%AE%A1%E5%88%92/)(1)

### 随笔档案

- [2016年1月 (2)](http://www.cnblogs.com/QQParadise/archive/2016/01.html)
- [2015年12月 (1)](http://www.cnblogs.com/QQParadise/archive/2015/12.html)
- [2013年4月 (1)](http://www.cnblogs.com/QQParadise/archive/2013/04.html)
- [2012年12月 (1)](http://www.cnblogs.com/QQParadise/archive/2012/12.html)
- [2012年9月 (1)](http://www.cnblogs.com/QQParadise/archive/2012/09.html)
- [2012年7月 (1)](http://www.cnblogs.com/QQParadise/archive/2012/07.html)
- [2011年11月 (2)](http://www.cnblogs.com/QQParadise/archive/2011/11.html)
- [2011年10月 (1)](http://www.cnblogs.com/QQParadise/archive/2011/10.html)
- [2011年4月 (1)](http://www.cnblogs.com/QQParadise/archive/2011/04.html)
- [2011年3月 (1)](http://www.cnblogs.com/QQParadise/archive/2011/03.html)
- [2011年1月 (1)](http://www.cnblogs.com/QQParadise/archive/2011/01.html)
- [2009年6月 (1)](http://www.cnblogs.com/QQParadise/archive/2009/06.html)
- [2009年5月 (1)](http://www.cnblogs.com/QQParadise/archive/2009/05.html)
- [2009年3月 (1)](http://www.cnblogs.com/QQParadise/archive/2009/03.html)
- [2009年2月 (1)](http://www.cnblogs.com/QQParadise/archive/2009/02.html)
- [2008年12月 (1)](http://www.cnblogs.com/QQParadise/archive/2008/12.html)
- [2008年10月 (4)](http://www.cnblogs.com/QQParadise/archive/2008/10.html)
- [2008年9月 (6)](http://www.cnblogs.com/QQParadise/archive/2008/09.html)
- [2008年8月 (2)](http://www.cnblogs.com/QQParadise/archive/2008/08.html)

### 文章分类

- [Android(5)](http://www.cnblogs.com/QQParadise/category/435191.html)
- [C#(2)](http://www.cnblogs.com/QQParadise/category/150566.html)
- [CSS(5)](http://www.cnblogs.com/QQParadise/category/188076.html)
- [DB2(16)](http://www.cnblogs.com/QQParadise/category/301641.html)
- [HardWare (31)](http://www.cnblogs.com/QQParadise/category/150881.html)
- [HTML(1)](http://www.cnblogs.com/QQParadise/category/540282.html)
- [JAVA(131)](http://www.cnblogs.com/QQParadise/category/150258.html)
- [JavaScript(30)](http://www.cnblogs.com/QQParadise/category/152789.html)
- [MSSQL(43)](http://www.cnblogs.com/QQParadise/category/150565.html)
- [mysql(1)](http://www.cnblogs.com/QQParadise/category/797294.html)
- [Oracle(21)](http://www.cnblogs.com/QQParadise/category/191395.html)

### 相册

- [山水人物(6)](http://www.cnblogs.com/QQParadise/gallery/153050.html)

### 积分与排名

- 积分 - 202466
- 排名 - 793

### 最新评论

- [1. Re:oracle行转列（动态行转不定列)](http://www.cnblogs.com/QQParadise/articles/1712093.html#3378174)
- 谢谢，受益了！
- --恬静的生活
- [2. Re:java比较两个日期大小](http://www.cnblogs.com/QQParadise/articles/1501420.html#3366746)
- 也是一种解法。
- --StoneBridge
- [3. Re:The content of element type "configuration" must match "(properties?,settings?,typeAliases?,typeHandlers?,objectFactory?...](http://www.cnblogs.com/QQParadise/articles/4770965.html#3349595)
- 赞一个
- --小虫1
- [4. Re:java比较两个日期大小](http://www.cnblogs.com/QQParadise/articles/1501420.html#3297772)
- after不就好了
- --jimwirtfgghert
- [5. Re:java比较两个日期大小](http://www.cnblogs.com/QQParadise/articles/1501420.html#3266583)
- 提示信息反了！
- --龙须子

### 阅读排行榜

- [1. 安卓手机如何获得Root权限(18408)](http://www.cnblogs.com/QQParadise/archive/2011/11/25/2263215.html)
- [2. B2B，B2C和C2C的区别(5183)](http://www.cnblogs.com/QQParadise/archive/2011/01/27/1946078.html)
- [3. Android手机WIFI与电脑间共享文件(3977)](http://www.cnblogs.com/QQParadise/archive/2012/09/03/2668533.html)
- [4. 12个球问题--微软面试题(3639)](http://www.cnblogs.com/QQParadise/archive/2008/08/15/1268335.html)
- [5. 从零开始破解WEP、WPA无线网络(3183)](http://www.cnblogs.com/QQParadise/archive/2011/04/15/2017000.html)

### 评论排行榜

- [1. 隐马尔可夫模型HMM[转载牛人，看了半天没看懂](2)](http://www.cnblogs.com/QQParadise/archive/2008/10/21/1316265.html)
- [2. 高通全系列手机处理器深度解析 （升级选手机必备）附参数对比表(1)](http://www.cnblogs.com/QQParadise/archive/2012/12/05/2803418.html)
- [3. Android手机WIFI与电脑间共享文件(1)](http://www.cnblogs.com/QQParadise/archive/2012/09/03/2668533.html)
- [4. 安卓手机如何获得Root权限(1)](http://www.cnblogs.com/QQParadise/archive/2011/11/25/2263215.html)
- [5. 张老师的生日究竟是哪天(温故经典推理题[转载])(1)](http://www.cnblogs.com/QQParadise/archive/2008/09/12/1289780.html)

### 推荐排行榜

- [1. 从零开始破解WEP、WPA无线网络(3)](http://www.cnblogs.com/QQParadise/archive/2011/04/15/2017000.html)
- [2. JPA(Java Persistence API)(1)](http://www.cnblogs.com/QQParadise/archive/2009/02/24/1397242.html)
- [3. DRP与ERP、CRM、PRM (1)](http://www.cnblogs.com/QQParadise/archive/2008/10/25/1319477.html)
- [4. 隐马尔可夫模型HMM[转载牛人，看了半天没看懂](1)](http://www.cnblogs.com/QQParadise/archive/2008/10/21/1316265.html)
- [5. Android手机WIFI与电脑间共享文件(1)](http://www.cnblogs.com/QQParadise/archive/2012/09/03/2668533.html)

Copyright ©2016 QQ天堂
