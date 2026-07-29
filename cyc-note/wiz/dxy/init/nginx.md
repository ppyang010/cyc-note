---
Title: "nginx"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-11-02 12:16:56"
Cover: ""
WizGuid: "83393e47-1795-4e64-b16d-3a595a84dd7f"
WizType: ""
WizLocation: "/dxy/init/"
WizDataMd5: "7bb9281b495603297106189cba43eb02"
Modified: "2017-11-03 09:25:42"
WizSyncedAt: "2026-07-29 15:36:28"
---

目录为

/usr/local/etc/nginx

```
1、Mac下Nginx的启动：
```

```
[code]cd usr/local/nginx/sbin
sudo ./nginx
```

[/code]

```
2、Mac下判断配置文件是否正确
```

```
cd  /usr/local/nginx/sbin
sudo ./nginx -t
```

```
3、Mac下重启Nginx
```

```
cd /usr/local/nginx/sbinsudo ./nginx -s reload
```

```
4、Mac下Nginx的关闭
```

```
查询nginx主进程号：ps -ef|grep nginx
```

```

```

```
正常停止   sudo kill -QUIT 主进程号快速停止   sudo kill -TERM 主进程号
```
