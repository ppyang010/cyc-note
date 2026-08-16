---
id: "2842865539"
title: "sql in 条件超过 1000 怎么办？"
author: "liuyafei"
type: zhihu-answer
source: "https://www.zhihu.com/question/578354887/answer/2842865539"
created: "2023-01-13 08:02"
updated: "2023-01-13 08:02"
collected: "2023-01-13 08:02"
downloaded: "2026-08-16"
---
三种办法1. 用or 例如：in (a,b,c.....几百条） or in （x,y,z....几百条）

方法2 用union

select \* from table where in (a,b,c.....几百条）

union

select \* from table where （x,y,z....几百条）

方法3

把数据导入表中表名XXX

select \* from table where column in （ select column from xxx）

可自行改写成exist