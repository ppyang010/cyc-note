---
id: "3579395509"
title: "spring为什么使用三级缓存而不是两级？"
author: "威哥爱编程"
type: zhihu-answer
source: "https://www.zhihu.com/question/445446018/answer/3579395509"
created: "2024-07-31 14:03"
updated: "2024-07-31 14:03"
collected: "2024-07-31 14:03"
downloaded: "2026-08-16"
---
Spring框架中的三级缓存主要用于解决循环依赖问题，特别是在单例Bean的创建过程中。下面V哥会解释为什么Spring需要三级缓存，而不是仅仅使用两级。

1.  **一级缓存（Singleton Objects）**：存储已经完全初始化好的单例Bean。当一个Bean被成功创建并注入到其他Bean中后，它会被放入一级缓存中。  
    
2.  **二级缓存（Early Singleton Objects）**：存储已经完成了BeanNameAware、BeanFactoryAware等Aware接口的回调，但是还没有完全初始化的Bean。这个缓存主要用于存放早期引用的Bean，这些Bean在完成属性填充和初始化方法调用之前，就可以被其他Bean引用。  
    
3.  **三级缓存（Singleton Factories）**：存储Bean工厂对象（BeanFactory）创建Bean实例的工厂信息。这个缓存是为了解决构造器循环依赖问题。当Spring容器创建一个Bean时，如果这个Bean的构造器依赖于其他Bean，Spring会首先尝试创建这个Bean的实例，这个实例的引用会被放入三级缓存中。然后，Spring会尝试创建依赖的Bean，如果依赖的Bean也存在循环依赖，Spring会从三级缓存中获取Bean的早期引用，而不是再次创建一个新的实例。  
    

为什么需要三级缓存：

-   **解决循环依赖**：在Spring中，如果两个或多个Bean相互依赖对方的构造器，就会发生循环依赖。两级缓存无法解决这个问题，因为它们都是在Bean实例化之后才被使用。三级缓存允许在Bean实例化过程中就提供对其他Bean的引用，从而打破循环依赖。  
    
-   **优化性能**：通过使用三级缓存，Spring可以在Bean实例化阶段就解决循环依赖问题，避免了额外的Bean创建尝试，从而提高了性能。  
    
-   **保持Bean的创建过程的原子性**：三级缓存确保了Bean的创建过程是原子性的，即在Bean完全初始化之前，不会将其暴露给其他Bean。  
    
-   **支持延迟初始化**：三级缓存允许Spring在Bean完全初始化之前，就能够提供Bean的引用，这支持了延迟初始化的模式，即只有在Bean被实际使用时才进行初始化。  
    

总之，三级缓存是Spring框架解决循环依赖问题的关键机制，它允许在Bean的创建过程中提供对其他Bean的引用，同时保持了Bean创建的原子性和性能。

## 三级缓存使用案例

在Spring框架中，三级缓存主要用于解决单例Bean的循环依赖问题。下面是一个简单的使用案例，展示如何通过Spring的三级缓存机制解决循环依赖。

首先，定义两个Bean，它们在构造器中相互依赖：

```text
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class ClassA {
    private ClassB classB;

    @Autowired
    public ClassA(ClassB classB) {
        this.classB = classB;
    }

    // ClassA的其他方法...
}

@Component
public class ClassB {
    private ClassA classA;

    @Autowired
    public ClassB(ClassA classA) {
        this.classA = classA;
    }

    // ClassB的其他方法...
}
```

在这个例子中，`ClassA`和`ClassB`通过构造器相互注入，形成了循环依赖。如果没有Spring的三级缓存机制，这种情况会导致异常，因为Spring无法完成其中一个Bean的创建。

Spring框架内部是如何处理这个问题的呢？以下是Spring容器创建这两个Bean时的大致步骤：

1.  Spring容器开始创建`ClassA`的Bean实例，并将其放入三级缓存`singletonFactories`中。
2.  容器尝试注入`ClassB`到`ClassA`的构造器中。由于`ClassB`还没有完全创建，Spring会尝试创建`ClassB`。
3.  在创建`ClassB`时，容器发现`ClassB`的构造器需要一个`ClassA`的实例。由于`ClassA`已经在三级缓存中，Spring会使用这个早期引用来注入`ClassB`。
4.  一旦`ClassB`被创建，它会被放入二级缓存`earlySingletonObjects`中，并完成剩余的初始化步骤。
5.  然后，容器继续完成`ClassA`的创建和初始化，将其放入一级缓存`singletonObjects`中。

这样，即使存在循环依赖，Spring也能够通过三级缓存机制确保每个Bean都能被正确创建和注入。

注意一下哈，这个例子中的代码是简化的，实际的Spring实现会更复杂，涉及到更多的细节和步骤。此外，Spring的使用者通常不需要直接操作这些缓存，因为Spring容器会自动处理这些逻辑。上述代码只是为了说明Spring如何解决循环依赖的问题。