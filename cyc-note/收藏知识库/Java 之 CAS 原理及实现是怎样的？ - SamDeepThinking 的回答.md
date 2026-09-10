---
Title: "Java 之 CAS 原理及实现是怎样的？ - SamDeepThinking 的回答"
Url: "https://www.zhihu.com/question/485099364/answer/2081393914901173093"
Author: "SamDeepThinking​​软件开发行业 研发高级经理​ 关注"
Origin: "知乎回答"
Description: "来我这边面试的Java程序员呢，我必定会问的其中一个问题是如下这个，我们现场回放一下。我问：一段代码被…"
Tags:
  - "职场"
  - "Java"
  - "Java 编程"
  - "并发"
Created: "2026-09-10 15:05:31"
Cover: "https://pica.zhimg.com/v2-d4037a975c6be26e723acb795fafc273_l.jpg?source=2c26e567"
---

[收录于 · 随笔](https://www.zhihu.com/column/c_1992153637800150476)

1 人赞同了该回答

来我这边面试的Java程序员呢，我必定会问的其中一个问题是如下这个，我们现场回放一下。

我问：一段代码被synchronized括住后，两个线程A和B，同时想进入这个代码块，假设线程A拿到锁了，进入代码块。那拿不到锁的线程B会被怎么处理?

应聘者：被操作系统挂起

我又问：一定要被挂起吗? 如果挂起后，而之前进入代码块的线程A执行的很快，马上释放锁了。那操作系统还得把线程B重新调度回来，得不偿失哦

应聘者：那可以先空跑，自旋一下。

我继续问：那万一线程A执行很久了呢? 线程B就一直在那自旋?

应聘者：这个。。。。。。。

这个问题呢，表面是考察synchronized，其实我最终想问的是CAS。关于CAS呢，不太容易理解，下面我们尝试使用通俗易懂的方式来讲解一下。 争取做到： （1）帮助读者理解一些令人困惑的话题。 （2）带有清晰可理解的代码或例子。 （3）让事情变得更简单。

好，我们现在开始。

### 先说说直接挂起的代价

线程从运行状态切换到挂起状态，涉及CPU寄存器保存和恢复、CPU流水线清空等操作。这个上下文切换的开销在微秒级别。

如果持有锁的线程执行的临界区很短，比如给一个变量加1，几十纳秒就完成了，这时候把竞争线程挂起，等锁释放后再唤醒，两次上下文切换加起来花了几微秒，比等锁本身的时间长得多。

以前的JVM版本，是会挂起的，后面做了改进，JVM不会在第一次拿不到锁时就直接挂起线程。

### 再说空转问题

就是让线程在CPU上跑，空的循环，也就是自旋。线程不离开CPU，反复尝试拿锁。如果持锁线程很快就释放了锁，自旋几十次CPU循环就拿到了，省掉了一次上下文切换。

问题在于，如果持锁线程执行很久，自旋就变成了白白在烧CPU了。

JVM的策略是先尝试自旋，实在拿不到再挂起。但自旋需要一个前提：得有一种很低成本的方式去反复尝试拿锁。如果每次尝试都要进内核态走系统调用，那自旋本身性价比并不高的。

### 来了，有无低成本获取锁的方式?

这个低成本的抢锁机制是CAS。CAS的全称是Compare-And-Swap，是CPU提供的一条原子指令。它做的事情是：读取内存中某个位置的值，和预期值比较，如果相等，就把新值写进去。整个过程不会被其他线程打断。

我们用一段Java 17代码来演示CAS的行为：

```java
AtomicInteger lock = new AtomicInteger(0);
// 期望值是0（没人持有），想改成1（我来持有）
boolean first = lock.compareAndSet(0, 1);
// 再来一次，当前值已经是1，期望0不匹配，失败
boolean second = lock.compareAndSet(0, 1);
```

在Windows 11上运行的结果如下：

```
first CAS: true
second CAS: false
current value: 1
```

第一次CAS成功了，因为当前值确实是0，和预期匹配。第二次失败，因为值已经被改成了1，不再等于预期的0。

JVM里synchronized的加锁就用了类似的思路。完整源代码如下：

```java
import java.util.concurrent.atomic.AtomicInteger;

public class CasDemo {
    public static void main(String[] args) {
        AtomicInteger lock = new AtomicInteger(0);
        boolean first = lock.compareAndSet(0, 1);
        boolean second = lock.compareAndSet(0, 1);
        System.out.println("first CAS: " + first);
        System.out.println("second CAS: " + second);
        System.out.println("current value: " + lock.get());
    }
}
```

### 那CAS这种轻量级锁的工作方式是怎么样的呢?

流程大概是这样的：

synchronized(obj)这种写法，括号里的obj就是锁对象(目标对象)，线程加锁时读取的就是这个obj的Mark Word。Mark Word是对象头的一部分，里面存了对象的状态信息。如果Mark Word处于无锁状态（最低两位是 `01`），线程就用CAS把Mark Word替换成指向自己栈上BasicLock的指针。CAS成功后，Mark Word的最低两位变成 `00`，表示轻量级锁已持有。

CAS失败说明已经有其他线程持有这把锁。在JIT编译的代码里，这个CAS操作会被包在一个短暂的重试循环里，连续尝试几次。这就是轻量级锁层面的自旋。重试多少次没有固定值，由编译器和CPU架构决定。

轻量级锁的好处是整个过程在「用户态」完成，不需要进入「内核态」，不需要操作系统参与。如果锁很快释放，几次CPU循环就能拿到，比上下文切换快得多。

但如果持锁线程迟迟不释放，轻量级锁的CAS重试也会耗尽。这时候JVM就需要升级策略。

### 自旋失败后的膨胀

轻量级锁自旋失败后，JVM会创建一个ObjectMonitor对象，把锁从轻量级膨胀为重量级。把刚才上面提到的那个obj的Mark Word再改一下：锁标记从 `00` 变成 `10`，原来存的是指向栈上BasicLock的指针，现在换成ObjectMonitor的指针。

线程B进入ObjectMonitor后，并不是马上就挂起，ObjectMonitor会让它再自旋一段时间。为什么不直接挂起呢? 挂起的代价高，能晚一点挂起就晚一点，这个原则到这里还在用。不过这次的自旋和轻量级锁层面的自旋不太一样，它的自旋时长是 **自适应的**。

每个ObjectMonitor内部维护一个自旋计数器，控制自旋的持续时间。每次自旋成功拿到锁，这个字段对应的值会增加；自旋失败，会减少。JVM通过历史成功率来调整下次的自旋时长，成功率高的锁就多转几圈，成功率低的就少转甚至直接跳过自旋。

自旋最终还是拿不到锁，才会被挂起，进入ObjectMonitor的等待队列，让出CPU给其他线程用。

整个过程分三步：

**快速路径**：CAS尝试抢锁，不进入内核态，成本最低。失败后膨胀为重量级锁。

**ObjectMonitor内自旋**：自适应调整自旋时长，检查持锁线程是否可执行。成本中等。

**挂起阻塞**：线程挂起，让出CPU。成本最高，涉及上下文切换。

每一步的成本是递增的，JVM只在低成本的步骤不管用时才升级到下一步。

### Java 17简化了锁状态

Java 8时代，synchronized有四层状态：无锁、偏向锁、轻量级锁、重量级锁。偏向锁的设计，是假设是大多数synchronized对象只有一个线程反复访问，所以把线程ID直接写进Mark Word，后续同一个线程加锁连CAS都不用做，直接比较线程ID就行。

这个假设在多核高并发场景下越来越不成立了。偏向锁的撤销需要进入「安全点」做全局同步，开销是比收益大的。在Java 15中废弃了偏向锁。

锁状态简化为三层：无锁 → 轻量级锁 → 重量级锁。升级是单向的，不能从重量级降回轻量级。

下面是轻量级锁和重量级锁的对比：

| 维度 | 轻量级锁 | 重量级锁 |
| --- | --- | --- |
| Mark Word锁标记 | 00 | 10 |
| 加锁方式 | CAS修改对象头 | ObjectMonitor互斥量 |
| 拿不到锁时 | CPU空循环重试 | 挂起线程 |
| CPU消耗 | 自旋期间占用CPU | 挂起后不占CPU |
| 上下文切换 | 无 | 有，微秒级开销 |
| 适合场景 | 临界区短、竞争少 | 临界区长、竞争激烈 |

### 小结

synchronized在JVM里的实现，体现了系统软件中一个常见的模式：分层，然后去应对不同量级的成本。轻量级锁用CAS在CPU上直接抢，成本最低。ObjectMonitor的自适应自旋是中间层，根据历史成功率动态调整策略。操作系统层面的挂起唤醒成本最高，放在最后一步。

这种逐级升级的思路在很多系统设计里都能看到。TCP重传的等待时间从短到长逐步增加，数据库查询优先走索引最后不得已才走全表扫描，核心逻辑是一样的：先用最低成本的方式去尝试，搞不定了再逐渐升级到更重量级的方案。

还没有人送礼物，鼓励一下作者吧

[所属专栏 · 15 分钟前 更新](https://zhuanlan.zhihu.com/c_1992153637800150476)

![](https://pic1.zhimg.com/v2-67f14de1feb645bc79be20f20ce6ebd5_720w.jpg?source=172ae18b)

随笔

![](https://pic1.zhimg.com/v2-d4037a975c6be26e723acb795fafc273_l.jpg?source=172ae18b)

SamDeepThinking

软件开发行业 研发高级经理

436 篇内容 · 12725 赞同

最热内容 ·

Spring Cloud各个微服务之间为什么要用http交互？难道不慢吗？

[发布于2026-09-10 14:49](https://www.zhihu.com/question/485099364/answer/2081393914901173093) ・广东

[FPGA 学习需要哪些东西？](https://www.zhihu.com/question/27183855/answer/3434530366)

FPGA 学习需要哪些东西？三样东西：第一就是完整的理论，第二一套开发板，第三可练手的项目https://xg.z...

[刘翔被体育局买断获49.4万 409 万](https://www.zhihu.com/search?q=%E5%88%98%E7%BF%94%E8%A2%AB%E4%BD%93%E8%82%B2%E5%B1%80%E4%B9%B0%E6%96%AD%E8%8E%B749.4%E4%B8%87&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 新

[宁德时代已报警 408 万](https://www.zhihu.com/search?q=%E5%AE%81%E5%BE%B7%E6%97%B6%E4%BB%A3%E5%B7%B2%E6%8A%A5%E8%AD%A6&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热

[霍奇猜想疑被OpenAI解决 386 万](https://www.zhihu.com/search?q=%E9%9C%8D%E5%A5%87%E7%8C%9C%E6%83%B3%E7%96%91%E8%A2%ABOpenAI%E8%A7%A3%E5%86%B3&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热

[江西孩子看演唱会后全家低保取消 364 万](https://www.zhihu.com/search?q=%E6%B1%9F%E8%A5%BF%E5%AD%A9%E5%AD%90%E7%9C%8B%E6%BC%94%E5%94%B1%E4%BC%9A%E5%90%8E%E5%85%A8%E5%AE%B6%E4%BD%8E%E4%BF%9D%E5%8F%96%E6%B6%88&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热

[DeepSeek V4.1 Flash 发布 364 万](https://www.zhihu.com/search?q=DeepSeek+V4.1+Flash+%E5%8F%91%E5%B8%83&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 新

[教师节 363 万](https://www.zhihu.com/search?q=%E6%95%99%E5%B8%88%E8%8A%82&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4)

[上海市体育局回应刘翔买断 363 万](https://www.zhihu.com/search?q=%E4%B8%8A%E6%B5%B7%E5%B8%82%E4%BD%93%E8%82%B2%E5%B1%80%E5%9B%9E%E5%BA%94%E5%88%98%E7%BF%94%E4%B9%B0%E6%96%AD&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 新

[知乎 CLI 创作者能力上新 363 万](https://www.zhihu.com/search?q=%E7%9F%A5%E4%B9%8E+CLI+%E5%88%9B%E4%BD%9C%E8%80%85%E8%83%BD%E5%8A%9B%E4%B8%8A%E6%96%B0&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热

[2026 苹果秋季发布会 362 万](https://www.zhihu.com/search?q=2026+%E8%8B%B9%E6%9E%9C%E7%A7%8B%E5%AD%A3%E5%8F%91%E5%B8%83%E4%BC%9A&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热

[高考132分学生开学数学考12分 308 万](https://www.zhihu.com/search?q=%E9%AB%98%E8%80%83132%E5%88%86%E5%AD%A6%E7%94%9F%E5%BC%80%E5%AD%A6%E6%95%B0%E5%AD%A6%E8%80%8312%E5%88%86&search_source=Trending&utm_content=search_hot&utm_medium=organic&utm_source=zhihu&type=content&request_click_id=2897178f-be6a-4bc8-9090-963c2c2b14f4) 热