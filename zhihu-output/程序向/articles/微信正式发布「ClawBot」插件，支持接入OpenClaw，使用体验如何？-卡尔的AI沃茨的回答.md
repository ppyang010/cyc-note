---
id: "2019725957049659496"
title: "微信正式发布「ClawBot」插件，支持接入OpenClaw，使用体验如何？"
author: "卡尔的AI沃茨"
type: zhihu-answer
source: "https://www.zhihu.com/question/2019397044381376559/answer/2019725957049659496"
created: "2026-03-24 10:43"
updated: "2026-03-24 10:43"
collected: "2026-03-24 10:43"
downloaded: "2026-08-16"
---
本来以为要灰度要ios才能用微信龙虾，结果都不需要，安卓也行，不灰度也行，两步搞定。这个方法是从好朋友@Max那学到的，ios的就先把微信版本更新到最新的8.0.70，安卓的可以等第二步主动触发更新。

更新完成后打开微信，进入【我】-【设置】-【插件】页，就能看到新增的微信ClawBot插件了。还没有的话就完全关掉微信后再打开。

现在就差了OpenClaw了，可以看我之前做的教程，  
🔗 [Clawdbot超级小白入门指南，不靠MacMini和云，安全用上满血版](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s%3F__biz%3DMzg3MTk3NzYzNw%3D%3D%26mid%3D2247504469%26idx%3D1%26sn%3D529c3c44419ee375d0dbb3e2cb389058%26scene%3D21%23wechat_redirect)

也可以省流版，  
用Codex app让GPT5.4根据你的电脑环境来自动安好，配好模型，安装上基本技能，直接用我这提示语，  
'''  
确认我的本地环境，安装最新版本的OpenClaw，然后以对话的方式跟我确认，我目前有哪些大模型的API Key能够接入到OpenClaw里，然后帮我安装这几个Skills，要从Clawhub里面选同名下载量最高的。  
self-imporving-agent（自我迭代）  
skill-creator（技能创造）  
find-skills（发现新技能）  
skills-vetter（保证技能安全）  
automation-workflows（把技能串起来当工作流）  
'''

接下来这步亮点了，不管有没有灰度名额，  
给Openclaw（其他龙虾变体也都可以）发，  
'''  
npx -y @tencent-weixin/openclaw-weixin-cli@latest install  
'''  
出现二维马后用手机微信的扫一扫。  
扫马成功并确认连接后，  
只要看到安装成功的提示就OK。  
安卓版这时候扫马就能升级微信了。

这次的微信Clawbot还是比较初期的阶段。只能单聊不能拉进群聊里，电脑版是用不了的，不能连多个openclaw，不支持流式输出，也没有markdown格式，出的链接基本点不了，没有支持定时任务，如果想要看图看视频的话需要另接skills。

我在线蹲一个能读取合并聊天记录的skills，这功能对我这种一天5k条消息的人太刚需了。

总的来说，  
微信的流量入口还是很大的，  
这下14亿人都能用上了，  
不只有小龙虾，  
Claude Code，OpenCode等都可以接入，  
这波属于是史诗级加强啊！  
在线蹲后续的版本更新。

小彩蛋，

隔壁也是鹅家的Qclaw也更新了微信对话了。