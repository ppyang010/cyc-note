---
Title: "nginx所需"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-08-04 15:42:18"
Cover: ""
WizGuid: "2641db2f-5595-4e07-8a83-8b7abace0131"
WizType: ""
WizLocation: "/工作/浙江宇天/"
WizDataMd5: "a5f6604150e2d94d56fc6f8047da2e84"
Modified: "2016-09-08 17:13:32"
WizSyncedAt: "2026-08-18 18:48:31"
---

find / -name tomcat   查询文件 文件夹

启动

nginx -c /usr/local/nginx/conf/nginx.conf

nginx -c /opt/nginx/conf/nginx.conf

停止操作

停止操作是通过向nginx进程发送信号（什么是信号请参阅linux文 章）来进行的

步骤1：查询nginx主进程号

ps -ef | grep nginx

在进程列表里 面找master进程，它的编号就是主进程号了。

步骤2：发送信号

从容停止Nginx：

kill -QUIT 主进程号

快速停止Nginx：

kill -TERM 主进程号

强制停止Nginx：

pkill -9 nginx

另外， 若在nginx.conf配置了pid文件存放路径则该文件存放的就是Nginx主进程号，如果没指定则放在nginx的logs目录下。有了pid文 件，我们就不用先查询Nginx的主进程号，而直接向Nginx发送信号了，命令如下：

kill -信号类型 '/usr/nginx/logs/nginx.pid'

平滑重启

如果更改了配置就要重启Nginx，要先关闭Nginx再打开？不是的，可以向Nginx 发送信号，平滑重启。

平滑重启命令：

kill -HUP 住进称号或进程号文件路径

或者使用

/usr/nginx/sbin/nginx -s reload

注意，修改了配置文件后最好先检查一下修改过的配置文件是否正 确，以免重启后Nginx出现错误影响服务器稳定运行。判断Nginx配置是否正确命令如下：

nginx -t -c /usr/nginx/conf/nginx.conf

或者

/usr/nginx/sbin/nginx -t
