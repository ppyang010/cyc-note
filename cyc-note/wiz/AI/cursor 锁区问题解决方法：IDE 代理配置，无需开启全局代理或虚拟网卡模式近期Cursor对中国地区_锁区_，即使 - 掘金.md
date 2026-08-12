---
Title: "cursor 锁区问题解决方法：IDE 代理配置，无需开启全局代理或虚拟网卡模式近期Cursor对中国地区\"锁区\"，即使 - 掘金.md"
Url: "https://juejin.cn/post/7529020018618695730"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2026-01-05 17:52:42"
Cover: ""
WizGuid: "4715f2d0-ea1c-11f0-83e2-8fc20612ab3f"
WizType: ""
WizLocation: "/AI/"
WizDataMd5: "ea6015c26b6c0d3954498deb0c5ef2a5"
Modified: "2026-01-05 17:52:42"
WizSyncedAt: "2026-08-12 14:23:17"
---

[cursor 锁区问题解决方法：IDE 代理配置，无需开启全局代理或虚拟网卡模式近期Cursor对中国地区"锁区"，即使 - 掘金](https://juejin.cn/post/7529020018618695730)

 ### 前言

近期Cursor对中国地区"锁区"，即使付费会员也无法继续使用Claude，gpt等模型，官方给了退款入口，但如果想继续使用，只能通过一些代理方式绕过锁区。 `Model not available. This model provider doesn't serve your region`

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/374dbad4ed05495dabc6a989a7f9407c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=TDPHu71WUykKUJo1%2FOqrZFTPF%2F4%3D)

网上主流的方法是开启🪜虚拟网卡模式，但是这种全局代理模式，会导致开发环境，测试域名等均不能正常访问，配置白名单也没有效果。

通过测试多种方案找到一个目前比较完美的解决方案。通过IDE代理配置实现Cursor的正常使用，无需开启全局代理或虚拟网卡模式。这种方法简单高效，只需几步配置即可解决问题，特别适合那些只需要在Cursor中使用代理，而不想影响其他网络活动的开发者。

### 配置流程

#### cmd+shift+p: 搜索open user settins(json)

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/5d943f93b32f4699adec169d190c055c~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=l5UMCJlTku1pjDbzL1G3ymJhYuQ%3D)

#### 添加以下配置，代理地址需要从自己🪜获取

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4e20bf7719234272aea6b7f3c7d14d89~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=2UXWKiupLR0Viv8rhVl9T7XWwIc%3D)

#### 配置文件

```json

    "http.proxy": "http://127.0.0.1:7897",
    "http.proxyStrictSSL": false,
    "http.proxySupport": "override",
    "http.noProxy": [],
    "cursor.general.disableHttp2": true

```

### 启动代理软件

（实测：不需要全局代理，不需要开启虚拟网卡模式）

**注意：🪜节点要选海外节点，香港地区也在锁区范围内**

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3d1b5839b4974d6db72de58f36711c3b~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=epPIiqtvSG5W10jvWkK8GnA0yjQ%3D)

### 测试结果

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/11e9d3ba05994bd58fc8ddbfeaef92b0~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=HeV4uFzozHkGWLM7PXtwqqIdiBw%3D)

### 补充配置：network配置：将http2 替换为 http1.1

![](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/3ab9eaa10bea46c49cc585aadfeb9a90~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5ZKa5ZKa5ZKaZGRk:q75.awebp?rk3s=f64ab15b&x-expires=1767665805&x-signature=yiHs53h2SjQ0GZzCBiPhX2zUkhw%3D)
