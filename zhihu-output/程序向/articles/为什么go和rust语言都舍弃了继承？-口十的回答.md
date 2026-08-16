---
id: "3326820761"
title: "为什么go和rust语言都舍弃了继承？"
author: "口十"
type: zhihu-answer
source: "https://www.zhihu.com/question/511958588/answer/3326820761"
created: "2023-12-15 16:22"
updated: "2026-06-11 11:47"
collected: "2023-12-15 16:22"
downloaded: "2026-08-16"
---
数据和行为的组合方式是不一样的。类之所以是糟糕的设计，很大程度上是因为它将数据和行为绑在一起。

行为，即方法，是可以先声明后实现的，这就是为什么方法存在「覆写」一说。方法的实现由 *virtual method table* 动态获取，而使用处仅需按照声明调用即可，这一点给予方法极高的抽象能力。为了更好地组织对象的行为，我们发明了 interface/trait/protocol 等概念来囊括针对同一目的的仅存在声明的方法，多亏动态委派，我们可以基于覆写实现「接口继承」，如下所示：

```text
trait Iterator {
    alias Item

    fun next(this) -> Option[This.Item] # 声明
}

class HListIter[T] { ... }

actor [T] for HListIter[T] as Iterator {
    alias Item = T

    fun next(this) -> Option[This.Item] { # 实现
        ...
    }
}

val hlist = @hlist(0, 1)
mut val iter = hlist.iterate() as anony Iterator
val _ = iter.next() // 尽管 iter 的类型是 Iterator，但这里会调用 HListIter 中的实现
```

当类型继承自两个包含相同方法的接口时，我们只需强制类型覆写该方法即可，此时即使接口中有默认实现也无所谓，因为 virtual method table 会使用覆写后的实现。

但数据，即字段，就没有这么幸运了。字段声明即存在，它是不能被覆写的。类继承表示子类会继承父类的字段，而这就是类继承出现问题的时候，如下所示：

```text
class A {
    int i = 0;

    void f() {}
}

class B extends A {}

class C extends A {}

class D extends B, C {}
```

那么问题来了，`D`中的`i`是`B`中的`i`还是`C`中的`i`？

那为什么不能「覆写」字段呢？我们可以试试在`B`中加上`i`：

```text
class A {
    int i = 0;

    void f() {}
}

class B extends A {
    int i = 0;
}
```

事实上，在许多语言中，这两个`i`并不构成「覆写（override）」，而是「覆盖（shadow）」，也就是说，`A.i`依然存在，我们可以通过类似`super.i`的方式获取。

可是方法也可以通过`super.f()`的方式调用啊？

对，这就是最关键的问题，**`A`中的方法并不会影响`B.i`**，因为`B.i`是完全独立于`A.i`的，这就与`super.f()`不一样了，**`A`中的其他方法如果调用了`f`而`f`被`B`覆写，那么它一定会使用`B`中的实现**，这就是「覆写」与「覆盖」的区别。

这个问题有什么影响吗？

不能覆写字段，意味着**子类的字段不会比父类的字段少，即使子类覆写后的行为不会用到所有字段**，这是什么意思？举个例子，正方形是长方形，对吧？那么下面的代码就是合理的：

```text
class Rectangle {
    int width;
    int height;

    Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    int area() {
        return this.width * this.height;
    }
}

class Square extends Rectangle {
    Square(int width) {
        super(width, width);
    }

    @Override
    int area() {
        return this.width * this.width;
    }
}
```

真的合理吗？

`Rectangle.height`在`Square`里似乎完全没有意义，因为正方形只需要一条边长就足够了，那为什么我们说「正方形是长方形」？其实这句话的意思是正方形拥有长方形的行为，但请注意，这并不代表正方形需要长方形的数据，也就是说，**正方形继承长方形的行为，但并不继承长方形的数据**。

所以，更合理的体系是：

```text
trait RectangleLike {
    fun width(this) -> I32

    fun height(this) -> I32

    fun area(this) -> I32 {
        this.width() * this.height()
    }
}

class Rectangle {
    width: I32,
    height: I32,
}

actor for Rectangle as RectangleLike {
    fun width(this) -> I32 {
        this.width
    }

    fun height(this) -> I32 {
        this.height
    }
}

class Square {
    width: I32,
}

actor for Square as RectangleLike {
    fun width(this) -> I32 {
        this.width
    }

    fun height(this) -> I32 {
        this.width
    }
}
```

所以，数据和行为并不是共轭的，继承一方并不代表继承另一方，它们需要分开讨论。这就是为什么 structure/interface 设计更合理。

行为可以通过接口继承的方式组合，那数据需要怎么组合呢？比如说，我就是想要`Square`包含`Rectangle`的数据，structure 能 handle 这个需求吗？

很简单，既然你想要`Rectangle`的数据，那我就包含`Rectangle`呗：

```text
class Square {
    rectangle: Rectangle,
}
```

这就是组合的完全体，`Rectangle`和`Square`都是`RectangleLike`，但它们的实现不一样，通过`Square`的包装，同一份`Rectangle`数据就能表现出不同的行为。

我们甚至可以写出更灵活的实现：

```text
class Square[R]
    where R: RectangleLike
{
    inner: R,
}
```

既然是 *像长方形*，`RectangleLike`，那我们是不是可以认为，宽和高相等的像长方形的图形就是正方形呢？

不过，仅有组合可能 *写* 起来有点累，我们还需要委托，把不是`Square`独特的行为委托给`inner`：

```text
actor [R] for Square[R] as RectangleLike by this.inner
    where R: RectangleLike
{ # 提供一致的行为
    fun height(this) -> I32 {
        this.inner.width()
    }
}
```

这样，我们就不需要把所有要求实现的方法都抄一遍了。

类继承的其他诸如父子耦合的问题就不提了。总之，基于 class 的 OOP 设计确实不够好。（那些 class 单线继承要靠 interface 救场的就能说明类继承有多尴尬）

* * *

对了，我想反驳一下说 structure/interface 看起来乱糟糟的：

```text
class Rectangle {
    // Fields
    int width;
    int height;

    // Constructors
    Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    // Static functions
    static Rectangle unit() {
        return new Rectangle(1, 1);
    }

    // Instance functions
    int area() {
        return this.width * this.height;
    }
}
```

  

```text
# Fields + Intrinsic Constructor
class Rectangle {
    width: I32,
    height: I32,
}

# Static functions
actor for Rectangle {
    fun new(width: I32, height: I32) -> Rectangle {
        Rectangle(width, height)
    }

    fun unit() -> Rectangle {
        Rectangle.new(1, 1)
    }
}

# Instance functions
actor for Rectangle {
    fun area(this) -> I32 {
        this.width * this.height
    }
}
```

要说乱，我觉得把什么东西都堆到一个大括号里才叫乱罢。