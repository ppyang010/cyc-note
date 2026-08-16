---
id: "9788090206"
title: "为什么Spring官方不推荐使用 @Autowired？"
author: "東方幽静響"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/9788090206"
created: "2024-11-29 15:23"
updated: "2024-11-29 15:23"
collected: "2024-11-29 15:23"
downloaded: "2026-08-16"
---
## 前言

很多人刚接触 Spring 的时候，对 @Autowired 绝对是爱得深沉。

一个注解，轻松搞定依赖注入，连代码量都省了。

谁不爱呢？

但慢慢地，尤其是跑到稍微复杂点的项目里，@Autowired 就开始给你整点幺蛾子。

于是，官方在某些文档和社区交流中提到过：**不建议无脑用** **@Autowired，而是更推荐构造函数注入。**

为什么？是 @Autowired 不行吗？并不是。

它可以用，但问题是：**它不是无敌的，滥用起来容易埋坑。**

下面就来聊聊为啥官方建议你慎用 @Autowired，顺便再带点代码例子，希望对你会有所帮助。

## 1\. 容易导致隐式依赖

很多小伙伴在工作中喜欢直接写：

```text
@Service
public class MyService {
    @Autowired
    private MyRepository myRepository;
}
```

看着挺简单，但问题来了：**类的依赖关系藏得太深了**。

-   你看这段代码，MyService 和 MyRepository 的关系其实是个“隐形依赖”，全靠 @Autowired 来注入。
-   如果有个同事刚接手代码，打开一看，完全不知道 myRepository 是啥玩意儿、怎么来的，只有通过 IDE 或运行时才能猜出来。

隐式依赖的结果就是，代码看起来简单，但维护起来费劲。

后期加个新依赖，或者改依赖顺序，分分钟把人搞糊涂。

## 怎么破？

用 **构造函数注入** 替代。

```text
@Service
public class MyService {
    private final MyRepository myRepository;

    // 构造函数注入，依赖一目了然
    public MyService(MyRepository myRepository) {
        this.myRepository = myRepository;
    }
}
```

这样做的好处是：

-   **依赖清晰：**谁依赖谁，直接写在构造函数里，明明白白。
-   **更易测试：**构造函数注入可以手动传入 mock 对象，方便写单元测试。

## 2\. 会导致强耦合

再举个例子，很多人喜欢直接用 @Autowired 注入具体实现类，比如：

```text
@Service
public class MyService {
    @Autowired
    private SpecificRepository specificRepository;
}
```

表面上没毛病，但这是硬邦邦地把 MyService 和 SpecificRepository 绑死了。

万一有一天，业务改了，需要切换成另一个实现类，比如 AnotherSpecificRepository，你得改代码、改注解，连带着测试也崩。

## 怎么破？

用接口和构造函数注入，把依赖解耦。

```text
@Service
public class MyService {
    private final Repository repository;

    public MyService(Repository repository) {
        this.repository = repository;
    }
}
```

然后通过 Spring 的配置文件或者 @Configuration 类配置具体实现：

```text
@Configuration
public class RepositoryConfig {
    @Bean
    public Repository repository() {
        return new SpecificRepository();
    }
}
```

这么搞的好处是：

-   **灵活切换：**改实现类时，不用动核心逻辑代码。
-   **符合面向接口编程的思想：**降低耦合，提升可扩展性。

## 3\. 容易导致 NullPointerException

有些小伙伴喜欢这么写：

```text
@Service
public class MyService {
    @Autowired
    private MyRepository myRepository;

    public void doSomething() {
        myRepository.save(); // 啪！NullPointerException
    }
}
```

问题在哪？如果 Spring 容器还没来得及注入依赖，你的代码就跑了（比如在构造函数或初始化方法中直接调用依赖），结果自然就是 NullPointerException。

## 怎么破？

用构造函数注入，彻底干掉 null 的可能性。

```text
@Service
public class MyService {
    private final MyRepository myRepository;

    public MyService(MyRepository myRepository) {
        this.myRepository = myRepository; // 确保依赖在对象初始化时就已注入
    }

    public void doSomething() {
        myRepository.save();
    }
}
```

构造函数注入的另一个优点是：**依赖注入是强制的，Spring 容器不给你注入就报错**，让问题早暴露。

## 4.自动装配容易搞出迷惑行为

Spring 的自动装配机制有时候是“黑魔法”，尤其是当你的项目里有多个候选 Bean 时。比如：

```text
@Service
public class MyService {
    @Autowired
    private Repository repository; // 容器里有两个 Repository 实现类，咋办？
}
```

如果有两个实现类，比如 SpecificRepository 和 AnotherRepository，Spring 容器直接报错。解决方法有两种：

-   指定 @Primary。
-   用 @Qualifier 手动指定。

但这些方式都让代码看起来更复杂了，还可能踩坑。

## 怎么破？

构造函数注入 + 显式配置。

```text
@Configuration
public class RepositoryConfig {
    @Bean
    public Repository repository() {
        return new SpecificRepository();
    }
}
```

你明确告诉 Spring 该用哪个实现类，别让容器帮你猜，省得以后“配错药”。

## 5\. 写单元测试非常痛苦

最后，聊聊测试的事儿。

@Autowired 依赖 Spring 容器才能工作，但写单元测试时，大家都不想起 Spring 容器（麻烦、慢）。结果就是：

-   **字段注入：**没法手动传入 mock 对象。
-   **自动装配：**有时候不清楚用的 Bean 是哪个，测试难搞。

## 怎么破？

构造函数注入天生就是为单元测试设计的。

```text
public class MyServiceTest {
    @Test
    public void testDoSomething() {
        MyRepository mockRepository = mock(MyRepository.class);
        MyService myService = new MyService(mockRepository);

        // 测试逻辑
    }
}
```

看见没？

直接传入 mock 对象，测试简单、优雅。

## 总结

简单总结下问题：

1.  隐式依赖让代码可读性差。
2.  强耦合违背面向接口编程。
3.  字段注入容易 NPE。
4.  自动装配有坑。
5.  单元测试不好写。

那到底咋办？用 **构造函数注入**，清晰、稳健、测试友好，官方推荐不是没道理的。

但话说回来，@Autowired 也不是不能用，只是你得分场景。

开发中，养成用构造函数注入的习惯，能让你的代码更健壮，少挖坑，多干活！

  

来源

[https://www.cnblogs.com/12lisu/p/18575994](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/12lisu/p/18575994)