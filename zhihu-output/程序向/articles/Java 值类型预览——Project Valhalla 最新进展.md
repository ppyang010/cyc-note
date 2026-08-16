---
id: "588932823"
title: "Java 值类型预览——Project Valhalla 最新进展"
author: "Glavo"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/588932823"
created: "2022-12-04 18:29"
updated: "2022-12-04 21:11"
collected: "2022-12-04 18:29"
downloaded: "2026-08-16"
---
本文是对 Java 值类型项目（Project Valhalla）及其前沿进展的简略介绍。

在 Java 值类型的方案大体已经确定的现在，本文会向关心 Java 值类型的用户介绍 Java 值类型目前的方案，为之后的学习与迁移做好准备。

本文部分内容是我通过邮件从 Project Valhalla 开发人员口中得到的新消息，相关文档（主要是 JEP 401）部分已经过时，目前以本文为准，但随着项目发展具体细节仍会变化。

  

如果你之前没有关心过 Project Valhalla，你可能会好奇为什么 Java 的值类型拖了这么久还没有正式发布。对此，请先看看我之前翻译的关于 Project Valhalla 历史的文章：[Glavo：Java 的值类型与特化泛型 —— 通往 Valhalla 的道路](https://zhuanlan.zhihu.com/p/370256018)。

Project Valhalla 在这八年的发展中已经尝试过六个原型，放弃过多种不同的方案。本文讲述的内容主要来源于其中的第六原型：L-World。

  

## 托管还是手工管理？

谈到值类型，很多程序员可能想到的是 C++ 或者 C# 中的 struct。

对于这些惯于给用户更多控制，以便于用户进行优化的语言来说，值类型代表的是一种控制权的下放，允许用户手工精细地调整对象布局，写出高性能的代码。

但是 Java 作为一种强调“托管”的语言，在这个问题上却是用完全相反的思路在思考：

之所以 JVM 没有办法优化出相当于值类型的代码，是因为 JVM 放给用户了太多控制权，这种灵活性干扰了 JVM 优化。那么，我们应该从用户手中收走一些能力，这样才能让 JVM 最大限度地优化程序。

这种思维方式正是我喜欢 Java 的原因：它是少有的笔直沿着“托管”方向发展的主流语言。

虽然托管语言 native 化混合发展也是一种可行的方案，能够得到立竿见影的提升，但 Java/JVM 这种更纯粹的方向与探索让我看到了**托管**语言的未来。

## 逃逸分析与标量替换

在谈具体的方案之前，我们先来看看 Java 现在是怎么做的，这对于阐述 Project Valhalla 的设计是很重要的。

对于下面这段代码：

```java
record Pair<A, B>(A first, B second) {}

void f() {
  var pair = new Pair<>(0, "foo");
  // ... do something
}
```

由于目前 Java 没有值类型，所以 `Pair` 只是一个普通的引用类型，因此你或许觉得 `new Pair<>(...)` 一定会在堆上分配一个新对象。但这是真的吗？

答案是否定的。

现代 JVM 会通过一种名为“**逃逸分析**”（Escape Analysis）的技术，分析一个对象是否通过被设置为字段、静态变量、放入数组或成为返回值等方式“逃逸”。

假如 JVM 发现一个对象并没有“逃逸”，那么 JIT 编译器就可以选择做进一步的优化：标量替换（Scalar Replacement）。这项优化可以将对象的全部成员变量拆出来放到栈上，从而避免任何动态内存分配。

如果上面代码中的 `pair` 在之后没有逃逸出这个方法，那么 JVM 就可以直接消除对这个 `Pair` 的分配：

```java
void f() {
  var __pair_first = 0;
  var __pair_second = "foo";
  // ... do something
}
```

标量替换能够起到了值类型的作用，但标量替换不是万能的，它仅能对局部变量起效，且将对象作为静态变量、对象字段、数组元素，或者作为参数传递给无法内联的方法，都会使对象逃逸，从而阻止标量替换。

那么，为什么需要逃逸分析才能进行标量替换？是什么阻止了我们更广泛地进行标量替换？假如我们解决了这项阻碍，让 JVM 无需逃逸分析就可以进行标量替换，甚至能够允许对字段以及数组元素进行标量替换，我们不是就拥有了程序员们心心念念的值类型了？

这就是 Project Valhalla 的切入点：为标量替换扫清阻碍。

## 对象的同一性（Identity）

究竟是什么阻碍了标量替换？Project Valhalla 给出了答案：对象的**同一性（Identity）**。

所谓对象的同一性（Identity），是指对象拥有的某种可以把它与另一个对象区分开的性质。

就拿上面写过的 `Pair` 类来说，我们可以调用两次 `new Pair<>(0, "foo")` 创建两个对象，使用 `equals` 比较的话，它们的值是一样的，但我们依然能够通过 `==` 将它们区分开来，知道它们是不同的两个对象。在这里，能通过 `==` 进行比较就是一种同一性的体现。

在 Java 中，即使两个对象所有字段的内容都一样，我们依然能够通过以下方式区分开它们：

-   使用 `==` 或者 `!=` 可以直接比较它们是不是同一对象；
-   使用 `System.identityHashCode(Object)` 函数可以获取到对象的 identity-hash 值，该值对于不同的对象来说通常是不同的；
-   通过 `synchronized` 语句可以为对象加锁，其他线程尝试锁定同一个对象会被阻塞，而锁定不同对象不会受到影响；
-   如果对象包含可变字段，那么对一个对象的字段进行修改，另一个对象并不会同时发生变化。

因为以上性质都是围绕着“真正有一个存在于堆上的对象”所提供的，所以朴素地在堆上分配对象很容易满足以上的性质，而想要以其他方法实现对象就要付出额外的努力。

之所以只能对未逃逸的对象进行标量替换，就是因为 JVM 只有在能确保对象没有用到同一性的情况下才能安全地展开对象，而逃逸分析能够保证 JVM 在优化代码时掌握了该对象的所有用法。只要对象的所有用途都在掌握中，那想要知道它有没有用到同一性就是很轻松的事情。

为了维护同一性，JVM 付出了高昂的代价，但这种性质真的总是能用得上吗？比如对于 `Integer` 对象，你会用 `==` 来比较它们，还是会对它们加锁，或者想改它的内容值？

现实中，有相当一部分对象都是像 `Integer` 这样永远用不上同一性。为此，Project Valhalla 创造了一种叫做**无同一性对象（Identity-free objects）**的概念，这种对象有以下几点特殊性质：

-   `==` 与 `!=` 操作符不再比较是否是同一个对象，而是会递归通过 `==` 比较对象的所有字段值是否相同；
-   `System.identityHashCode(Object)` 将为类型以及所有字段都相同的无同一性对象生成一样哈希值；
-   不允许通过 `synchronized` 语句同步无同一性对象，尝试这样做会抛出异常；
-   无同一性对象是不可变的，所有字段都被标记为 `final`，不可修改。

这样做，JVM 就不需要继续为这些对象维护同一性，那么就可以更自由地处理这些对象。

逃逸分析不再必要，只要 JVM 愿意就能在栈上进行标量替换，把对象拆散成一堆变量紧凑地存储。

如果对象还需要多态性，比如要赋值给一个超类的引用，那按需再在堆上分配一个对象出来都行，反正已经把用户所有分辨它和原先的对象区别的手段禁止了，那么对于用户来说新对象和原本被拆散的对象就没有任何区别。

在这背后，JVM 可以透明地缓存堆上的对象（像现在 `Integer.valueOf` 那样干的），也可以通过 GC 合并相同的对象（现在 JVM 就给 String 开了个洞，将其内部数组视为 Identity-free 的，可以用 JVM 选项开启字符串内部数组去重功能），或者干脆不进行任何标量替换，当成普通的对象用也是可行的。

  

在了解了 Project Valhalla 中同一性的概念后，我们就可以来看看 JEP 文档中 Project Valhalla 的具体实施细节了。

## 值对象（Value Objects）

Project Valhalla 的 JEP 草案 [值对象（Value Objects）](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8277163)描述的就是无同一性对象的具体实施方案。

值对象草案中，Java 将允许使用 `value` 这个上下文关键词来修饰类声明：

```java
value class Substring implements CharSequence {
    private String str;
    private int start;
    private int end;

    public Substring(String str, int start, int end) {
        checkBounds(start, end, str.length());
        this.str = str;
        this.start = start;
        this.end = end;
    }

    public int length() {
        return end - start;
    }

    public char charAt(int i) {
        checkBounds(0, i, length());
        return str.charAt(start + i);
    }

    public Substring subSequence(int s, int e) {
        checkBounds(s, e, length());
        return new Substring(str, start + s, start + e);
    }

    public String toString() {
        return str.substring(start, end);
    }

    private static void checkBounds(int start, int end, int length) {
        if (start < 0 || end < start || length < end)
            throw new IndexOutOfBoundsException();
    }
}
```

这样的类的实例被称为值对象。

值对象是无同一性的，也就是说它不可被锁定，无法用 `==` 区分两个内容相同的对象，而且不可修改，所有字段都是被隐式声明为 `final`。

值对象除了以上性质外，用起来与普通的对象没有其他不同。它依然具有多态性，你可以将它赋值给 `CharSequence` 类型的变量，正常地调用虚方法。

值对象与普通对象最大的区别在于，只要 JVM 能够知道一个局部变量是类型是一个 value class，那么通常来说这个变量会被标量替换，所有内容直接放置在栈上，而无需进行逃逸分析后再尝试优化。

但可惜的是，value class 依然是传统的引用类型，因此一些性质导致标量替换通常仅限于局部变量，在作为字段或者数组成员时值对象通常还是需要保存于堆上。

## 原始对象（Primitive Objects）

在无同一性对象的基础上，Project Valhalla 认为以下引用类型的性质在继续阻碍着 JVM 优化：

-   引用类型的变量可被设置为 `null`，如果想要通过字段或数组保存对象，那必须去以其他方式编码 `null` 值，可能要付出额外的存储成本，或者实现起来非常麻烦；
-   对引用类型的字段写入是原子操作，如果一个线程写入引用类型的字段，另一个线程读取字段看到的要么是新对象，要么是老对象，并不会看到一部分字段更新了另一部分还没更新的损坏对象。

因为这些原因，在 value class 以外，Project Valhalla 提供了一类新的构造：**原始对象（Primitive Objects）**。（原始对象相关的 [JEP 401](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/401) 我曾经翻译过（[Glavo：JEP 401：原始对象（Primitive Objects）](https://zhuanlan.zhihu.com/p/354841176) ），不过 JEP 文档内容部分过时还没有更新）

通过上下文关键字 `primitive` 修饰的类是**原始类（Primitive Class），**就像下面的 `Point` 类。而原始类的实例便是原始对象：

```java
primitive class Point implements Shape {
    private double x;
    private double y;

    public Point(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double x() { return x; }
    public double y() { return y; }

    public Point translate(double dx, double dy) {
        return new Point(x+dx, y+dy);
    }

    public boolean contains(Point p) {
        return equals(p);
    }
}

interface Shape {
    boolean contains(Point p);
}
```

原始对象也是一种无同一性对象，不支持使用 `==` 比较引用、不可被锁定、所有字段都是隐式 `final` 的。你可以像使用值对象那样使用原始对象，这种用法下他们是相似的。

但与 value class 不同的是，以上的 `Point` 类同时声明了两个类型：`Point.ref` 和 `Point.val`。

`Point.val` 被称为**原始值类型 （primitive value type）**，而 `Point.ref` 被称为**原始引用类型（primitive reference type）** 。简单的类型名 `Point` 被视为是 `Point.ref` 的别名。

原始对象可以作为**原始值（primitive value）**被直接存储进变量和进行操作，没有对象头也不进行指针操作，此时使用的类型是原始值类型。

原始对象也可以作为**对象引用（references to objects）**被存储与操作。对它们引用的类型则为原始引用类型。

当作为原始值使用时，它具有了值对象不存在的性质：

-   原始值类型的值总是非 `null` 的；
-   对非 `volatile` 的原始值类型的字段或数组元素赋值的时候，不保证是原子的，同时在另一个线程中读取时可能会观察到一个损坏了的对象；
-   原始值总是存在一个绕过了构造器构造出来的默认值，其成员全部是对应类型的默认值（数字类型成员为 0，引用类型成员为 null，其他原始值类型成员为它的默认值）；
-   原始值类型的字段以及数组元素都会被默认初始化为其默认值，而不是 `null`。

现在，没有什么能够阻止 JVM 进行标量替换了！

只要原始值类型出现的地方，不管是局部变量、方法参数、返回值、字段还是数组，JVM 都可以自由地处理他们。只要 JVM 愿意，就可以在无需任何逃逸分析的情况下将它们内联成其所有字段的内容，不再需要在堆上创建对象。

原始类也可以实现接口，或者继承抽象类。当作为超类型变量使用时，原始值=对象也具有多态性，只是失去了原始值的特征，与值对象没有区别。

而每个原始类的原始引用类型就是对应的原始值类型的超类型，所以你当你需要作为引用类型使用它（比如需要存储 `null`）时，你可以直接使用对应的原始引用类型。

因为有子类型关系，所以将原始值赋值给原始引用类型的变量是自然的，这种转换被称为**原始引用转换（primitive reference conversions）**，而反过来用原始引用类型的值给原始值类型变量赋值的时会发生一种新的隐式转换——**原始值转换（primitive value conversion）**。因此你可以不用强制转换就能在原始值类型与原始引用类型之间互相转换，这种转换也会在调用方法时自动发生。

### 为什么还需要值对象？

看起来原始对象的功能能完全覆盖值对象，但值对象的存在依然是必要的。

一部分类仅仅是不需要同一性的（比如 `LocalDateTime`），原始对象的默认值、字段撕裂等特性对它们来说都是很大的困扰；而原始对象更适合描述的是那些默认值存在现实意义的类（比如 `Complex`、`UnsignedLong` 等）。

## 统一基本值与对象

由于原始对象的出现，我们终于能够将基本值与对象统一，实现一切皆对象的目标。

这项大一统的工作有一个独立的 JEP：[JEP 402](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/402)（翻译：[Glavo：JEP 402：统一基本值与对象](https://zhuanlan.zhihu.com/p/354979657)）。

当原始对象实现后，基本类型的包装器将会成为原始类，而基本类型的关键字将成为其对应的原始值类型的别名。原本的拆箱与装箱操作被更通用的原始值转换和原始引用转换所取代，但使用上没有任何区别。

因为这些关键字是别名，所以每个原始值类型和原始引用类型都有两种方法表示，如下表所示：

| 原始类 | 值类型 | 引用类型 |
| ----- | ----- | ----- |
| Boolean | boolean 或 Boolean.val | boolean.ref 或 Boolean |
| Character | char 或 Character.val | char.ref 或 Character |
| Byte | byte 或 Byte.val | byte.ref 或 Byte |
| Short | short 或 Short.val | short.re）f 或 Short |
| Integer | int 或 Integer.val | int.ref 或 Integer |
| Long | long 或 Long.val | long.ref 或 Long |
| Float | float 或 Float.val | float.ref 或 Float |
| double 或 Double | double 或 Double.val | double.ref 或 Double |

让基本值成为原始对象，除了概念上的大一统外，最大的变化是让基本值可以拥有方法，原先包装器上的所有方法都成为基本值的成员，未来我们可以直接像 `1.toString()` 这样调用方法。

## 通用泛型（**Universal Generics**）

让值类型成为泛型参数也是许多程序员对 Java 的期望，这项工作由一个单独的 JEP 草案描述：[JEP draft: Universal Generics (Preview)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8261529)（翻译：[Glavo：JEP 草案：通用泛型（预览）](https://zhuanlan.zhihu.com/p/379313127)）。

在**通用泛型（Universal Generics）**完成后，所有泛型参数默认都可以是值类型，`List<int>` 这样的类型将是合法的。想要要求泛型参数只能为引用类型，需要使用上下文关键字 `ref` 对参数进行修饰：

```java
class C<ref T> { T x = null; /* ok */ }
  
FileReader r = new C<FileReader>().x;
Point.ref p = new C<Point.ref>().x;
```

同时也可以使用新的语法 `.ref` 从泛型参数映射至对应的引用类型：

```java
class C<T> { T.ref x = null; /* ok */ }
  
FileReader r = new C<FileReader>().x;
Point.ref p = new C<Point.ref>().x;
Point.ref p2 = new C<Point>().x;
```

但是默认允许泛型参数为值类型也带来了一些问题，比如对于以下的现有代码：

```java
class Box<T> {

    T x;
    
    public Box() {} // warning: uninitialized field
    
    T get() {
        return x;
    }
    
    void set(T newX) {
        x = newX;
    }
    
    void clear() {
        x = null; // warning: null assignment
    }
    
    T swap(T oldX, T newX) {
        T currentX = x;
        if (currentX != oldX)
            return null; // warning: null assignment
        x = newX;
        return oldX;
    }
    
}
```

由于现在泛型参数一定是引用类型，所以它在现在是合法的，但在 Project Valhalla 到来后就不再合法，因为如果 T 是值类型，那么给它赋值为 null 就会出问题。

对于此现象，Project Valhalla 完成后会对这样的代码添加更多检查与警告，督促开发者迁移适配通用泛型。

在未来，泛型代码的物理布局会针对每个原始值类型特化。那时会更早地检测到空污染，未能解决警告的代码可能会无法使用。 解决了警告的代码做好了*被特化的准备*：未来的 JVM 增强不会破坏程序的功能。

  

为了方便迁移，Project Valhalla 还定义了一系列参数化类型转换规则，方便用户进行从 `List<Integer>` 至 `List<int>` 这样的迁移。新的未受检转换包含以下新规则：

-   将参数化类型的类型参数从通用类型变量（`T`）更改为其引用类型（`T.ref`），反之亦然

```text
List<T.ref> newList() { return Arrays.asList(null, null); }
List<T> list = newList(); // unchecked warning
```

-   将参数化类型的类型参数从原始值类型（`Point`、`LocalDate.val`）更改为其引用类型（`Point.ref`、`LocalDate`），反之亦然

```text
void plot(Function<Point.ref, Color> f) { ... }
Function<Point, Color> gradient = p -> Color.gray(p.x());
plot(gradient); // unchecked warning
```

-   将参数化类型中的类型通配符边界从通用类型变量（`T`）或原始值类型（`Point`、`LocalDate.val`）更改为其引用类型（`T.ref`、`Point.ref`、`LocalDate`），反之亦然（其子类型尚不允许转换）

```text
Supplier<? extends T.ref> nullFactory() { return () -> null; }
Supplier<? extends T> factory = nullFactory(); // unchecked warning
```

-   递归地将未受检转换应用于参数化类型的任何类型参数或通配符边界

```text
Set<Map.Entry<String, T>> allEntries() { ... }
Set<Map.Entry<String, T.ref>> entries = allEntries(); // unchecked warning
```

这些未受检的转换在小代码段中似乎很容易避免，但它们提供的灵活性将大大简化迁移，因为不同的程序组件和库可能在不同时间采用通用泛型。

除了未受限的赋值外，这些转换还可以用于未受检的强制转换和方法覆盖。

```text
interface Calendar<T> {
    Set<T> get(Set<LocalDate> dates);
}

class CalendarImpl<T> implements Calendar<T> {
    Set<T.ref> get(Set<LocalDate.val> dates) { ... } // unchecked warning
}
```

## 原型：LW4

在 2019 年给出了 LW2 原型后，经过三年时间 Project Valhalla 终于再次给出了新的阶段性成果：LW4 原型。

LW4 原型的 EA 构建（基于 JDK 20）向所有人开放，想要体验 Project Valhalla 的用户可以直接下载尝试：

[Project Valhalla Early-Access Builds](https://link.zhihu.com/?target=https%3A//jdk.java.net/valhalla/)

## 未来的工作

以上这部分内容是 Project Valhalla 已经通过 JEP 给出的方案，但 Project Valhalla 将带来的不止这些，比如：

-   冻结数组（[JEP draft: Frozen Arrays (Preview)](https://link.zhihu.com/?target=https%3A//openjdk.org/jeps/8261007)）作为不可变的数组，可能会作为 Project Valhalla 中所述的“无同一性对象”而实现；
-   现在 Java 标准库中被标注为 value based 的类，在 Project Valhalla 实现后将会迁移至 value class 或者 primitive class，现有代码可能会得到免费的性能提升；
-   未来，泛型代码的物理布局会针对每个原始值类型特化（通用泛型暂时还是基于擦除实现，真正的特化将在独立的 JEP 中进行）；
-   OpenJDK 中还有一些项目迟迟无动静也是在等待 Project Valhalla 完成，这样才能够在 API 中更好的利用值类型以改善性能。

过去 Java 的慢节奏迭代严重拖累了 Java 的发展进度，使得其落后于时代，直到 Java 9 才开始快速追赶。当 OpenJDK 研发已久几个重要 Project（Valhalla/Panama/Loom）完成后，Java 也算彻底完成了现代化。

你可能不在乎 Java 语言本身怎么样，但这些项目给 JVM 带来的基础设施也会给 Kotlin/Scala 等 JVM 语言受益，我很期待那一天的来临。