---
id: "3031869890"
title: "为什么spring一定要弄个三级缓存？"
author: "廖雪峰"
type: zhihu-answer
source: "https://www.zhihu.com/question/594297402/answer/3031869890"
created: "2023-05-17 13:18"
updated: "2023-05-22 20:49"
collected: "2023-05-17 13:18"
downloaded: "2026-08-16"
---
Spring用三级缓存完全是因为早期发布的API有BeanFactory和ApplicationContext两种接口，前者要求延迟创建Bean，后者要求启动就创建Bean，所以才会搞复杂的三级缓存。延迟创建虽然实际没啥卵用，但大大增加了创建Bean的复杂度。比如A、B、C三个Bean，默认都没创建，现在要创建A，那么创建流程：

```text
┌ ─ ─ ─ ─ ─ ─ ─ ┐
  ┌───────────┐     ┌───────────┐    ┌───────────┐
│ │  A(null)  │ │   │  B(null)  │    │  C(null)  │
  └───────────┘     └───────────┘    └───────────┘
│       │       │
        ▼
│ ┌───────────┐ │
  │  new A()  │
│ └───────────┘ │
        │
│       ▼       │
  ┌───────────┐
│ │postProcess│ │
  └───────────┘
│       │       │
        ▼
│ ┌───────────┐ │
  │  setter   │
│ └───────────┘ │
        │
│       ▼       │
  ┌───────────┐
│ │   init    │ │
  └───────────┘
└ ─ ─ ─ ─ ─ ─ ─ ┘
```

如果A依赖B，那么B也需要被动来一遍创建流程，这种竖着切的方式复杂度非常高，引入三级缓存才能实现AOP的功能，因为注入要求Proxy，而setter要求原始Bean。

此外，延迟加载和Prototype类型的Bean存在一个多线程同时请求的问题，Spring早期版本其实有并发访问问题（很难发现，因为绝大多数app创建bean并发度不够），在lazy init的条件下三级缓存随时都有可能更改，而此时还要考虑其他线程并发createBean的问题，构造全面的测试想想都头大。

如果自己手写类似Spring的框架，放弃BeanFactory和Prototype，只支持ApplicationContext，一启动就完成所有Bean的初始化，那么一级缓存就足够了。这种情况下，我们横着切：

```text
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌───────────┐     ┌───────────┐    ┌───────────┐ │
│ │  A(null)  │     │  B(null)  │    │  C(null)  │
  └───────────┘     └───────────┘    └───────────┘ │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                          │
                          ▼
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌───────────┐     ┌───────────┐    ┌───────────┐ │
│ │  new A()  │     │  new B()  │    │  new C()  │
  └───────────┘     └───────────┘    └───────────┘ │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                          │
                          ▼
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌───────────┐     ┌───────────┐    ┌───────────┐ │
│ │postProcess│     │postProcess│    │postProcess│
  └───────────┘     └───────────┘    └───────────┘ │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                          │
                          ▼
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌───────────┐     ┌───────────┐    ┌───────────┐ │
│ │  setter   │     │  setter   │    │  setter   │
  └───────────┘     └───────────┘    └───────────┘ │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
                          │
                          ▼
┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
  ┌───────────┐     ┌───────────┐    ┌───────────┐ │
│ │   init    │     │   init    │    │   init    │
  └───────────┘     └───────────┘    └───────────┘ │
└ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
```

横着切有多简单？简单到不超过1000行代码，单个类实现IoC容器：

[AnnotationConfigApplicationContext.java](https://link.zhihu.com/?target=https%3A//github.com/michaelliao/summer-framework/blob/master/framework/summer-context/src/main/java/com/itranswarp/summer/context/AnnotationConfigApplicationContext.java)

[实现IoC容器](https://link.zhihu.com/?target=https%3A//www.liaoxuefeng.com/wiki/1539348902182944/1539427782361120)

因为启动就初始化，单线程操作，后续无多线程createBean，缓存固定，所以无锁无同步，代码简单。

检测循环依赖也用不到三级缓存，一级缓存就能检测。三级缓存与效率、重复创建也没有关系（Bean本来就要求保证不可重复创建），实现AOP也不需要三级缓存，一级缓存照样可以。当然，前提是需求被简化了，只支持ApplicationContext。

建议通过手写Spring来学习Spring设计思想：

[手写Spring](https://link.zhihu.com/?target=https%3A//www.liaoxuefeng.com/wiki/1539348902182944)

Talk is cheap, show me the code. —— Linus