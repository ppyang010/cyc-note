---
title: changedetection.io：网页变动监控工具速览
date: 2026-10-23
tags:
  - 工具/监控
  - AI/Agent
  - 自动化
aliases:
  - changedetection.io
  - 网页盯盘外挂
summary_model: DeepSeek-V4.1-Flash
source_type: 微信公众号图片消息
author: 公众号「zippic」
original_title: 不少搞监控降价、抢票和抓羊毛的佬都在偷着用这个工具
source: https://mp.weixin.qq.com/s/-4OpvCLZiKKYnvNtvuocdw
published: 2026-08-06
---

# changedetection.io：网页变动监控工具速览

> [!abstract] 来源与整理说明
> 原文是公众号「zippic」的一条微信**图片消息**（发布地广东，8月6日），原文标题为《不少搞监控降价、抢票和抓羊毛的佬都在偷着用这个工具》，本笔记标题为按内容重拟。
> **总结模型：DeepSeek-V4.1-Flash**；正文按原文提取，未经改写。
> 这类「图片消息」的正文图不在 `#js_content` 里，提取脚本的 `imageCount` 会误报为 0；图是我事后从渲染后的页面补下的，已存本地 `ai-output/assets/changedetection-io/01.png`。
> 原文为推荐性质的短文，未提供实测数据；文中 Star 数、模型支持等均为作者转述，未逐项核实。

## 目录

- [[#一、核心定位]]
- [[#二、五项核心能力]]
- [[#三、典型使用场景]]
- [[#四、为什么值得关注]]
- [[#五、对我的可用性判断]]

## 一、核心定位

`changedetection.io` 是一个已获 **32.6k Star** 的开源网页变动监控工具，原文称之为"全网网页盯盘外挂"。

它的基本逻辑很朴素：盯住某个网页，只要内容变动哪怕一个字，就推送通知。真正的差异在于——新版直接接了 AI（支持 **GPT-4o-mini**、**Ollama 本地大模型**），不再只报"网页变了"，而是能归纳出"降了 50 块""新增了某某功能"这类结论，并且可以用自然语言写规则来过滤噪音。

![[ai-output/assets/changedetection-io/01.png]]
*原文配图 · 官网首页截图（RELEASE v0.55.8 / DOCKER PULLS 11M / LICENSE Apache-2.0）。图中演示的是「Add a new web page change detection watch」：填入 URL 后可选 **Restock & Price**（单品补货+降价）或 **Webpage Text/HTML, JSON and PDF changes** 两种模式；下方列表逐条列出监控项、当前价格、上次检查时间，右侧是 Recheck / Edit / Preview 操作。*

## 二、五项核心能力

| 能力        | 说明                          |
| --------- | --------------------------- |
| 可视化画框监控   | 鼠标点选页面区域，只监视关心的部分，自动跳过广告与页脚 |
| AI 智能去噪摘要 | 接入免费模型，只推送真正关心的变动细节         |
| 通知通道      | 微信、钉钉、Telegram、Discord、邮件   |
| 自动模拟点击    | 自动登录、自动点同意 Cookie、自动翻页后再监控  |
| 本地私有化部署   | Docker 一键拉起，数据完全自持          |

最后一条对长期使用很关键：AI 摘要通常意味着内容要出网，能自部署 + 本地 Ollama 才谈得上数据不外流。

## 三、典型使用场景

- 商品降价、库存补货提醒
- 网页静默改版、条款悄悄打补丁的取证
- 微博 / 推文被删的痕迹留存
- 抢票、抓羊毛类信息的时间窗监控

## 四、为什么值得关注

它解决的是"人不可能一直刷新页面"这个古老问题，但价值点已经从**检测**迁移到了**解读**：

1. 检测层面几乎无门槛，同类工具很多；
2. 真正的成本在"变动通知太多，人懒得看"——AI 摘要直接把这个成本砍掉了；
3. 自然语言规则降低了配置门槛，不需要写 XPath / CSS selector 逻辑。

## 五、对我的可用性判断

和我现有的「考试 API 监控 + 微信推送」自动化线路有直接可比性。差异在于：

- 我那条线是**接口级**监控（JSON 字段变化），精准但需要知道接口；
- changedetection.io 是**页面级**监控，无需接口，适合对方不提供 API、或接口带签名难复现的场景；
- 它自带微信通知通道和 Docker 部署，等于把"抓取 + 判断 + 推送"三段打了个包。

可以把它当作接口监控失效时的兜底方案：接口拿不到时就退回页面监控 + AI 摘要。

---
原文链接：https://mp.weixin.qq.com/s/-4OpvCLZiKKYnvNtvuocdw
