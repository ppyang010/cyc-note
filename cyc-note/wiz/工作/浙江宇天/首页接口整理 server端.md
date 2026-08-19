---
Title: "首页接口整理 server端"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-07-05 14:09:52"
Cover: ""
WizGuid: "5e0ac999-b224-47bf-a576-e5b8c50c2f38"
WizType: "document"
WizLocation: "/工作/浙江宇天/"
WizDataMd5: "3ee0b224d65ff025419b9ea62bfe836e"
Modified: "2017-07-06 14:36:45"
WizSyncedAt: "2026-08-18 18:48:31"
---

## 目录

getContentClass查询内容一级分类列表接口
getBannerInfo查询banner
getRecommedList查询推荐内容列表
查询独家分类下内容列表
getContentIdList 查询分类下内容列表接口

getContentInfoById查询内容信息接口
getUserAttitudeList 获取用户顶踩列表
updateUserAttitude 更新顶踩数据
addUsFavorite 添加收藏接口
addDownloadLog 记录下载日志
getDownloadUrl获取视频下载地址接口
getVideoDownloadFee获取下载价格接口

## ---

##

## getContentClass查询内容一级分类列表接口

请求消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| classId | Request | String | 0..1 | 分类ID |

响应消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentClassInfo | Response | List<ContentClassInfo> | 1 | 内容分类列表 |
| totalCount |  | int | 1 | 总数 |
|  |  |  |  |  |

ContentClassInfo实体

| classId | ContentClassInfo | String | 0..1 | 分类ID |
| --- | --- | --- | --- | --- |
| className | ContentClassInfo | String | 0..1 | 分类名称 |
| parentClassId | ContentClassInfo | String | 0..1 | 父分类编码 |
| classLevel | ContentClassInfo | String | 0..1 | 级别深度 |

---

## getBannerInfo查询banner

请求消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| portalType |  | String | 1 | 门户类型 |
| count |  | int | 0..1 | 需要获取的数量 |
| bannerType |  | String | 0..1 | 获取的banner类型, 为空代表查询全部类型 |

响应消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| bannerInfos |  | List<BannerInfo> | 1 |  |
|  |  |  |  |  |

BannerInfo实体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| bannerID |  | long | 1 | id |
| type |  | String | 1 | 类型 1，视频，2，链接，3，页面 |
| bigURL |  | String |  | 大图url |
| miniURL |  | String |  | basewapurl |
| param |  | String |  | 类型为1时为contentid，类型为2时空，类型为3时可以填写plans |
| title |  | String |  | 显示标题 |
| needlogin |  | String |  | 是否需要登录, 0:不需要 , 1:需要 |
| cutBigUrl |  | String |  | basewap 首页banner展示图片 |

---

## getRecommedList查询推荐内容列表

请求消息题

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| identityId | Request | String | 0..1 | 用户标识 |
| portalType | Request | String | 1 | 门户类型 |

响应消息提

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentIds | Response | List<Long> | 1 | 内容ID列表 |

---

## 查询独家内容列表

请求消息题

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| portalType | Request | String | 1 | 门户类型 |

响应消息提

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentIds | Response | List<Long> | 1 | 内容ID列表 |

---

## getContentIdList 查询分类下内容列表接口

请求消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| classId | Request | String | 1 | 分类ID |
| descType | Request | Integer | 1 | 内容标志：0时间，1访问量，2收藏次数，3评分人数，4内容总分 |
| start | Request | String | 1 | 起始页 |
| count | Request | String | 1 | 每页条数 |
| portalType | Request | String | 1 | 门户类型 |

响应消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentIds | Response | List<Long> | 1 | 内容ID列表 |
| totalcount | Response | Integer | 1 | 内容列表数量 |

---

## getContentInfoById查询内容信息接口

请求

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentId | Request | String | 1 | 内容ID |
| portalType | Request | String | 1 | 门户类型 |

响应

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| contentInfo | Response | ContentInfo | 1 | 内容列表 |
|  |  |  |  |  |
|  |  |  |  |  |
| contentInfo | 内容实体 |  |  |  |
| contentid | ContentInfo | String | 0..1 | 内容标识 |
| name | ContentInfo | String | 0..1 | 内容名称 |
| score | ContentInfo | int | 0..1 | 评分 |
| scoreCount | ContentInfo | int | 0..1 | 参与评分的人数 |
| chargeMode | ContentInfo | String | 0..1 | 收费方式 0,免费 1,登录免费 2,VIP免费 |
| searchCode | ContentInfo | String | 0..1 | 关键字 |
| contentClass | ContentInfo | String | 0..1 | 分类ID |
| authorId | ContentInfo | String | 0..1 | 作者ID |
| createDate | ContentInfo | String | 0..1 | 上传时间 |
| mcpId | ContentInfo | String | 0..1 | MCPID |
| authorName | ContentInfo | String | 0..1 | 作者名 |
| recommendReason | ContentInfo | String | 0..1 | 视频简介 |
| wwwDescription | ContentInfo | String | 0..1 | 备注 |
| smallLogo | ContentInfo | String | 0..1 | 封面小图 |
| middleLogo | ContentInfo | String | 0..1 | 封面中图 |
| bigLogo | ContentInfo | String | 0..1 | 封面大图 |
| favoriteCount | ContentInfo | String | 0..1 | 内容被收藏的次数 |
| videotime | ContentInfo | Long | 0..1 | 视频时长 |
| viewCount | ContentInfo | Integer | 0..1 | 访问人次 |
| contentUploadTime | ContentInfo | String | 0..1 | 内容上传时间 |
| likeCount | ContentInfo | Integer | 0..1 | 顶人数 |
| unlikeCount | ContentInfo | Integer | 0..1 | 踩人数 |
| fileSize |  | int | 0..1 | 视频大小 |
| actorList |  | ActorInfo | 0..1 | 演员列表 |

ActocInfo 实体（暂订）

| **字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- |
| actorId | String | 1 |  |
| actorName | String |  |  |
| actorPicture | String |  |  |
|  |  |  |  |

---

## getUserAttitudeList 获取用户顶踩列表

请求消息提

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| identityId | Request | String | 1 | 用户标识 |
| type | Request | String | 1 | 内容类型 1：评论 2：内容+ |
| attitude | Request | String | 1 | 态度标识 1：顶 2：踩 |
| portalType | Request | String | 1 | 门户类型 |

响应消息题

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| resultIdList | Response | List<String> | 1 | ID列表 |

---

## updateUserAttitude 更新顶踩数据

请求消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| identityId | Request | String | 1 | 用户标识 |
| targetId | Request | String | 1 | 内容Id 或评论id |
| type | Request | String | 1 | 内容类型 1：评论 2：内容 |
| attitude | Request | String | 1 | 态度标识 1：顶 2：踩<br>0：<br>取消顶踩 |
| portalType | Request | String | 1 | 门户类型 |

响应消息体

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |

---

## addDownloadLog 记录下载日志

请求

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| identityId | Request | String | 1 | 用户标识 |
| contentId | Request | String | 1 | 内容ID |
| ip | Request | String | 1 | 用户IP |
| agent | Request | String | 1 | 用户浏览器agent |
| codingCode | Request | String | 1 | 码率 |
| portalType | Request | String | 1 | 门户类型 |

响应

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |

---

## getDownloadUrl获取下载地址接口

请求

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| portalType | Requset | String | 1 | 门户类型 |
| codingCode | Requset | String | 0..1 | 每页条数 |
| identityId | Requset | String | 1 | 门户唯一标识 |
| conetentId | Requset | String | 1 | 内容id |
|  |  |  |  |  |

响应

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| playUrl | Response | String | 1 | 下载地址 |
| expiredTime | Response | long | 1 | 失效时间 |
| urlParam | Response | String | 1 | 地址参数 |
| uuid | Response | String | 1 |  |

---

## getVideoDownloadFee获取下载价格接口

响应

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| OriginalPriceCode | Response | String | 1 | 原价码 |
| OriginalPrice | Response | String | 0..1 | 原价 |
| DiscountPriceCode | Response | String | 1 | 优惠码 |
| DiscountPrice | Response | String | 0..1 | 优惠价 |

---

## videoViewLog 播放视频接口

请求

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| identityId | Request | String | 1 | 用户标识 |
| contentId | Request | String | 1 | 内容ID |
| ip | Request | String | 1 | 用户IP |
| agent | Request | String | 1 | 用户浏览器agent |
| codingCode | Request | String | 1 | 码率 |
| portalType | Request | String | 1 | 门户类型<br>来源： [http://192.168.101.167:8090/pages/viewpage.action?pageId=1179875](http://192.168.101.167:8090/pages/viewpage.action?pageId=1179875) |

响应

| **字段名** | **父字段名** | **字段类型** | **出现次数** | **描述** |
| --- | --- | --- | --- | --- |
| playUrl | Response | String | 0..1 | 播放地址 |
| expiredTime | Response | Long | 0..1 | 过期时间 |
| urlParam | Response | String | 0..1 | 网址参数 |
