---
Title: "abTest 接入"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2023-02-27 11:08:10"
Cover: ""
WizGuid: "3590269c-6ac5-4f2e-befa-867049cc04b8"
WizType: "TemplateNote"
WizLocation: "/dxy/init/"
WizDataMd5: "71c67aa3644d50a265cd9a443ccfa05c"
Modified: "2023-02-27 11:24:06"
WizSyncedAt: "2026-07-29 15:36:28"
---

yml

新增配置项

abtest: enable: true template-path-regex: ^((/web/.*)|(/))$

```
xxxxxxxxxx
```

1

```
abtest:
```

2

```
  enable: true
```

3

```
  template-path-regex: ^((/web/.*)|(/))$
```

根据不同环境使用不同的授权码

abtest: auth-code: 8nAGXNfk

```
xxxxxxxxxx
```

1

```
abtest:
```

2

```
  auth-code: 8nAGXNfk
```

![[attachments/40241825.png]]

前端打点标识  根据下方目录

https://wiki.dxy.net/pages/viewpage.action?pageId=87065534
