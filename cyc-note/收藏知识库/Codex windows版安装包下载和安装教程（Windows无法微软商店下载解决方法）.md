---
Title: Codex windows版安装包下载和安装教程（Windows无法微软商店下载解决方法）
Url: "https://blog.csdn.net/weixin_41961749/article/details/160064919"
Author: weixin_41961749
Origin: weixin_41961749
Description: 文章浏览阅读1.9w次，点赞54次，收藏47次。最近在折腾 GPT 官方推出的Codex，准备在 Windows 电脑上体验一下本地客户端。微软商店无法下载，直接提示应用不可用。折腾了一圈后，我用另一台能正常访问微软商店的电脑把安装包拷贝出来，最终成功安装。为了节省大家时间，这里把完整过程记录下来，并把安装包分享出来，方便有需要的人自行使用。这次折腾的核心结论：微软商店只是分发渠道，并不是必须环境。通过提取安装文件，Windows 依然可以正常使用 Codex。如果你也被微软商店卡住，这个方法可以直接解决问题。_codex下载不了
Tags:
  - Codex
  - Codex windows版
  - codex安装包
  - codex.exe
  - codex安装包下载
  - Codex下载
  - Codex安装包
Created: "2026-05-11 17:04:09"
Cover: "https://csdnimg.cn/release/blogv2/dist/pc/img/newHeart2023Active.png"
---
## Codex windows版安装包下载和 安装教程 （Windows无法微软商店下载解决方法）

**关键词：Codex安装包、Codex下载、Windows安装Codex、微软商店无法下载应用、GPT Codex 安装教程**

---

### 前言

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/b622a4249699495398f4cbb9823349d1.png)

最近在折腾 GPT 官方推出的 **Codex**，准备在 Windows 电脑上体验一下本地客户端。  
结果第一步就被卡住： **微软商店无法下载**，直接提示应用不可用。

折腾了一圈后，我用另一台能正常访问微软商店的电脑把安装包拷贝出来，最终成功安装。为了节省大家时间，这里把完整过程记录下来，并把安装包分享出来，方便有需要的人自行使用。

---

### Codex Windows 安装包下载

安装包已整理好，可直接下载使用：

👉 下载地址  
[https://pan.quark.cn/s/c1674162f4f9](https://pan.quark.cn/s/c1674162f4f9)

下载后解压即可看到完整安装文件。

### 遇到的问题

在 GPT 官网下载 Codex 时，Windows 版本会跳转到 **Microsoft Store**。  
但很多人会遇到以下情况：

- 打不开微软商店
- 商店无法登录
- 提示“此应用在你的地区不可用”
- 点击安装无反应

本质原因很简单：  
Codex Windows 客户端 **只提供微软商店分发**，没有直接的 exe 安装包。

这就导致很多开发者卡在第一步。

---

### 解决 思路

既然微软商店能安装，说明本质上 **本地一定存在安装包**。

思路非常直接：

1. 在能正常下载的电脑安装 Codex
2. 从系统中提取安装包
3. 拷贝到目标电脑安装

我已经帮大家完成了这一步。

---

### Codex Windows 安装包下载

安装包已整理好，可直接下载使用：

👉 下载地址  
[https://pan.quark.cn/s/c1674162f4f9](https://pan.quark.cn/s/c1674162f4f9)

下载后解压即可看到完整安装文件。

---

### Windows 安装步骤

#### 第一步：运行安装包

如果运行不了安装包 则使用这个办法  
以管理员身份运行 PowerShell。

Powershell 运行以下 部署 命令(路径改成你安装包的路径)：

```
Add-AppxPackage -Path ".\OpenAI.Codex_26.304.1528.0_x64__2p2nqsd0c76g0.msix" 
1
```

---

#### 第三步：运行 Codex

打开主程序：

双击即可启动。

首次启动需要登录 GPT 账号。

---

### 成功运行效果

启动后即可看到 Codex 主界面，可以直接进行：

- AI 编程
- 项目生成
- 代码解释
- 自动补全

体验和官方商店安装版一致。

---

### 常见问题

#### 运行时报错 code=3221225781

[Codex客户端运行时报错 code=3221225781 的解决方法（Windows）](https://blog.csdn.net/weixin_41961749/article/details/160674108)

#### 报错 错误 0x8007177E:

在终端输入下面命令重启电脑就行。

```bash
fsutil behavior set disableencryption 0
bash1
```

#### Q1：是否需要微软商店？

不需要。该安装包已脱离商店，可直接运行。

#### Q2：是否会自动更新？

不会自动更新，需要后续手动更新版本。

#### Q3：是否和官方版本一致？

来源于微软商店安装文件，功能一致。

---

### 总结

这次折腾的核心结论：

微软商店只是 **分发渠道**，并不是必须环境。  
通过提取安装文件，Windows 依然可以正常使用 Codex。

如果你也被微软商店卡住，这个方法可以直接解决问题。

后续如果 Codex 有大版本更新，我会再同步新的安装包与安装方法。

![](https://i-blog.csdnimg.cn/direct/e1f8d95739bc4452bfde90b9680f811c.png)

代码简单说 扫码关注公众号"代码简单说" 获取资源教程

![](https://g.csdnimg.cn/extension-box/2.0.3/image/weixin.png) 微信公众号

![](https://g.csdnimg.cn/extension-box/2.0.3/image/ic_move.png)