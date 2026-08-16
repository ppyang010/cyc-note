---
id: "2396553186"
title: "国内Java面试总是问StringBuffer，StringBuilder区别是啥？档次为什么这么低？"
author: "yuantj"
type: zhihu-answer
source: "https://www.zhihu.com/question/50211894/answer/2396553186"
created: "2022-03-19 10:58"
updated: "2022-06-20 09:20"
collected: "2022-03-19 10:58"
downloaded: "2026-08-16"
---
20220620有更新，为保证初次阅读体验，放在原答案的后面。

以下为原答案：

* * *

我知道这道题的“标准答案”是“前者线程安全，后者线程不安全”。

但我偏不这么答。

这道题的正确答案其实非常简单，历史遗留问题而已。

随着当时 CPU 主频和核心数的增长，为了充分利用 CPU 的算力，“并发”的概念应运而生。而支持多进程的类 UNIX 系统当时还是高端计算机的专利，大多数家用电脑使用的 DOS 和 Windows 系统使用多进程开销太大。所以，多线程在当时几乎是唯一的并发解决方案。然而，无论是 C 还是 C++，都原生不支持多线程。

Java 语言设计之初，就是为了替代（当时）极其复杂原始的 C/C++，其中的一个大改进就是，把并发（多线程）的理念贯彻到了语言的各个角落。例如， Java 语言的所有对象都支持作为 `synchronized` 代码块的互斥锁使用，而且 `wait`、`notify` 等 `final` 方法还出现在万物之源 `Object` 类中。

为什么最初几乎所有可变对象如 `StringBuffer`、`Vector`、`Hashtable`、`ByteArray{Input,Output}Stream` 等都要设计成线程安全的？

因为当初的语言设计者认为多线程是万金油，这些可变对象几乎都会被多个线程同时修改，所以为了避免 Race Condition，也为了避免程序员频繁使用 `synchronized` 代码块造成可读性和易用性降低，就把它们统统设计成“线程安全”的，让保持同步的脏活累活都留给标准库干，反正也不影响单线程下的准确性，无非损失亿点性能而已。

但事实证明，多个线程同时修改一个对象的场景才是少数，绝大多数可变对象只会被一个线程修改，然而因为频繁不必要的上锁、释放锁的操作，使得性能损失很大，所以你会看到，后来的 `ArrayList`、`HashMap` 等可变类都不再默认线程安全，以此换取单线程下的性能提升，然后用 `Collections.synchronizedXxx` 等方法提供少数情况需要多线程安全的可变对象。

这个问题的主角 `StringBuffer` 和 `StringBuilder` 也是一样的，后者就是为纠正历史遗留问题，提高单线程下的性能而生的，而为了向下兼容性和需要线程安全的场景，才保留 `StringBuffer` 类。

随着内存越来越大，函数式编程的“万物皆 immutable”的思想流行，Java 也出现越来越多的不可变类，例如 `java.time` 包中的类、`Optional` 类、 `List.of`、`Set.of` 返回的不可变集合等。这才是多进程、多线程下保证准确性、提升性能的新的解决方案。

* * *

20220620 更新：

说句题外话，大家知道 `String` 的 `+` 运算符，如果两边不全是字面量，是怎么实现的吗？相信大家都知道，就是利用了大名鼎鼎的 `StringBuilder` 。

比如 `java.lang.Object.toString()` 的默认实现：

```java
public String toString() {
    return getClass().getName() + "@" + Integer.toHexString(hashCode());
}
```

对字节码进行反汇编，就是这个样子：

```text
public java.lang.String toString();
    descriptor: ()Ljava/lang/String;
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=2, locals=1, args_size=1
         0: new           #1   // class java/lang/StringBuilder
         3: dup
         4: invokespecial #3   // Method java/lang/StringBuilder."<init>":()V
         7: aload_0
         8: invokevirtual #7   // Method getClass:()Ljava/lang/Class;
        11: invokevirtual #13  // Method java/lang/Class.getName:()Ljava/lang/String;
        14: invokevirtual #19  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
        17: ldc           #23  // String @
        19: invokevirtual #19  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
        22: aload_0
        23: invokevirtual #25  // Method hashCode:()I
        26: invokestatic  #29  // Method java/lang/Integer.toHexString:(I)Ljava/lang/String;
        29: invokevirtual #19  // Method java/lang/StringBuilder.append:(Ljava/lang/String;)Ljava/lang/StringBuilder;
        32: invokevirtual #35  // Method java/lang/StringBuilder.toString:()Ljava/lang/String;
        35: areturn
      LineNumberTable:
        line 256: 0
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
            0      36     0  this   Ljava/lang/Object;
```

直译成 Java 源代码就是这样的：

```java
public java.lang.String toString() {
    return new java.lang.StringBuilder()
        .append(this.getClass().getName())
        .append("@")
        .append(java.lang.Integer.toHexString(this.hashCode()))
        .toString();
}
```

那么你猜，在 Java 1.5，也就是首次出现 `StringBuilder` 之前，这个 `+` 是怎么实现的呢？难道真的像有些人想象中的那样，大量构造 `String` 对象吗？

非也。恰好本人这两天在 Windows NT 4.0 的系统目录中翻到了 Java 1.0 中 `Object` 的字节码，遂反编译之：

```text
public java.lang.String toString();
    descriptor: ()Ljava/lang/String;
    flags: (0x0001) ACC_PUBLIC
    Code:
      stack=3, locals=1, args_size=1
         0: new           #4    // class java/lang/StringBuffer
         3: dup
         4: invokespecial #11   // Method java/lang/StringBuffer."<init>":()V
         7: aload_0
         8: invokevirtual #10   // Method getClass:()Ljava/lang/Class;
        11: invokevirtual #14   // Method java/lang/Class.getName:()Ljava/lang/String;
        14: invokevirtual #15   // Method java/lang/StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;
        17: ldc           #2    // String @
        19: invokevirtual #15   // Method java/lang/StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;
        22: aload_0
        23: invokevirtual #12   // Method hashCode:()I
        26: iconst_1
        27: ishl
        28: iconst_1
        29: iushr
        30: bipush        16
        32: invokestatic  #13   // Method java/lang/Integer.toString:(II)Ljava/lang/String;
        35: invokevirtual #15   // Method java/lang/StringBuffer.append:(Ljava/lang/String;)Ljava/lang/StringBuffer;
        38: invokevirtual #16   // Method java/lang/StringBuffer.toString:()Ljava/lang/String;
        41: areturn
      LineNumberTable:
        line 76: 0
        line 77: 22
        line 76: 38
```

也就是：

```java
public java.lang.String toString() {
    return new java.lang.StringBuffer()
        .append(this.getClass().getName())
        .append("@")
        // 没错，那时候连 Integer.toHexString(int) 都没有。
        .append(java.lang.Integer.toString(this.hashCode() << 1 >>> 1, 16))
        .toString();
}
```

显然，当时的 Java 设计者也认为拼接字符串时大量创建不可变字符串对象是个开销非常大的行为，于是就巧妙地利用了 `StringBuffer` 这个东西拼接字符串。然而，这是个单线程操作， `StringBuffer` 这个不分青红皂白就是追求线程安全性的设计，就显得低效了（毕竟每次调用 `append` 都要上锁释放锁一次）。所以本人猜测，这也是 `StringBuilder` 诞生的一大原因（具体的 JEP 因为太过古老，没在 openjdk 官网上发现，等我以后再找找）。