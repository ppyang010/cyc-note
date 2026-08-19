---
Title: "哪位大虾知道怎么把javaweb项目发布到外网？使用自己的机器做服务器，windows系统，项目部署在tomcat上_百度知道 (3)"
Url: "http://jingyan.baidu.com/article/90bc8fc864699af653640cf7.html"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2015-10-15 17:25:09"
Cover: ""
WizGuid: "ca324c8b-6217-401b-8af0-c6468174d13b"
WizType: ""
WizLocation: "/工作/工作日记/"
WizDataMd5: "0179260d08757e21ad3ad96a936df1e1"
Modified: "2015-10-15 17:26:25"
WizSyncedAt: "2026-08-18 18:48:31"
---

[百度经验](http://jingyan.baidu.com/) | [百度知道](http://zhidao.baidu.com/) | [百度首页](http://www.baidu.com/) | [登录](https://passport.baidu.com/v2/?login) | [注册](https://passport.baidu.com/v2/?reg&tpl=exp&u=http%3A%2F%2Fjingyan.baidu.com%2Farticle%2F90bc8fc864699af653640cf7.html)

![[attachments/logo_1e63520.png|百度经验]]
- [新闻](http://news.baidu.com/)
- [网页](http://www.baidu.com/)
- [贴吧](http://tieba.baidu.com/)
- [知道](http://zhidao.baidu.com/)
- **经验**
- [音乐](http://music.baidu.com/)
- [图片](http://image.baidu.com/)
- [视频](http://video.baidu.com/)
- [地图](http://map.baidu.com/)
- [百科](http://baike.baidu.com/)
- [文库](http://wenku.baidu.com/)

[帮助](http://www.baidu.com/search/jingyan_help.html)

- [首页](http://jingyan.baidu.com/)
- [分类](#)
- [杂志](http://jingyan.baidu.com/magazine/home)
- [任务](http://jingyan.baidu.com/task)
- [签到](http://jingyan.baidu.com/usersign)
- [回享计划](http://jingyan.baidu.com/user/income)
- [商城](http://jingyan.baidu.com/shop)
- [知道](http://zhidao.baidu.com/)
[http://jingyan.baidu.com/edit/content](http://jingyan.baidu.com/edit/content)

[百度经验](http://jingyan.baidu.com/) > [游戏/数码](http://jingyan.baidu.com/list/10) > [电脑](http://jingyan.baidu.com/list/11) > 电脑软件

# 如何将自己的Java项目部署到外网

-
- |
- 浏览：815
- |
- 更新：2015-03-03 15:32
.

- ![[attachments/4bed2e738bd4b31c60a986ce83d6277f9e2ff82a.jpg.png|如何将自己的Java项目部署到外网]]1
- ![[attachments/7af40ad162d9f2d3aea0389aadec8a136327cc16.jpg.png|如何将自己的Java项目部署到外网]]2
- ![[attachments/d52a2834349b033b7c20e3af11ce36d3d539bd1e.jpg.png|如何将自己的Java项目部署到外网]]3
- ![[attachments/377adab44aed2e735d2f85598301a18b86d6fa85.jpg.png|如何将自己的Java项目部署到外网]]4
- ![[attachments/0b7b02087bf40ad18832c496532c11dfa8eccef5.jpg.png|如何将自己的Java项目部署到外网]]5
- ![[attachments/fd039245d688d43f12789287791ed21b0ff43bf5.jpg.png|如何将自己的Java项目部署到外网]]6
- ![[attachments/b999a9014c086e06ffdb333e06087bf40ad1cb50.jpg.png|如何将自己的Java项目部署到外网]]7
[分步阅读](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html).

做b/s模式的web开发不同于c/s模式的客户端开发，c/s模式我们只要做好生成可执行文件发送给其他人，其他人就可以用了。但是c/s模式不同，在同一局域网下，我们还可以通过IP访问，如果处于不同的局域网怎么办？下面我就教大家如何将自己的项目发布到外网，让处于互联网上的所有人都可以访问我们的网站。

## [#](#)工具/原料

- 花生壳软件

## [#](#)方法/步骤

1. 1 百度花生壳，去下载最新的花生壳客户端安装好。
2. 2 如果你没有帐号，去花生壳官网注册一个账号，这个账号将会用户登陆花生壳以及部署项目时的域名。
3. 3 如果你具备以上条件时，那么接下来可以启动花生壳客户端并登陆了。如图所示的界面，，说明你已经登陆成功，并且可以进行下一步操作。注意花生壳分配的给你的账号域名，比如我的是“jingtoo.oicp.net”。 ![[attachments/4bed2e738bd4b31c60a986ce83d6277f9e2ff82a.jpg.png|如何将自己的Java项目部署到外网]].
4. 4 双击上图列表中的域名，会弹出一个对话框，里面什么都没有，因为你还没有添加映射关系，点击“添加映射”，如图所示。你会看到 ![[attachments/7af40ad162d9f2d3aea0389aadec8a136327cc16.jpg.png|如何将自己的Java项目部署到外网]]. ![[attachments/d52a2834349b033b7c20e3af11ce36d3d539bd1e.jpg.png|如何将自己的Java项目部署到外网]].
5. 5 因为你可能存在局域网中，而局域网中有多台计算机，所以我要知道你的内外IP。开始--运行---输入cmd---在打开的窗口中输入ipconfig回车，找到你的ip，回到花生壳中，在内网主机中输入你刚刚看到的IP，在端口映射中输入你项目运行的端口号，然后确定。 [http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=4](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=4). [http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=5](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=5).
6. 6 再次回到花生壳主界面，会看到其中多了一条数据，里面就包含你外网访问的地址。 [http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=6](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=6).
7. 7 启动你的项目，现在浏览器中输入“http://localhost:8080/test”,然后再输入“http://jingtoo.oicp.net/test”。会发现两次的效果是一样的。 [http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=7](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=7). [http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=8](http://jingyan.baidu.com/album/90bc8fc864699af653640cf7.html?picindex=8).
8. 8 在一般情况下，我们是不需要做这种外网映射的，但是设计到和外网做接口对接测试时，就显得很有必要了，比如支付支付接口。 END

经验内容仅供参考，如果您需解决具体问题(尤其法律、医学等领域)，建议您详细咨询相关领域专业人士。

[举报](#)*作者声明：*本篇经验系本人依照真实经历原创，未经许可，谢绝转载。

投票(3)

有得(0)

我有疑问(0)

.

### [换一批](http://jingyan.baidu.com/article/90bc8fc864699af653640cf7.html#)相关经验.

- [怎样在xp下利用tomcat部署一个java web项目](http://jingyan.baidu.com/article/4e5b3e1976cabe91901e242e.html)12012.01.10
- [java项目升级部署的步骤和注意事项](http://jingyan.baidu.com/article/77b8dc7fe5c1076174eab69b.html)02015.08.07
- [java项目如何创建包以及调试运行](http://jingyan.baidu.com/article/47a29f2456f477c01423999d.html)162015.08.20
- [java 如何使用eclipse导出跟导入项目](http://jingyan.baidu.com/article/73c3ce28e99596e50343d904.html)72014.04.14
- [eclipse如何创建java项目？创建时需要注意什么](http://jingyan.baidu.com/article/d169e1864e8a4c436611d8e1.html)142015.08.19

**相关标签**

今日支出

.

元

[写经验 有钱赚 >>](http://jingyan.baidu.com/user/income)

![[attachments/f7fd7978773833393834313233314115.jpg]]

## [yxw839841231](http://jingyan.baidu.com/user/npublic?un=yxw839841231)

[http://jingyan.baidu.com/help?page=income-author](http://jingyan.baidu.com/help?page=income-author)

[#](#)

.

个性签名：小屌丝

### 作者的经验

- [如何用tomcat发布自己的Java项目](http://jingyan.baidu.com/article/a501d80c0c65baec630f5ef6.html)
- [JavaScript绘图：html5标签canvas](http://jingyan.baidu.com/article/cb5d6105173683005c2fe0f6.html)
- [最简单的换IP方法](http://jingyan.baidu.com/article/fcb5aff7acdb2aedaa4a71f5.html)
- [html5——css中的div妙用](http://jingyan.baidu.com/article/19020a0a260803529d28422a.html)
- [新手如何学习Java——菜鸟篇](http://jingyan.baidu.com/article/3c343ff709afe40d37796338.html)

![[attachments/44a815e5c6e56012f9bd31f9dac5d42c.jpg|经验5周年]]

如要投诉，请到[百度经验投诉中心](http://tousu.baidu.com/jingyan/add#2)，如要提出意见、建议， 请到[百度经验管理吧](http://tieba.baidu.com/f?kw=%B0%D9%B6%C8%BE%AD%D1%E9%B9%DC%C0%ED)反馈。

.

## 热门杂志

- 第1期 **你不知道的iPad技巧** 2536次分享 [http://jingyan.baidu.com/magazine/6872](http://jingyan.baidu.com/magazine/6872)
- 第1期 **win7电脑那些事** 4465次分享 [http://jingyan.baidu.com/magazine/6454](http://jingyan.baidu.com/magazine/6454)
- 第2期 **新人玩转百度经验** 744次分享 [http://jingyan.baidu.com/magazine/17909](http://jingyan.baidu.com/magazine/17909)
- 第1期 **Win8.1实用小技巧** 1962次分享 [http://jingyan.baidu.com/magazine/17761](http://jingyan.baidu.com/magazine/17761)
- 第1期 **小白装大神** 1058次分享 [http://jingyan.baidu.com/magazine/17450](http://jingyan.baidu.com/magazine/17450)

©2015Baidu  [使用百度前必读](http://www.baidu.com/duty/)  [百度经验协议](http://www.baidu.com/search/jingyan_help.html#经验协议)  [作者创作作品协议](http://www.baidu.com/search/jingyan_editor.html)

[#](#)[#](#)[#](#)[#](#)

◆

![[attachments/778b4cb8d92c0fd6b8f50a81ece3f59a.png]]

请扫描分享到朋友圈

[登录](#)

[http://jingyan.baidu.com/](http://jingyan.baidu.com/)

[http://jingyan.baidu.com/article/90bc8fc864699af653640cf7.html#](http://jingyan.baidu.com/article/90bc8fc864699af653640cf7.html#)
