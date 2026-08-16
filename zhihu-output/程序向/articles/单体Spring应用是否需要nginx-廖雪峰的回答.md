---
id: "3150595697"
title: "单体Spring应用是否需要nginx?"
author: "廖雪峰"
type: zhihu-answer
source: "https://www.zhihu.com/question/609079086/answer/3150595697"
created: "2023-08-04 22:57"
updated: "2023-08-04 22:57"
collected: "2023-08-04 22:57"
downloaded: "2026-08-16"
---
## 需要。

Java应用要专注于业务，虽然Java服务器也提供各种全面的功能，但比不上更专业的nginx：

https证书：nginx配置更简单；

一组host：nginx配置更简单；

限流：nginx配置更简单；

限ip：nginx配置更简单；

静态文件：nginx可缓存；

http2：nginx支持，内部转http1.x到tomcat；

http3：nginx支持，内部转http1.x到tomcat；

临时重定向url：nginx改配置reload不重启；

遇到500错误：nginx可重试；

很多cors、自定义header配置、www.example.com转example.com放nginx不用改java应用。

核心思想是利用nginx强大的配置能力，避免改配置反复部署java应用。