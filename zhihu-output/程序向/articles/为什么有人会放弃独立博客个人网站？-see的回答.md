---
id: "3461216186"
title: "为什么有人会放弃独立博客（个人网站）？"
author: "see"
type: zhihu-answer
source: "https://www.zhihu.com/question/343334951/answer/3461216186"
created: "2024-04-10 17:33"
updated: "2025-05-22 14:23"
collected: "2024-04-10 17:33"
downloaded: "2026-08-16"
---
欢迎来到我成本200块的个人小站a.luckgirl.top,如果什么时候它挂了，说明个人小站基本不可能了，但至少我钻研的历史还留存于此：

**一、基础&硬件**

**电信10000号申请开通家庭宽带的公网IP**

域名

服务器：J1900处理器(4核4G)

基础成本：.top域名1元+服务器212元=213元

维持成本：.top域名续费28元+服务器电费约43.2元(10w即86.4度电，每度0.5元)=71.2元/年

**二、技术&插件**

服务器系统：linux(ubtun18.04)

服务器接口转发：nginx

前端框架：vue+ElementUI

后端框架：Springboot

后端持久层框架(控制数据库)：Mybatis-plus

后端权限控制：shiro

后端构建工具：maven

数据库：Mysql、redis

数据爬取与处理 python

**外网访问配置**

1、确认已经通过电信10000号申请开通家庭宽带的公网IP

2、路由器设置内外网端口映射

3、DDNS设置

4、服务器定时器：crontab定时设置，触发ddns刷新域名映射

**无80端口自签发https证书**

letsencrypt

**三、工具&软件**

项目部署容器：docker

项目自动化部署工具：jenkins

项目管理工具：gitee

前端编程软件：vscode

后端编程软件：idea

数据库远程连接软件：navicat

服务器远程连接软件：putty

服务器远程传输软件：psftp

> 虽然没流量，但好歹最终可以归纳点架构出来，供后来者借鉴，若有帮助，点个赞，望与诸君共勉

显性URL解析已经挂了，也许部分浏览器可用，但基本都不行了，现在只有这个可用

[https://luckgirl.top:888](https://link.zhihu.com/?target=https%3A//luckgirl.top%3A888/)