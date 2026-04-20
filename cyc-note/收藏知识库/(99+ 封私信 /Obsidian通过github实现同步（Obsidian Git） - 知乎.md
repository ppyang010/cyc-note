[(99+ 封私信 / 84 条消息) Obsidian通过github实现同步（Obsidian Git） - 知乎](https://zhuanlan.zhihu.com/p/657924375) 

 感觉是最快最方便的实现同步的方法了。整套操作下来如果顺利五分钟就可以搞定~而且一劳永逸╰(\*°▽°\*)╯

文章末尾有俺滴碎碎念...

### 功能实现

本文包含配置Github的步骤，Github新手友好。所以文科小姐姐也可以轻松按照下面的步骤完成配置~步骤非常详细啦~

基本思路也很简单： 通过**[Obsidian Git](https://zhida.zhihu.com/search?content_id=234334096&content_type=Article&match_order=1&q=Obsidian+Git&zhida_source=entity)插件**，自动把本地保存的笔记push到github仓库里。每次打开Obsidian，github仓库中的笔记文件也会被自动pull到本地。相当于把github当网盘用。

（对不熟悉github操作的小伙伴，可以这样非常通俗地理解github的工作机制：**使用git commit命令就是把文件装上一辆货车（但货车暂时还留在原地）；git push就是发车，把文件运往/推向Github远程仓库；git pull就是把远程仓库的文件全运/拉回来**（实现同步）。所以定期执行pull命令是必要的，避免在push时远程仓库中的文件与本地有冲突、以至于不能更新远程仓库中的内容）。

### Obsidian端

打开一个vault。这里我新建了一个名叫test的新vault。然后安装Obsidian Git插件。如下：

Obsidian关闭安全模式，即可安装插件。

![](https://pica.zhimg.com/v2-0fab4c76a11ac116f092fb6b7ce32d8e_1440w.jpg)

关闭安全模式后，可以看到社区插件市场选项，搜索并安装Obsidian git插件

![](https://pic1.zhimg.com/v2-6976dcacbed2b2972bc78e8da44b567a_1440w.jpg)

点击安装，然后点击启用。

![](https://pic4.zhimg.com/v2-e7c3ba43c1c629ea55649e86bf41b297_1440w.jpg)

接下来进行三个设置（**自动备份、自动同步、快捷键**）。打开小齿轮窗口

![](https://pic2.zhimg.com/v2-785c383cd5920ad29f232df32e2a5a2d_1440w.jpg)

Step1： 将自动备份时间从0调整到5分钟。

![](https://picx.zhimg.com/v2-9dfa8ce5f73a2505bcad65b89a0ad7b9_1440w.jpg)

Step2: 打开：启动软件时自动从远程拉取（pull）文件。

![](https://pic1.zhimg.com/v2-547302c4e48507845bbf6c74cc8c9c1e_1440w.jpg)

Step3: 设置一些快捷键。主要需要commit、push、pull这三个操作。我的设置如图：

![](https://picx.zhimg.com/v2-7455e4b0991dfa0d56e9d494a662a8cf_1440w.jpg)

![](https://picx.zhimg.com/v2-81452a62c8c953efc771fbbd018c853d_1440w.jpg)

OK, Obsidian端基本配置完成，其他的配置可以自己按需再调整。接下来配置github。

### Github

首先要注册一个github账号！然后下载一个github desktop并安装并登陆。

[GitHub Desktop | Simple collaboration from your desktop](https://link.zhihu.com/?target=https%3A//desktop.github.com/)

![](https://pica.zhimg.com/v2-19320f3ba614c7d2a74197aba0d071c8_1440w.jpg)

接下来，我们将会将本地的Obsidian Vault文件夹设置为一个仓库，然后也在github中建立一个远程仓库，二者可以“连接”在一起。

选择“New repository", 选择你的Obsidian vault所在路径，如图，我的Obsidian vault是F盘中的test文件夹。这样就把本地的F:\\test文件夹设置为了一个本地的git 仓库。

![](https://pic2.zhimg.com/v2-8c350d0bdeda18e457b5ba5f90915985_1440w.jpg)

接着把这个本地仓库publish到远程github中。点击publish repository，记得勾选private。可以打开网页端github检查，我们的确有了一个新的名叫test\_zhihu的仓库。

![](https://pica.zhimg.com/v2-8eef87d25e610ce644a655133167a578_1440w.jpg)

![](https://pic3.zhimg.com/v2-660fcc3d7a99ac65fee08328fbdbfab6_1440w.jpg)

记得勾选private

![](https://pic1.zhimg.com/v2-56a1b478fea14c167a249745569306ea_1440w.jpg)

在Obsidian vault中使用Alt+C快捷键commit（如果上面没设置快捷键的，也可以ctrl+p打开Obsidian面板搜索commit命令），会蹦出来github登录与授权界面。登录并授权。

![](https://pic4.zhimg.com/v2-c8484ff8d54b6d56f5c77bedba9f281d_1440w.jpg)

![](https://pic4.zhimg.com/v2-af256bc9141eeebb1427c85620b8eb6f_1440w.jpg)

OK！大功告成！

让我们来测试一下。在vault中随便添加一个文件，按照commit-push的顺序操作（可以直接用刚刚设置的快捷键，或使用Obsidian面板），可以看到文件被成功push到github仓库中啦！也可以在github中检查。

![](https://pic2.zhimg.com/v2-320d702a5f5a5dac1aa869947b666bd1_1440w.jpg)

实现多设备同步，只需在另一台机器上进行相同的设置。

### 碎碎念

最开始记笔记是用的[语雀](https://zhida.zhihu.com/search?content_id=234334096&content_type=Article&match_order=1&q=%E8%AF%AD%E9%9B%80&zhida_source=entity)。语雀的好处是操作非常简单易学，傻瓜操作，功能基本也能满足需求，也有自动同步。但是自从工位的workstation换成了Linux，致命bug就出现了——在Linux系统上语雀只能用网页端。没有桌面端我也能忍，但网页笔记加载速度真的太慢了，太卡了ಥ\_ಥ

另一款很火的笔记软件[Notion](https://zhida.zhihu.com/search?content_id=234334096&content_type=Article&match_order=1&q=Notion&zhida_source=entity)很fancy，看了看感觉很适合做杂七杂八的生活小记录，或者小团队/情侣的空间分享，但是依然是辣个致命问题：卡+Linux没有桌面端。

我的基础需求很简单：插入图片方便、可以轻松美观插入代码块（偶尔还有公式）、可以多设备同步、各种操作都不卡、支持linux系统。其他高端的操作（比如双向连接）有更好，没有也可以。

Obsidian的完美就在于：

1.  本地存储，打开和编辑都极其丝滑迅速，而且支持Linux系统！
2.  开源，所以有相当多可用的插件，很多需求都可以通过简单安装个插件解决。
3.  便于迁移。所有文件都以markdown格式保存，笔记直接从文件夹里copy出来放哪都能用。（不像OneNote(╬▔皿▔)╯)
4.  也是我后来发现的——与[Zotero](https://zhida.zhihu.com/search?content_id=234334096&content_type=Article&match_order=1&q=Zotero&zhida_source=entity)笔记的联动极其简单（后面再写一篇介绍联动），Zotero笔记可以直接导出到Obsidian中（且可以自动同步）。  
    

Obsidian唯一的缺点就是同步。官方提供了同步的订阅，但是一个月8刀我感觉对我来说有点贵。最初试了用google drive做同步，直接把vault保存到网盘，但是又是老问题——卡。后来发现Obsidian Git这个宝藏插件，好方便。真心感谢这些开源插件的制作者，仰慕又感动。感觉就像小说里的武林高手！

希望这篇文章可以帮助到世界上某个角落的小朋友，如果有什么问题可以留言~还是要坚持好好分享好的经验，给世界带来真善美！upup！