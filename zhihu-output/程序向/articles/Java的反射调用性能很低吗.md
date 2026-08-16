---
id: "55075493"
title: "Java的反射调用性能很低吗?"
author: "dwing"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/55075493"
created: "2019-01-17 11:45"
updated: "2019-09-24 17:58"
collected: "2019-01-17 11:45"
downloaded: "2026-08-16"
---
使用静态语言做开发时,方法/函数通常是直接调用的,而不常用反射调用. 因为前者能被编译器检查出各种不符合调用规则的问题,且运行时直接调用的开销最小.

但有时即使做很多抽象,也不太方便某些灵活的调用需求,或者很难设计出易写易扩展的方法接口. 这时通过反射就获得了很大的灵活性, 当然是否真的需要反射要有很好的权衡,而不能滥用.

  

然而一提起反射调用, 很多人马上会意识到比普通调用增加了很多开销, 尤其是调用的方法本身开销很小的情况下, 反射调用的性能恐怕要低好几倍, 甚至一个数量级.

事实真的如此么, 估计不少牛人心里都会想到反射调用的流程会带来多少参数验证和间接步骤,本能地留下了很差的印象.

网上这样的评测文章不多,尤其是很多文章的测试环境已经过时,而且测试用例不佳(如果简单的直接调用被内联甚至还被循环展开,就跟反射调用的需求无法相提并论了). 今天我就来亲自做个最新的测试,看看反射调用的性能是否真的像传说中那么不堪, 如果是则分析一下原因在哪.

  

测试系统: Win10 64-bit; Intel I5-4430 (3GHz)

Java版本: OpenJDK 11.0.1 (64-bit)

测试程序如下:

```java
import java.lang.reflect.Method;

public class Bench1 {
    long v;

    public void func0() { v++; }
    public void func1() { v--; }
    public void func2() { v++; }
    public void func3() { v--; }

    public void testInterface() {
        long t = System.nanoTime();
        Runnable[] rs = {
            this::func0,
            this::func1,
            this::func2,
            this::func3,
        };
        for(int i = 0; i < 1_0000_0000; i++)
            rs[i & 3].run(); // 关键调用
        t = (System.nanoTime() - t) / 1_000_000;
        System.out.format("testInterface: %d %dms\n", v, t);
    }

    public void testReflect() throws Exception {
        long t = System.nanoTime();
        Method[] ms = {
            Bench1.class.getMethod("func0"),
            Bench1.class.getMethod("func1"),
            Bench1.class.getMethod("func2"),
            Bench1.class.getMethod("func3"),
        };
        for(int i = 0; i < 1_0000_0000; i++)
            ms[i & 3].invoke(this); // 关键调用
        t = (System.nanoTime() - t) / 1_000_000;
        System.out.format("testReflect  : %d %dms\n", v, t);
    }

    public static void main(String[] args) throws Exception {
        Bench1 b;
        b = new Bench1(); // 预热部分
        b.testInterface();
        b = new Bench1();
        b.testReflect();

        b = new Bench1(); // 实测部分
        b.testInterface();
        b = new Bench1();
        b.testReflect();
    }
}
```

先解释一下这里为什么要用接口调用对比反射调用.

因为反射调用通常的需求是比较动态地调用方法, 这跟接口调用的动态分派比较接近, 而不是直接调用方法.

还因为单个接口调用容易被JIT优化成内联的, 且单个接口的频繁调用也不太符合现实中的需求, 因此这里给出4个方法轮流调用.

然后为了避免JIT预热影响, 只看后面实测的部分的结果, 并运行5次取最小时间的结果, 如下:

> testInterface: 0 595ms  
> testReflect : 0 809ms

可见反射调用只比接近相同需求的直接调用慢了36%, 这个结果估计超过大多数人的意料了吧.

但先不要高兴, 也许还有改进空间, 我们来看看GC日志, 发现这个测试程序出现了25次GC,共回收了3G左右的内存,GC总时间25.8毫秒.

而且只测试接口调用发现并没有触发GC, 说明反射调用是有临时内存分配的, 从Method.invoke方法就能看到我们总是要传变长参数给它.

而Java的变长参数其实是数组的语法糖, 也就是每次调用invoke都要临时创建数组, 哪怕数组长度为空.

这个测试程序正好因为没有实际方法的参数而传了空数组, 因此我们尝试自己只构造一次空数组,并传给invoke, 改动如下:

```java
        Object[] EMPTY = new Object[0];
        for(int i = 0; i < 1_0000_0000; i++)
            ms[i & 3].invoke(this, EMPTY);
```

测试结果:

> testReflect : 0 705ms

这次只慢了18.5%,而且没有触发GC! 这还是在调用的方法内容极少情况下的差距, 调用的方法越复杂,那么这个差距就越小, 可见我们真要打破反射调用性能低的印象了.

当然最好是自己构造可手动回收利用的参数数组, 这样就几乎没有反射调用的内存分配开销了.

  

有兴趣的人会问为什么反射的开销这么小, 其实翻一下JDK的源码就很清楚了, 我只简单说下关键的部分:

1\. Method的invoke调用在JDK内部是通过MethodAccessor来调用的,而这个接口有一些不同的实现;

2\. 如果某个Method的invoke调用次数较多, 会通过MethodAccessorGenerator的generate方法为Method的目标方法动态字节码生成一个MethodAccessor的实现类, 针对该Method的特征做了代码级的优化,用最少的字节码实现特殊的间接调用;

3\. 这个实现类再通过JIT的编译优化, 就能使Method的invoke性能达到最大化.

更多相关的技术分析,可以看R大的这篇文章: [https://rednaxelafx.iteye.com/blog/548536](https://link.zhihu.com/?target=https%3A//rednaxelafx.iteye.com/blog/548536)

* * *

**补充:**

最近看JDK11中ConcurrentLinkedQueue的高性能原理时发现了MethodHandles的应用, 这在JDK8中是用Unsafe类实现的, 既然现在不用Unsafe了, 说明MethodHandles有类似Unsafe的高性能.

仔细一看, 这个类确实有很多类似反射的方法, 其中有一个"public MethodHandle unreflect(Method m)"非常惹眼. 难道还能"反反射"?

于是把testReflect方法稍改了一下:

```java
    public void testReflect() throws Throwable {
        long t = System.nanoTime();
        Lookup lookup = MethodHandles.lookup();
        MethodHandle[] ms = {
            lookup.unreflect(Bench1.class.getMethod("func0")),
            lookup.unreflect(Bench1.class.getMethod("func1")),
            lookup.unreflect(Bench1.class.getMethod("func2")),
            lookup.unreflect(Bench1.class.getMethod("func3")),
        };
        for(int i = 0; i < 1_0000_0000; i++)
            ms[i & 3].invoke(this);
        t = (System.nanoTime() - t) / 1_000_000;
        System.out.format("testReflect  : %d %dms\n", v, t);
    }
```

测试结果:

> testReflect : 0 528ms

这是实实在在可以用"震惊"来形容了, **反反射竟然比接口调用还快**! 而且没有GC,即使invoke方法是不定长的参数. 看来只能用JVM做了黑魔法般的intrinsic优化来解释了.

这个反反射跟反射相比几乎没有任何代价, 也就是说任何反射调用都可以这么改进而得到明显的性能提升.

PS: 当然接口调用的性能也可以提出怀疑, 见 [如何解释这一小段Java程序的性能问题?](https://www.zhihu.com/question/302934953)