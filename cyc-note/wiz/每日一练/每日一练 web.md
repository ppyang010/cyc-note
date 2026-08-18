---
Title: "每日一练 web"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2016-12-12 23:11:13"
Cover: ""
WizGuid: "15940b5f-87cb-4553-8c3b-7f5c5265661d"
WizType: "document"
WizLocation: "/每日一练/"
WizDataMd5: "172439d4d786d64e715e2f07385ebe71"
Modified: "2017-02-08 11:04:47"
WizSyncedAt: "2026-08-18 18:31:49"
---

总数 30题z

html20

css43+5

#### 2017年1月18日11:28:10

**有一个高度自适应的div，里面有两个div，一个高度100px，希望另一个填满剩下的高度。**

display table

```
<html lang="en"><style media="screen">/*    html,body{        height: 100%;    }*/    .main{display: table;width: 100%;height: 500px;}    .box1{display: table-row;width: 100%;height: 100px;}    .box11{display: table-cell;border-bottom: 1px solid #000;}    .box2{display: table-row;}</style><body><div class="main">    <div class="box1">        <div class="box11"></div>    </div>    <div class="box2"></div></div></body></html>
```

display flex

```
<html lang="en"><style media="screen">    .main{display: flex; flex-direction: column; width: 100%;height: 500px; }    .box1{ width: 100%;height: 100px; flex-basis:100px; border-bottom: 1px solid #000}    .box2{flex-grow: 1;}</style><body><div class="main">    <div class="box1">    </div>    <div class="box2"></div></div></body></html>
```

**png、jpg、gif 这些图片格式解释一下，分别什么时候用。有没有了解过webp？**

jpg/jpeg:优点:体积比png小,打开速度比png快缺点:属于有损压缩，每次保存都会产生数据损失(jpeg artifacts), 故不适合用于多次编辑保存。压缩率过高图像会失真PS:网络上最最常见的格式，也是静态图片(不只是照片)就常用的保存格式,就算是同一小组开发的jp2(相当于jpg第2代)也无法取代它。一般如果肉眼无法识别与png的差别和没有特殊要求就用jpg

.png:优点:无损压缩，有透明选项，压缩效率高于bmp缺点:一般体积比同尺寸的90%压缩率的jpg要大很多(通常是5倍以上),但人眼很难识别其中的区别PS:最常见的无损压缩图片格式,如果是经常对某图片进行编辑保存,要求图片数据100%完整,或需要透明效果(给PS当素材或用作图标等)则推荐使用

gif: 一般只作为动态图像格式使用，正在被google的webm格式取代中=。= 好吧感觉gif真没啥可说的，要不是因为有动态效果谁会用这破玩意。。。

webp ：体积比jpg小 有动画  google出品

[http://blog.csdn.net/playboyanta123/article/details/44655749](http://blog.csdn.net/playboyanta123/article/details/44655749)

**什么是Cookie 隔离？（或者说：请求资源的时候不要让它带cookie怎么做）**

如果静态文件都放在主域名下，那静态文件请求的时候都带有的cookie的数据提交给server的，非常浪费流量，

所以不如隔离开。

cookie根据作用域隔离 Set-Cookie: user=xxxx; Path=/; Domain=.example.com 像这样作用域为域名 但没有设置主机 则该域名下所有的主机（www，mail ，）都可以访问

都会提交给server

cookie还能根据路径隔离

![[attachments/684ba1b2-a94c-492f-bb23-29db9a02db91.jpg]]
![[attachments/7d4fd4a3-a165-40e7-8e78-a1a12e9a3d2c.jpg]]

请求资源的时候不要让它带cookie怎么做？

根据设置不同的作用路径或作用域实现

因为cookie有域的限制，因此不能跨域提交请求，故使用非主要域名的时候，请求头中就不会带有cookie数据，

这样可以降低请求头的大小，降低请求时间，从而达到降低整体请求延时的目的。

同时这种方式不会将cookie传入Web Server，也减少了Web Server对cookie的处理分析环节，

提高了webserver的http请求的解析速度。

**style标签写在body后与body前有什么区别？**

页面加载自上而下 在前面先加载

#### 什么是CSS 预处理器 / 后处理器？

- 预处理器例如：LESS、Sass、Stylus，用来预编译Sass或less，增强了css代码的复用性，

还有层级、mixin、变量、循环、函数等，具有很方便的UI组件模块化开发能力，极大的提高工作效率。

- 后处理器例如：PostCSS，通常被视为在完成的样式表中根据CSS规范处理CSS，让其更有效；目前最常做的

是给CSS属性添加浏览器私有前缀，实现跨浏览器兼容性的问题。

---

#### 2017年1月15日20:38:34

**position:fixed;在android下无效怎么处理？**

fixed的元素是相对整个页面固定位置的，你在屏幕上滑动只是在移动这个所谓的viewport，

原来的网页还好好的在那，fixed的内容也没有变过位置，

所以说并不是iOS不支持fixed，只是fixed的元素不是相对手机屏幕固定的。

<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no"/>

设置宽度为屏幕宽度 初始倍数1.0

**如果需要手动写动画，你认为最小时间间隔是多久，为什么？（阿里）**

多数显示器默认频率是60Hz，即1秒刷新60次，所以理论上最小间隔为1/60＊1000ms ＝ 16.7ms

**display:inline-block 什么时候会显示间隙？(携程)**

移除空格、使用margin负值、使用font-size:0、letter-spacing、word-spacing

---

#### 2017年1月13日20:22:34

**让页面里的字体变清晰，变细用CSS怎么做？**

```
-webkit-font-smoothing: antialiased;
```

只在macos中的webkit中生效

参考：[https://segmentfault.com/q/1010000000467910](https://segmentfault.com/q/1010000000467910)

**font-style属性可以让它赋值为“oblique” oblique是什么意思？**

使字体倾斜 而不是使用字体中的斜体字

italic：指定文本字体样式为斜体。对于没有设计斜体的特殊字体，如果要使用斜体外观将应用oblique

oblique：指定文本字体样式为倾斜的字体。人为的使文字倾斜，而不是去选取字体中的斜体字

---

#### 2017年1月9日21:32:51

**::before 和 :after中双冒号和单冒号 有什么区别？解释一下这2个伪元素的作用。**

单冒号(:)用于CSS3伪类，双冒号(::)用于CSS3伪元素。（伪元素由双冒号和伪元素名称组成）

双冒号是在当前规范中引入的，用于区分伪类和伪元素。不过浏览器需要同时支持旧的已经存在的伪元素写法，

比如:first-line、:first-letter、:before、:after等，

而新的在CSS3中引入的伪元素则不允许再支持旧的单冒号的写法。

想让插入的内容出现在其它内容前，使用::before，否者，使用::after；

在代码顺序上，::after生成的内容也比::before生成的内容靠后。

如果按堆栈视角，::after生成的内容会在::before生成的内容之上

**如何修改chrome记住密码后自动填充表单的黄色背景 ？**

```
input:-webkit-autofill, textarea:-webkit-autofill, select:-webkit-autofill {  background-color: rgb(250, 255, 189); /* #FAFFBD; */  background-image: none;  color: rgb(0, 0, 0);}
```

-webkit-autofill 伪类

**你对line-height是如何理解的？**

css中起高度作用的应该就是height以及line-height

先说一个大家都熟知的现象，有一个空的div，<div></div>，如果没有设置至少大于1像素高度height值时，该div的高度就是个0。如果该div里面打入了一个空格或是文字，则此div就会有一个高度。并不是文字大小给了div高度 而是 你添加文字后系统会给一个默认行高 就是说如果你给了文字但设置line-height为0 则这个div的高度还是会为0

也就是说div高度 由其内容的height或者line-height（最后会转换辰height）决定

谷歌浏览器字体的默认大小是：16px，字体的最小值为：12px，默认行高为：18px；默认情况下如果没有给div设置高度，那么这个div的高度会比其中文本的大小大一点（这个大多少现在没有办法确定）

浏览器会給每段文字一个line-box 他只有高度

![[attachments/f1a7c965-9830-44ea-987f-58e03b25d335.png]]

行距：行高-字体大小（上底线到下顶线）

半行距：(行高-字体大小)/2（底线到最近的绿线或顶到最近的绿线）

参考

[https://segmentfault.com/a/1190000005870340](https://segmentfault.com/a/1190000005870340)

[https://segmentfault.com/a/1190000005870340](https://segmentfault.com/a/1190000005870340)

[https://segmentfault.com/a/1190000005122321](https://segmentfault.com/a/1190000005122321)

[http://www.zhangxinxu.com/wordpress/2009/11/css%E8%A1%8C%E9%AB%98line-height%E7%9A%84%E4%B8%80%E4%BA%9B%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E5%8F%8A%E5%BA%94%E7%94%A8/](http://www.zhangxinxu.com/wordpress/2009/11/css%E8%A1%8C%E9%AB%98line-height%E7%9A%84%E4%B8%80%E4%BA%9B%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3%E5%8F%8A%E5%BA%94%E7%94%A8/)

**设置元素浮动后，该元素的display值是多少？**

**或者说是所有脱离文档流的方式 postion ab fix 或float 都会转变**

**一般都会变成block 具体看下面有张表**

**并且该元素无法再被设置辰其他display  但齐子元素不受影响**

自动变成了 display:block

**怎么让Chrome支持小于12px 的文字？**

原因**：**中文版Chrome浏览器不支持12px以下字体的解决方案

Chrome 27之前的中文版桌面浏览器会默认设定页面的最小字号是12px，英文版则没有限制，主要是因为chrome认为汉字小于12px就会增加识别难度，尤其是中文常用的宋体和微软雅黑。而我们在实际项目中，对于数字/英文内容，其他字体的文本可能会有特殊的需求要求它们以更小的字号来显示，这个时候就需要取消浏览器的自动调整功能了。

1、用图片：如果是内容固定不变情况下，使用将小于12px文字内容切出做图片，这样不影响兼容也不影响美观。

2、使用12px及12px以上字体大小：为了兼容各大主流浏览器，建议设计美工图时候设置大于或等于12px的字体大小，如果是接单的这个时候就需要给客户讲解小于12px浏览器不兼容等事宜。

3、继续使用小于12px字体大小样式设置：如果不考虑chrome可以不用考虑兼容，同时在设置小于12px对象设置**-webkit-text-size-adjust:none，**做到最大兼容考虑。

4、使用12px以上字体：为了兼容、为了代码更简单 从新考虑权重下兼容性。

#### --- 2017年1月4日14:47:37

**什么是响应式设计？响应式设计的基本原理是什么？如何兼容低版本的IE？**

响应式网站设计(Responsive Web design)（RWD）的理念是集中创建页面的图片排版大小，可以智能地根据用户行为以及使用的设备环境（系统平台、屏幕尺寸、屏幕定向等）进行相对应的布局。

基本原理: 媒体查询 @media

兼容IE可以使用JS辅助一下来解决

####

##### **视差滚动效果，如何给每页做不同的动画？**

**（回到顶部，向下滑动要再次出现，和只出现一次分别怎么做？）**

---

#### 2017年1月3日23:00:58

**元素竖向的百分比设定是相对于容器的高度吗？**

例如padding-top,padding-bottom,margin-top,margin-bottom等，当按百分比设定它们时，依据的也是父容器的宽度，而不是高度。

##### 全屏滚动

fullpage.js 基于jq

**全屏滚动的原理是什么？用到了CSS的那些属性？**

类似轮播图  展示的高度为100%  多个图片的高度为500%  transform 的translateY来实现

---

#### 2016年12月29日22:46:43

**CSS优化、提高性能的方法有哪些？**

关键选择器（key selector）。选择器的最后面的部分为关键选择器（即用来匹配目标元素的部分）；

如果规则拥有 ID 选择器作为其关键选择器，则不要为规则增加标签。过滤掉无关的规则（这样样式系统就不会浪费时间去匹配它们了）；

提取项目的通用公有样式，增强可复用性，按模块编写组件；增强项目的协同开发性、可维护性和可扩展性;

使用预处理工具或构建工具（gulp对css进行语法检查、自动补前缀、打包压缩、自动优雅降级）；

链接：https://www.zhihu.com/question/19886806/answer/108097437

css性能优化的地方很多，结合以上几位大神的回答，总结如下：

1.慎重使用高性能属性：浮动、定位；

2.尽量减少页面重排、重绘  详情见链接

3.去除空规则：｛｝减少代码量；

4.属性值为0时，不加单位减少代码量；

5.属性值为浮动小数0.**，可以省略小数点之前的0减少代码量；

6.标准化各种浏览器前缀：带浏览器前缀的在前。标准属性在后；

7.不使用@import前缀，它会影响css的加载速度；

8.充分利用css继承属性，减少代码量；

9.抽象提取公共样式，减少代码量；

10.选择器优化嵌套，尽量避免层级过深；

11.css雪碧图，同一页面相近部分的小图标，方便使用，减少页面的请求次数，但是同时图片本身会变大，使用时，优劣考虑清楚，再使用;

12.将css文件放在页面最上面

减少代码量  选择器层次  慎用高性能属性  雪碧图

总结  部分 该https://www.zhihu.com/question/19886806/answer/80432295

1、提高代码性能

1、提高页面的加载性能

提高页面的加载性能，简单说就是减小CSS文件的大小，提高页面的加载速度，尽可以的利用http缓存

2、提高CSS代码性能

不同的CSS代码，浏览器对其解析的速度也是不一样的，如何提高浏览器解析CSS代码的速度也是我们要考虑的

2、提高代码的可维护性

1、可重用性

一般来说，一个项目的整体设计风格是一致的，页面中肯定有几个风格一致但有些许不同的模块，如何在尽可能多地重用CSS代码，尽可能少地增加新代码，这是CSS代码中非常重要的一点。如果CSS代码的重用性高，我们可能只需要写一些不一样的地方，对页面性能和可维护性、提高开发效率都有很大的帮助。

2、可扩展性

如果产品增加了某个功能，我们应该保证新增加的CSS代码不会影响到旧的CSS代码和页面，并且尽可能少地增加新代码而重用旧代码。

3、可修改性

如果某个模块产品经理觉得要修改样式，或者要删掉它，如果没有规划好相应的CSS代码，过了一段时间之后，开发人员可能已经不记得这段代码作用了几个地方，不敢修改或删除它，这样下去CSS代码也就越来越多，影响了页面的性能，还造成了代码的复杂度。

**浏览器是怎样解析CSS选择器的？**

样式系统从关键选择器开始匹配，然后左移查找规则选择器的祖先元素。

只要选择器的子树一直在工作，样式系统就会持续左移，直到和规则匹配，或者是因为不匹配而放弃该规则。

即从右到左 直到匹配成功或者失败  （最右即关键选择器）(先匹配所有满足最右边的选择器的元素)

**在网页中的应该使用奇数还是偶数的字体？为什么呢？**

偶数

网页设计中为啥少用奇数字体？

一、UI设计师的原因

多数设计师用的设计软件（如：ps）大多数都是偶数，所以前端工程师一般都是用偶数字体

二、浏览器的原因

其一是为了迁就ie6，万恶的ie6会把定义为13px的字渲染成14px，你可以写个页面试试

还有一个原因是，偶数宽的汉字，比如12px宽的汉字，去掉1像素的间距，填充了像素的实际宽是11px，这样汉字的中竖线左右是平分的，以“中”这个字为例，在12像素时，竖线在中间，左右各5像素，显得均衡。

其二像谷歌一些比较流行的浏览器一般会有个默认的最小字体，而且对奇数字体渲染的不太好看

三、实际应用

偶数字号相对更容易和 web 设计的其他部分构成比例关系。比如：当我用了 14 px 的正文字号，我可能会在一些地方用 14 × 0.5 = 7 px 的 margin，在另一些地方用 14 × 1.5 = 21 px 的标题字号。

Windows 自带的点阵宋体（中易宋体）从 Vista 开始只提供 12、14、16 px 这三个大小的点阵，而 13、15、17 px 时用的是小一号的点阵（即每个字占的空间大了 1 px，但点阵没变），于是略显稀疏

ui原因 浏览器兼容ie和chrome中偶数好看  实际应用中方便可以跟其他部分构成比例关系

**margin和padding分别适合什么场景使用？**

margin是用来隔开元素与元素的间距；padding是用来隔开元素与内容的间隔。

margin用于布局分开元素使元素与元素互不相干；

padding用于元素与内容之间的间隔，让内容（文字）与（包裹）元素之间有一段

**抽离样式模块怎么写，说出思路，有无实践经验？[阿里航旅的面试题]**

[http://www.cnblogs.com/yoomin/p/5670589.html](http://www.cnblogs.com/yoomin/p/5670589.html)

[http://www.cnblogs.com/WebShare-hilda/p/4686067.html](http://www.cnblogs.com/WebShare-hilda/p/4686067.html)

[http://blog.csdn.net/holmes89757/article/details/51690470](http://blog.csdn.net/holmes89757/article/details/51690470)

如果是我，做15个页面，不会先考虑 CSS 样式文件怎么分割，而是先通读视觉稿，把所有类似的、可复用的部分划分出来，抽出结构和样式做成模块。

达到一段 HTML 代码、一段 CSS 样式，粘贴到任意位置都正常。

抽出模块之后，再思考怎么管理就很方便了。

在开发阶段，可以用 SCSS 等来开发，这样可以直接将模块分成单独的 CSS 文件，import 进来，比较清晰。

作者：于江水

链接：https://www.zhihu.com/question/38429404/answer/76353209

来源：知乎

著作权归作者所有，转载请联系作者获得授权。

结构与样式的分离（一个结构多个样式）  容器与内容的分离（一个容器多个内容）

---

#### 2016年12月28日22:22:19

**请解释一下为什么需要清除浮动？清除浮动的方式**

清除浮动是为了清除使用浮动元素产生的影响。浮动的元素，高度会塌陷，而高度的塌陷使我们页面后面的布局不能正常显示。

1、父级div定义height；

2、父级div 也一起浮动；

3、常规的使用一个class；

```
    .clearfix:before, .clearfix:after {        content: " ";        display: table;    }    .clearfix:after {        clear: both;    }    .clearfix {        *zoom: 1;    }
```

```
.clearfix:after{content:'.';display:block;clear:both;height:0;overflow:hidden;visibility:hidden;}.clearfix{zoom:1}
```

4、SASS编译的时候，浮动元素的父级div定义伪类:after

&:after,&:before{

content: " ";

visibility: hidden;

display: block;

height: 0;

clear: both;

}

解析原理：

1) display:block 使生成的元素以块级元素显示,占满剩余空间;

2) height:0 避免生成内容破坏原有布局的高度。

3) visibility:hidden 使生成的内容不可见，并允许可能被生成内容盖住的内容可以进行点击和交互;

4）通过 content:"."生成内容作为最后一个元素，至于content里面是点还是其他都是可以的，例如oocss里面就有经典的 content:".",有些版本可能content 里面内容为空,一丝冰凉是不推荐这样做的,firefox直到7.0 content:”" 仍然会产生额外的空隙；

5）zoom：1 触发IE hasLayout。

通过分析发现，除了**clear：both**用来闭合浮动的，其他代码无非都是为了隐藏掉content生成的内容，这也就是其他版本的闭合浮动为什么会有font-size：0，line-height：0。

**什么是外边距合并？**

外边距合并指的是，当两个垂直外边距相遇时，它们将形成一个外边距。

合并后的外边距的高度等于两个发生合并的外边距的高度中的较大者。

w3school介绍网址： [http://www.w3school.com.cn/css/css_margin_collapsing.asp](http://www.w3school.com.cn/css/css_margin_collapsing.asp)

**zoom:1的清除浮动原理?**

清除浮动，触发hasLayout；

Zoom属性是IE浏览器的专有属性，它可以设置或检索对象的缩放比例。解决ie下比较奇葩的bug。

譬如外边距（margin）的重叠，浮动清除，触发ie的haslayout属性等。

来龙去脉大概如下：

当设置了zoom的值之后，所设置的元素就会就会扩大或者缩小，高度宽度就会重新计算了，这里一旦改变zoom值时其实也会发生重新渲染，运用这个原理，也就解决了ie下子元素浮动时候父元素不随着自动扩大的问题。

Zoom属是IE浏览器的专有属性，火狐和老版本的webkit核心的浏览器都不支持这个属性。然而，zoom现在已经被逐步标准化，出现在 CSS 3.0 规范草案中。

目前非ie由于不支持这个属性，它们又是通过什么属性来实现元素的缩放呢？

可以通过css3里面的动画属性scale进行缩放。

**移动端的布局用过媒体查询吗？**

假设你现在正用一台显示设备来阅读这篇文章，同时你也想把它投影到屏幕上，或者打印出来， 而显示设备、屏幕投影和打印等这些媒介都有自己的特点，CSS就是为文档提供在不同媒介上展示的适配方法

当媒体查询为真时，相关的样式表或样式规则会按照正常的级联规被应用。 当媒体查询返回假， 标签上带有媒体查询的样式表 仍将被下载 （只不过不会被应用）。

包含了一个媒体类型和至少一个使用 宽度、高度和颜色等媒体属性来限制样式表范围的表达式。 CSS3加入的媒体查询使得无需修改内容便可以使样式应用于某些特定的设备范围。

@media (min-width: 700px) and (orientation: landscape){ .sidebar { display: none; } }

![[attachments/4d744cf6-e633-49ef-ac78-e25e438e04eb.jpg]]

**使用 CSS 预处理器吗？喜欢那个？**

SASS (SASS、LESS没有本质区别，只因为团队前端都是用的SASS)

#### **2016年12月22日21:41:26**

**absolute的containing block(容器块)计算方式跟正常流有什么不同？**

无论属于哪种，都要先找到其祖先元素中最近的 position 值不为 static 的元素，然后再判断：

1、若此元素为 inline 元素，则 containing block 为能够包含这个元素生成的第一个和最后一个 inline box 的 padding box (除 margin, border 外的区域) 的最小矩形；

2、否则,则由这个祖先元素的 padding box 构成。

如果都找不到，则为 initial containing block。

补充：

1. static(默认的)/relative：简单说就是它的父元素的内容框（即去掉padding的部分）

2. absolute: 向上找最近的定位为absolute/relative的元素

3. fixed: 它的containing block一律为根元素(html/body)，根元素也是initial containing block

**CSS里的visibility属性有个collapse属性值是干嘛用的？在不同浏览器下以后什么区别？**

当一个元素的visibility属性被设置成collapse值后，对于一般的元素，它的表现跟hidden是一样的，但如果是table相关的元素，例如table行，table group，table列，table column group，它的表现跟display:none一样，也就是说，它们占用的空间会释放。

在谷歌浏览器中，使用collapse值和使用visibility:hidden值没什么区别，在Firefox、Opera和IE11里，使用collapse值的效果就会消失，下面一行会补充它的位置。

分别用以上浏览器打开http://www.w3school.com.cn/tiy/t.asp?f=csse_visibility_collapse看效果。

chorme

![[attachments/c1a86bd2-0964-4285-9c84-28a2bd327038.png]]

ie ff

![[attachments/c9b8ac0b-72cb-4ac0-a4bf-259066311cce.png]]

**position跟display、margin collapse、overflow、float这些特性相互叠加后会怎么样？**

部分答案： 参考：[http://www.cnblogs.com/jackyWHJ/p/3756087.html](http://www.cnblogs.com/jackyWHJ/p/3756087.html)

进行下面的哦昂的

display 为none position 和float 不生效

postion为absolute或fixed   float 不生效 display 会按照下表转换  （一般情况转换成block）

folat 为left或，，，  dispaly 会按照下表转换  （一般情况转换成block）

元素为根元素会按照下表转换  （一般情况转换成block）

一、'display'、'position' 和 'float' 的相互关系

![[attachments/710a865d-46ac-4b21-bef7-51d477314960.png]]

转换对应表：

| 设定值 | 计算值 |
| --- | --- |
| inline-table | table |
| inline, run-in, table-row-group, table-column, table-column-group, table-header-group,<br>table-footer-group, table-row, table-cell, table-caption, inline-block | block |
| 其他 | 同设定值<br>来源： [http://www.cnblogs.com/jackyWHJ/p/3756087.html](http://www.cnblogs.com/jackyWHJ/p/3756087.html) |

**对BFC规范(块级格式化上下文：block formatting context)的理解？**

（W3C CSS 2.1 规范中的一个概念,它是一个独立容器，决定了元素如何对其内容进行定位,以及与其他元素的关系和相互作用。）

一个页面是由很多个 Box 组成的,元素的类型和 display 属性,决定了这个 Box 的类型。

不同类型的 Box,会参与不同的 Formatting Context（决定如何渲染文档的容器）,因此Box内的元素会以不同的方式渲染,也就是说BFC内部的元素和外部的元素不会互相影响。

**css定义的权重**

以下是权重的规则：标签的权重为1，class的权重为10，id的权重为100，以下例子是演示各种定义的权重值：

/*权重为1*/

div{

}

/*权重为10*/

.class1{

}

/*权重为100*/

#id1{

}

/*权重为100+1=101*/

#id1 div{

}

/*权重为10+1=11*/

.class1 div{

}

/*权重为10+10+1=21*/

.class1 .class2 div{

}

如果权重相同，则最后定义的样式会起作用，但是应该避免这种情况出现

---

#### 2016年12月21日22:51:43

**一个满屏 品 字布局 如何设计?**

简单的方式：

上面的div宽100%，

下面的两个div分别宽50%，

然后用float或者inline使其不换行即可

**css多列等高如何实现？**

利用padding-bottom|margin-bottom正负值相抵；

设置父容器设置超出隐藏（overflow:hidden），这样子父容器的高度就还是它里面的列没有设定padding-bottom时的高度，

当它里面的任 一列高度增加了，则父容器的高度被撑到里面最高那列的高度，

其他比这列矮的列会用它们的padding-bottom补偿这部分高度差。

![[attachments/98953a5c-94df-4c18-af4a-f812ada13ce5.png]]

http://blog.csdn.net/u010874036/article/details/51078572

**经常遇到的浏览器的兼容性有哪些？原因，解决方法是什么，常用hack的技巧 ？**

* png24位的图片在iE6浏览器上出现背景，解决方案是做成PNG8.

* 浏览器默认的margin和padding不同。解决方案是加一个全局的*{margin:0;padding:0;}来统一。

* IE6双边距bug:块属性标签float后，又有横行的margin情况下，在ie6显示margin比设置的大。

浮动ie产生的双倍距离 #box{ float:left; width:10px; margin:0 0 0 100px;}

这种情况之下IE会产生20px的距离，解决方案是在float的标签样式控制中加入 ——_display:inline;将其转化为行内属性。(_这个符号只有ie6会识别)

渐进识别的方式，从总体中逐渐排除局部。

首先，巧妙的使用“\9”这一标记，将IE游览器从所有情况中分离出来。

接着，再次使用“+”将IE8和IE7、IE6分离开来，这样IE8已经独立识别。

css

.bb{

background-color:red;/*所有识别*/

background-color:#00deff\9; /*IE6、7、8识别*/

+background-color:#a200ff;/*IE6、7识别*/

_background-color:#1e0bd1;/*IE6识别*/

}

*  IE下,可以使用获取常规属性的方法来获取自定义属性,

也可以使用getAttribute()获取自定义属性;

Firefox下,只能使用getAttribute()获取自定义属性。

解决方法:统一通过getAttribute()获取自定义属性。

*  IE下,even对象有x,y属性,但是没有pageX,pageY属性;

Firefox下,event对象有pageX,pageY属性,但是没有x,y属性。

*  解决方法：（条件注释）缺点是在IE浏览器下可能会增加额外的HTTP请求数。

*  Chrome 中文界面下默认会将小于 12px 的文本强制按照 12px 显示,

可通过加入 CSS 属性 -webkit-text-size-adjust: none; 解决。

超链接访问过后hover样式就不出现了 被点击访问过的超链接样式不在具有hover和active了解决方法是改变CSS属性的排列顺序:

L-V-H-A :  a:link {} a:visited {} a:hover {} a:active {}

**li与li之间有看不见的空白间隔是什么原因引起的？有什么解决办法？**

行框的排列会受到中间空白（回车\空格）等的影响，因为空格也属于字符,这些空白也会被应用样式，占据空间，所以会有间隔，把字符大小设为0，就没有空格了。

**为什么要初始化CSS样式。**

- 因为浏览器的兼容问题，不同浏览器对有些标签的默认值是不同的，如果没对CSS初始化往往会出现浏览器之间的页面显示差异。

- 当然，初始化样式会对SEO有一定的影响，但鱼和熊掌不可兼得，但力求影响最小的情况下初始化。

最简单的初始化方法： * {padding: 0; margin: 0;} （强烈不建议）

淘宝的样式初始化代码：

body, h1, h2, h3, h4, h5, h6, hr, p, blockquote, dl, dt, dd, ul, ol, li, pre, form, fieldset, legend, button, input, textarea, th, td { margin:0; padding:0; }

body, button, input, select, textarea { font:12px/1.5tahoma, arial, \5b8b\4f53; }

h1, h2, h3, h4, h5, h6{ font-size:100%; }

address, cite, dfn, em, var { font-style:normal; }

code, kbd, pre, samp { font-family:couriernew, courier, monospace; }

small{ font-size:12px; }

ul, ol { list-style:none; }

a { text-decoration:none; }

a:hover { text-decoration:underline; }

sup { vertical-align:text-top; }

sub{ vertical-align:text-bottom; }

legend { color:#000; }

fieldset, img { border:0; }

button, input, select, textarea { font-size:100%; }

table { border-collapse:collapse; border-spacing:0; }

---

#### 2016年12月20日22:39:57

**display有哪些值？说明他们的作用。**

block         块类型。默认宽度为父元素宽度，可设置宽高，换行显示。

none          缺省值。象行内元素类型一样显示。

inline        行内元素类型。默认宽度为内容宽度，不可设置宽高，同行显示。

inline-block  默认宽度为内容宽度，可以设置宽高，同行显示。

list-item     象块类型元素一样显示，并添加样式列表标记。

table         此元素会作为块级表格来显示。

inherit       规定应该从父元素继承 display 属性的值。

**position的值relative和absolute定位原点是？**

absolute

生成绝对定位的元素，相对于值不为 static的第一个父元素进行定位。

fixed （老IE不支持）

生成绝对定位的元素，相对于浏览器窗口进行定位。

relative

生成相对定位的元素，相对于其正常位置进行定位。

static

默认值。没有定位，元素出现在正常的流中（忽略 top, bottom, left, right z-index 声明）。

inherit 规定从父元素继承 position 属性的值。

**CSS3有哪些新特性？**

新增各种CSS选择器  （: not(.input)：所有 class 不是“input”的节点）

圆角            （border-radius:8px）

多列布局      （multi-column layout）

阴影和反射   （Shadow\Reflect）

文字特效      （text-shadow、）

文字渲染      （Text-decoration）

线性渐变      （gradient）

旋转            （transform）

缩放,定位,倾斜,动画,多背景

例如:transform:\scale(0.85,0.90)\ translate(0px,-30px)\ skew(-9deg,0deg)\Animation:

**请解释一下CSS3的Flexbox（弹性盒布局模型）,以及适用场景？**

一个用于页面布局的全新CSS3功能，Flexbox可以把列表放在同一个方向（从上到下排列，从左到右），并让列表能延伸到占用可用的空间。

较为复杂的布局还可以通过嵌套一个伸缩容器（flex container）来实现。

采用Flex布局的元素，称为Flex容器（flex container），简称"容器"。

它的所有子元素自动成为容器成员，称为Flex项目（flex item），简称"项目"。

常规布局是基于块和内联流方向，而Flex布局是基于flex-flow流可以很方便的用来做局中，能对不同屏幕大小自适应。

在布局上有了比以前更加灵活的空间。

具体：

[http://www.w3cplus.com/css3/flexbox-basics.html](http://www.w3cplus.com/css3/flexbox-basics.html)

**用纯CSS创建一个三角形的原理是什么？**

把上、左、右三条边隐藏掉（颜色设为 transparent）

上面的是正三角

倒三角则是把左右下三遍隐藏掉

```
#demo {  width: 0;  height: 0;  border-width: 20px;  border-style: solid;  border-color: transparent transparent red transparent;}
```

---

#### 2016年12月18日21:43:48

**介绍一下标准的CSS的盒子模型？低版本IE的盒子模型有什么不同的？**

（1）有两种， IE 盒子模型、W3C 盒子模型；

（2）盒模型： 内容(content)、填充(padding)、边界(margin)、 边框(border)；

（3）区  别： IE的content部分把 border 和 padding计算了进去;   个人立即     相当于标准的borderbox

**CSS选择符有哪些？哪些属性可以继承？**

*   1.id选择器（ # myid）

2.类选择器（.myclassname）

3.标签选择器（div, h1, p）

4.相邻选择器（h1 + p）

5.子选择器（ul > li）

6.后代选择器（li a）

7.通配符选择器（ * ）

8.属性选择器（a[rel = "external"]）

9.伪类选择器（a:hover, li:nth-child）

*   可继承的样式： font-size font-family color, UL LI DL DD DT;

*   不可继承的样式：border padding margin width height ;

**CSS优先级算法如何计算？**

*   优先级就近原则，就近原则优于权重  当就近原则相同时在考虑权重 例div>a  都定义了字体 但是以a上的样式为准

*   载入样式以最后载入的定位为准;

优先级为:

同就近  同权重: 内联样式表（标签内部）> 嵌入样式表（当前文件中）> 外部样式表（外部文件中）。

上面的时由于样式 载入样式以最后载入的定位为准; 外部样式表最先载入  在是嵌入样式标 最后时内联样式   后面的样式覆盖前面的样式

!important >  id > class > tag

important 比 内联优先级高

参考  [页面制作 css笔记2（选择器 文本 文本装饰 颜色）](wiz://open_document?guid=94bedfc5-162b-42d2-838c-26166028e95f&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

**CSS3新增伪类有那些？**

举例：

p:first-of-type 选择属于其父元素的首个 <p> 元素的每个 <p> 元素。

p:last-of-type  选择属于其父元素的最后 <p> 元素的每个 <p> 元素。

p:only-of-type  选择属于其父元素唯一的 <p> 元素的每个 <p> 元素。

p:only-child        选择属于其父元素的唯一子元素的每个 <p> 元素。

p:nth-child(2)  选择属于其父元素的第二个子元素的每个 <p> 元素。

:after          在元素之前添加内容,也可以用来做清除浮动。

:before         在元素之后添加内容

:enabled

:disabled       控制表单控件的禁用状态。

:checked        单选框或复选框被选中。

**如何居中div？**

<u>水平居中</u>：给div设置一个宽度，然后添加margin:0 auto属性

```
div{    width:200px;    margin:0 auto;}
```

<u>让绝对定位的div居中</u>

```
div {    position: absolute;    width: 300px;    height: 300px;    margin: auto;    top: 0;    left: 0;    bottom: 0;    right: 0;    background-color: pink; /* 方便看效果 */}
```

<u>水平垂直居中一</u>

确定容器的宽高 宽500 高 300 的层

设置层的外边距

```
div {    position: relative;     /* 相对定位或绝对定位均可 */    width:500px;    height:300px;    top: 50%;    left: 50%;    margin: -150px 0 0 -250px;      /* 外边距为自身宽高的一半 */    background-color: pink;     /* 方便看效果 */ }
```

<u>水平垂直居中二</u>

未知容器的宽高，利用 `transform` 属性

```
div {    position: absolute;     /* 相对定位或绝对定位均可 */    width:500px;    height:300px;    top: 50%;    left: 50%;    transform: translate(-50%, -50%);    background-color: pink;     /* 方便看效果 */ }
```

<u>水平垂直居中三</u>

利用 flex 布局

实际使用时应考虑兼容性

```
 .container {    display: flex;    align-items: center;        /* 垂直居中 */    justify-content: center;    /* 水平居中 */ }.container div {    width: 100px;    height: 100px;    background-color: pink;     /* 方便看效果 */}
```

参考：[布局解决方案-居中布局（水平、垂直）](wiz://open_document?guid=b0b03cd5-63d1-44ad-8284-3d4f8f96c55a&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

---

#### 2016年12月15日23:00:18

**页面可见性（Page Visibility API） 可以有哪些用途？**

通过 visibilityState 的值检测页面当前是否可见，以及打开网页的时间等;

在页面被切换到其他后台进程的时候，自动暂停音乐或视频的播放；

document.hidden: Boolean值，表示当前页面可见还是不可见

document.visibilityState: 返回当前页面的可见状态。

> “hidden“ 隐藏
>
> “visible“ 可见
>
> “prerender” 这个表示纳尼呢~~恩，我也不确定，字面意思是“预渲染”。莫非指的是啪啪啪一下子开了很多个选项卡，之前选项卡依然在加载渲染的状态？或者说是浏览器新打开时记住的上一次关闭选项卡的状态？求达人指明！
>
> “preview” 预览。根据部分2011年底相关国外部分文章的说法，这种状态出现在，如window7系统下，鼠标放在底部（一般是）任务栏的图标上（预览）的时候。见下截图：
>
> win7鼠标图标程序界面预览 张鑫旭-鑫空间-鑫生活
>
> 但是根据自己的实际测试，似乎并没有这种状态的改变——包括IE10浏览器。可能是时代改变，一切都遵循规范了吧。因此，我们重点关注前面三个状态值就可以了。

visibilitychange: 当可见状态改变时候触发的事件。

详细地址 [http://www.zhangxinxu.com/wordpress/2012/11/page-visibility-api-introduction-extend/](http://www.zhangxinxu.com/wordpress/2012/11/page-visibility-api-introduction-extend/)

**如何在页面上实现一个圆形的可点击区域？**

1、map+area或者svg   map参考：[http://www.cnblogs.com/ITRoad/archive/2011/12/14/2287520.html](http://www.cnblogs.com/ITRoad/archive/2011/12/14/2287520.html)

2、border-radius

3、纯js实现 需要求一个点在不在圆上简单算法、获取鼠标坐标等等

**实现不使用 border 画出1px高的线，在不同浏览器的标准模式与怪异模式下都能保持一致的效果。**

<div style="height:1px;overflow:hidden;background:red"></div>

**网页验证码是干嘛的，是为了解决什么安全问题。**

区分用户是计算机还是人的公共全自动程序。可以防止恶意破解密码、刷票、论坛灌水；

有效防止黑客对某一个特定注册用户用特定程序暴力破解方式进行不断的登陆尝试。

**title与h1的区别、b与strong的区别、i与em的区别？**

title属性没有明确意义只表示是个标题，H1则表示层次明确的标题，对页面信息的抓取也有很大的影响；

strong是标明重点内容，有语气加强的含义，使用阅读设备阅读网络时：<strong>会重读，而<B>是展示强调内容。

i内容展示为斜体，em表示强调的文本；

Physical Style Elements -- 自然样式标签

b, i, u, s, pre

Semantic Style Elements -- 语义样式标签

strong, em, ins, del, code

应该准确使用语义样式标签, 但不能滥用, 如果不能确定时首选使用自然样式标签。

---

#### 2016年12月14日21:34:51

**请描述一下 cookies，sessionStorage 和 localStorage 的区别？**

cookie是网站为了标示用户身份而储存在用户本地终端（Client Side）上的数据（通常经过加密）。

cookie数据始终在同源的http请求中携带（即使不需要），记会在浏览器和服务器间来回传递。

sessionStorage和localStorage不会自动把数据发给服务器，仅在本地保存。

存储大小：

cookie数据大小不能超过4k。

sessionStorage和localStorage 虽然也有存储大小的限制，但比cookie大得多，可以达到5M或更大。

有期时间：

localStorage    存储持久数据，浏览器关闭后数据不丢失除非主动删除数据；

sessionStorage  数据在当前浏览器窗口关闭后自动删除。

cookie          设置的cookie过期时间之前一直有效，即使窗口或浏览器关闭

**iframe有那些缺点？**

*iframe会阻塞主页面的Onload事件；

*搜索引擎的检索程序无法解读这种页面，不利于SEO;

*iframe和主页面共享连接池，而浏览器对相同域的连接有限制，所以会影响页面的并行加载。

使用iframe之前需要考虑这两个缺点。如果需要使用iframe，最好是通过javascript

动态给iframe添加src属性值，这样可以绕开以上两个问题。

**Label的作用是什么？是怎么用的？**

label标签来定义表单控制间的关系,当用户选择该标签时，浏览器会自动将焦点转到和标签相关的表单控件上。

<label for="Name">Number:</label>

<input type=“text“name="Name" id="Name"/>

<label>Date:<input type="text" name="B"/></label>

**HTML5的form如何关闭自动完成（自动提示）功能？**

给不想要提示的 form 或某个 input 设置为 autocomplete=off。

**如何实现浏览器内多个标签页之间的通信? (阿里)**

WebSocket、SharedWorker；

也可以调用localstorge、cookies等本地存储方式；

localstorge另一个浏览上下文里被添加、修改或删除时，它都会触发一个事件，

我们通过监听事件，控制它的值来进行页面信息通信；

注意quirks：Safari 在无痕模式下设置localstorge值时会抛出 QuotaExceededError 的异常；

---

#### 2016年12月13日23:08:06

**常见的浏览器内核有哪些？**

Trident内核：IE,MaxThon,TT,The World,360,搜狗浏览器等。[又称MSHTML]

Gecko内核：Netscape6及以上版本，FF,MozillaSuite/SeaMonkey等

Presto内核：Opera7及以上。      [Opera内核原为：Presto，现为：Blink;]

Webkit内核：Safari,Chrome等。   [ Chrome的：Blink（WebKit的分支）]

[http://www.cnblogs.com/fullhouse/archive/2011/12/19/2293455.html](http://www.cnblogs.com/fullhouse/archive/2011/12/19/2293455.html)

**html5有哪些新特性、移除了那些元素？如何处理HTML5新标签的浏览器兼容问题？如何区分 HTML 和 HTML5？**

* HTML5 现在已经不是 SGML 的子集，主要是关于图像，位置，存储，多任务等功能的增加。

绘画 canvas;

用于媒介回放的 video 和 audio 元素;

本地离线存储 localStorage 长期存储数据，浏览器关闭后数据不丢失;

sessionStorage 的数据在浏览器关闭后自动删除;

语意化更好的内容元素，比如 article、footer、header、nav、section;

表单控件，calendar、date、time、email、url、search;

新的技术webworker, websocket, Geolocation;

移除的元素：

纯表现的元素：basefont，big，center，font, s，strike，tt，u;

对可用性产生负面影响的元素：frame，frameset，noframes；

* 兼容问题 支持HTML5新标签：

IE8/IE7/IE6支持通过document.createElement方法产生的标签，

可以利用这一特性让这些浏览器支持HTML5新标签，

浏览器支持新标签后，还需要添加标签默认的样式。

当然也可以直接使用成熟的框架、比如html5shim;

<!--[if lt IE 9]>

<script> src="http://html5shim.googlecode.com/svn/trunk/html5.js"</script>

<![endif]-->

* 如何区分HTML5： DOCTYPE声明\新增的结构元素\功能元素

**简述一下你对HTML语义化的理解？**

用正确的标签做正确的事情。

html语义化让页面的内容结构化，结构更清晰，便于对浏览器、搜索引擎解析;

即使在没有样式CSS情况下也以一种文档格式显示，并且是容易阅读的;

搜索引擎的爬虫也依赖于HTML标记来确定上下文和各个关键字的权重，利于SEO;

使阅读源代码的人对网站更容易将网站分块，便于阅读维护理解。

**HTML5的离线储存怎么使用，工作原理能不能解释一下？**

在用户没有与因特网连接时，可以正常访问站点或应用，在用户与因特网连接时，更新用户机器上的缓存文件。

原理：HTML5的离线存储是基于一个新建的.appcache文件的缓存机制(不是存储技术)，通过这个文件上的解析清单离线存储资源，这些资源就会像cookie一样被存储了下来。之后当网络在处于离线状态下时，浏览器会通过被离线存储的数据进行页面展示。

如何使用：

1、页面头部像下面一样加入一个manifest的属性；

2、在cache.manifest文件的编写离线存储的资源；

CACHE MANIFEST

#v0.11

CACHE:

js/app.js

css/style.css

NETWORK:

resourse/logo.png

FALLBACK:

/ /offline.html

3、在离线状态时，操作window.applicationCache进行需求实现。

详细参考 [http://yanhaijing.com/html/2014/12/28/html5-manifest/](http://yanhaijing.com/html/2014/12/28/html5-manifest/)
[https://segmentfault.com/a/1190000000732617](https://segmentfault.com/a/1190000000732617)

**浏览器是怎么对HTML5的离线储存资源进行管理和加载的呢？**

在线的情况下，浏览器发现html头部有manifest属性，它会请求manifest文件，如果是第一次访问app，那么浏览器就会根据manifest文件的内容下载相应的资源并且进行离线存储。如果已经访问过app并且资源已经离线存储了，那么浏览器就会使用离线的资源加载页面，然后浏览器会对比新的manifest文件与旧的manifest文件，如果文件没有发生改变，就不做任何操作，如果文件改变了，那么就会重新下载文件中的资源并进行离线存储。

离线的情况下，浏览器就直接使用离线存储的资源。

详细请参考 [https://segmentfault.com/a/1190000000732617](https://segmentfault.com/a/1190000000732617)

---

#### 2016年12月12日23:11:36

**Doctype作用？标准模式与兼容模式各有什么区别?**

（1）、<!DOCTYPE>声明位于位于HTML文档中的第一行，处于 <html> 标签之前。告知浏览器的解析器用什么文档标准解析这个文档。DOCTYPE不存在或格式不正确会导致文档以兼容模式呈现。

（2）、标准模式的排版 和JS运作模式都是以该浏览器支持的最高标准运行。在兼容模式中，页面以宽松的向后兼容的方式显示,模拟老式浏览器的行为以防止站点无法工作。

**HTML5 为什么只需要写 <!DOCTYPE HTML>？**

HTML5 不基于 SGML，因此不需要对DTD进行引用，但是需要doctype来规范浏览器的行为（让浏览器按照它们应该的方式来运行）；

而HTML4.01基于SGML,所以需要对DTD进行引用，才能告知浏览器文档所使用的文档类型。

**行内元素有哪些？块级元素有哪些？ 空(void)元素有那些？**

首先：CSS规范规定，每个元素都有display属性，确定该元素的类型，每个元素都有默认的display值，如div的display默认值为“block”，则为“块级”元素；span默认display属性值为“inline”，是“行内”元素。

（1）行内元素有：a b span img input select strong（强调的语气）

（2）块级元素有：div ul ol li dl dt dd h1 h2 h3 h4…p

（3）常见的空元素：

<br> <hr> <img> <input> <link> <meta>

鲜为人知的是：

<area> <base> <col> <command> <embed> <keygen> <param> <source> <track> <wbr>

不同浏览器（版本）、HTML4（5）、CSS2等实际略有差异

参考: [http://stackoverflow.com/questions/6867254/browsers-default-css-for-html-elements](http://stackoverflow.com/questions/6867254/browsers-default-css-for-html-elements)

**页面导入样式时，使用link和@import有什么区别？**

（1）link属于XHTML标签，除了加载CSS外，还能用于定义RSS, 定义rel连接属性等作用；而@import是CSS提供的，只能用于加载CSS;

（2）页面被加载的时，link会同时被加载，而@import引用的CSS会等到页面被加载完再加载;

（3）import是CSS2.1 提出的，只在IE5以上才能被识别，而link是XHTML标签，无兼容问题;

**介绍一下你对浏览器内核的理解？**

主要分成两部分：渲染引擎(layout engineer或Rendering Engine)和JS引擎。

渲染引擎：负责取得网页的内容（HTML、XML、图像等等）、整理讯息（例如加入CSS等），以及计算网页的显示方式，然后会输出至显示器或打印机。浏览器的内核的不同对于网页的语法解释会有不同，所以渲染的效果也不相同。所有网页浏览器、电子邮件客户端以及其它需要编辑、显示网络内容的应用程序都需要内核。

JS引擎则：解析和执行javascript来实现网页的动态效果。

最开始渲染引擎和JS引擎并没有区分的很明确，后来JS引擎越来越独立，内核就倾向于只指渲染引擎。  v8引擎
