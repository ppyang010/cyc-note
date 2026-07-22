---
Title: "javaweb项目  eclispe和intellj"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-07-29 19:51:15"
Cover: ""
Pinned: true
WizPinned: true
WizGuid: "875a5c12-03e3-4df7-88cf-f7e743e04c52"
WizType: "document"
WizLocation: "/开发工具/"
WizDataMd5: "36a3950c61ebc5669650d1fe277e1e22"
Modified: "2017-07-30 01:58:13"
WizSyncedAt: "2026-07-22 16:05:38"
---

javaweb项目在eclipse中一般需要设置

##

## 1.eclipse 开发时设置（eclipse编译项目设置 ）

编译报错，eclipse 提示报错之类的

#### 1.1设置source文件夹（源码文件）

添加source文件所在目录（需要编译的文件）（源码文件），resouce文件所在目录（不需要编译的文件）

一般resource文件跟着source文件走即可

#### 1.2设置编译后输出的文件目录

![[attachments/b470b8e9-4904-47bb-8bfa-74ee45c67e12.png]]

#### 1.3设置依赖的jar包

包含jre 和 servlet依赖jar包（tomcat7 那个就是）

![[attachments/6452ec97-8da8-47ad-97f3-4ddbf291a99f.png]]

## 2 eclipse设置需要部署到应用服务器的文件

一般将webroot设置为根目录 将源码（source文件和resource文件）部署（编译）到web-inf/classes下 依赖的jar包部署到web-inf/lib下

![[attachments/83974f7c-3136-4b11-b7a9-93327eef8c14.png]]

部署后的目录情况

![[attachments/e6a7c641-a3b8-4c29-8953-e3f7c1aa4015.png]]

## 3.配置服务器

eclipse

## 4.部署到服务器操作

在eclipse配置tomcat后右键add  and  remove

![[attachments/d0c909f4-c35e-414d-ab6e-d4e135a97579.png]]

或者

![[attachments/5ed930fc-9fe5-40cc-b07f-2f461d40a02f.png]]

地址选择到根目录即一般为webroot的

<Context docBase="bysj" path="/bysj" reloadable="true" source="org.eclipse.jst.jee.server:bysj"/></Host>

---

# intell普通web项目

## 1.inteljj开发时（编译）设置

解决编译检查错误 开发工具提示错误等

#### 1.1设置souce文件夹  源码

source 和resoure 两者都会被输出到compile output path目录（该目录在下一步配置）（前者会被编译后者不会被编译）

idea中将这些文件分的比较细

![[attachments/05c1e256-d2b7-458b-8833-2c6aa8aa2da0.png]]![[attachments/b82071f4-86a7-4737-917e-cb45fcc2b896.png]]

#### 1.2设置编译输出地址

![[attachments/4f1ed5db-6e68-4e5d-bf99-5b0253051a73.png]]

![[attachments/f7363cc4-6fd6-49f6-a447-31f7d10b2b87.png]]

#### 1.3设置依赖jar包

注意跟eclipse不同 这里需要单独的把servlet-api的jar包加上

![[attachments/b308cd51-b2fc-4deb-964d-d637f0e567db.png]]

intellj还提供了依赖范围 和export

其中依赖范围跟maven差不多

依赖范围

**compile（编译范围）:**

compile是默认的范围；如果没有提供一个范围，那该依赖的范围就是编译范围。编译范围依赖在所有的classpath中可用，同时它们也会被打包。

**provided（已提供范围）:**

provided依赖只有在当JDK或者一个容器已提供该依赖之后才使用。例如，如果你开发了一个web应用，你可能在编译classpath中需要可用的Servlet API来编译一个servlet，但是你不会想要在打包好的WAR中包含这个Servlet API；这个Servlet API JAR由你的应用服务器或者servlet容器提供。已提供范围的依赖在编译classpath（不是运行时）可用。它们不是传递性的，也不会被打包。

**runtime（运行时范围）:**

runtime依赖在运行和测试系统的时候需要，但在编译的时候不需要。比如，你可能在编译的时候只需要JDBC API JAR，而只有在运行的时候才需要JDBC驱动实现。

**test（测试范围）:**

test范围依赖 在一般的 编译和运行时都不需要，它们只有在测试编译和测试运行阶段可用。

export

这里有个export选项，这个选项被选上了话，那么说明：将来某一个module依赖本module的话，那么被选中这个选项的项也会出现在那个module中。也就是说，有一个传递性。

比如项目A依赖fastjson的jar包并勾选上export选项    项目B依赖项目A 则也依赖了fastjson这个jar包

![[attachments/8feedb79-65e8-4000-ba29-b21297442d2c.png]]

## 2.intellj设置需要部署到应用服务器的文件

在eclipse中需要设置需要部署的文件有

1.源码目录（包含需要编译的和不需要编译的） 部署到WEB-INF/classes下

2.依赖的jar包WEB-INF/lib下

3.将webroot作为根目录  或者说是将wenroot下的所有文件（主要时静态文件html，css，js）部署到根目录下（tomcat/webapps/项目名/）

![[attachments/83d1e30f-5e18-47ad-8ba1-da0a540bc560.png]]

在intellj中需要部署的东西基本同上

#### 2.1准备工作

这个web在module是创建 但是在facets中可见

![[attachments/7a264619-1572-499f-9771-ab5d625d260c.png]]

![[attachments/1205441765.png]]

#### 2.2进行配置

配置需要部署的内容

首先创建一个web app  exp

图中1 设置源码部署目录  目录为步骤1.2中的编译输出目录

图中2 为依赖的目录

图中3 为上面设置的facets web中的资源文件根目录（就是html之类的） 或者说将上面设置的facets web中目录的资源文件全部部署到根目录（tomcat/webapps/项目名/）

注意图中available  elements 区域为可用未部署的资源

![[attachments/1206483500.png]]

##### 重要最后检查和异常排查

最后部署后的文件目录（上图 output directory 设置）如下

即部署到tomcat后的目录结构

最后检查这个目录中结构是否正常即可

关于这个目录粗略的可以理解为 将其设置为serverxml中 docbase值

<Context docBase="bysj" path="/bysj" reloadable="true" source="org.eclipse.jst.jee.server:bysj"/></Host>

![[attachments/cb851806-5aa6-4ee6-95e3-3bcb56e722b1.png]]

## 3.配置应用服务器

![[attachments/31776ba4-b0e8-4128-befe-b6d97b01bf32.png]]

添加artifacts 设置访问路径（对应下面所示的项目部分）

即ip:port/项目/

![[attachments/493d0e8d-0fb1-45db-87f0-69cc20ffeeb3.png]]
