---
Title: "每日一练  java"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-05-03 22:23:53"
Cover: ""
WizGuid: "c170f30f-5302-4012-b92c-af296d53e552"
WizType: "document"
WizLocation: "/每日一练/"
WizDataMd5: "7988616fac390ea412581160b49e85d8"
Modified: "2018-04-17 21:55:23"
WizSyncedAt: "2026-08-18 18:31:49"
---

[http://blog.csdn.net/u014206526/article/category/6374632](http://blog.csdn.net/u014206526/article/category/6374632)

[http://blog.csdn.net/zxq1138634642/article/details/8094621](http://blog.csdn.net/zxq1138634642/article/details/8094621)

[Java面试宝典2016版.pdf](wiz://open_attachment?guid=17fe3ec5-f813-4d98-adb7-bb3dfa328d11)

[http://blog.csdn.net/jackfrued/article/details/44921941](http://blog.csdn.net/jackfrued/article/details/44921941)

#### 2017年7月12日22:29:02

16、页面间对象传递的方法

request， session， application， cookie 等

17、 JSP 和 Servlet 有哪些相同点和不同点，他们之间的联系是什么？

JSP 是 Servlet 技术的扩展，本质上是 Servlet 的简易方式，更强调应用的外表表达。

JSP编译后是"类 servlet"。

Servlet 和 JSP 最主要的不同点在于， Servlet 的应用逻辑是在 Java文件中，并且完全从表示层中的 HTML 里分离开来。

而 JSP 的情况是 Java 和 HTML 可以组合成一个扩展名为.jsp 的文件。 JSP 侧重于视图， Servlet 主要用于控制逻辑。

18、 MVC 的各个部分都有那些技术来实现?如何实现?

答:MVC 是 Model－View－Controller 的简写。 Model 代表的是应用的业务逻辑（通过

JavaBean， EJB 组件实现）， View 是应用的表示面（由 JSP 页面产生）， Controller 是提供

应用的处理过程控制（一般是一个 Servlet），通过这种设计模型把应用逻辑，处理过程和显

示逻辑分成不同的组件实现。这些组件可以进行交互和重用。

19、我们在 web 应用开发过程中经常遇到输出某种编码的字符，如 iso8859-1

等，如何输出一个某种编码的字符串？

tempStr = newString(str.getBytes("ISO-8859-1"), "GBK");

20升或者降序排序

Arrays.sort(数组) 默认是升序

后面的算法是改良过的快速排序

自定义排序

public static <T> void sort(T[] a  Comparator<? super T> c)

```
package test;
import java.util.Arrays;
import java.util.Comparator;
publicclassMain {publicstaticvoid main(String[] args) {
//注意，要想改变默认的排列顺序，不能使用基本类型（int,double, char）//而要使用它们对应的类
         Integer[] a = {9, 8, 7, 2, 3, 4, 1, 0, 6, 5};
//定义一个自定义类MyComparator的对象
        Comparator cmp = new MyComparator();
        Arrays.sort(a, cmp);
for(int i = 0; i < a.length; i ++) {
             System.out.print(a[i] + " ");
        }
    }
}
//Comparator是一个接口，所以这里我们自己定义的类MyComparator要implents该接口//而不是extends Comparator
```

```
class MyComparator implements Comparator<Integer>{
```

```
  @Overridepublicint compare(Integer o1, Integer o2) {
//如果n1小于n2，我们就返回正值，如果n1大于n2我们就返回负值，//这样颠倒一下，就可以实现反向排序了
```

```
if(o1 < o2) {
return1;
         }elseif(o1 > o2) {
return -1;
         }else {
return0;
```

```
     }
    }
 }来源： http://www.cnblogs.com/upstart/p/6011927.html
```

简单的记法就是：顺序（a-b）升序；逆序（b-a）降序。

升序 a-b 都为负数   降序 b-a 都为负数

简单来说 返回负数的话 参数a会排在参数b的前面

返回正数参数b排在参数a前面

可以直接a-b 升序 或  b-a 降序

下面时冒泡排序

public class BubbleSort{ 2 public static void main(String[] args){ 3 int score[] = {67, 69, 75, 87, 89, 90, 99, 100}; 4 for (int i = 0; i < score.length -1; i++){ //最多做n-1趟排序 5 for(int j = 0 ;j < score.length - i - 1; j++){ //对当前无序区间score[0......length-i-1]进行排序(j的范围很关键，这个范围是在逐步缩小的) 6 if(score[j] < score[j + 1]){ //把小的值交换到后面 //目前降序 修改这里的为> 可以改造为升序 7 int temp = score[j]; 8 score[j] = score[j + 1]; 9 score[j + 1] = temp; 10 } 11 } 12 System.out.print("第" + (i + 1) + "次排序结果："); 13 for(int a = 0; a < score.length; a++){ 14 System.out.print(score[a] + "\t"); 15 } 16 System.out.println(""); 17 } 18 System.out.print("最终排序结果："); 19 for(int a = 0; a < score.length; a++){ 20 System.out.print(score[a] + "\t"); 21 } 22 } 23 }

23

1

```
 public class BubbleSort{
```

2

```
 2      public static void main(String[] args){
```

3

```
 3          int score[] = {67, 69, 75, 87, 89, 90, 99, 100};
```

4

```
 4          for (int i = 0; i < score.length -1; i++){    //最多做n-1趟排序
```

5

```
 5              for(int j = 0 ;j < score.length - i - 1; j++){    //对当前无序区间score[0......length-i-1]进行排序(j的范围很关键，这个范围是在逐步缩小的)
```

6

```
 6                  if(score[j] < score[j + 1]){    //把小的值交换到后面     //目前降序  修改这里的为> 可以改造为升序
```

7

```
 7                      int temp = score[j];
```

8

```
 8                      score[j] = score[j + 1];
```

9

```
 9                      score[j + 1] = temp;
```

10

```
10                  }
```

11

```
11              }
```

12

```
12              System.out.print("第" + (i + 1) + "次排序结果：");
```

13

```
13              for(int a = 0; a < score.length; a++){
```

14

```
14                  System.out.print(score[a] + "\t");
```

15

```
15              }
```

16

```
16              System.out.println("");
```

17

```
17          }
```

18

```
18              System.out.print("最终排序结果：");
```

19

```
19              for(int a = 0; a < score.length; a++){
```

20

```
20                  System.out.print(score[a] + "\t");
```

21

```
21         }
```

22

```
22      }
```

23

```
23  }
```

---

#### 2017年7月11日22:50:54

11. jsp 有哪些内置对象?作用分别是什么?分别有什么方法？

答:JSP 共有以下9个内置的对象：

request 用户端请求，此请求会包含来自 GET/POST 请求的参数

response 网页传回用户端的回应

pageContext 网页的属性是在这里管理

session 与请求有关的会话期

application servlet 正在执行的内容

out 用来传送回应的输出

config servlet 的构架部件

page JSP 网页本身

exception 针对错误网页，未捕捉的例外

request 表示 HttpServletRequest 对象。它包含了有关浏览器请求的信息，并且提供了几个

用于获取 cookie, header,和 session 数据的有用的方法

response 表示 HttpServletResponse 对象，并提供了几个用于设置送回浏览器的响应的

方法（如 cookies,头信息等）

out 对象是 javax.jsp.JspWriter 的一个实例，并提供了几个方法使你能用于向浏览器回送

输出结果。

pageContext 表示一个 javax.servlet.jsp.PageContext 对象。它是用于方便存取各种范

围的名字空间、 servlet 相关的对象的 API，并且包装了通用的 servlet 相关功能的方法。

session 表示一个请求的 javax.servlet.http.HttpSession 对象。 Session 可以存贮用户的

状态信息

applicaton 表示一个 javax.servle.ServletContext 对象。这有助于查找有关 servlet 引擎

和 servlet 环境的信息

config 表示一个 javax.servlet.ServletConfig 对象。该对象用于存取 servlet 实例的初始

化参数。

page 表示从该页面产生的一个 servlet 实例

[java快速提纲 jsp](wiz://open_document?guid=5b6bb4ea-b9b1-466d-8102-b98aa7b51e82&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

12. jsp 有哪些动作?作用分别是什么?

（这个问题似乎不重要，不明白为何有此题）

答:JSP 共有以下6种基本动作

jsp:include：在页面被请求的时候引入一个文件。

jsp:useBean：寻找或者实例化一个 JavaBean。

jsp:setProperty：设置 JavaBean 的属性。

jsp:getProperty：输出某个 JavaBean 的属性。

jsp:forward：把请求转到一个新的页面。

jsp:plugin：根据浏览器类型为 Java 插件生成 OBJECT 或 EMBED 标记

13、 JSP 的常用指令

isErrorPage(是否能使用 Exception 对象)， isELIgnored(是否忽略表达式)

14. JSP 中动态 INCLUDE 与静态 INCLUDE 的区别？

答：动态 INCLUDE 用 jsp:include 动作实现

<jsp:include page=included.jsp flush=true />它总是会检查所含文件中的变化，适合用于包

含动态页面，并且可以带参数

静态 INCLUDE 用 include 伪码实现,定不会检查所含文件的

变化，适用于包含静态页面 <%@include file=included.htm %>

15、两种跳转方式分别是什么?有什么区别?

答：有两种，分别为：

<jsp:include page=included.jsp flush=true>

<jsp:forward page= nextpage.jsp/>

前者页面不会转向 include 所指的页面，只是显示该页的结果，主页面还是原来的页面。执行完后还会回来，相当于函数调用。并且可以带参数.

后者完全转向新页面，不会再回来。相当于 go to 语句

---

#### 2017年6月28日22:31:27

4、说一说 Servlet 的生命周期?

答:servlet 有良好的生存期的定义，包括加载和实例化、初始化、处理请求以及服务结束。

这个生存期由 javax.servlet.Servlet 接口的 init,service 和 destroy 方法表达。

web 容器加载 servlet，生命周期开始。通过调用 servlet 的 init()方法进行 servlet 的初始化。通过调用 service()方法实现，根据请求的不同调用不同的 do***()方法。结束服务， web 容器调用 servlet 的 destroy()方法

6、 SERVLET API 中 forward()与 redirect()的区别？

答:前者仅是容器中控制权的转向，在客户端浏览器地址栏中不会显示出转向后的地址；后者则是完全的跳转，浏览器将会得到跳转的地址，并重新发送请求链接。这样，从浏览器的

地址栏中可以看到跳转后的链接地址。

所以，前者更加高效，在前者可以满足需要时，尽量使用 forward()方法，并且，这样也有助于隐藏实际的链接。在有些情况下，比如，需要跳

转到一个其它服务器上的资源，则必须使用sendRedirect()方法。

forward浏览器根本不知道服务器发送的内容是从哪儿来的，地址栏中还是原来的地址。

redirect 就是服务端根据逻辑,发送一个状态码,告诉浏览器重新去请求那个地址

10、 request.getAttribute()和 request.getParameter()有何区别?

getParameter获取请求参数  只能时string】

getAttribute 获取属性  可以时对象

当两个Web组件之间为转发关系时，转发目标组件通过getAttribute()方法来和转发源组件共享request范围内的数据

---

#### 2017年6月27日22:43:44

81、 java 中会存在内存泄漏吗，请简单描述

内存泄漏是程序分配了内存  但是对象无用（之类的）  导致占用了内存

在java中当被分配的对象可达但已无用（未对作废数据内存单元的引用置null）即会引起。

java 中的内存泄露的情况： 长生命周期的对象持有短生命周期对象的引用就很可能发生内存泄露，尽管短生命周期对象已经不再需要，但是因为长生命周期对象持有它的引用而导致

不能被回收，这就是 java 中内存泄露的发生场景，

通俗地说，就是程序员可能创建了一个对象，以后一直不再使用这个对象，这个对象却一直被引用，即这个对象无用但是却无法被垃圾回收器回收的，这就是 java 中可能出现内存泄露的情况，

例如，缓存系统，我们加载了一个对象放在缓存中(例如放在一个全局 map 对象中)，然后一直不再使用它，这个对象一直被缓存引用，但却不再被使用。

82、能不能自己写个类，也叫 java.lang.String？

可以，但在应用的时候，需要用自己的类加载器去加载，否则，系统的类加载器永远只是去加载 jre.jar 包中的那个 java.lang.String

由于在 tomcat 的 web 应用程序中，都是由 webapp自己的类加载器先自己加载 WEB-INF/classess 目录中的类，然后才委托上级的类加载器加载，如果我们在 tomcat 的 web 应用程序中写一个 java.lang.String，这时候 Servlet 程序加载的就是我们自己写的 java.lang.String，但是这么干就会出很多潜在的问题，原来所有用了 java.lang.String 类的都将出现问题

83. Java 代码查错

1.

abstract class Name {

private String name;

public abstract boolean isStupidName(String name) {}

}

大侠们，这有何错误?

答案: 错。 abstract method 必须以分号结尾，且不带花括号。

2.

public class Something {

void doSomething () {

private String s = "";

int l = s.length();

}

}

有错吗?

答案: 错。局部变量前不能放置任何访问修饰符 (private， public，和 protected)。 final 可

以用来修饰局部变量

(final 如同 abstract 和 strictfp，都是非访问修饰符， strictfp 只能修饰 class 和 method 而非

variable)。

3.

abstract class Something {

private abstract String doSomething ();

}

这好像没什么错吧?

答案: 错。 abstract 的 methods 不能以 private 修饰。 abstract 的 methods 就是让子类

implement(实现)具体细节的，怎么可以用 private 把 abstract

method 封锁起来呢? (同理， abstract method 前不能加 final)。

4

public class Something {

public int addOne(final int x) {

return ++x;

}

}

这个比较明显。

答案: 错。 int x 被修饰成 final，意味着 x 不能在 addOne method 中被修改。

5

public class Something {

public static void main(String[] args) {

Other o = new Other();

new Something().addOne(o);

}

public void addOne(final Other o) {

o.i++;

}

}

class Other {

public int i;

}

和上面的很相似，都是关于 final 的问题，这有错吗?

答案: 正确。在 addOne method 中，参数 o 被修饰成 final。如果在 addOne method 里我

们修改了 o 的 reference

(比如: o = new Other();)，那么如同上例这题也是错的。但这里修改的是 o 的 member

vairable

(成员变量)，而 o 的 reference 并没有改变。

6

class Something {

int i;

public void doSomething() {

System.out.println("i = "+ i);

}

}

有什么错呢? 看不出来啊。

答案: 正确。输出的是"i = 0"。 int i 属於 instant variable (实例变量，或叫成员变量)。 instant

variable 有 default value。 int 的 default value 是0。

7

class Something {

final int i;

public void doSomething() {

System.out.println("i = "+ i);

}

}

和上面一题只有一个地方不同，就是多了一个 final。这难道就错了吗?

答案: 错。 final int i 是个 final 的 instant variable (实例变量，或叫成员变量)。 final 的 instant

variable 没有 default value，必须在 constructor (构造器)结束之前被赋予一个明确的值。可

以修改为"final int i =0;"。

8.

public class Something {

public static void main(String[] args) {

Something s = new Something();

System.out.println("s.doSomething() returns " + doSomething());

}

public String doSomething() {

return "Do something ...";

}

}

看上去很完美

错 实例方法要用实例对象去调用

s.doSomething())

9

此处， Something 类的文件名叫 OtherThing.java

class Something {

private static void main(String[] something_to_do){

System.out.println("Dosomething ...");

}

}

正确。从来没有人说过 Java 的 Class 名字必须和其文件名相同。但 public class 的

名字必须和文件名相同

10．

interface A{

int x = 0;

}

class B{

int x =1;

}

class C extends B implements A {

public void pX(){

System.out.println(x);

}

public static void main(String[] args) {

new C().pX();

}

}

答案：错误。在编译时会发生错误(错误描述不同的 JVM 有不同的信息，意思就是未明确的

x 调用，两个 x 都匹配（就象在同时 import java.util 和 java.sql 两个包时直接声明 Date 一

样）。对于父类的变量,可以用 super.x 来明确，而接口的属性默认隐含为 public staticfinal.

所以可以通过 A.x 来明确

11.

interface Playable {

void play();

}

interface Bounceable {

void play();

}

interface Rollable extends Playable, Bounceable {  //java中接口可以继承多个接口

Ball ball = new Ball("PingPang");  //这里是 public static final

}

class Ball implements Rollable {

private String name;

public String getName() {

return name;

}

public Ball(String name) {

this.name =name;

}

public void play() {

ball = new Ball("Football");  //这里不能修改

System.out.println(ball.getName());

}

}

---

#### 2017年6月26日22:34:34

77、 GC 是什么?为什么要有 GC?

GC 是垃圾收集的意思（ Gabage Collection） ,内存处理是编程人员容易出现问题的地方，忘记或者错误的内存回收会导致程序或系统的不稳定甚至崩溃。

java释放内存由gc自动完成   没有显式的内存释放方法

78、垃圾回收的优点和原理。并考虑 2 种回收机制。

垃圾回收可以有效的防止内存泄露，有效的使用可以使用的内存。

两种回收机制

对新生代 使用 复制算法 回收内存

对老年带使用 标记清理的方法回收内存

标记要回收的对象

先通过判断在gcroot的引用链上是否有该对象的引用

对象进行根搜索之后，如果发现没有与GC Roots 相连接的引用链，就会被第一次标记并进行筛选

第一次标记 检查对象是否实现finalize方法并且没有调用过。

如果是没有实现finalze方法或者已经调用过finalze方法 但是 gc roots 上还是没有相应的应用链  则就会被标记

如果有实现finalze方法 放入队列F-Queue，随后会有一个低优先级的线程去执行这个队列里面对象的finalize方法

第二次标记：JVM 将对F-Queue队列里面的对象进行第二次标记。

参考：[jvm](wiz://open_document?guid=d7a3e539-cc24-43d0-9cfa-1203404964b9&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

79、垃圾回收器的基本原理是什么？垃圾回收器可以马上回收内存吗？有什么办法主动通知虚拟机进行垃圾回收？

根据根搜索算法判断对象是否可达   对不可达的对象进行标记筛选  对标记的对象进行回收

对新生代 使用 复制算法 回收内存

对老年带使用 标记清理的方法回收内存

手动执行systerm.gc()方法可以主动调用gc

但不保证马上执行

#### ---

####

#### 2017年6月22日22:26:47

71、说出一些常用的类，包，接口，请各举 5 个

要让人家感觉你对 java ee 开发很熟，所以，不能仅仅只列 core java 中的那些东西，要多

列你在做 ssh 项目中涉及的那些东西。就写你最近写的那些程序中涉及的那些类。

常用的类： BufferedReader BufferedWriter FileReader FileWirter String Integer，java.util.Date， System， Class， List,HashMap

常用的包： java.lang java.io java.util

java.sql,javax.servlet,org.apache.strtuts.action,org.hibernate

常用的接口： Remote List Map Document

NodeList,Servlet,HttpServletRequest,HttpServletResponse,Transaction(Hibernate)、

Session(Hibernate),HttpSessio

72、java 中有几种类型的流？ JDK 为每种类型的流提供了一些抽象类以供继承，

请说出他们分别是哪些类？

字节流，字符流。

字节流继承于 InputStream OutputStream，

字符流继承于InputStreamReaderOutputStreamWriter。

在 java.io 包中还有许多其他的流，主要是为了提高性能和使用方便。

[java快速提纲 IO流](wiz://open_document?guid=ea3dbc61-b017-4c49-84dd-30dd268633d8&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

73、字节流与字符流的区别

字符流时字节流的包装

字节流 根据一个编码格式 转换字符流

字符流 根据同一个编码格式可以转回字节流

74、什么是 java 序列化，如何实现 java 序列化？或者请解释 Serializable 接口的作用。

将一个 java 对象变成字节流的形式传出去或者从一个字节流中恢复成一个 java对象。

实现系列化，被传输的对象必须实现 serializable 接口，

实现序列化后， javac 编译时就会进行特殊处理，编译的类才可以被 writeObject 方法操作，这就是所谓的序列化。

75、描述一下 JVM 加载 class 文件的原理机制?

JVM 中类的装载是由 ClassLoader 和它的子类来实现的,Java ClassLoader 是一个重要的

Java 运行时系统组件。它负责在运行时查找和装入类文件的类。查找和加载类

76、 heap 和 stack 有什么区别。

java 的内存分为两类，一类是栈内存，一类是堆内存。

栈内存是指程序进入一个方法时，会为这个方法单独分配一块私属存储空间，用于存储这个方法内部的局部变量，当这个方法结束时，分配给这个方法的栈会释放，这个栈中的变量也将随之释放。

堆是与栈作用不同的内存，一般用于存放不放在当前方法栈中的那些数据，例如，使用 new创建的对象都放在堆里，所以，它不会随方法的结束而消失。 方法中的局部变量使用 final

修饰后，放在堆中，而不是栈中。

虚拟机栈是当方法执行时 为这个方法存储局部变量表、操作栈、动态链接、方法出口

局部变量表中存放了各种基本数据类型（boolean，byte，char，short，int，float，long，double）、对象引用（reference类型，

java堆 存放的是java实例对象。

---

#### 2017年6月15日23:25:08

66、 Collection 和 Collections 的区别。

Collection 是集合类的上级接口，继承与他的接口主要有 Set 和 List

Collections 是针对集合类的一个帮助类，他提供一系列静态方法实现对各种集合的搜索、排序、线程安全化等操作。

67、 Set 里的元素是不能重复的，那么用什么方法来区分重复与否呢?是用==还是 equals()?它们有何区别?

Set 里的元素是不能重复的，元素重复与否是使用 equals()方法进行判断的。

equals()和==方法决定引用值是否指向同一对象 equals()在类中被覆盖，为的是当两个

分离的对象的内容和类型相配的话，返回真值

68、你所知道的集合类都有哪些？主要方法？

最常用的集合类是 List 和 Map。 List 的具体实现包括 ArrayList 和 Vector，它们是可变大小的列表，比较适合构建、存储和操作任何类型对象的元素列表。 List 适用于按数值索

引访问元素的情形。

Map 提供了一个更通用的元素存储方法。 Map 集合类用于存储元素对（称作"键"和"值"），其中每个键映射到一个值。

我记的不是方法名，而是思想，我知道它们都有增删改查的方法，但这些方法的具体名称，我记得不是很清楚，

对于 set，大概的方法是 add,remove, contains；

我记住的一些思想就是 List 类会有 get(int index)这样的方法，因为它可以按顺序取元素，而 set 类中没有 get(int index)这样的方法。

List 和 set 都可以迭代出所有元素，迭代时先要得到一个 iterator 对象，所以， set 和 list 类都有一个 iterator 方法，用于返回那个 iterator 对象。

对于 map，大概的方法就是 put,remove， contains 等，因为，我只要在 eclispe 下按点操作符，很自然的这些方法就出来了。

map 可以返回三个集合，一个是返回所有的 key 的集合，另外一个返回的是所有 value 的集合，再一个返回的 key 和 value 组合成的 EntrySet 对象的集合， map 也

有 get 方法，参数是 key，返回值是 key 对应的 value。

69、两个对象值相同(x.equals(y) == true)，但却可有不同的 hash code，这句话对不对?

对。

如果对象要保存在 HashSet 或 HashMap 中，它们的 equals 相等，那么，它们的 hashcode值就必须相等。

如果两个对象equals相等 但是hashcode值不同 放入到HashSet 或 HashMap可能会被认为是两个不同的值 。因为这两个类型时通过hashcode来设定存放位置

如果不是要保存在HashSet或HashMap，则与hashcode没有什么关系了，这时候hashcode不等是可以的，例如 arrayList 存储的对象就不用实现 hashcode，当然，我们没有理由不实

现，通常都会去实现的。

以HashSet为例子  （hashmap的key部分应该也可以这么理解）

添加对象时

先判断hashcode是否存在  不存在直接添加

hashcode值存在再去进行equals比较

equals比较返回true表示元素以存在不添加

equals比较全部返回false表示元素不存在进行添加

[Java提高篇——equals()与hashCode()方法详解](wiz://open_document?guid=d8525b9e-573c-4c29-a7f6-1a15c4264689&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

70、 TreeSet 里面放对象，如果同时放入了父类和子类的实例对象，那比较时使用的是父类的 compareTo 方法，还是使用的子类的 compareTo 方法，还是抛异常

当前的 add 方法放入的是哪个对象，就调用哪个对象的 compareTo 方法，至于这个 compareTo 方法怎么做，就看当前这个对象的类中是如何编写这个方法的

public class ParentimplementsComparable { private int age = 0; public Parent(int age){ this.age = age; } public int compareTo(Object o){ // TODO Auto-generated method stub System.out.println("method ofparent"); Parent o1 = (Parent)o; return age>o1.age?1:age<o1.age?-1:0; } } public class Childextends Parent { public Child(){ super(3); } public int compareTo(Object o){ // TODO Auto-generated methodstub System.out.println("methodof child"); // Child o1 = (Child)o; return 1; } } public class TreeSetTest { /** * @paramargs */ public static voidmain(String[] args) { // TODO Auto-generated method stub TreeSet set = new TreeSet(); set.add(newParent(3)); set.add(new Child()); set.add(newParent(4)); System.out.println(set.size()); } }

36

1

```
public class ParentimplementsComparable {
```

2

```
private int age = 0;
```

3

```
public Parent(int age){
```

4

```
this.age = age;
```

5

```
}
```

6

```
public int compareTo(Object o){
```

7

```
// TODO Auto-generated method stub
```

8

```
System.out.println("method ofparent");
```

9

```
Parent o1 = (Parent)o;
```

10

```
return age>o1.age?1:age<o1.age?-1:0;
```

11

```
}
```

12

```
}
```

13

```
public class Childextends Parent {
```

14

```
public Child(){
```

15

```
super(3);
```

16

```
}
```

17

```
public int compareTo(Object o){
```

18

```
// TODO Auto-generated methodstub
```

19

```
System.out.println("methodof child");
```

20

```
// Child o1 = (Child)o;
```

21

```
return 1;
```

22

```
}
```

23

```
}
```

24

```
public class TreeSetTest {
```

25

```
/**
```

26

```
* @paramargs
```

27

```
*/
```

28

```
public static voidmain(String[] args) {
```

29

```
// TODO Auto-generated method stub
```

30

```
TreeSet set = new TreeSet();
```

31

```
set.add(newParent(3));
```

32

```
set.add(new Child());
```

33

```
set.add(newParent(4));
```

34

```
System.out.println(set.size());
```

35

```
}
```

36

```
}
```

---

#### 2017年6月13日22:14:51

61、 List 和 Map 区别?

一个是存储单列数据的集合，另一个是存储键和值这样的双列数据的集合，

List 中存储的数据是有顺序，并且允许重复；

Map 中存储的数据是没有顺序的，其键是不能重复的，它的值是可以有重复的。

62、 List, Set, Map 是否继承自 Collection 接口?

List， Set 是， Map 不是

63、 List、 Map、 Set 三个接口，存取元素时，各有什么特点？

首先， List 与 Set 具有相似性，它们都是单列元素的集合，所以，它们有一个功共同的父接口，叫 Collection。

Set 里面不允许有重复的元素，

List 表示有先后顺序的集合，是按插入的先后顺序  可以插队  可以元素可以重复

Map 与 List 和 Set 不同，它是双列的集合

List 以特定次序来持有元素，可有重复元素。 Set 无法拥有重复元素,内部排序。 Map 保存key-value 值， value 可多值

HashSet 按照 hashcode 值的某种运算方式进行存储，而不是直接按 hashCode 值的大小进行存储。

!hashset 集合比较两个对象是否相等，首先看hashcode 方法是否相等，然后看 equals 方法是否相等

同一个对象可以在 Vector 中加入多次。往集合里面加元素，相当于集合里用一根绳子连接到了目标对象。往 HashSet 中却加不了多次的

64、说出 ArrayList,Vector, LinkedList 的存储性能和特性

ArrayList 和 Vector 都是使用数组方式存储数据，此数组元素数大于实际存储的数据以便增加和插入元素，它们都允许直接按序号索引元素，但是插入元素要涉及数组元素移动等内存

操作，所以索引数据快而插入数据慢， Vector 由于使用了 synchronized 方法（线程安全），通常性能上较 ArrayList 差，

而 LinkedList 使用双向链表实现存储，按序号索引数据需要进行前向或后向遍历，但是插入数据时只需要记录本项的前后项即可，所以插入速度较快。LinkedList 也是线程不安全的， LinkedList 提供了一些方法，使得 LinkedList 可以被当作堆栈和队列来使用。

65、去掉一个 Vector 集合中重复的元素

Vector newVector = new Vector();

For (int i=0;i<vector.size();i++)

{

Object obj = vector.get(i);

if(!newVector.contains(obj);

newVector.add(obj);

}

还有一种简单的方式， HashSet set = new HashSet(vector);

---

#### 2017年6月11日22:54:27

41、运行时异常与一般异常有何异同？

异常表示程序运行过程中可能出现的非正常状态，运行时异常表示虚拟机的通常操作中可能遇到的异常，是一种常见运行错误。

java 编译器要求方法必须声明抛出可能发生的非运行时异常，但是并不要求必须声明抛出未被捕获的运行时异常

[java快速提纲 异常](wiz://open_document?guid=40a37b86-d630-402a-bca5-31fe069c1a73&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

检查性异常：（）非运行时异常是RuntimeException以外的异常，类型上都属于Exception类及其子类

非检查性异常（运行时异常）：都是RuntimeException类及其子类异常。对于这种异常，JAVA编译器强制要求我们必需对出现的这些异常进行catch并处理，否则程序就不能编译通过

42、 error 和 exception 有什么区别?

error 表示恢复不是不可能但很困难的情况下的一种严重问题。比如说内存溢出。不可能指望程序能处理这样的情况。 应用程序不能处理

exception 表示一种设计或实现问题。也就是说，它表示如果程序运行正常，从不会发生的情况。

43、 Java 中的异常处理机制的简单原理和应用。

异常是指 java 程序运行时（非编译）所发生的非正常情况或错误

44、请写出你最常见到的 5 个 runtime exception。

| ArithmeticException | 当出现异常的运算条件时，抛出此异常。例如，一个整数"除以零"时，抛出此类的一个实例。 |
| --- | --- |
| ArrayIndexOutOfBoundsException | 用非法索引访问数组时抛出的异常。如果索引为负或大于等于数组大小，则该索引为非法索引。 |
| ArrayStoreException | 试图将错误类型的对象存储到一个对象数组时抛出的异常。 |
| ClassCastException | 当试图将对象强制转换为不是实例的子类时，抛出该异常。 |
| IllegalArgumentException | 抛出的异常表明向方法传递了一个不合法或不正确的参数。 |
| IllegalMonitorStateException | 抛出的异常表明某一线程已经试图等待对象的监视器，或者试图通知其他正在等待对象的监视器而本身没有指定监视器的线程。 |
| IllegalStateException | 在非法或不适当的时间调用方法时产生的信号。换句话说，即 Java 环境或 Java 应用程序没有处于请求操作所要求的适当状态下。 |
| IllegalThreadStateException | 线程没有处于请求操作所要求的适当状态时抛出的异常。 |
| IndexOutOfBoundsException | 指示某排序索引（例如对数组、字符串或向量的排序）超出范围时抛出。 |
| NegativeArraySizeException | 如果应用程序试图创建大小为负的数组，则抛出该异常。 |
| NullPointerException | 当应用程序试图在需要对象的地方使用 `null` 时，抛出该异常 |
| NumberFormatException | 当应用程序试图将字符串转换成一种数值类型，但该字符串不能转换为适当格式时，抛出该异常。 |
| SecurityException | 由安全管理器抛出的异常，指示存在安全侵犯。 |
| StringIndexOutOfBoundsException | 此异常由 `String` 方法抛出，指示索引或者为负，或者超出字符串的大小。 |
| UnsupportedOperationException | 当不支持请求的操作时，抛出该异常。<br>来源： [http://www.runoob.com/java/java-exceptions.html](http://www.runoob.com/java/java-exceptions.html) |

45、 JAVA 语言如何进行异常处理，关键字： throws,throw,try,catch,finally 分别代表什么意义？在 try 块中可以抛出异常吗？

throws 捕获并继续向上层抛出异常

throw 抛出异常

try catch 是内部捕获异常并做自定义处理

finally 是无论是否有异常都会被处理的语句，除非在 finally 前存在被执行的

System.exit(int i)时除外

---

#### 2017年6月8日21:57:36

57、介绍 Collection 框架的结构

[java 快速提纲 集合](wiz://open_document?guid=1c88dc9f-d74f-435f-943a-45d074e2ac8b&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

Collection：List列表，Set集

Map：Hashtable，HashMap，TreeMap

**Collection**是单列集合

**List**元素是有序的、可重复

有序的 collection，可以对列表中每个元素的插入位置进行精确地控制。

可以根据元素的整数索引（在列表中的位置）访问元素，并搜索列表中的元素。

可存放重复元素，元素存取是有序的。

List接口中常用类

**l****Vector**： 线程安全，但速度慢，已被ArrayList替代。

底层数据结构是数组结构

**l****ArrayList**：线程不安全，查询速度快。

底层数据结构是数组结构

**l****LinkedList**：线程不安全。增删速度快。

底层数据结构是链表结构

Stack

是Vector 的子类，栈 的结构（后进先出）

Queue（队列）

Queue 内部是队列的数据结构（先进先出），新插入的元素会在尾部；插入之后，会慢慢向顶部移动；

类似生活中的排队

PriorityQueue（优先级队列)

除了实现Queue 接口，PriorityQueue 还对插入的元素进行重新排序（Comparator）

Deque

双端队列，Deque 可以从两端来添加啊，删除元素，因此，Deque 可以当作队列使用，也可当作栈来使用

ArrayDeque

基于数组的双端队列，和ArrayList 类似，底层都是采用一个动态可分配的Object[] 的数组

**Set**(集)元素无序的、不可重复。

取出元素的方法只有迭代器。不可以存放重复元素，元素存取是无序的。

Set接口中常用的类

**l****HashSet**：线程不安全，存取速度快。

它是如何保证元素唯一性的呢？依赖的是元素的hashCode方法和euqals方法。

**l****TreeSet**：线程不安全，可以对Set集合中的元素进行排序。

它的排序是如何进行的呢？通过compareTo或者compare方法中的来保证元素的唯一性。元素是以二叉树的形式存放的。

LinkedHashSet

和HashSet 一样，是利用hashCode 来觉得元素的存储位置，但是使用链表维护元素的次序

当遍历的时候，是按照插入的顺序遍历的

LinkedHashSet 需要维护元素的插入顺序，因此性能会略低于HashSet的性能，但是在迭代访问所有元素是性能会很高（链表适合遍历）

SortedSet

排序，compareTo() 方法进行比较，插入的元素类型需要一样，否则出现ClassCastException

EnumSet

为枚举类设计的集合类

**Map**是一个双列集合

|--**Hashtable**:线程安全，速度快。底层是哈希表数据结构。是**同步**的。

不允许null作为键，null作为值。

|--**Properties**:用于配置文件的定义和操作，使用频率非常高，同时键和值都是字符串。

是集合中可以和IO技术相结合的对象。(到了IO在学习它的特有和io相关的功能。)

|--**HashMap**:线程不安全，速度慢。底层也是哈希表数据结构。是**不同步**的。

允许null作为键，null作为值。替代了Hashtable.

|--**LinkedHashMap**: 可以保证HashMap集合有序。存入的顺序和取出的顺序一致。

|--**TreeMap**：可以用来对Map集合中的**键**进行排序.

来源： [http://blog.csdn.net/coodlong/article/details/50835440](http://blog.csdn.net/coodlong/article/details/50835440)

58、 Collection 框架中实现比较要实现什么接口

comparable/comparator

只是 Comparable 是在集合内部定义的方法实现的排序，Comparator 是在集合外部实现的排序，所以，如想实现排序，就需要在集合外定义 Comparator 接口的方法或在集合内实现 Comparable 接口的方法。

59、 ArrayList 和 Vector 的区别

这两个类都实现了 List 接口（ List 接口继承了 Collection 接口），他们都是有序集合，，相当于一种动态的数组，我们以后可以按位置索引号取出某个元素，，并且其中的数据是允许重复的，

区别

（ 1）同步性：

Vector 是线程安全的，也就是说是它的方法之间是线程同步的，而 ArrayList 是线程序不安全的，它的方法之间是线程不同步的

备注：对于 Vector&ArrayList、 Hashtable&HashMap，要记住线程安全的问题，记住 Vector与 Hashtable 是旧的，是 java 一诞生就提供了的，它们是线程安全的，ArrayList 与 HashMap

是 java2时才提供的，它们是线程不安全的。所以，我们讲课时先讲老的。

（ 2）数据增长：

ArrayList 与 Vector 都有一个初始的容量大小，当存储进它们里面的元素的个数超过了容量时，就需要增加 ArrayList 与 Vector 的存储空间，每次要增加存储空间时，不是只增

加一个存储单元，而是增加多个存储单元，每次增加的存储单元的个数在内存空间利用与程序效率之间要取得一定的平衡。 Vector 默认增长为原来两倍，而 ArrayList 的增长策略在文

档中没有明确规定（从源代码看到的是增长为原来的1.5倍）。 ArrayList 与 Vector 都可以设置初始的空间大小， Vector 还可以设置增长的空间大小，而 ArrayList 没有提供设置增长空

间的方法。

总结：即 Vector 增长原来的一倍， ArrayList 增加原容量的 1.5倍+1

60、 HashMap 和 Hashtable 的区别

（条理上还需要整理，也是先说相同点，再说不同点）

相同点 ： 都实现了map接口

不同点：

HashMap 是 Hashtable 的轻量级实现（非线程安全的实现），他们都完成了 Map 接口，主要区别在于 HashMap 允许空（ null）键值（ key） ,由于非线程安全，在只有一个线程访问

的情况下，效率要高于 Hashtable。

HashMap 允许将 null 作为一个 entry 的 key 或者 value，而 Hashtable 不允许。

HashMap 把 Hashtable 的 contains 方法去掉了，改成 containsvalue 和 containsKey。因为contains 方法容易让人引起误解。

Hashtable 继承自 Dictionary 类，而 HashMap 是 Java1.2引进的 Map interface 的一个实现。

最大的不同是， Hashtable 的方法是 Synchronize 的，而 HashMap 不是，在多个线程访问Hashtable 时，不需要自己为它的方法实现同步，而 HashMap 就必须为之提供外同步。

Hashtable 和 HashMap 采用的 hash/rehash 算法都大概一样，所以性能不会有很大的差异。

就 HashMap 与 HashTable 主要从三方面来说。

一.历史原因:Hashtable 是基于陈旧的 Dictionary 类的， HashMap 是 Java 1.2引进的 Map接口的一个实现

二.同步性:Hashtable 是线程安全的，也就是说是同步的，而 HashMap 是线程序不安全的，不是同步的

三.值：只有 HashMap 可以让你将空值作为一个表的条目的 key 或 value

---

#### 2017年6月6日22:22:57

51、启动一个线程是用 run()还是 start()? .

启动一个线程是调用 start()方法，使线程就绪状态，以后可以被调度为运行状态，一个线程

必须关联一些具体的执行代码， run()方法是该线程所关联的执行代码。

52、当一个线程进入一个对象的一个 synchronized 方法后，其它线程是否可进入此对象的其它方法?

分几种情况：

1. 其他方法前是否加了 synchronized 关键字，如果没加，则能。

2. 如果这个方法内部调用了 wait （释放锁并等待重新获取到锁 等待notify），则可以进入其他 synchronized 方法。

3. 如果其他个方法都加了 synchronized 关键字，并且内部没有调用 wait，则不能。

53、 线程的基本概念、线程的基本状态以及状态之间的关系

多进程是指操作系统能同时运行多个任务（程序）。

多线程是指在同一程序中有多个顺序流在执行。

多线程：指的是这个程序（一个进程）运行时产生了不止一个线程

并行与并发：

并行：多个cpu实例或者多台机器同时执行一段处理逻辑，是真正的同时。

并发：通过cpu调度算法，让用户看上去同时执行，实际上从cpu操作层面不是真正的同时。并发往往在场景中有公用的资源，那么针对这个公用的资源往往产生瓶颈，我们会用TPS或者QPS来反应这个系统的处理能力。

![[attachments/ff1f9a76-250b-4f52-b68b-8b2eea6a244b.png]]

线程的状态简单来说 分为五个阶段：创建、就绪、运行、阻塞（ synchronize 阻塞， wait 和 sleep 挂起）、终止。

调用线程的 start 方法后线程进入就绪状态，

线程调度系统将就绪状态的线程转为运行状态，

遇到 synchronized 语句时，由运行状态转为阻塞，

当 synchronized 获得锁后，由阻塞转为运行，在这种情况可以调用 wait 方法转为挂起状态，

当线程关联的代码执行完后，线程变为结束状态。

54 简述 synchronized 和 java.util.concurrent.locks.Lock 的异同？

主要相同点： Lock 能完成 synchronized 所实现的所有功能

主要不同点： Lock 有比 synchronized 更精确的线程语义和更好的性能。 synchronized 会自

动释放锁（包括在方法抛出异常的时候会自动解锁 ），而 Lock 一定要求程序员手工释放，并且必须在 finally 从句中释放。

Lock 还有更强大的功能，例如，它的 tryLock 方法可以非阻塞方式去拿锁。

55、设计 4 个线程，其中两个线程每次对 j 增加 1，另外两个线程对 j 每次减少

public class ThreadTest1 { private int j; public static void main(String args[]){ ThreadTest1 tt=newThreadTest1(); Inc inc=tt.new Inc(); Dec dec=tt.new Dec(); for(inti=0;i<2;i++){ Thread t=newThread(inc); t.start(); t=new Thread(dec); t.start(); } } private synchronized void inc(){ j++; System.out.println(Thread.currentThread().getName()+"-inc:"+j); } private synchronized void dec(){ j--; System.out.println(Thread.currentThread().getName()+"-dec:"+j); } class Inc implements Runnable{ public void run(){ for(inti=0;i<100;i++){ inc(); } } } class Dec implements Runnable{ public void run(){ for(inti=0;i<100;i++){ dec(); } } } }

37

1

```
public class ThreadTest1
```

2

```
{
```

3

```
private int j;
```

4

```
public static void main(String args[]){
```

5

```
ThreadTest1 tt=newThreadTest1();
```

6

```
Inc inc=tt.new Inc();
```

7

```
Dec dec=tt.new Dec();
```

8

```
for(inti=0;i<2;i++){
```

9

```
Thread t=newThread(inc);
```

10

```
t.start();
```

11

```
t=new Thread(dec);
```

12

```
t.start();
```

13

```
}
```

14

```
}
```

15

```
private synchronized void inc(){
```

16

```
j++;
```

17

```
System.out.println(Thread.currentThread().getName()+"-inc:"+j);
```

18

```
}
```

19

```
private synchronized void dec(){
```

20

```
j--;
```

21

```
System.out.println(Thread.currentThread().getName()+"-dec:"+j);
```

22

```
}
```

23

```
class Inc implements Runnable{
```

24

```
public void run(){
```

25

```
for(inti=0;i<100;i++){
```

26

```
inc();
```

27

```
}
```

28

```
}
```

29

```
}
```

30

```
class Dec implements Runnable{
```

31

```
public void run(){
```

32

```
for(inti=0;i<100;i++){
```

33

```
dec();
```

34

```
}
```

35

```
}
```

36

```
}
```

37

```
}
```

---

#### 2017年6月4日21:48:32

46、java 中有几种方法可以实现一个线程？用什么关键字修饰同步方法? stop()和 suspend()方法为何不推荐使用？

[java快速提纲 多线程 线程池 并发编程](wiz://open_document?guid=4259dc58-7e8d-4c43-90a4-e73458298eda&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

有两种实现方法， 分别是继承 Thread 类与实现 Runnable 接口

方式1直接new对象然后调用start（）方法  new Thread(){}.start(); 进入就绪状态  就绪状态就是等待cpu分配  分配到后执行run（）方法

方式2需要先通过Thread类的构造方法Thread(Runnable target) 构造出对象，然后调用Thread对象的start()方法来进入就绪状态 来运行多线程代码。new Thread(new Runnable(){}).start();

示例

1. `class Thread1 extends Thread{`
2. `private String name;`
3. `public Thread1(String name) {`
4. `this.name=name;`
5. `}`
6. `public void run() {`
7. `for (int i = 0; i < 5; i++) {`
8. `System.out.println(name + "运行  :  " + i);`
9. `try {`
10. `sleep((int) Math.random() * 10);`
11. `} catch (InterruptedException e) {`
12. `e.printStackTrace();`
13. `}`
14. `}`
15. ``
16. `}`
17. `}`
18. `public class Main {`
19. ``
20. `public static void main(String[] args) {`
21. `Thread1 mTh1=new Thread1("A");`
22. `Thread1 mTh2=new Thread1("B");`
23. `//        mTh1.start();`
24. `//        mTh2.start();`
25. `Runnable runnable1 = new Thread2("C");`
26. `Runnable runnable2 = new Thread2("D");`
27. `new Thread(runnable1).start();`
28. `new Thread(runnable2).start();`
29. ``
30. `}`
31. ``
32. `}`
33. ``
34. `class Thread2 implements Runnable{`
35. `private String name;`
36. ``
37. `public Thread2(String name) {`
38. `this.name=name;`
39. `}`
40. ``
41. `@Override`
42. `public void run() {`
43. `for (int i = 0; i < 5; i++) {`
44. `System.out.println(name + "运行  :  " + i);`
45. `try {`
46. `Thread.sleep((int) Math.random() * 10);`
47. `} catch (InterruptedException e) {`
48. `e.printStackTrace();`
49. `}`
50. `}`
51. ``
52. `}`
53. ``
54. `}`

用 synchronized 关键字修饰同步方法

反对使用 stop()，是因为它不安全。它会解除由线程获取的所有锁定，而且如果对象处于一种不连贯状态，那么其他线程能在那种状态下检查和修改它们。结果很难检查出真正的问题

所在。

suspend()方法容易发生死锁。调用 suspend()的时候，目标线程会停下来，但却仍然持有在这之前获得的锁定。此时，其他任何线程都不能访问锁定的资源，除非被"挂起"的

线程恢复运行。对任何线程来说，如果它们想恢复目标线程，同时又试图使用任何一个锁定的资源，就会造成死锁。所以不应该使用 suspend()，而应在自己的 Thread 类中置入一个

标志，指出线程应该活动还是挂起。若标志指出线程应该挂起，便用 wait()命其进入等待状态。若标志指出线程应当恢复，则用一个 notify()重新启动线

47 sleep()和 wait()有什么区别?

sleep 是线程类（ Thread）的方法，导致此线程暂停执行指定时间，给执行机会给其他线程，但是监控状态依然保持，到时后会自动恢复。调用 sleep 不会释放对象锁。 即使当前线程使用 sleep 方法让出了 cpu，但其他被同步锁挡住了的线程也无法得到执行。

wait 是 Object 类的方法，对此对象调用 wait 方法导致本线程放弃对象锁，进入等待此对象的等待锁定池，只有针对此对象发出 notify 方法（或 notifyAll）后本线程才进入

对象锁定池准备获得对象锁进入运行状态

代码解释看pdf

48、同步和异步有何异同，在什么情况下分别使用他们？举例说明。

如果数据将在线程间共享。例如正在写的数据以后可能被另一个线程读到，或者正在读的数据可能已经被另一个线程写过了，那么这些数据就是共享数据，必须进行同步存取。

当应用程序在对象上调用了一个需要花费很长时间来执行的方法，并且不希望让程序等待方法的返回时，就应该使用异步编程， 在很多情况下采用异步途径往往更有效率。

异步就是耗时的操作不等待操作的结果 先进行后面的操作

同步相反

上面的好像时同步锁的解释

50、多线程有几种实现方法?同步有几种实现方法?

多线程有两种实现方法，分别是继承 Thread 类与实现 Runnable 接口

多线程同步的实现方式

7钟

[http://www.cnblogs.com/XHJT/p/3897440.html](http://www.cnblogs.com/XHJT/p/3897440.html)

[http://www.cnblogs.com/x_wukong/p/4009709.html](http://www.cnblogs.com/x_wukong/p/4009709.html)

[java 快速提纲 多线程同步](wiz://open_document?guid=01d68f75-152f-4647-b28e-9b8ad73ec837&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

主要使用synchronized关键字和obj对象的wait/notify（与线程的wait/notify有点不同）

方法执行中的线程获得对象锁（内存锁）（）其他线程不能执行这个方法

**1.同步方法**
    即有synchronized关键字修饰的方法。
    由于java的每个对象都有一个内置锁，当用此关键字修饰方法时，
    内置锁会保护整个方法。在调用该方法前，需要获得内置锁，否则就处于阻塞状态。

代码如：
    public synchronized void save(){}

注： synchronized关键字也可以修饰静态方法，此时如果调用该静态方法，将会锁住整个类

**2.同步代码块**    即有synchronized关键字修饰的语句块。
    被该关键字修饰的语句块会自动被加上内置锁，从而实现同步

代码如：
    synchronized(object){
    }

注：同步是一种高开销的操作，因此应该尽量减少同步的内容。
    通常没有必要同步整个方法，使用synchronized代码块同步关键代码即可。

    代码实例：

![[attachments/0.8059682425530403.png|复制代码]]

```
package com.xhj.thread;

    /**
     * 线程同步的运用
     *
     * @author XIEHEJUN
     *
     */
    public class SynchronizedThread {

        class Bank {

            private int account = 100;

            public int getAccount() {
                return account;
            }

            /**
             * 用同步方法实现
             *
             * @param money
             */
            public synchronized void save(int money) {
                account += money;
            }

            /**
             * 用同步代码块实现
             *
             * @param money
             */
            public void save1(int money) {
                synchronized (this) {
                    account += money;
                }
            }
        }

        class NewThread implements Runnable {
            private Bank bank;

            public NewThread(Bank bank) {
                this.bank = bank;
            }

            @Override
            public void run() {
                for (int i = 0; i < 10; i++) {
                    // bank.save1(10);
                    bank.save(10);
                    System.out.println(i + "账户余额为：" + bank.getAccount());
                }
            }

        }

        /**
         * 建立线程，调用内部类
         */
        public void useThread() {
            Bank bank = new Bank();
            NewThread new_thread = new NewThread(bank);
            System.out.println("线程1");
            Thread thread1 = new Thread(new_thread);
            thread1.start();
            System.out.println("线程2");
            Thread thread2 = new Thread(new_thread);
            thread2.start();
        }

        public static void main(String[] args) {
            SynchronizedThread st = new SynchronizedThread();
            st.useThread();
        }

    }
```

![[attachments/0.3165074155229435.png|复制代码]]

---

#### 2017年6月1日22:25:15

36、数组有没有 length()这个方法? String 有没有 length()这个方法？
数组没有 length()这个方法，有 length 的属性。 String 有有 length()这个方法。   集合有size（）方法

37、下面这条语句一共创建了多少个对象： String s="a"+"b"+"c"+"d";

直接创建了一个对象

题目中的第一行代码被编译器在编译时优化后，相当于直接定义了一个”abcd”的字符串，

所以，上面的代码应该只创建了一个 String 对象。写如下两行代码，

String s ="a" + "b" + "c" + "d";

System.out.println(s== "abcd");

最终打印的结果应该为 true。

答：对于如下代码：

String s1 = "a";

String s2 = s1 + "b";  //这里相当于new String（"ab"）; 产生了一个新的对象 与“ab”不同

String s3 = "a" + "b";

System.out.println(s2 == "ab");

System.out.println(s3 == "ab");

java中的==比较变量栈内存中的值

第一条语句打印的结果为 false，第二条语句打印的结果为 true，

这说明 javac 编译可以对字符串常量直接相加的表达式进行优化，不必要等到运行期去进行加法运算处理，而是在编译时去掉其中的加号，直接将其编译成一个这些常量相连的结果。

equals和==

[http://www.cnblogs.com/dolphin0520/p/3592500.html](http://www.cnblogs.com/dolphin0520/p/3592500.html)

38、 try {}里有一个 return 语句，那么紧跟在这个 try 后的 finally {}里的 code会不会被执行，什么时候被执行，在 return 前还是后?

```
 /**
 2  *
 3  */
 4 package com.b510.test;
 5
 6 /**
 7  * try {}里有一个return语句，那么紧跟在这个try后的finally {}里的code会不会被执行，什么时候被执行，还是在return之后执行？
 8  * @author Hongten
 9  * @date 2013-12-10
10  */
11 public class TestC {
12
13     @SuppressWarnings("static-access")
14     public static void main(String[] args) {
15         System.out.println("结果： " + new TestC().test());
16     }
17
18     static int test(){
19         int i = 1;
20         try {
21             System.out.println("try里面的i : " + i);
22             return i;
23         }finally{
24             System.out.println("进入finally...");
25             ++i;
26             System.out.println("fianlly里面的i : " + i);
27         }
28     }
29 }
```

![[attachments/0.2255555544249488.png|复制代码]]

输出结果：

```
try里面的i : 1
进入finally...
fianlly里面的i : 2
结果： 1来源： http://www.cnblogs.com/hongten/archive/2013/12/10/hongten_java_finally.html
```

根据java规范：在try-catch-finally中，如果try-finally或者catch-finally中都有return~~（不能trycatch中同时有return）~~，则两个return语句都执行并且最终返回到调用者那里的是finally中return的值；而如果finally中没有return，则理所当然的返回的是try或者catch中return的值，

但是finally中的代码是必须要执行的,而且是在return前执行,除非碰到exit()。

39、下面的程序代码输出的结果是多少？

public class smallT { public static void main(String args[]) { smallT t = new smallT(); int b = t.get(); System.out.println(b); } public int get() { try { Return 1 ; } finally { Return 2 ; } } }

20

1

```
public class smallT
```

2

```
{
```

3

```
public static void main(String args[])
```

4

```
{
```

5

```
smallT t = new smallT();
```

6

```
int b = t.get();
```

7

```
System.out.println(b);
```

8

```
}
```

9

```
public int get()
```

10

```
{
```

11

```
try
```

12

```
{
```

13

```
Return 1 ;
```

14

```
}
```

15

```
finally
```

16

```
{
```

17

```
Return 2 ;
```

18

```
}
```

19

```
}
```

20

```
}
```

返回的结果是2

根据java规范：在try-catch-finally中，如果try-finally或者catch-finally中都有return（不能trycatch中同时有return），则两个return语句都执行并且最终返回到调用者那里的是finally中return的值；而如果finally中没有return，则理所当然的返回的是try或者catch中return的值，

但是finally中的代码是必须要执行的,而且是在return前执行,除非碰到exit()。

40、 final, finally, finalize 的区别。

final 用于声明属性，方法和类，分别表示属性不可变，方法不可覆盖，类不可继承。内部类要访问局部变量，局部变量必须定义成 final 类型，例如，一段代码……

finally 是异常处理语句结构的一部分，表示总是执行。

finalize 是 Object 类的一个方法，在垃圾收集器执行的时候会调用被回收对象的此方法，可以覆盖此方法提供垃圾收集时的其他资源回收，例如关闭文件等。 JVM 不保证此方法总被

调用

---

#### 2017年5月31日22:22:10

31、 String s = "Hello";s = s + " world!";这两行代码执行后，原始的 String对象中的内容到底变了没有？

[String、StringBuffer与StringBuilder之间区别](wiz://open_document?guid=f521cd8e-dbed-4776-8b84-a4b6273c7826&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

没有。 因为 String 被设计成不可变(immutable)类  这里指向了一个新的String对象  原来的String对象还存在

StringBuffer 类，StringBuilder 允许修改

对于字符串常量，如果内容相同， Java 认为它们代表同一个 String 对象。而用关键字 new 调用构造器，总是会创建一个新的对象，无论内容是否相同。

不可变类有一些优点，比如因为它的对象是只读的，所以多线程并发访问也不会有任何问题。 当然也有一些缺点，比如每个不同的状态都要一个对象来代表，可能会造成性能上的问题。

关于不可变类

1. 将类声明为final，所以它不能被继承
2. 将所有的成员声明为私有的，这样就不允许直接访问这些成员
3. 将所有可变的成员声明为final，这样只能对它们赋值一次
4. 对变量不要提供setter方法
5. 在getter方法中，不要直接返回对象本身，而是克隆对象，并返回对象的拷贝
6. 通过构造器初始化所有成员，如果某一个类成员不是原始变量(primitive)或者不可变类  （成员变量不是原始变量就）进行深拷贝(deep copy)
7. [http://www.cnblogs.com/yg_zhang/p/4355354.html](http://www.cnblogs.com/yg_zhang/p/4355354.html)

32、是否可以继承 String 类?

String 类是 final 类故不可以继承

33、 String s = new String("xyz");创建了几个 String Object?二者之间有什么区别？

两个或一个， ”xyz”对应一个对象，这个对象放在字符串常量缓冲区，常量”xyz”不管出现多少遍，都是缓冲区中的那一个。 New String 每写一遍，就创建一个新的对象，它依据那个

常量”xyz”对象的内容来创建出一个新 String 对象。如果以前就用过’xyz’，这句代表就不会创建”xyz”自己了，直接从缓冲区拿。

所有的字符串常量都放在字符串常量缓冲区中 对于字符串常量，如果内容相同， Java 认为它们代表同一个对象。

这里调用的时String的构造方法  其中“xyz”作为构造方法的参数（参数是一个对象）  所以这里会创建一个“xyz”的字符串常量（如果以前就用过’xyz’，这句代表就不会创建”xyz”自己了，直接从缓冲区拿。）  然后New String 每写一遍，就创建一个新的对象，它依据那个常量”xyz”对象的内容来创建出一个新 String 对象

下面的表达式应该等同于题目的意思

String x=“xyz”;

String s = new String(x);

34、 String 和 StringBuffer 的区别

区别

这个 String 类提供了数值不可改变的字符串。而这个 StringBuffer 类提供的字符串进行修改。

三者在执行速度方面的比较：StringBuilder >  StringBuffer  >  String

String 覆盖了 equals 方法和 hashCode 方法，而 StringBuffer 没有覆盖 equals 方法和hashCode 方法，所以，将 StringBuffer 对象存储进 Java 集合类中时会出现问题。（在进行一些需要比较的操作时会出现问题）

[String、StringBuffer与StringBuilder之间区别](wiz://open_document?guid=f521cd8e-dbed-4776-8b84-a4b6273c7826&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

35、如何把一段逗号分割的字符串转换成一个数组?

如果不查 jdk api，我很难写出来！我可以说说我的思路：

1 用正则表达式，代码大概为： String [] result = orgStr.split(“,”);

2 用 StingTokenizer ,代码为： StringTokenizer tokener =StringTokenizer(orgStr,”,”);

String [] result =new String[tokener .countTokens()];

Int i=0;

while(tokener.hasNext(){result[i++]=toker.nextToken();}

---

#### 2017年5月23日22:03:22

26.什么是内部类？ Static Nested Class 和 Inner Class 的不同。

内部类就是在一个类的内部定义的类，内部类中不能定义静态成员

内部类可以直接访问外部类中的成员变量，内部类可以定义在外部类的方法外面，也可以定义在外部类的方法体中

定义在外部类的方法外

定义在外部类的方法内

在方法外部定义的内部类前面可以加上 static 关键字，从而成为 Static Nested Class，

static Nested Class 能访问

外部类的非 static 成员变量(不能直接访问，需要创建外部类实例才能访问非静态变量)

匿名内部类

abstract class Person { public abstract void eat(); } public class Demo { public static void main(String[] args) { Person p = new Person() { public void eat() { System.out.println("eat something"); } }; p.eat(); } }

14

1

```
abstract class Person {
```

2

```
    public abstract void eat();
```

3

```
}
```

4

```

```

5

```
public class Demo {
```

6

```
    public static void main(String[] args) {
```

7

```
        Person p = new Person() {
```

8

```
            public void eat() {
```

9

```
                System.out.println("eat something");
```

10

```
            }
```

11

```
        };
```

12

```
        p.eat();
```

13

```
    }
```

14

```
}
```

可以看到，我们直接将抽象类Person中的方法在大括号中实现了

这样便可以省略一个类的书写

并且，匿名内部类还能用于接口上

27、内部类可以引用它的包含类的成员吗？有没有什么限制？

完全可以。如果不是静态内部类，那没有什么限制！

静态内部类不能访问外部类的成员

28、 Anonymous Inner Class (匿名内部类)是否可以 extends(继承)其它类，

是否可以 implements(实现)interface(接口)?

可以继承其他类或实现其他接口。不仅是可以，而是必须!

29、 super.getClass()方法调用

下面程序的输出结果是多少？

importjava.util.Date;

public class Test extends Date{

public static void main(String[] args) {

new Test().test();

}

public void test(){

System.out.println(super.getClass().getName());

}

}

在 test 方法中，直接调用 getClass().getName()方法，返回的是 Test 类名

由于 getClass()在 Object 类中定义成了 final，子类不能覆盖该方法，所以，在test 方法中调用 getClass().getName()方法，其实就是在调用从父类继承的 getClass()方法，等效于调用 super.getClass().getName()方法，所以， super.getClass().getName()方法返回的也应该是 Test。

如果想得到父类的名称，应该用如下代码：

getClass().getSuperClass().getName();

30、 String 是最基本的数据类型吗?

基本数据类型包括 byte、 int、 char、 long、 float、 double、 boolean 和 short。

java.lang.String 类是 final 类型的，因此不可以继承这个类、不能修改这个类。为了提高效率节省空间，我们应该用 StringBuffer 类

---

#### 2017年5月22日22:17:59

21、写 clone()方法时，通常都有一行代码，是什么？

clone 有缺省行为，

super.clone();

因为首先要把父类中的成员复制到位，然后才是复制自己的成员。

[http://www.importnew.com/16094.html](http://www.importnew.com/16094.html)

默认的clone是浅拷贝

一个类需要实现clone功能

需要继承Cloneable接口  实现clone方法 在clone方法中通过调用super.clone（）返回一个当前实例（相同类型）的浅拷贝

（super  指向父类的对象实例 ）

public class Person implements Cloneable{ private int age ; private String name; public Person(int age, String name) { this.age = age; this.name = name; } public Person() {} public int getAge() { return age; } public String getName() { return name; } @Override protected Object clone() throws CloneNotSupportedException { return (Person)super.clone(); } }

25

1

```
public class Person implements Cloneable{
```

2

```

```

3

```
    private int age ;
```

4

```
    private String name;
```

5

```

```

6

```
    public Person(int age, String name) {
```

7

```
        this.age = age;
```

8

```
        this.name = name;
```

9

```
    }
```

10

```

```

11

```
    public Person() {}
```

12

```

```

13

```
    public int getAge() {
```

14

```
        return age;
```

15

```
    }
```

16

```

```

17

```
    public String getName() {
```

18

```
        return name;
```

19

```
    }
```

20

```

```

21

```
    @Override
```

22

```
    protected Object clone() throws CloneNotSupportedException {
```

23

```
        return (Person)super.clone();
```

24

```
    }
```

25

```
}
```

简单的实现深拷贝

static class Body implements Cloneable{ public Head head; public Body() {} public Body(Head head) {this.head = head;} @Override protected Object clone() throws CloneNotSupportedException { Body newBody = (Body) super.clone(); newBody.head = (Head) head.clone(); return newBody; } } static class Head implements Cloneable{ public Face face; public Head() {} public Head(Face face){this.face = face;} @Override protected Object clone() throws CloneNotSupportedException { return super.clone(); } } public static void main(String[] args) throws CloneNotSupportedException { Body body = new Body(new Head()); Body body1 = (Body) body.clone(); System.out.println("body == body1 : " + (body == body1) ); System.out.println("body.head == body1.head : " + (body.head == body1.head)); }

34

1

```
static class Body implements Cloneable{
```

2

```
    public Head head;
```

3

```
    public Body() {}
```

4

```
    public Body(Head head) {this.head = head;}
```

5

```

```

6

```
    @Override
```

7

```
    protected Object clone() throws CloneNotSupportedException {
```

8

```
        Body newBody =  (Body) super.clone();
```

9

```
        newBody.head = (Head) head.clone();
```

10

```
        return newBody;
```

11

```
    }
```

12

```

```

13

```
}
```

14

```
static class Head implements Cloneable{
```

15

```
    public  Face face;
```

16

```

```

17

```
    public Head() {}
```

18

```
    public Head(Face face){this.face = face;}
```

19

```
    @Override
```

20

```
    protected Object clone() throws CloneNotSupportedException {
```

21

```
        return super.clone();
```

22

```
    }
```

23

```
}
```

24

```
public static void main(String[] args) throws CloneNotSupportedException {
```

25

```

```

26

```
    Body body = new Body(new Head());
```

27

```

```

28

```
    Body body1 = (Body) body.clone();
```

29

```

```

30

```
    System.out.println("body == body1 : " + (body == body1) );
```

31

```

```

32

```
    System.out.println("body.head == body1.head : " +  (body.head == body1.head));
```

33

```

```

34

```
}
```

浅拷贝时 是拷贝的对象中的引用类型属性只拷贝引用值

深拷贝 是拷贝的对象中的引用类型属性只再进行拷贝操作

![[attachments/3e356754-82db-4e4c-b8a2-5f0370cfd22c.png]]

22、面向对象的特征有哪些方面

封装

封装是保证软件部件具有优良的模块性的基础，封装的目标就是要实现软件部件的“高内聚、低耦合”，防止程序相互依赖性而带来的变动影响。

只要记住让变量和访问这个变量的方法放在一起，将一个类中的成员变量全部定义成私有的，只有这个类自己的方法才可以访问到这些成员变量，这就基本上实现对象的封装，就很容易找出要分配到这个类上的方法了，就基本上算是会面向对象的编程了。把握一个原则：把对同一事物进行操作的方法和相关的方法放在同一个类中，把方法和它操作的数据放在同一个类中

抽象：

抽象就是找出一些事物的相似和共性之处，然后将这些事物归为一个类，这个类只考虑这些事物的相似和共性之处，并且会忽略与当前主题和目标无关的那些方面，将注意力集中在与当前目标有关的方面。

继承：

继承是子类自动共享父类数据和方法的机制，这是类之间的一种关系，提高了软件的可重用性和可扩展性。

再一个已经存在的类的基础上进行 在扩展新的内容

多态：

多态是指程序中定义的引用变量所指向的具体类型和通过该引用变量发出的方法调用在编程时并不确定，而是在程序运行期间才确定，即一个引用变量倒底会指向哪个类的实例对象，该引用变量发出的方法调用到底是哪个类中实现的方法，必须在由程序运行期间才能决定。因为在程序运行时才确定具体的类，这样，不用修改源程序代码，就可以让引用变量绑定到各种不同的类实现上，从而导致该引用调用的具体方法随之改变，即不修改程序代码就可以改变程序运行时所绑定的具体代码，让程序可以选择多个运行状态，这就是多态性

23、 java 中实现多态的机制是什么？

靠的是定义父类或接口定义的引用变量可以指向子类或具体实现类的实例对象，而程序调用的方法在运行期才动态绑定，就是引用变量所指向的具体实例对象的方法，也就是内存里正在运行的那个对象的方法，而不是引用变量的类型中定义的方法。

###### 24、 abstract class 和 interface 有什么区别?

含有 abstract 修饰符的 class 即为抽象类， abstract 类不能创建的实例对象。

含有 abstract方法的类必须定义为abstract class，abstract class 类中的方法不必是抽象的。

abstract class定义的抽象方法必须在继承它的子类中实现。如果的子类没有实现抽象父类中的所有抽象方法，那么子类也必须定义为 abstract类型

接口（ interface）可以说成是抽象类的一种特例，接口中的所有方法都必须是抽象的。 接口中的方法定义默认为 public abstract 类型，接口中的成员变量类型默认为 public static final。

接口中只有public static final 静态常量和public abstract 类型抽象方法。没有其他内部东西  一个类可以实现多个接口

abstract class除了不能创建实例 和 存在abstract  方法 其他的跟一般的类一样  因为差不多可以理解为一搬类的特例所以只能单继承

下面比较一下两者的语法区别：

1.抽象类可以有构造方法，接口中不能有构造方法。

2.抽象类中可以有普通成员变量，接口中没有普通成员变量

3.抽象类中可以包含非抽象的普通方法，接口中的所有方法必须都是抽象的，不能有非抽象的普通方法。

4. 抽象类中的抽象方法的访问类型可以是 public， protected 和（默认类型,虽然eclipse 下不报错，但应该也不行），但接口中的抽象方法只能是 public 类型的，并且默认即为 public abstract 类型。

5. 抽象类中可以包含静态方法，接口中不能包含静态方法 （）

6. 抽象类和接口中都可以包含静态成员变量，抽象类中的静态成员变量的访问类型可以任意，但接口中定义的变量只能是 public static final 类型，并且默认即为 public static final 类型。

7. 一个类可以实现多个接口，但只能继承一个抽象类。

比较两者语法细节区别的条理是：

先从一个类中的构造方法、普通成员变量和方法（包括抽象方法），静态变量和方法，继承性等6个方面逐一去比较回答，

25、 abstract 的 method 是否可同时是 static,是否可同时是 native，是否可同时是 synchronized?

抽象方法不能同时是静态的  因为抽象方法的存在就是为了让子类来实现  而静态方法只属于当前类

（或者说抽象方法还是属于实例方法  而加上static就属于类方法）

native 方法表示该方法要用另外一种依赖平台的编程语言实现的，不存在着被子类实现的问题，所以，它也不能是抽象的，不能与 abstract 混用

例如， FileOutputSteam 类要硬件打交道，底层的实现用的是操作系统相关的 api 实现，例如，在 windows 用 c 语言实现的，所以，查看 jdk 的源代码，可以发现 FileOutputStream 的 open 方法的定义如下：private native void open(Stringname) throws FileNotFoundException;

关于 synchronized 与 abstract 合用的问题，我觉得也不行我觉得 synchronized 应该是作用在一个具体的方法上才有意义。而且，方法上的 synchronized 同步所使用的同步锁对象是 this，而抽象方法上无法确定 this 是什么。

---

#### 2017年5月18日22:15:58

16、下面的代码有什么不妥之处?

1. if(username.equals(“zxx”){}

username 可能为 NULL,会报空指针错误；改为"zxx".equals(username)

2. int x = 1;

return x==1?true:false; 这个改成 return x==1;就可以!

###### 17、请说出作用域 public， private， protected，以及不写时的区别

这四个作用域的可见范围如下表所示。
说明：如果在修饰的元素上面没有写任何访问修饰符，则表示 friendly。（可以简单的理解为方法的修饰符）

| 作用域 | 当前类 | 同一包（ package） | 子孙类 | 其他包（ package） |
| --- | --- | --- | --- | --- |
| public | √ | √ | √ | √ |
| protected | √ | √ | √ | × |
| friendly | √ | √ | × | × |
| private | √ | × | × | × |

备注：只要记住了有4种访问权限， 4个访问范围，然后将全选和范围在水平和垂直方向上
分别按排从小到大或从大到小的顺序排列，就很容易画出上面的图了。

18、 Overload 和 Override 的区别。 Overloaded 的方法是否可以改变返回值的类型?

Overload 是重载的意思， Override 是覆盖的意思，也就是重写。

重载 Overload 表示同一个类中可以有多个名称相同的方法，但这些方法的参数列表各不相同（即参数个数或类型不同）。

（关于重载返回类型）如果几个 Overloaded 的方法的参数列表不一样，它们的返回者类型当然也可以不一样

如果两个方法的参数列表完全一样，是否可以让它们的返回值不同来实现重载 Overload。这是不行的，

1、在使用重载时只能通过不同的参数样式。例如，不同的参数类型，不同的参数个数，不同的参数顺序（当然，同一方法内的几个参数类型必须不一样，例如可以是 fun(int,float)，但是不能为fun(int,int)）；

2、不能通过访问权限、返回类型、抛出的异常进行重载；

3、方法的异常类型和数目不会对重载造成影响；

4、对于继承来说，如果某一方法在父类中是访问权限是 priavte，那么就不能在子类对其进行重载，如果定义的话，也只是定义了一个新方法，而不会达到重载的效果

重写 Override 表示子类中的方法可以与父类中的某个方法的名称和参数完全相同，通过子类创建的实例对象调用这个方法时，将调用子类中的定义方法，这相当于把父类中定义的那

个完全相同的方法给覆盖了，这也是面向对象编程的多态性的一种表现。

子类覆盖父类的方法时， 只能比父类抛出更少的异常，或者是抛出父类抛出的异常的子异常，因为子类可以解决父类的一些问题，不能比父类有更多的问题。子类方法的访问权限只能比父类的更大，不

能更小。如果父类的方法是 private 类型，那么，子类则不存在覆盖的限制，相当于子类中增加了一个全新的方法。

1、覆盖的方法的标志必须要和被覆盖的方法的标志完全匹配，才能达到覆盖的效果；

2、覆盖的方法的返回值必须和被覆盖的方法的返回一致；

3、覆盖的方法所抛出的异常必须和被覆盖方法的所抛出的异常一致，或者是其子类；

4、 被覆盖的方法不能为 private，否则在其子类中只是新定义了一个方法，并没有对其进行覆盖。

19、构造器 Constructor 是否可被 override?

构造器 Constructor 不能被继承，因此不能重写 Override，但可以被重载 Overload。

20、接口是否可继承接口?

抽象类是否可实现(implements)接口?

抽象类是否可继承具体类(concrete class)?

抽象类中是否可以有静态的 main 方法？

接口可以继承接口。抽象类可以实现(implements)接口，抽象类可以继承具体类。抽象类中可以有静态的 main 方法。

备注：只要明白了接口和抽象类的本质和作用，这些问题都很好回答，你想想，如果你是 java语言的设计者，你是否会提供这样的支持，如果不提供的话，有什么理由吗？如果你没有道理不提供，那答案就是肯定的了。

只有记住抽象类与普通类的唯一区别： 就是不能创建实例对象和允许有 abstract 方法。

---

#### 2017年5月17日22:25:40

11、 "=="和 equals 方法究竟有什么区别？

==操作符专门用来比较两个变量的值是否相等，也就是比价较其存在栈内存中的值是否相等。要比较两个基本类型的数据或两个引用变量是否引用同一个对象，只能用==操作符。

如果时两个变量并且指向不同的对象而想要比较这两个对象是否相同则需要使用equals

equals 方法是用于比较两个独立对象的内容是否相同，

String a=new String("foo");

String b=new String("foo");

两条 new 语句创建了两个对象，然后用 a/b 这两个变量分别指向了其中一个对象，这是两个不同的对象，它们的首地址是不同的，即 a 和 b 中存储的数值是不相同的，所以，表达

式 a==b 将返回 false，而这两个对象中的内容是相同的，所以，表达式 a.equals(b)将返回true。

记住，字符串的比较基本上都是使用 equals 方法。

如果一个类没有自己定义 equals 方法，那么它将继承 Object 类的 equals 方法， Object 类的 equals 方法的实现代码如下：

boolean equals(Object o){

return this==o;

}

就是相当于使用==

12、静态变量和实例变量的区别？

在语法定义上的区别： 静态变量前要加 static 关键字，而实例变量前则不加。

在程序运行时的区别：

实例变量属于某个对象的属性，必须创建了实例对象，其中的实例变量才会被分配空间，才能使用这个实例变量。

静态变量不属于某个实例对象，而是属于类，所以也称为类变量，只要程序加载了类的字节码，不用创建任何实例对象，静态变量就会被分配空间，静态变量就可以被使用了。

类（静态）变量是唯一的。不管这个类创建了多少个实例 但是他们使用的都是同一个类变量

总之，实例变量必须创建对象后才可以通过这个对象来使用，静态变量则可以直接使用类名来引用。

13.是否可以从一个 static 方法内部发出对非 static 方法的调用？

不可以。因为非 static 方法是要与对象关联在一起的，必须创建一个对象后，才可以在该对象上进行方法调用，。

一般调用在同一个类中的方法时 为直接调用  xxx()  而实际情况是 this.xxx()  而这个this指向的时当前创建的实例。而在static中this并没有指向实例对象 违反实例方法必须在实例对象上进行方法调用

14、 Integer 与 int 的区别

int 是 java 提供的8种原始数据类型之一。Java 为每个原始类型提供了封装类，Integer 是 java为 int 提供的封装类。

int 的默认值为0，而 Integer 的默认值为 null，即 Integer 可以区分出未赋值和值为0的区别， int 则无法表达出未赋值的情况。

Integer 提供了多个与整数相关的操作方法，例如，将一个字符串转换成整数， Integer中还定义了表示整数的最大值和最小值的常量

15、 Math.round(11.5)等於多少? Math.round(-11.5)等於多少?

Math 类中提供了三个与取整有关的方法： ceil、 floor、 round，这些方法的作用与它们的英文名称的含义相对应，例如，

ceil 的英文意义是天花板，该方法就表示向上取整，Math.ceil(11.3)的结果为12,Math.ceil(-11.3)的结果是-11；

floor 的英文意义是地板，该方法就表示向下取整， Math.ceil(11.6)的结果为11,Math.ceil(-11.6)的结果是-12；

最难掌握的是round 方法，它表示“四舍五入”，算法为 Math.floor(x+0.5)，即将原来的数字加上0.5后再向下取整，所以， Math.round(11.5)的结果为12， Math.round(-11.5)的结果为-11。

---

#### 2017年5月16日22:05:16

6、 short s1 = 1; s1 = s1 + 1;有什么错? short s1 = 1; s1 += 1;有什么错?

对于 short s1 = 1; s1 = s1 + 1;由于 s1+1运算时会自动提升表达式的类型，所以结果是 int型，再赋值给 short 类型 s1时， 编译器将报告需要强制转换类型的错误。

对于 short s1 = 1; s1 += 1;由于 +=是 java 语言规定的运算符， java 编译器会对它进行特殊处理，因此可以正确编译。

7、 char 型变量中能不能存贮一个中文汉字?为什么?

char 型变量是用来存储[Unicode 编码](http://baike.baidu.com/link?url=Im7HPhffHqUt3DnJ9fKUw8wWNt3tk72BvgGIwZdRPgUFmehDayVSWpftTzs2Ymwg22XCbqKWcC67zrN4aoEeye3w7Vfoq_otPxZnKQ1HpYq)的字符的， unicode 编码字符集中包含了汉字，所以，char 型变量中当然可以存储汉字啦。不过，如果某个特殊的汉字没有被包含在 unicode 编

码字符集中，那么，这个 char 型变量中就不能存储这个特殊汉字。 补充说明： unicode 编

码占用两个字节，所以， char 类型的变量也是占用两个字节。

备注：后面一部分回答虽然不是在正面回答题目，但是，为了展现自己的学识和表现自己对

问题理解的透彻深入，可以回答一些相关的知识，做到知无不言，言无不尽。

8、用最有效率的方法算出 2 乘以 8 等于几?

2 << 3，（0010   --- 10000）

因为将一个数左移 n 位，就相当于乘以了2的 n 次方，那么，一个数乘以8只要将其左移3位

即可，而位运算 cpu 直接支持的，效率最高，所以， 2乘以8等於几的最效率的方法是2 << 3

9、请设计一个一百亿的计算器

计算机中的算术运算是会发生越界情况的，两个数值的运算结果不能超过计算机中的该类型的数值范围.

并且java 中涉及表达式运算时的类型自动提升

[http://www.cnblogs.com/xiaonanhai/p/6075729.html](http://www.cnblogs.com/xiaonanhai/p/6075729.html)

10、使用 final 关键字修饰一个变量时，是引用不能变，还是引用的对象不能变？

使用 final 关键字修饰一个变量时，是指引用变量不能变，引用变量所指向的对象中的内容还是可以改变的。例如，对于如下语句：

final StringBuffer a=new StringBuffer("immutable");

执行如下语句将报告编译期错误：

a=new StringBuffer("");

但是，执行如下语句则可以通过编译：

a.append(" broken!");

有人在定义方法的参数时，可能想采用如下形式来阻止方法内部修改传进来的参数对象：

public void method(final StringBuffer param){

}

实际上，这是办不到的，在该方法内部仍然可以增加如下代码来修改参数对象：

param.append("a");

---

#### 2017年5月15日22:05:08

1、一个".java"源文件中是否可以包括多个类（不是内部类）？有什么限制？

可以有多个类，但只能有一个 public 的类，并且 public 的类名必须与文件名相一致。

2、 Java 有没有 goto?

java 中的保留字，现在没有在 java 中使用。

3、说说&和&&的区别。

&和&&都可以用作逻辑与的运算符，表示逻辑与（ and），当运算符两边的表达式的结果都为 true 时，整个运算结果才为 true，否则，只要有一方为 false，则结果为 false。

&&还具有短路的功能（&不具有），即如果第一个表达式为 false，则不再计算第二个表达式，例如，对于 if(str != null&& !str.equals(“”))表达式，当 str 为 null 时，后面的表达式不会执行，所以不

会出现 NullPointerException 如果将&&改为&，则会抛出 NullPointerException 异常。If(x==33 &++y>0) y 会增长， If(x==33 && ++y>0)不会增长

&还可以用作位运算符，当&操作符两边的表达式不是 boolean 类型时， &表示按位与操作，

我们通常使用0x0f 来与一个整数进行&运算，来获取该整数的最低4个 bit 位，例如， 0x31 &

0x0f 的结果为0x01。

备注：这道题先说两者的共同点，再说出&&和&的特殊之处，并列举一些经典的例子来表明

自己理解透彻深入、实际经验丰富。

4、在 JAVA 中如何跳出当前的多重嵌套循环？

在 Java 中，要想跳出多重循环，可以在外面的循环语句前定义一个标号，然后在里层循环

体的代码中使用带有标号的 break 语句，即可跳出外层循环。例如，

ok:

for(int i=0;i<10;i++) {

for(int j=0;j<10;j++) {

System.out.println(“i=” + i + “,j=” + j);

if(j == 5) break ok;

}

}

另外，我个人通常并不使用标号这种方式，而是让外层的循环条件表达式的结果可以受到里层循环体代码的控制，例如，要在二维数组中查找到某个数字。

int arr[][] ={{1,2,3},{4,5,6,7},{9}};

boolean found = false;

for(int i=0;i<arr.length&& !found;i++) {

for(int j=0;j<arr[i].length;j++){

System.out.println(“i=” + i + “,j=” + j);

if(arr[i][j] ==5) {

found = true;

break;

}

}

}

5、 switch 语句能否作用在 byte 上，能否作用在 long 上，能否作用在 String上?

在 switch（ expr1）中， expr1只能是一个整数表达式或者枚举常量（更大字体），整数表达式可以是 int 基本类型或 Integer 包装类型，由于， byte,short,char 都可以隐含转换为 int，

所以，这些类型以及这些类型的包装类型也是可以的。显然， long 和 String 类型都不符合 switch 的语法规定，并且不能被隐式转换成 int 类型，所以，它们不能作用于 swtich 语句中。

![[attachments/14b6562c-55ed-4018-bf1e-6b9c0df008ff.jpg]]
