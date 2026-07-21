---
Title: "本地源码关联远程服务器调试代码 - java_min的专栏 - 博客频道 - CSDN.NET"
Url: "http://blog.csdn.net/java_min/article/details/9497943"
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-07-06T16:14:00+08:00"
Cover: ""
WizGuid: "1adc81f9-d5d9-4fa6-8982-19f2cc43d5c5"
WizType: ""
WizLocation: "/开发工具/"
WizDataMd5: "277fc9b379162ddf8e60d81f973d04da"
Modified: "2016-07-06T16:14:00+08:00"
WizSyncedAt: "2026-07-21T15:18:27+08:00"
---

[http://www.csdn.net/?ref=toolbar](http://www.csdn.net/?ref=toolbar)[http://blog.csdn.net/?ref=toolbar_logo](http://blog.csdn.net/?ref=toolbar_logo).

- [登录](https://passport.csdn.net/account/login?ref=toolbar)|[注册](http://passport.csdn.net/account/mobileregister?ref=toolbar&action=mobileRegister)
-
-

## [java_min的专栏](http://blog.csdn.net/java_min)

###

- [目录视图](http://blog.csdn.net/java_min?viewmode=contents)
- [摘要视图](http://blog.csdn.net/java_min?viewmode=list)
- [订阅](http://blog.csdn.net/java_min/rss/list)
 .

# [本地源码关联远程服务器调试代码](http://blog.csdn.net/java_min/article/details/9497943)

 .

2013-07-26 16:49 1530人阅读  [评论](http://blog.csdn.net/java_min/article/details/9497943#comments)(0)  [收藏](#)  [举报](http://blog.csdn.net/java_min/article/details/9497943#report)

 .

![[attachments/category_icon.jpg]] 分类：

It*（186）* ![[attachments/1db119b0089be63f5674c35ec53f1d8f.jpg]]

 .

版权声明：本文为博主原创文章，未经博主允许不得转载。

1. 在tomcat下的catalina.bat中添加如下内容：

set JAVA_OPTS=-server -Xdebug -Xnoagent -Djava.compiler=NONE -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8000

2. 在eclipse中进行如下设置：

a. 点击一下三角符号

![[attachments/SouthEast.jpg]]

b. debug configurations... 出现如下界面：

![[attachments/SouthEast.jpg]]

c. 右击 Remote Java Application ---> new 出现如下窗口：

![[attachments/SouthEast.jpg]]

d. 标号1处为选择我们需要远程调试的项目的源代码，标号2出为远程服务器的地址及端口号（即：tomcat）

e. 点击debug完成

f. 在我们eclipse中的源码中打上断点，再去执行就可以debug调试了。

[http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) [http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) [http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) [http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) [http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) [http://blog.csdn.net/java_min/article/details/9497943#](http://blog.csdn.net/java_min/article/details/9497943#) .

**顶**
 : 1

**踩**
 : 0

 .

[#](#)

[#](#)

- 上一篇[解决tomcat6.0.33 配置SSL时报“No Certificate file specified or invalid file format”异常](http://blog.csdn.net/java_min/article/details/9344619)
- 下一篇[webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815)

#### 我的同类文章

**It*（186）***

- *•*[mysql远程访问](http://blog.csdn.net/java_min/article/details/28417663)2014-06-04*阅读***254**
- *•*[禁止浏览器缓存](http://blog.csdn.net/java_min/article/details/19413777)2014-02-18*阅读***288**
- *•*[在任意bean中获取spring上下文集合](http://blog.csdn.net/java_min/article/details/17628511)2013-12-28*阅读***1058**
- *•*[struts2中的常量](http://blog.csdn.net/java_min/article/details/17219741)2013-12-09*阅读***508**
- *•*[BigDecimal value is always zero when transfered with spring remoting via hessian](http://blog.csdn.net/java_min/article/details/16826731)2013-11-19*阅读***1137**
- *•*[win7 64位 开机密码忘记](http://blog.csdn.net/java_min/article/details/12611749)2013-10-11*阅读***1358**

- *•*[error at ::0 can't find referenced pointcut..](http://blog.csdn.net/java_min/article/details/19507199)2014-02-19*阅读***1735**
- *•*[文件遍历，递归消除](http://blog.csdn.net/java_min/article/details/18056117)2014-01-09*阅读***327**
- *•*[通过 ServletContext 获取 WebApplicationContext](http://blog.csdn.net/java_min/article/details/17615237)2013-12-27*阅读***470**
- *•*[struts2中的默认值](http://blog.csdn.net/java_min/article/details/17166843)2013-12-06*阅读***329**
- *•*[java 加密中的注意事项](http://blog.csdn.net/java_min/article/details/15498991)2013-11-12*阅读***376**
 [更多文章](http://blog.csdn.net/java_min/article/category/541173)

**猜你在找**

查看评论

暂无评论

您还没有登录,请[[登录]](#)或[[注册]](http://passport.csdn.net/account/register?from=http%3A%2F%2Fblog.csdn.net%2Fjava_min%2Farticle%2Fdetails%2F9497943)

* 以上用户言论只代表其个人观点，不代表CSDN网站的观点或立场

##### [核心技术类目](http://www.csdn.net/tag/)

[全部主题](http://www.csdn.net/tag) [Hadoop](http://g.csdn.net/5272865) [AWS](http://g.csdn.net/5272866) [移动游戏](http://g.csdn.net/5272870) [Java](http://g.csdn.net/5272871) [Android](http://g.csdn.net/5272872) [iOS](http://g.csdn.net/5272873) [Swift](http://g.csdn.net/5272868) [智能硬件](http://g.csdn.net/5272869) [Docker](http://g.csdn.net/5272867) [OpenStack](http://g.csdn.net/5272925) [VPN](http://www.csdn.net/tag/vpn) [Spark](http://g.csdn.net/5272924) [ERP](http://www.csdn.net/tag/erp) [IE10](http://www.csdn.net/tag/ie10) [Eclipse](http://www.csdn.net/tag/eclipse) [CRM](http://www.csdn.net/tag/crm) [JavaScript](http://www.csdn.net/tag/javascript) [数据库](http://www.csdn.net/tag/%E6%95%B0%E6%8D%AE%E5%BA%93) [Ubuntu](http://www.csdn.net/tag/ubuntu) [NFC](http://www.csdn.net/tag/nfc) [WAP](http://www.csdn.net/tag/wap) [jQuery](http://www.csdn.net/tag/jquery) [BI](http://www.csdn.net/tag/bi) [HTML5](http://www.csdn.net/tag/html5) [Spring](http://www.csdn.net/tag/spring) [Apache](http://www.csdn.net/tag/apache) [.NET](http://www.csdn.net/tag/.net) [API](http://www.csdn.net/tag/api) [HTML](http://www.csdn.net/tag/html) [SDK](http://www.csdn.net/tag/sdk) [IIS](http://www.csdn.net/tag/iis) [Fedora](http://www.csdn.net/tag/fedora) [XML](http://www.csdn.net/tag/xml) [LBS](http://www.csdn.net/tag/lbs) [Unity](http://www.csdn.net/tag/unity) [Splashtop](http://www.csdn.net/tag/splashtop) [UML](http://www.csdn.net/tag/uml) [components](http://www.csdn.net/tag/components) [Windows Mobile](http://www.csdn.net/tag/windowsmobile) [Rails](http://www.csdn.net/tag/rails) [QEMU](http://www.csdn.net/tag/qemu) [KDE](http://www.csdn.net/tag/kde) [Cassandra](http://www.csdn.net/tag/cassandra) [CloudStack](http://www.csdn.net/tag/cloudstack) [FTC](http://www.csdn.net/tag/ftc) [coremail](http://www.csdn.net/tag/coremail) [OPhone](http://www.csdn.net/tag/ophone) [CouchBase](http://www.csdn.net/tag/couchbase) [云计算](http://www.csdn.net/tag/%E4%BA%91%E8%AE%A1%E7%AE%97) [iOS6](http://www.csdn.net/tag/iOS6) [Rackspace](http://www.csdn.net/tag/rackspace) [Web App](http://www.csdn.net/tag/webapp) [SpringSide](http://www.csdn.net/tag/springside) [Maemo](http://www.csdn.net/tag/maemo) [Compuware](http://www.csdn.net/tag/compuware) [大数据](http://www.csdn.net/tag/%E5%A4%A7%E6%95%B0%E6%8D%AE) [aptech](http://www.csdn.net/tag/aptech) [Perl](http://www.csdn.net/tag/perl) [Tornado](http://www.csdn.net/tag/tornado) [Ruby](http://www.csdn.net/tag/ruby) [Hibernate](http://www.csdn.net/hibernate) [ThinkPHP](http://www.csdn.net/tag/thinkphp) [HBase](http://www.csdn.net/tag/hbase) [Pure](http://www.csdn.net/tag/pure) [Solr](http://www.csdn.net/tag/solr) [Angular](http://www.csdn.net/tag/angular) [Cloud Foundry](http://www.csdn.net/tag/cloudfoundry) [Redis](http://www.csdn.net/tag/redis) [Scala](http://www.csdn.net/tag/scala) [Django](http://www.csdn.net/tag/django) [Bootstrap](http://www.csdn.net/tag/bootstrap)

- [It](http://blog.csdn.net/java_min/article/category/541173)(187)

- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815)(23829)
- [DB2 SQL error: SQLCODE: -302, SQLSTATE: 22001, SQLERRMC: null](http://blog.csdn.net/java_min/article/details/5720431)(23664)
- [jstl 格式化时间日期标签讲解](http://blog.csdn.net/java_min/article/details/5953957)(20004)
- [session销毁](http://blog.csdn.net/java_min/article/details/4256942)(12853)
- [linux 服务器之间拷贝文件](http://blog.csdn.net/java_min/article/details/8591516)(12847)
- [spring事务管理](http://blog.csdn.net/java_min/article/details/4427523)(11472)
- [Server Tomcat v6.0 Server at localhost was unable to start within 45 seconds...](http://blog.csdn.net/java_min/article/details/7884857)(8636)
- [查询数据库当前连接数(session)，进程数等操作](http://blog.csdn.net/java_min/article/details/8501699)(7929)
- [ASCII与中文互转](http://blog.csdn.net/java_min/article/details/7898934)(7263)
- [Cannot forward after response has been committed 异常](http://blog.csdn.net/java_min/article/details/5262518)(5956)

- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815)(46)
- [java中的文件上传及下载组件介绍](http://blog.csdn.net/java_min/article/details/4223402)(6)
- [spring事务管理](http://blog.csdn.net/java_min/article/details/4427523)(4)
- [JVM调优浅谈](http://blog.csdn.net/java_min/article/details/8349721)(3)
- [DB2 SQL error: SQLCODE: -302, SQLSTATE: 22001, SQLERRMC: null](http://blog.csdn.net/java_min/article/details/5720431)(3)
- [Windows下访问VMware中tomcat](http://blog.csdn.net/java_min/article/details/8458654)(2)
- [poi 和jxl的性能比较，借鉴别人的，本人没有测试过，不过感觉自己可以接收这种解释](http://blog.csdn.net/java_min/article/details/5883706)(2)
- [ubuntu 桌面环境下显示文件全路径](http://blog.csdn.net/java_min/article/details/7792205)(2)
- [jstl 格式化时间日期标签讲解](http://blog.csdn.net/java_min/article/details/5953957)(1)
- [qq工具大全](http://blog.csdn.net/java_min/article/details/4149489)(1)

- [Cannot forward after response has been committed 异常](http://blog.csdn.net/java_min/article/details/5262518#comments) [qq_26508467](http://blog.csdn.net/qq_26508467): 感谢楼主 你救了我一命
- [JVM调优浅谈](http://blog.csdn.net/java_min/article/details/8349721#comments) [QQUCHAO](http://blog.csdn.net/QQUCHAO): @sjjsh2:我看到http://www.cnblogs.com/ywl925/p/3925637...
- [JVM调优浅谈](http://blog.csdn.net/java_min/article/details/8349721#comments) [sjjsh2](http://blog.csdn.net/sjjsh2): gc处理的应该是堆中的信息吧
- [JVM调优浅谈](http://blog.csdn.net/java_min/article/details/8349721#comments) [sjjsh2](http://blog.csdn.net/sjjsh2): 当Eden区满时，还存活的对象将被复制到Survivor区（两个中的一个），当这个Survivor区...
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [qq_34283674](http://blog.csdn.net/qq_34283674): 灰常感谢分享
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [LutosX](http://blog.csdn.net/LutosX): 问题完美解决，谢谢作者分享，赞一个！
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [Larch_h](http://blog.csdn.net/u014249394): 学习了。素人派http://surenpi.com
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [zhm123456](http://blog.csdn.net/zhm123456): 感谢分享，解决了我的问题，节省了时间！
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [哈瓦那民兵](http://blog.csdn.net/u010647197): 有用
- [webservcie生成客户端代码报错----javax.xml.ws.soap.SOAPFaultException: Cannot create a secure XMLInputFactory](http://blog.csdn.net/java_min/article/details/9833815#comments) [为谁落泪](http://blog.csdn.net/caohongli05183624): 没有用啊， 还是报这个错

  .

: [公司简介](http://www.csdn.net/company/about.html)|[招贤纳士](http://www.csdn.net/company/recruit.html)|[广告服务](http://www.csdn.net/company/marketing.html)|[银行汇款帐号](http://www.csdn.net/company/account.html)|[联系方式](http://www.csdn.net/company/contact.html)|[版权声明](http://www.csdn.net/company/statement.html)|[法律顾问](http://www.csdn.net/company/layer.html)|[问题报告](http://blog.csdn.net/java_min/article/details/9497943mailto:webmaster@csdn.net)|[合作伙伴](http://www.csdn.net/friendlink.html)|[论坛反馈](http://bbs.csdn.net/forums/Service)
: [网站客服](#)[杂志客服](http://wpa.qq.com/msgrd?v=3&uin=2251809102&site=qq&menu=yes)[微博客服](http://e.weibo.com/csdnsupport/profile)[webmaster@csdn.net](http://blog.csdn.net/java_min/article/details/9497943mailto:webmaster@csdn.net)400-600-2320|北京创新乐知信息技术有限公司 版权所有|江苏乐知网络技术有限公司 提供商务支持
: 京 ICP 证 09002463 号|Copyright © 1999-2014, CSDN.NET, All Rights Reserved ![[attachments/gongshang_logos.gif|GongshangLogo]]
