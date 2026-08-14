---
Title: "Java常量池理解与总结"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags:
  - "0碎"
Created: "2017-06-29 15:02:10"
Cover: ""
WizGuid: "96f99403-7ed3-4513-9201-15634f11efc8"
WizType: "document"
WizLocation: "/碎片/"
WizDataMd5: "cd34b454ed0a85e0e179bb000590a109"
Modified: "2017-06-29 15:06:46"
WizSyncedAt: "2026-08-14 22:20:57"
---

# Java常量池理解与总结

![[attachments/0.2948155753165451.png|144]]

作者 [梦工厂](http://www.jianshu.com/u/6e7c82da2a5e) 关注

2015.08.26 11:34* 字数 2535 阅读 12160评论 19喜欢 99

#### 一.相关概念

---

1. **什么是常量**
  用final修饰的成员变量表示常量，值一旦给定就无法改变！
  final修饰的变量有三种：静态变量、实例变量和局部变量，分别表示三种类型的常量。
2. **Class文件中的常量池**
  在Class文件结构中，最头的4个字节用于存储魔数Magic Number，用于确定一个文件是否能被JVM接受，再接着4个字节用于存储版本号，前2个字节存储次版本号，后2个存储主版本号，再接着是用于存放常量的常量池，由于常量的数量是不固定的，所以常量池的入口放置一个U2类型的数据(constant_pool_count)存储常量池容量计数值。
  常量池主要用于存放两大类常量：**字面量**(Literal)和**符号引用量**(Symbolic References)，字面量相当于Java语言层面常量的概念，如文本字符串，声明为final的常量值等，符号引用则属于编译原理方面的概念，包括了如下三种类型的常量：
  - 类和接口的全限定名
  - 字段名称和描述符
  - 方法名称和描述符
3. **方法区中的运行时常量池**
  运行时常量池是方法区的一部分。
  CLass文件中除了有类的版本、字段、方法、接口等描述信息外，还有一项信息是常量池，用于存放编译期生成的各种字面量和符号引用，这部分内容将在类加载后进入方法区的运行时常量池中存放。
  运行时常量池相对于CLass文件常量池的另外一个重要特征是**具备动态性**，Java语言并不要求常量一定只有编译期才能产生，也就是并非预置入CLass文件中常量池的内容才能进入方法区运行时常量池，运行期间也可能将新的常量放入池中，这种特性被开发人员利用比较多的就是**String类的intern()**方法。
4. **常量池的好处**
  常量池是为了避免频繁的创建和销毁对象而影响系统性能，其实现了对象的共享。
  例如字符串常量池，在编译阶段就把所有的字符串文字放到一个常量池中。
  （1）节省内存空间：常量池中所有相同的字符串常量被合并，只占用一个空间。
  （2）节省运行时间：比较字符串时，==比equals()快。对于两个引用变量，只用==判断引用是否相等，也就可以判断实际值是否相等。
5. **双等号==的含义**
  基本数据类型之间应用双等号，比较的是他们的数值。
  复合数据类型(类)之间应用双等号，比较的是他们在内存中的存放地址。

#### 二.8种基本类型的包装类和常量池

---

1. java中基本类型的包装类的大部分都实现了常量池技术，
  即Byte,Short,Integer,Long,Character,Boolean； ```
  Integer i1 = 40;
  Integer i2 = 40;
  System.out.println(i1==i2);//输出TRUE
  ``` 这5种包装类默认创建了数值[-128，127]的相应类型的缓存数据，但是超出此范围仍然会去创建新的对象。 ```
  //Integer 缓存代码 ：
  public static Integer valueOf(int i) {
       assert IntegerCache.high >= 127;
       if (i >= IntegerCache.low && i <= IntegerCache.high)
           return IntegerCache.cache[i + (-IntegerCache.low)];
       return new Integer(i);
   }
  ``` ```
  Integer i1 = 400;
  Integer i2 = 400;
  System.out.println(i1==i2);//输出false
  ```
2. **两种浮点数类型的包装类Float,Double并没有实现常量池技术。** ```
  Double i1=1.2;
  Double i2=1.2;
  System.out.println(i1==i2);//输出false
  ```
3. **应用常量池的场景**
  (1)`Integer i1=40；`Java在编译的时候会直接将代码封装成`Integer i1=Integer.valueOf(40);`，从而使用常量池中的对象。
  (2)`Integer i1 = new Integer(40);`这种情况下会创建新的对象。 ```
  Integer i1 = 40;
  Integer i2 = new Integer(40);
  System.out.println(i1==i2);//输出false
  ```
4. **Integer比较更丰富的一个例子** ```
  Integer i1 = 40;
  Integer i2 = 40;
  Integer i3 = 0;
  Integer i4 = new Integer(40);
  Integer i5 = new Integer(40);
  Integer i6 = new Integer(0); System.out.println("i1=i2   " + (i1 == i2));
  System.out.println("i1=i2+i3   " + (i1 == i2 + i3));
  System.out.println("i1=i4   " + (i1 == i4));
  System.out.println("i4=i5   " + (i4 == i5));
  System.out.println("i4=i5+i6   " + (i4 == i5 + i6));
  System.out.println("40=i5+i6   " + (40 == i5 + i6));
  ``` ```
  i1=i2   true
  i1=i2+i3   true
  i1=i4   false
  i4=i5   false
  i4=i5+i6   true
  40=i5+i6   true
  ``` 解释：语句`i4 == i5 + i6`，因为+这个操作符不适用于Integer对象，首先i5和i6进行自动拆箱操作，进行数值相加，即`i4 == 40`。然后Integer对象无法与数值进行直接比较，所以i4自动拆箱转为int值40，最终这条语句转为`40 == 40`进行数值比较。
  [Java中的自动装箱与拆箱](http://droidyue.com/blog/2015/04/07/autoboxing-and-autounboxing-in-java/)

#### 三.String类和常量池

---

1. **String对象创建方式** ```
    String str1 = "abcd";
    String str2 = new String("abcd");
    System.out.println(str1==str2);//false
  ``` 这两种不同的创建方法是有差别的，第一种方式是在常量池中拿对象，第二种方式是直接在堆内存空间创建一个新的对象。
  **只要使用new方法，便需要创建新的对象。**
2. **连接表达式 +**
  （1）只有使用引号包含文本的方式创建的String对象之间使用“+”连接产生的新对象才会被加入字符串池中。
  （2）对于所有包含new方式新建对象（包括null）的“+”连接表达式，它所产生的新对象都不会被加入字符串池中。 ```
  String str1 = "str";
  String str2 = "ing"; String str3 = "str" + "ing";
  String str4 = str1 + str2;
  System.out.println(str3 == str4);//false String str5 = "string";
  System.out.println(str3 == str5);//true
  ``` [java基础：字符串的拼接](http://www.jianshu.com/p/88aa19fc21c6)
  - 特例1 ```
    public static final String A = "ab"; // 常量A
    public static final String B = "cd"; // 常量B
    public static void main(String[] args) {
    String s = A + B;  // 将两个常量用+连接对s进行初始化
    String t = "abcd";
    if (s == t) {
        System.out.println("s等于t，它们是同一个对象");
    } else {
        System.out.println("s不等于t，它们不是同一个对象");
    }
    }
    s等于t，它们是同一个对象
    ``` A和B都是常量，值是固定的，因此s的值也是固定的，它在类被编译时就已经确定了。也就是说：String s=A+B; 等同于：String s="ab"+"cd";
  - 特例2 ```
    public static final String A; // 常量A
    public static final String B;    // 常量B
    static {
    A = "ab";
    B = "cd";
    }
    public static void main(String[] args) {
    // 将两个常量用+连接对s进行初始化
    String s = A + B;
    String t = "abcd";
    if (s == t) {
        System.out.println("s等于t，它们是同一个对象");
    } else {
        System.out.println("s不等于t，它们不是同一个对象");
    }
    }
    s不等于t，它们不是同一个对象
    ``` A和B虽然被定义为常量，但是它们都没有马上被赋值。在运算出s的值之前，他们何时被赋值，以及被赋予什么样的值，都是个变数。因此A和B在被赋值之前，性质类似于一个变量。那么s就不能在编译期被确定，而只能在运行时被创建了。
3. `String s1 = new String("xyz");` **创建了几个对象？**
  考虑类加载阶段和实际执行时。
  （1）类加载对一个类只会进行一次。"xyz"在类加载时就已经创建并驻留了（如果该类被加载之前已经有"xyz"字符串被驻留过则不需要重复创建用于驻留的"xyz"实例）。驻留的字符串是放在全局共享的字符串常量池中的。
  （2）在这段代码后续被运行的时候，"xyz"字面量对应的String实例已经固定了，不会再被重复创建。所以这段代码将常量池中的对象复制一份放到heap中，并且把heap中的这个对象的引用交给s1 持有。
  这条语句创建了2个对象。

动态 new String只有在调用intern()时才会放入常量池。

1. **java.lang.String.intern()**
  运行时常量池相对于CLass文件常量池的另外一个重要特征是**具备动态性**，Java语言并不要求常量一定只有编译期才能产生，也就是并非预置入CLass文件中常量池的内容才能进入方法区运行时常量池，运行期间也可能将新的常量放入池中，这种特性被开发人员利用比较多的就是**String类的intern()**方法。
  String的intern()方法会查找在常量池中是否存在一份equal相等的字符串,如果有则返回该字符串的引用,如果没有则添加自己的字符串进入常量池。 ```
  public static void main(String[] args) {
     String s1 = new String("计算机");
     String s2 = s1.intern();
     String s3 = "计算机";
     System.out.println("s1 == s2? " + (s1 == s2));
     System.out.println("s3 == s2? " + (s3 == s2));
  }
  ``` ```
  s1 == s2? false
  s3 == s2? true
  ```
2. **字符串比较更丰富的一个例子** ```
  public class Test {
  public static void main(String[] args) {
     String hello = "Hello", lo = "lo";
     System.out.println((hello == "Hello") + " ");
     System.out.println((Other.hello == hello) + " ");
     System.out.println((other.Other.hello == hello) + " ");
     System.out.println((hello == ("Hel"+"lo")) + " ");
     System.out.println((hello == ("Hel"+lo)) + " ");
     System.out.println(hello == ("Hel"+lo).intern());
  }
  }
  class Other { static String hello = "Hello"; }
  package other;
  public class Other { public static String hello = "Hello"; }
  ``` ```
  true true true true false true
  ``` 在同包同类下,引用自同一String对象.
  在同包不同类下,引用自同一String对象.
  在不同包不同类下,依然引用自同一String对象.
  在编译成.class时能够识别为同一字符串的,自动优化成常量,引用自同一String对象.
  在运行时创建的字符串具有独立的内存地址,所以不引用自同一String对象. 来源： [http://www.jianshu.com/p/c7f47de2ee80](http://www.jianshu.com/p/c7f47de2ee80)

# integer 题目

今天My partner问我一个让他头疼的[Java](http://lib.csdn.net/base/java)question，求输出结果：

```
/**  *   * @author DreamSea 2011-11-19  */ public class IntegerTest {     public static void main(String[] args) {             objPoolTest();     }      public static void objPoolTest() {         Integer i1 = 40;         Integer i2 = 40;         Integer i3 = 0;         Integer i4 = new Integer(40);         Integer i5 = new Integer(40);         Integer i6 = new Integer(0);                  System.out.println("i1=i2\t" + (i1 == i2));         System.out.println("i1=i2+i3\t" + (i1 == i2 + i3));         System.out.println("i4=i5\t" + (i4 == i5));         System.out.println("i4=i5+i6\t" + (i4 == i5 + i6));                      System.out.println();             } }
```

输出结果：

```
i1=i2true
i1=i2+i3　  true
i4=i5false
i4=i5+i6true
```

看起来比较Easy的问题，但是Console输出的Result和我们所想的确恰恰相反，我们就疑惑了，这是为什么咧？

最后通过网上搜索得知Java为了提高性能提供了和String类一样的对象池机制，当然Java的八种基本类型的包装类（Packaging Type）也有对象池机制。

Integer i1=40；Java在编译的时候会执行将代码封装成Integer i1=Integer.valueOf(40);通过查看Source Code发现：

Integer.valueOf()中有个内部类IntegerCache（类似于一个常量数组，也叫对象池），它维护了一个Integer数组cache，长度为（128+127+1）=256，Integer类中还有一个Static Block(静态块)。

从这个静态块可以看出，Integer已经默认创建了数值【-128-127】的Integer缓存数据。所以使用Integer i1=40时，JVM会直接在该在对象池找到该值的引用。也就是说这种方式声明一个Integer对象时，JVM首先会在Integer对象的缓存池中查找有木有值为40的对象，如果有直接返回该对象的引用；如果没有，则使用New keyword创建一个对象，并返回该对象的引用地址。因为Java中【==】比较的是两个对象是否是同一个引用（即比较内存地址），i2和i2都是引用的同一个对象，So i1==i2结果为”true“；而使用new方式创建的i4=new Integer(40)、i5=new Integer(40)，虽然他们的值相等，但是每次都会重新Create新的Integer对象，不会被放入到对象池中，所以他们不是同一个引用，输出false。

对于i1==i2+i3、i4==i5+i6结果为True，是因为，Java的数学计算是在内存栈里操作的，Java会对i5、i6进行拆箱操作，其实比较的是基本类型（40=40+0），他们的值相同，因此结果为True。

好了，我想说道这里大家应该都会对Integer对象池有了更进一步的了解了吧，我在诺诺的问一句如果把40改为400猜猜会输出什么？

```
i1=i2false
i1=i2+i3true
i4=i5false
i4=i5+i6true
```

这是因为Integer i1=400，Integer i2=400他们的值已经超出了常量池的范围，JVM会对i1和i2各自创建新的对象（即Integer i1=new Integer(400)），所以他们不是同一个引用。

来源： [http://blog.csdn.net/qq_27093465/article/details/52033409](http://blog.csdn.net/qq_27093465/article/details/52033409)
