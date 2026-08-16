---
id: "3213863207"
title: "一般大家怎么部署java项目，要不要部署在docker里？"
author: "二环狄仁杰"
type: zhihu-answer
source: "https://www.zhihu.com/question/615138190/answer/3213863207"
created: "2023-09-16 17:48"
updated: "2023-09-16 17:48"
collected: "2023-09-16 17:48"
downloaded: "2026-08-16"
---
我的做法是打包成docker image上传到阿里云免费的仓库里，然后把docker-compose.yml复制到服务器上，执行up就启动了。

改了代码要更新，打包新的image传到阿里云仓库，服务器上执行pull & up就可以了，非常方便。