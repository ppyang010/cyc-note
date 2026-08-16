---
id: "3576046681"
title: "如何理解 Java 泛型？"
author: "李斯维"
type: zhihu-answer
source: "https://www.zhihu.com/question/23432488/answer/3576046681"
created: "2024-07-28 12:17"
updated: "2024-07-28 12:17"
collected: "2024-07-28 12:17"
downloaded: "2026-08-16"
---
作为一个 Java 程序员，用到泛型最多的，我估计应该就是这一行代码：

```java
List<String> list = new ArrayList<>();
```

这也是所有 Java 程序员的泛型之路开始的地方啊。

不过本文讲泛型，先不从这里开始讲，而是再往前看一下，看一看没有泛型的时候，Java 代码是怎么写的，然后我们才会知道为什么要加入泛型，泛型代码该怎么写。在了解了这些内容之后，我们将继续深入介绍泛型中的 `extends`、`super`、`<?>` 通配符。

## 为什么要设计泛型

### 提高代码重用性

没有泛型之前，我们写一个两数相加的函数：

```java
public static int add(int a, int b) {
    return a + b;
}
```

看似没问题，对吧。不过这个时候我们想计算 float 类型的加法，那这个函数就不行了，因为他只能计算 int 值。此时就只能再加入一个相同的函数了：

```java
public static float add(float a, float b) {
    return a + b;
}
```

现在我们有两个方法能够计算 int 和 float 类型的加法。那现在如果要计算 String 类型的加法呢，这两个方法就又不够用了。面对这样的需求，在没有泛型的支持下，我们只能不断地增加逻辑基本相同的方法，代码重用性极低。 这就是泛型要解决的第一个问题：提高代码重用性。 那在泛型的加持下，我们如何编写这个函数呢？

```java
public static <T extends Number> double add(T a, T b) {
    return a.doubleValue() + b.doubleValue();
}
```

这个方法使用了泛型，它能够处理任何类型的数字相加，不需要针对每个类型编写各自的加法方法。这就大大提高了代码的重用性，有了这个方法，那些固定类型的方法就都可以删了。 特别是一些逻辑相同的代码，使用泛型不仅能够提高代码重用性，还能够提高可读性。比如说下面这段代码，真是的是非常好用：

```java
public static <T> void printArray(T[] array) {
    for (T element : array) {
        System.out.println(element);
    }
}
```

泛型的这个特性虽然很牛了，但是这还不是 Java 要设计泛型的全部原因。因为泛型还有一个作用，那就是保证类型安全。

### 保证类型安全

在说泛型的这个作用之前，先问大家一个问题，咱们常用的集合 `ArrayList` 是 Java 哪个版本加入的呢？泛型又是 Java 哪个版本加入的呢？

答案：`ArrayList` 是 Java 1.2 版本加入的，而泛型是 Java 1.5 加入的。

也就是说，有一段时时间，`ArrayList` 不是大家普遍认识的带泛型的 `ArrayList<T>` 这种形式，而是一个只能存放 `Object` 的列表。

在那一段泛型之光没有照耀到 Java 的日子里，保证类型安全成为了 Java 程序员在使用集合时不得不考虑的事情，考虑下面这一段代码：

```java
ArrayList list = new ArrayList();
list.add("123");
// do some work......
Integer num = (Integer) list.get(0);
```

这段代码没有使用泛型来使用 `ArrayList`，我们加入了字符串 `"123"`，但是在使用时，我们假定程序员忘记了加入的类型，他只记得好像应该是数字，于是在获取时就直接使用了 `Integer` 类强转。

这样的代码是能通过编译的，但是在运行的时候，会崩溃：

````text
Caused by: java.lang.ClassCastException: java.lang.String cannot be cast to java.lang.Integer
 ```
这是一个典型的未使用泛型，而导致的类型安全无法保证，引发的崩溃。让程序员去保证类型安全，本身是不靠谱的做法，特别是在这种都是 Object 对象的列表中，鬼都不会知道存着的是个什么鬼。

这个时候就需要泛型出场了，泛型能够在编译时保证类型安全。例如上面的代码，我们加入泛型：
```java
ArrayList<String> list = new ArrayList<>();
list.add("123");
Integer num = (Integer) list.get(0);
````

首先，`ArrayList` 加入泛型后，我们就知道这个列表是只能存入 `String` 类型的，也就不会将其转换为 `Integer`。那如果我非要转换呢，javac 编译器就会报错：

```text
错误: 不兼容的类型: String无法转换为Integer
    Integer num = (Integer) list.get(0);
```

这样类型安全就可以在编译时得到保证，不会出现在运行时的崩溃。

例子的代码很简单，大家可能看不到这一点对于软件开发有多重要，在大型复杂的项目中，这种类型安全的保证，是能减少很多运行时的崩溃的。特别是，一般像这种类型不一致的崩溃很多都是偶现的，偶现的 BUG 是最恶心的，因此使用泛型保证类型安全是十分必要的。

### 消除强制类型转换

泛型的这个作用其实就是上面保证类型安全这一点带来的。没有用泛型时，需要我们使用强制类型转化，但是加入泛型后，编译器已经能够知道我们存入的是什么类型，因此也就不需要我们进行强制类型转换了。

既然泛型有那么大的作用，那我们就赶紧把泛型用起来吧。

![](images/233_001.jpg)

## 使用泛型

这一节，我们来看看如何使用系统提供的泛型类，以及其中需要注意的事项。

最常用到泛型的地方便是集合了，使用这些泛型集合类时，只需要把具体泛型参数 `<T>` 替换为需要的类型即可，例如 `ArrayList<String>`、`ArrayList<Number>`、 `Map<String, Integer>` 等。

如果在使用泛型类时不指定类型参数，编译器会给出警告，且只能将 `<T>` 视为 `Object` 类型。这个时候就需要程序员自己去保证类型安全了，因此强烈不建议这么做，因为这样容易将类型转换异常带到运行时中去。

使用泛型基本就需要注意以上两点，下面介绍一下在使用泛型时的注意事项，这也是大家很少关注到的向上转型的问题。

在 Java 中，`ArrayList<T>` 是实现了 `List<T>` 接口，也就是说它可以向上转型为 `List<T>` ：

```java
public class ArrayList<E> extends AbstractList<E>
        implements List<E>, RandomAccess, Cloneable, java.io.Serializable
```

那么问题就来了，当泛型参数不同时，还能向上转型么，说具体一点，`ArrayList<String>` 能转型为 `List<Number>` 么？

答案是不行的：

```java
ArrayList List = new ArrayList<String>();    //Raw use of parameterized class 'ArrayList'
List<Integer> list = new ArrayList<String>();    //直接报错
```

为什么 Java 不允许这么转型呢？因为运行转型的话，那么对于一个 `ArrayList<String>` 的容器，我将其转型为 `ArrayList<Integer>` 就可以往里面加入 `Integer` 对象了，这明显会造成 `ClassCastException`。泛型的存在用于限定类型的，这么一搞，泛型就失去了其作用。

这里，大家可以简单理解为，当泛型参数不一样时，两个类就没有太大关系了。例如 `ArrayList<Integer>` 和 `List<Number>` 两者完全没有继承关系。

## 编写泛型

知道怎么使用系统的泛型之后，我们现在就来看看如何编写自己的泛型类。

泛型作为对类型进行限制的一种方式，我们编写泛型代码，也就是对使用我们代码的人进行一种限制。在这种情况下，我们是作为其他程序员的底层，向上提供某种框架代码，让其他程序员能够在我们设定的框架中更容易地编写代码实现功能。这有点类似于库的开发者，或是框架开发者，作为这种角色，写好泛型代码就更显得尤为重要了。毕竟，你也不想让别人说，这代码写得就跟一坨屎一样吧。

### 编写泛型类

编写泛型类，是比普通类要复杂的。这里我们就用 `Pair<F, S>` 这个类作为目标，一步一步编写出一个合格的泛型类。`Pair` 类是 Android 开发中一个简单的使用工具类，用于存储一对相关联的对象。

我们的第一版 `Pair` 只能使用没有使用泛型：

```java
public class Pair {
    public final String first;
    public final String second;
}
```

那这肯定是不行的，因为这个 Pair 只能存放 String 类型的 first 和 second，那了能够存放所有类型，我们就使用泛型 `<T>`：

```java
public class Pair<T> {
    public final T first;
    public final T second;
}
```

我们把 `first` 和 `second` 用 `T` 来修饰，表示其这两个成员变量是 `T` 类型的。而这个 `T` 类型，Java 是不知道的，我们必须声明告诉 Java 这是一个类型，因此类名从 `Pair` 变成了 `Pair<T>`，后面的 `<T>` 就是我们的泛型类型声明。

上面的代码看上去没问题，但是这个 `Pair<T>` 只能存放的 `first` 和 `second` 必须是相同的类型 `T`，那不同类型的怎么办呢？这时候我们再加一个泛型不就行了：

```java
public class Pair<F, S> {
    public final F first;
    public final S second;
}
```

在加入两个泛型之后，`first` 和 `second` 的类型对应不同的泛型，这样就可以表示不同的类型了，注意 `F`、`S` 这两个不同的泛型都需要在类上进行声明。

我们在为 `Pair<F, S>` 添加个构造方法：

```java
public class Pair<F, S> {
    public final F first;
    public final S second;

    public Pair(F first, S second) {
        this.first = first;
        this.second = second;
    }
}
```

这算是一个简单的泛型类，那接下来，我们再为它编写一个泛型方法。

## 编写泛型方法

此处的泛型方法是指静态方法，而不是成员方法。这两种方法在使用泛型时是有一些区别的，其中最重要的一点就是，静态方法是不能使用类上声明的泛型类型，必须得自己声明泛型类型。例如，下面的代码将编译错误：

```java
public static class Pair<F, S> {
    public final F first;
    public final S second;

    //编译错误，F、S 类型不能在 static 方法上使用
    public static Pair<F, S> create(F a, S b) {
        return new Pair<F, S>(a, b);
    }
}
```

可以想一想，为什么静态方法不能使用类上已经声明的泛型类型呢？

在回答这个问题之前，我们可以先想一下，类上的泛型类型，是在什么时候确定下来的呢？是在类创建的时候，我们在 `new` 的时候是需要提供具体类型的，这个时候泛型就被具体化为某个特定类型。不同的对象可能被创建为不同的类型，而静态方法只跟类相关，跟具体对象无关，而这些泛型又是跟具体对象相关的。所以静态对象不能使用类上声明的泛型也就变得合理了。

那要想使静态方法使用泛型，那就必须这个静态方法自己声明泛型：

```java
public static <F, S> Pair <F, S> create(F a, S b) {
    return new Pair<F, S>(a, b);
}
```

这个静态方法在函数名前使用 `<F, S>` 来声明了两个泛型，那么后续这两个泛型就可以在这个函数中使用了。此时注意，这里的 `F`、`S` 虽然与 `Pair` 上的 `F`、`S` 泛型看似相同，实际上是没有任何关系的。所以为了避免产生误会，一般都会使用不同的泛型名，例如将这个方法的 `<F, S>` 变成 `<A, B>`：

```java
public static class Pair<F, S> {
    public final F first;
    public final S second;

    public static <A, B> Pair <A, B> create(A a, B b) {
        return new Pair<A, B>(a, b);
    }
}
```

这样才能够清楚地将静态方法的泛型类型和实例类型的泛型类型区分开。

在使用时，我们可以使用如下代码创建一个 `Pair<F, S>` 实例：

```java
Pair<String, Integer> pair = Pair.create("123", 123);
```

这里总结一下编写泛型需要注意的几点： - 编写泛型时，需要定义泛型类型 `<T>`； - 静态方法不能引用类上的泛型类型 `<T>`，必须定义自己方法特有的泛型类型； - 泛型可以同时定义多个，例如 `<F, S>`、`<F、S、T>`；

在这里我们需要注意泛型的一个限制，那就是不能使用泛型类型直接创建对象。这一点也好理解，`T` 是什么类型只有在使用时，指定了泛型的具体类型才能确定。`T` 类型是一个抽象的类型，它是无法直接 `new` 出来的，就像你无法直接 `new` 一个 `interface` 一样。例如下面的代码是错误的：

```java
public static class Pair<F, S> {
    public final F first;
    public final S second;

    public Pair(F first, S second) {
        this.first = new F();        //错误
        this.second = new S();       //错误
    }
}
```

这里使用 `F` 类型的默认构造，设想一下假如这个类型被确定为一个没有默认构造方法的类型呢。所以使用泛型类型创建对象是不行的。

![](images/233_002.jpg)

  

## Java 的泛型实现方式：类型擦除

上面的几节介绍了泛型的好处，泛型的使用，那这一节我们就来看看 Java 是如何实现泛型技术的。

首先，泛型编程并非 Java 特有的，在其他语言 C++、C# 上都有类似的技术，只不过名称不同而已，例如 C++ 上叫模版。在这些技术的加持下，程序员可以编写与具体类型无关的代码，只需要在使用时指定具体类型，从而提高代码的复用性；并且在编译时进行类型检查，减少运行时错误。

Java 的泛型是通过类型擦除（Type Erasure）来实现的。也就是说在编译时将泛型类型擦除，替换为其上限类型（通常为 `Object`），并在必要时插入类型转换。这种机制在编译时处理泛型类型，而在运行时移除了所有的泛型信息，因此叫做类型擦除。

这也就意味着，Java 的泛型是由编译器实现的，在编译成 class 文件时类型信息已经被擦除了，因此运行时，Java 虚拟机是没有任何泛型信息的。

例如上面我们编写的 `Pair` 的这个类，在我们看来，它是这样的，在源代码阶段，里面是包含泛型信息的：

```java
public static class Pair<F, S> {
    public final F first;
    public final S second;

    public Pair(F first, S second) {
        this.first = first;
        this.second = second;
    }

    public static <A, B> Pair<A, B> create(A a, B b) {
        return new Pair<A, B>(a, b);
    }
}
```

那么在虚拟机的视角，它是这样的：

```java
public class Pair {
    private Object first;
    private Object last;
    public Pair(Object first, Object last) {
        this.first = first;
        this.last = last;
    }
}
```

从这里就能看到，这个 `Pair` 在运行时已经没有泛型信息了，所有的泛型类型都被替换为了 `Object`。

那么既然我们定义的泛型类型最终都变成了 `Object`，那我们就知道了 Java 泛型的一个局限：泛型类型 `<T>` 不能是基本类型。 因为像 `int`、`float` 这些基本类型不是 `Object` 的子类，所以我们必须使用包装类：

```java
Pair<float, int> pair = Pair.create(3.15, 123);    //编译错误
Pair<Float, Integer> pair = Pair.create(3.15F, 123);    //编译通过
```

尽管 Java 的泛型在编译时通过类型擦除机制移除了泛型类型信息，但 Java 编译器会在 `class` 文件中保留一些泛型信息，以便工具和开发人员能够利用这些信息进行反射和调试。所以如果大家把这个类编译为 `class` 文件之后，再查看它的反编译的内容，会发现它是有一些泛型信息的。但这并不意味着 JVM 在运行时会携带这些类型信息，既然是类型擦除，也就是说泛型类型参数被擦除并替换为其边界类型，如果没有指定边界，则默认为 `Object`。

这里又引入了边界类型这个概念，下面我们就来详细聊聊这个边界类型，这也是泛型中比较重要和难的点。

## extends 通配符，确定上界

在 Java 中，可以通过使用边界类型来限制泛型参数的类型范围。边界类型分为上界（upper bounds）和下界（lower bounds）。上界类型限制了泛型类型参数必须是某个特定类型的子类型，通常用 `<T extends SomeType>` 来表示。

前面我们写了一个很有用的函数，用于打印任意类型的数组，现在我们把它改造一下，用于打印上面的 `Pair` 类：

```java
public void printPair(Pair<Number, Number> pair) {
    System.out.println(pair);
    System.out.println("\tfirst = "+pair.first);
    System.out.println("\tsecond = "+pair.second);
}
```

这个方法能够正常编译，其接收的参数是 `Pair<Number, Number>`，既然是能够接受数字类型的，那我们给它传入一个 `Pair<Integer, Integer>` 试试：

```java
Pair<Integer, Integer> intPair = Pair.create(111, 222);
printPair(intPair);        //编译报错
```

原因很明显，`Pair<Integer, Integer>` 并不是 `Pair<Number, Number>` 的子类，因此 `printPair` 方法不接受 `Pair<Integer, Integer>` 类型的参数。但事实上这个这个参数是可以传递给 `printPair` 方法的，方法的内部代码也不会有任何问题，只是参数限制死了只能传入 `Pair<Number, Number>`。

那有没有方法能够限制接受的参数为 `Pair` 的泛型为 `Number` 的子类呢？这就是 `<? extends Number>`：

```java
public void printPair(Pair<? extends Number, ? extends Number> pair) {
    System.out.println(pair);
    System.out.println("\tfirst = "+pair.first);
    System.out.println("\tsecond = "+pair.second);
}
```

在看一下之前的报错，消失了，代码正常运行。因为 `Pair<Integer, Integer>` 类型是符合 `Pair<? extends Number, ? extends Number>` 限制的，这种使用 `<? extends Number>` 的泛型定义称之为上界通配符（Upper Bounds Wildcards），即把泛型类型 T 的上界限定在 `Number` 了。

在这种上界限制下，传入的参数 `pair` 的 `first` 和 `second` 都被限制在了 `Number` 和其子类，但具体是什么类型，是不能确定的。

现在我们掌握了 `<T extends SomeType>` 作为函数参数的第一种作用：用于限定传入的参数的类型。但 `<T extends SomeType>` 作为函数参数还有另外一个作用，标识方法内部不会对参数进行参数设置。这一点有点不好理解，我们来看下面的例子：

```java
public class Pair<F, S> {
    public F first;
    public S second;

    public Pair(F first, S second) {
        this.first = first;
        this.second = second;
    }

    public void setFirst(F first) {
        this.first = first;
    }

    public void setSecond(S second) {
        this.second = second;
    }
}
```

我们在 `Pair` 对象中加入了 `set` 方法，然后我们再添加一个 `modify` 方法，这个方法只是修改传入的 `pair` 的内容：

```java
public void modifyPair(Pair<? extends Number, ? extends Number> pair) {
    System.out.println(pair);
    pair.setFirst(new Integer(100));    //编译错误
}
```

在这个方法中，当我们调用设置参数 `pair` 的 `first` 参数会发生编译错误。那么参数中的 `pair` 是 `Pair<? extends Number, ? extends Number>` 类型的，也就是 `first` 就是个 `<? extends Number>` 类型的，我给它设置个 `Integer` 应该是合理的啊，为什么会编译错误呢？

原因还是在 Java 泛型的实现方式：类型擦除。在这里我们这么理解，`modifyPair` 方法接受的 `pair` 参数只要求 `pair` 的泛型类型继承于 `Number` 类，也就是说我可以传入 `Pair<Integer, Integer>` 也可以传入 `Pair<Float, Float>`，其具体类型是不知道的，那你在方法中设置 `first` 为 `Integer`，是不是就不太对了。

如果传入的参数是 `Pair<Integer, Integer>` 那还好说，如果传入的是 `Pair<Float, Float>`，你设置一个 `Integer` 肯定是有问题的。

于是这里就是 `<T extends SomeType>` 在作为方法的参数的另一个作用了，简单说来，就是说明这个方法对参数只能进行读的操作，而不不能进行写的操作。

但是这里有一个例外，那就是你可以设置 `null` 值，但这种情况也是很少见，基本就属于恶意操作了。我想着也没有人会那么无聊，所以这里就不赘述了。

下面我们举一个例子：

```java
int sumOfList(List<? extends Integer> list) {
    int sum = 0;
    for (int i=0; i<list.size(); i++) {
        Integer n = list.get(i);
        sum = sum + n;
    }
    return sum;
}
```

这个方法用来计算 `Integer` 列表中所有元素的和，在这个代码作用使用了 `<? extends Integer>` 而不是是直接使用 `Integer`，这就表示了在这个方法中对参数 `list` 只进行读操作，而不进行写操作。如果只使用了 `Integer`，那么在方法内部就可以对 `list` 进行写入的操作了。

总结一下，`<? extends SomeType>` 这种泛型限定用在方法的参数上有两个作用： 1. 标识传入参数的泛型上限 2. 标识方法中只对参数进行读操作，而没有写操作

`extends` 通配符不仅可以用在方法的参数上，也可以用在类的定义上，用于标识泛型参数的上限。

例如上面我们定义的 `Pair<F, S>`，其实我们也可以做如下定义：

```java
public static class Pair<F extends Number, S extends Number> {
    //......
}
```

在这里，泛型参数 `F` 和 `S` 被限制为 `Number` 及其子类。

![](images/233_003.jpg)

  

## super 通配符，确定下界

上面说到边界类型分为上界（upper bounds）和下界（lower bounds）。上界类型限制了泛型类型参数必须是某个特定类型的子类型，通常用 `<T extends SomeType>` 来表示。那么下界自然就是限制了泛型类型参数必须是某个特定类型的超类型，通常用 `<? super SomeType>` 来表示。

我们先回到上一节中的 `modifyPair` 方法：

```java
public void modifyPair(Pair<? extends Number, ? extends Number> pair) {
    System.out.println(pair);
    pair.setFirst(new Integer(100));
}
```

我们已经明白了由于使用了 `extends` 类型限制，在这个方法中为 `pair` 设置值值错误的行为。那怎么样能够为 `pair` 设置新的值呢？

先这么想，我们要设置进去的是一个 `Integer` 对象，那么哪种类型的变量能够接受这个 `Integer` 类型呢？显然，只要是 `Integer` 的父类的变量都是能够接收 `Integer` 类型的。那我们如何表示 `Integer` 的父类呢？那就是 `<T extends SomeType>` 泛型限定了。

现在我们修改一下代码：

```java
public void modifyPair(Pair<? super Integer, ? super Integer> pair) {
    System.out.println(pair);
    pair.setFirst(Integer.valueOf(100));
    pair.setSecond(Integer.valueOf(200));
}
```

这时候编译器不报错了，这段代码可以正常编译。因为参数 `pair` 的 `first`、`second` 都被限制为了 `Integer` 或其父类，这个类型的变量显然是可以接收 `Integer` 对象的，因此代码可以通过编译。

这是 `super` 通配符的第一个作用。那有人就问了，参照 `extends`，这个 `super` 通配符是不是只能写，不能读了？

答案是对的，但是不完全对，听我一一道来。

首先，`<T super SomeType>` 通配符是允许写入的，这个上面说的，但是作为读来说，你就首先考虑用什么类型的变量来接收，在使用 `super` 通配符后，你只能用 `Object` 类型来接收，无法使用其他类型接收，这也是我为什么说答案是对的，但也不完全对。如果你再想一下，你接收到的对象你无法知道其具体的类型的，也只能用 `Object` 来接收，但是用 `Object` 类型能做的事情实在太少了。因此咱们就认为其不可读好了。

那现在咱们总结一下 `<T super SomeType>`： 1. 标识传入参数的泛型类型的下界 2. 标识方法内可以对参数进行写，而不能读

再明白了这两个通配符后，我们再把 `extends` 和 `super` 放到一起做一下比较： - `<T extends SomeType>` 标识上界，可读不可写 - `<T super SomeType>` 标识下界，可写不可读

那结合这两个统配符号我们来看一下 `Collections` 类中的 `copy()` 方法的定义：

```java
//将 src 列表中的元素复制到 dest 中
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    //......
}
```

这个方法体咱们不关注，咱们就关注参数。`src` 是 `List<? extends T>` 的类型，列表中的元素是 `T` 或其子类，由于是 `extends` 限定，因此方法中可以读 `src` 列表；`dest` 是 `List<? super T>` 类型，列表中的元素是 `T` 或其父类，由于是 `super` 限定，因此方法中只能写不能读。这完美地展示了这两个限定符的用途。

## <?> 无限定通配符

上面我们讨论了 `<? extends T>` 和 `<? super T>` 作为方法参数的作用。实际上，Java 的泛型还允许使用无限定通配符（Unbounded Wildcard Type），即只定义一个 `<?>`。看下面这个方法：

```java
public static boolean isNull(Pair<?, ?> pair) {
    return pair.first == null && pair.second == null;
}
```

这个方法中使用了 `Pair<?, ?>`，那这个无限定通配符有啥用呢？结合上面的 `extends` 和 `super`，这个 `<?>` 总结一下就是：既不能读也不能写。

这玩意集 `extends` 和 `super` 的限制于一身，既不能读也不能写，那能做的事情就很少了，基本只能做一些 `null` 判断，如上面的方法一样。也正是因为能做的事情不多，所以我们见得比较少。要说 `<?>` 的好处，也就是我们不用特意声明泛型参数了吧。

大多数情况下，可以使用泛型参数 `<T>` 消除 `<?>` 统配符：

```java
public static <T> boolean isNull(Pair<T, T> pair) {
    return pair.first == null && pair.second == null;
}
```

`<?>` 通配符有一个独特的特点，那就是 `Pair<?>` 是所有 `Pair<T>` 的超类：

```java
Pair<String, Integer> pair = Pair.create("aaa", 123);
Pair<?, ?> p = pair;            //编译通过
```

上面由于 `Pair<?, ?>` 是 `Pair<String, Integer>` 的超类，因此可以直接将 `pair` 转换为 `Pair<?, ?>`。

简单总结：无限定通配符 `<?>` 很少使用，可以用 `<T>` 替换，同时它是所有 `<T>` 类型的超类。

![](images/233_004.jpg)

  

## 泛型与反射

在说明泛型的反射之前，我们先要知道泛型中有个关于反射的局限：那就是无法从泛型类的对象的 `Class` 信息中获取到泛型信息。例如下面的代码，从 `intPair` 和 `strPair` 获取到的 `Class` 都是同一个 `Pair.class`，我们无法从这个 `Class` 中获取到有关这两个对象的泛型信息。

```java
Pair<Integer, Integer> intPair = Pair.create(111, 222);
Pair<String, String> strPair = Pair.create("aaa", "bbb");
Class intPairClass = intPair.getClass();
Class strPairClass = strPair.getClass();
System.out.println("是否是相同的 Class 对象：" + (intPairClass == strPairClass));    // true
```

在代码中虽然 `Pair` 的参数类型不一样，但是在虚拟机那里，都是 `Object`，因此对于代码中两个不同类型的 `Pair` 获取 `Class` 时，获取到的是同一个 `Class`，也就是 `Pair` 的 `Class`。通过这个 `Class`，是无法反射拿到泛型信息的。

那么在泛型时，我们可以做哪些反射操作呢？其实跟我们正常使用泛型一样，我们能够拿到在编译时已经确定好的代码结构的各种信息。这里我们用一段代码来做示例：

```java
public static class Pair<F, S> implements Comparable<F> {
    public F first;
    public S second;

    public Pair(F first, S second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public int compareTo(F o) {
        return this.first.hashCode() - o.hashCode();
    }

    public static <A, B> Pair<A, B> create(A a, B b) {
        return new Pair<>(a, b);
    }
}

public static class Example<T> {
    private Pair<String, Integer> pair1;
    private Pair<? extends Number, ? super Integer> pair2;
    private T[] array;
}
```

这两个类包含了很多泛型参数，那现在，咱们就看看如何通过反射来拿到这里面的与泛型有关的信息。

首先我们可以通过下面的代码获取 `Pair` 的泛型参数类型：

```java
Class<Pair> pairClass = Pair.class;
System.out.println("pairClass = "+pairClass);
TypeVariable<?>[] typeParameters = pairClass.getTypeParameters();
// 输出泛型参数信息
for (TypeVariable<?> typeParameter : typeParameters) {
    System.out.println("Generic parameter: " + typeParameter.getName());
}
```

输出，就可以看我们定义的 `F` 和 `S` 这两个泛型参数

```text
System.out                  I  Generic parameter: F
System.out                  I  Generic parameter: S
```

我们还可以通过这两个泛型参数去看它们的上界：

```java
// 输出泛型参数信息
for (TypeVariable<?> typeParameter : typeParameters) {
    System.out.println("Generic parameter: " + typeParameter.getName());

    // 输出泛型参数的上界
    for (Type bound : typeParameter.getBounds()) {
        System.out.println("  Bound: " + bound.getTypeName());       //输出 Object
    }
}
```

接下来我们再看成员变量的泛型：

```java
Field[] fields = pairClass.getDeclaredFields();
for(Field field : fields) {
    System.out.println("成员变量: " + field);
}
```

输出：

```text
System.out                  I  成员变量: public java.lang.Object lic.swift.demo.java.Pair.first
System.out                  I  成员变量: public java.lang.Object lic.swift.demo.java.Pair.second
```

可以看到，反射得到的，这两个成员变量都已经变成 `Object` 类型了。

那如果我想拿到泛型类型呢？可以通过 `field.getGenericType()` 方法获取：

```java
Field[] fields = pairClass.getDeclaredFields();
for(Field field : fields) {

    System.out.println("成员变量: " + field);
    System.out.println("\t泛型类型："+field.getGenericType());    //返回 F 和 S
}
```

这里我直接把反射的代码，贴出来，这段代码通过反射拿到了泛型中的所有信息：

```java
Class<?> pairClass = Pair.class;
System.out.println("Pair 类的 Class 对象：" + pairClass);
TypeVariable<?>[] typeParameters = pairClass.getTypeParameters();
// 输出泛型参数信息
for (TypeVariable<?> typeParameter : typeParameters) {
    System.out.println("Pair 类的泛型类型: " + typeParameter.getName());

    // 输出泛型参数的上界
    for (Type bound : typeParameter.getBounds()) {
        System.out.println("\t此泛型上界: " + bound.getTypeName());
    }
}

Field[] fields = pairClass.getDeclaredFields();
for (Field field : fields) {
    System.out.println("成员变量: " + field);
    System.out.println("\t泛型类型：" + field.getGenericType());
}

Constructor<?>[] constructors = pairClass.getDeclaredConstructors();
for (Constructor<?> constructor : constructors) {
    System.out.println("构造函数: " + constructor);
    Parameter[] parameters = constructor.getParameters();
    for (Parameter parameter : parameters) {
        System.out.println("\t此构造方法的参数：" + parameter + ", 参数的泛型类型：" + parameter.getParameterizedType());
    }
}

Method[] methods = pairClass.getDeclaredMethods();
for (Method method : methods) {
    if (Modifier.isStatic(method.getModifiers())) {
        System.out.println("静态方法：" + method);
    } else {
        System.out.println("成员方法：" + method);
    }
    Parameter[] parameters = method.getParameters();
    for (Parameter parameter : parameters) {
        System.out.println("\t此方法的参数：" + parameter + ", 参数的泛型类型：" + parameter.getParameterizedType());
    }
}

Type[] types = pairClass.getGenericInterfaces();
for (Type type : types) {
    System.out.println("此类实现的接口：" + type);
}

Class<?> exampleClass = Example.class;
System.out.println("Example 类的 Class 对象：" + exampleClass);

Field[] exampleFields = exampleClass.getDeclaredFields();
for (Field field : exampleFields) {
    System.out.println("Example 成员变量：" + field.getName());
    System.out.println("\t此变量类型：" + field.getGenericType());
}
```

这里注意代码中的输出，打印了 `Pair` 和 `Example` 这两个类的泛型相关信息。

关于反射的更多内容，大家可以看这篇文章，写得更详细一些：

[李斯维：Java Reflection 反射使用 完全指南](https://zhuanlan.zhihu.com/p/704275903)

## 总结

好了，这里关于 Java 泛型中的所有信息基本都已经说完了。我们知道为什么需要泛型，怎么用泛型，泛型中的三个通配符，相信通过这篇文章，诸位能对 Java 的泛型有一个更深的认识。

最后，祝各位衣食无忧，一夜暴富。

![](images/233_005.jpg)