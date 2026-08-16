---
id: "3326785196"
title: "为什么spring一定要弄个三级缓存？"
author: "Siland"
type: zhihu-answer
source: "https://www.zhihu.com/question/594297402/answer/3326785196"
created: "2023-12-15 15:55"
updated: "2024-01-08 10:13"
collected: "2023-12-15 15:55"
downloaded: "2026-08-16"
---
### 结论

解决有代理对象的循环依赖不一定要三级缓存，用二级甚至一级也能解决，下面讨论下Spring为什么选择三级缓存这个方案。

Spring最开始是没有三级缓存的，后面版本因为引入了AOP，有了代理对象，又因为存在循环依赖，为了保证依赖注入过程注入的是代理对象，且不完全打破Spring的设计原则（代理等这些后置处理器应当在初始化阶段完成），Spring选择稍微打破限制，提前对循环依赖的bean在依赖注入的时候就生成代理对象。

  

### 解释

Spring 现在的三级缓存如下：

```java
/** 第一级缓存，存放可用的成品Bean。 */
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);

/** 第三级缓存，存的是Bean工厂对象 */
private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);

/** 第二级缓存，存放半成品的Bean，半成品的Bean是已创建了对象，但是未注入属性和进行初始化*/
                                                                                                            private final Map<String, Object> earlySingletonObjects = new ConcurrentHashMap<>(16);
```

  

Spring目前是通过二三级缓存配合，进行循环依赖的解决。

  

首先，我们要明确Spring遵守的单例bean的创建流程，bean 先实例化，再属性赋值，依赖注入，再初始化。。。。这个基本过程。我们所说的代理对象其实就是初始化阶段，BeanPostProcessor后置处理器完成代理对象的。

网上有很多地方说三级缓存是为了解决代理对象，这个说法并没有说到根本。

如果我们单纯为了解决有代理的循环依赖，其实解决循环依赖用二级缓存甚至一级缓存就可以了，之所以用了三级缓存是Spring开发者的一种取舍造成的。

对于如何解决带有AOP的循环依赖，有如下两种解决方案：

  

1、无论这个bean有没有循环依赖，在依赖注入之前，就创建好这个bean的代理对象放入缓存，出现依赖注入的时候，直接从这个缓存拿取代理对象即可。

  

2、不提前创建代理对象，当只有出现循环依赖的时候，才实时地创建代理对象。

  

Spring 因为为了不完全违背bean的创建流程的定义（代理应当在属性赋值后的初始化过程中生成代理对象），只能勉为其难的提前进行。所以选择了上述的第二种方案。

  

接下来，说一下为啥选择第二种方案要用三级缓存。

spring 为了优雅，缓存尽量存储的是单一性质的元素，所以必须有第一级缓存，用来存放可用的成品Bean。

```text
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);
```

接下来，假如A 和 B存在循环依赖，A 和 C也存在循环依赖，所以当创建A的bean的时候，避免B和C 拿到不同的代理对象，因此我们需要第二个缓存来存储B拿到的A的代理对象，当C去A代理对象的时候，就可以直接从第二个缓存中拿取了。

为了实现只有出现循环依赖的时候，才实时地创建代理对象这个过程，Spring 又引入了第三个缓存，第三个缓存的作用是当A在实例化的时候，就把自己放入第三个缓存，代码如下：

```text
if (earlySingletonExposure) {
      if (logger.isTraceEnabled()) {
		logger.trace("Eagerly caching bean '" + beanName +
		"' to allow for resolving potential circular references");
	}
	addSingletonFactory(beanName, () -> getEarlyBeanReference(beanName, mbd, bean));
}
```

  

，表示A正在创建当中，其中() -> getEarlyBeanReference(beanName, mbd, bean))的函数式接口就是用来实现创建代理对象的，

```text
protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
	Object exposedObject = bean;
	if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
		for (SmartInstantiationAwareBeanPostProcessor bp : getBeanPostProcessorCache().smartInstantiationAware) {
			exposedObject = bp.getEarlyBeanReference(exposedObject, beanName);
		}
	}
	return exposedObject;
}
```

  

当B需要注入A的时候就会执行如下步骤：

```text
@Nullable
protected Object getSingleton(String beanName, boolean allowEarlyReference) {
	// Quick check for existing instance without full singleton lock
	Object singletonObject = this.singletonObjects.get(beanName);
	if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
		singletonObject = this.earlySingletonObjects.get(beanName);
		if (singletonObject == null && allowEarlyReference) {
			synchronized (this.singletonObjects) {
				// Consistent creation of early reference within full singleton lock
				singletonObject = this.singletonObjects.get(beanName);
				if (singletonObject == null) {
					singletonObject = this.earlySingletonObjects.get(beanName);
					if (singletonObject == null) {
						ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
						if (singletonFactory != null) {
							singletonObject = singletonFactory.getObject();
							this.earlySingletonObjects.put(beanName, singletonObject);
							this.singletonFactories.remove(beanName);
						}
					}
				}
			}
		}
	}
	return singletonObject;
}
```

先去第一级缓存拿，没有就去第二级缓存拿，二级没有的话，就去第三级缓存看看，当在第三级缓存发现有A的时候，说明此时A正在创建中，且未被其他bean引用，此时就会从三级缓存中取出beanFactory，beanFactory再执行getObject方法，getObjetc方法就前面的

```text
protected Object getEarlyBeanReference(String beanName, RootBeanDefinition mbd, Object bean) {
	Object exposedObject = bean;
	if (!mbd.isSynthetic() && hasInstantiationAwareBeanPostProcessors()) {
		for (SmartInstantiationAwareBeanPostProcessor bp : getBeanPostProcessorCache().smartInstantiationAware) {
			exposedObject = bp.getEarlyBeanReference(exposedObject, beanName);
		}
	}
	return exposedObject;
}
```

其中SmartInstantiationAwareBeanPostProcessor 是spring内部对于BeanPostProcessor的实现，大家可以自己点去看看，SmartInstantiationAwareBeanPostProcessor 的getEarlyBeanReference就是创建代理对象，并标记自己已经创建了代理对象（earlyProxyReferences）。

```text
@Override
public Object getEarlyBeanReference(Object bean, String beanName) {
	Object cacheKey = getCacheKey(bean.getClass(), beanName);
	this.earlyProxyReferences.put(cacheKey, bean);
	return wrapIfNecessary(bean, beanName, cacheKey);
}
```

此时B相当于从三级缓存中拿到了A的代理对象，B为了后面的C和自己拿到的是同一个A的代理对象，他就需要把这个A代理对象放入第二级缓存。同时移除第三级缓存的A，表示A已经提前创建好了代理对象，不需要再从三级缓存里面获取新代理对象了。

  

接下来，B的创建好后，A继续注入C，C直接从第二级拿到已经创建好了的A的代理对象。A在后面的初始化阶段执行applyBeanPostProcessorsAfterInitialization

```text
@Override
public Object applyBeanPostProcessorsAfterInitialization(Object existingBean, String beanName)
		throws BeansException {

	Object result = existingBean;
	for (BeanPostProcessor processor : getBeanPostProcessors()) {
		Object current = processor.postProcessAfterInitialization(result, beanName);
		if (current == null) {
			return result;
		}
		result = current;
	}
	return result;
}


@Override
public Object postProcessAfterInitialization(@Nullable Object bean, String beanName) {
	if (bean != null) {
		Object cacheKey = getCacheKey(bean.getClass(), beanName);
                //判断是否提前创建了代理对象
		if (this.earlyProxyReferences.remove(cacheKey) != bean) {
			return wrapIfNecessary(bean, beanName, cacheKey);
		}
	}
	return bean;
}
```

的时候, 会判断之前是否提前创建了代理对象，这样就解决了带有AOP的循环依赖。

当然，如果A没有循环依赖，那么就不会被其他bean从第三级缓存中取出来执行getEarlyBeanReference方法，这样A的AOP自然就留在了初始化阶段完成了，这样也就遵守了Spring定义的bean的创建过程。

  

### 继续解释

继续解释下为什么我说只用二级或者一级缓存也能解决带有AOP的循环依赖问题。

  

假如不遵守Spring强烈要求bean的创建过程，我们可以直接在依赖注入前，就往第二级缓存存入A的代理对象（如果没有代理就直接存原始对象），这样B和C直接就可以从第二级缓存拿到A的代理对象，这样两个缓存就能解决了，但是这样做就是提前把代理对象都创建好了。

  

如果我们更过分点，不遵守每一级缓存存入的是同一过程性质的bean，那么我们只需一级缓存，每个bean提前创建好代理对象就放入一级缓存，（此时一级缓存的bean还是未初始化的bean），接下来B直接从一级拿到A的代理对象，完成创建，B把自己完整的Bean也放入一级缓存，此时一级缓存的bean 就有中间态和完成态两种形态的bean, 最终A完成创建，一级缓存全是完成态Bean。这样做，只用一级缓存就能完成所有的过程，只是不优雅~~。