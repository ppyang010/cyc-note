---
id: "2013160634477457771"
title: "Spring 是如何解决循环依赖的？"
author: "花宝宝"
type: zhihu-answer
source: "https://www.zhihu.com/question/438247718/answer/2013160634477457771"
created: "2026-03-06 07:54"
updated: "2026-03-07 09:05"
collected: "2026-03-06 07:54"
downloaded: "2026-08-16"
---
Spring Boot 2.6 开始，循环依赖默认直接报错了。启动的时候你会看到这么一句：

> The dependencies of some of the beans in the application context form a cycle

Spring 团队的态度很明确：循环依赖是你代码的问题，框架不替你兜底了。

但是升级 Spring Boot 之后启动直接炸了的项目可不少，尤其是老项目。Spring 在 2.6 之前是怎么兜住这个问题的呢？三级缓存——面试考烂了，但大部分八股文只背了“三级缓存”四个字，没搞清楚为什么是三级而不是两级。

### 循环依赖长什么样

最典型的场景：

```text
@Service
public class OrderService {
    @Autowired
    private UserService userService;
}

@Service
public class UserService {
    @Autowired
    private OrderService orderService;
}
```

OrderService 需要 UserService，UserService 需要 OrderService。Spring 创建 Bean 的时候，要创建 OrderService 就得先注入 UserService，要创建 UserService 就得先注入 OrderService——死锁了。

如果 Spring 按照最朴素的方式处理——创建 A → 发现依赖 B → 创建 B → 发现依赖 A → 创建 A → 发现依赖 B → ……无限循环，程序直接栈溢出。

### 一级缓存解决不了

Spring 的一级缓存是 `singletonObjects`，存的是完全初始化好的 Bean。

问题在于：A 还没创建完（属性还没注入），就不能放进一级缓存。B 需要 A 的时候，去一级缓存里找不到 A，还是得重新创建 A，循环还是断不掉。

### 两级缓存能解决，但不够

那换个思路：A 刚 new 出来（还没注入属性），先把这个“半成品 A”存到一个地方。B 需要 A 的时候，拿到的是半成品，但至少有一个引用了，不用再创建新的 A。等 B 创建完了，回头给 A 注入 B，A 也就完整了。

这就是“提前暴露”的思路。一级缓存还是存完整的成品 Bean，加一个二级缓存专门存这种半成品——已经实例化、但还没注入属性的那种。

流程就是：创建 A → A 刚 new 出来就塞进二级缓存 → 发现要注入 B → 去创建 B → B 发现要注入 A → 去二级缓存一看，有个半成品 A，拿走 → B 创建完了 → 回头把 B 注入给 A → A 也完整了。

循环就这么断掉了。两级缓存搞定，收工？

没那么简单——AOP 会搅局。

### AOP 把事情搞复杂了

Spring 的 AOP 是通过动态代理实现的。你给 OrderService 加了一个 `@Transactional`，Spring 最终放进容器的不是 OrderService 原始对象，而是一个代理对象。这个代理对象包了一层事务逻辑，实际的业务方法调用会被代理拦截。

问题来了：A 实例化之后放进二级缓存的是原始对象。B 拿到的是 A 的原始对象。但 A 最终初始化完成后，Spring 发现 A 需要被代理，于是生成了一个代理对象放进一级缓存。

这时候 B 手里拿的还是 A 的原始对象，一级缓存里放的却是 A 的代理对象。B 引用的 A 和容器里的 A 不是同一个对象——单例被破坏了。

### 三级缓存：延迟决定给不给代理

Spring 的解决办法是加第三级缓存 `singletonFactories`，存的不是 Bean 本身，而是一个 ObjectFactory——一个工厂方法。

```text
addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
```

`getEarlyBeanReference` 这个方法会判断：如果 A 需要被 AOP 代理，就提前创建代理对象返回；如果不需要，就返回原始对象。

整个流程变成这样：

创建 A → A 实例化后，把一个能生产 A 的工厂放进三级缓存 → 注入属性发现需要 B → 创建 B → B 注入属性需要 A → 从三级缓存拿到工厂，调用工厂方法。

这一步是关键。工厂方法会判断 A 是否需要代理：需要的话返回代理对象，不需要就返回原始对象。拿到的结果放进二级缓存，三级缓存里的工厂删掉。

B 拿到了正确版本的 A（可能是代理对象），继续完成创建。B 完成后放进一级缓存。回到 A，注入 B。A 初始化完成，放进一级缓存。

你可能会问：为什么不一开始就判断需不需要代理，直接放代理对象进二级缓存？

因为 Spring 的设计原则是代理应该在 Bean 完全初始化之后再创建，而不是一实例化就急着代理。提前创建代理是不得已的妥协——只有发生循环依赖的时候才会提前，没有循环依赖就走正常流程。三级缓存的工厂方法干的就是这个”要用再提前、不用不动”的事。

### 哪些情况三级缓存也救不了

**构造器注入。** 如果依赖是通过构造方法注入的：

```text
@Service
public class OrderService {
    private final UserService userService;
    
    public OrderService(UserService userService) {
        this.userService = userService;
    }
}
```

A 的构造方法参数需要 B，但 A 还没实例化就要 B——连“半成品 A”都不存在，没东西可以提前暴露。所以构造器注入的循环依赖，Spring 直接报错，三级缓存帮不了。

**原型模式（Prototype）。** 三级缓存只对单例 Bean 生效。原型 Bean 每次都创建新的，不存缓存，循环依赖也是直接报错。

**`@Async` 导致的代理问题。** `@Async` 的代理是在 `BeanPostProcessor` 阶段创建的，跟 AOP 的代理机制不一样。如果 A 有 `@Async` 方法且参与了循环依赖，Spring 会发现提前暴露的对象和最终的代理对象不一致，抛出 `BeanCurrentlyInCreationException`。这是个历史遗留的坑，踩过的人不少。

### Spring Boot 2.6+ 为什么禁掉了

Spring 团队的理由很直接：两个 Service 互相依赖，说明职责划分有问题。

OrderService 依赖 UserService，下单要查用户信息，合理。但 UserService 为什么反过来要依赖 OrderService？查用户的时候顺便查订单？那这块逻辑是不是应该抽到别的地方去？

三级缓存让开发者不需要面对这个问题——反正 Spring 能兜住，先这么写着。时间一长，循环依赖像蜘蛛网一样越缠越密，A 依赖 B，B 依赖 C，C 又依赖 A，最后谁都不敢动。你从实际项目里见过的“改一个 Service 全盘炸了”的场景，十有八九底下藏着循环依赖。

你可以用 `spring.main.allow-circular-references=true` 临时放开，但 Spring 官方的原话是这只是过渡方案，未来版本可能会把这个开关直接删掉。

### 遇到循环依赖怎么改

最干净的做法当然是重构，把互相依赖的逻辑拆开。但老项目嘛，大规模重构不现实，先活下来再说：

**用 `@Lazy` 延迟加载。** 在其中一个注入点加 `@Lazy`，让 Spring 注入的是一个代理，真正用到的时候才去容器里拿：

```text
@Service
public class OrderService {
    @Lazy
    @Autowired
    private UserService userService;
}
```

这不是解决了循环依赖，是延迟了循环依赖的触发时机。本质上还是有循环引用，但启动不会报错了。

**抽出公共逻辑到第三个类。** A 和 B 互相依赖，往往是因为有一部分逻辑放在了不该放的地方。把共用的部分抽到 C 里，让 A 和 B 都依赖 C，循环就断了。

**用事件机制解耦。** OrderService 下单之后要通知 UserService 加积分，不直接调用，而是发一个事件：

```text
applicationEventPublisher.publishEvent(new OrderCreatedEvent(orderId));
```

UserService 监听这个事件去加积分。两个 Service 之间没有直接依赖关系了。

三级缓存是 Spring 在历史上做出的工程妥协——一个精巧的补丁，解决的是一个本不该存在的问题。面试的时候能讲清楚“为什么是三级”的人不多，但在实际写代码的时候，能主动把循环依赖消灭在设计阶段的人更少。