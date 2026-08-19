---
Title: "jfina demol 包的注释"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags:
  - "jFinal"
Created: "2015-09-21 22:24:44"
Cover: ""
WizGuid: "539937d0-ff86-448e-a1c9-e078b557f51f"
WizType: ""
WizLocation: "/工作/工作日记/"
WizDataMd5: "557f2dd0c569794a17d60b0feb619dde"
Modified: "2015-09-21 22:33:51"
WizSyncedAt: "2026-08-18 18:48:31"
---

![[attachments/ScreenClip.png]]

1. 是数据库链接池
2. 上传文件
3. jsp页面tl语句的使用  支持jsp视图
4. jetty-server-8.1.8.jar 用来支持无需额外安装 tomcat jetty 等 web server
      即可开始开发，同时它也是支持热部署的必要包。特别注意在使用tomcat开发或部署时需要去掉 jetty-server-8.1.8.jar 包，以免引起冲突
5. jfinal 2.0 开发包 + 源码 的整合，方便非 maven 开发者在开发时调试和查看源码，从而不用再单独绑定 jfinal-2.0-src.zip 就可以在 IDE 中查看源码
6. 开发 jfinal 项目唯一必须的 jar 包，其它所有 jar 包都不是必须的
7. 日志文件
8. 数据库操作使用
9. 支持jsp视图 同3   应一起使用
