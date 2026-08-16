---
id: "3167796510"
title: "Spring异步调用如何复制线程上下文信息?"
author: "搬砖后端研发"
type: zhihu-answer
source: "https://www.zhihu.com/question/617314399/answer/3167796510"
created: "2023-08-16 11:31"
updated: "2023-08-16 11:31"
collected: "2023-08-16 11:31"
downloaded: "2026-08-16"
---
可以使用 TaskExecutor 和 AsyncConfigurer 来实现复制线程上下文信息

比方：

```text
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Override
    @Bean(name = "taskExecutor")
    public TaskExecutor getAsyncExecutor() {
             ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10); // 设置核心线程数
        executor.setMaxPoolSize(50);  // 设置最大线程数
        executor.setQueueCapacity(100); // 设置队列容量
        executor.setThreadNamePrefix("AsyncThread-"); // 设置线程名前缀
        executor.initialize();
        return executor;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return new CustomAsyncExceptionHandler(); // 自定义异常处理器
    }
}
 
```

在这个配置类中，`@EnableAsync` 注解启用了 Spring 的异步功能。`TaskExecutor` 实例定义了异步任务的线程池配置。

然后，在异步方法中通过 `SecurityContextHolder`、`TransactionSynchronizationManager` 或其他需要的上下文信息进行复制：

```text
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.transaction.support.TransactionSynchronizationManager;
import org.springframework.util.concurrent.ListenableFuture;
import org.springframework.util.concurrent.ListenableFutureCallback;

@Service
public class MyAsyncService {

    @Async("taskExecutor")
    public void asyncMethod() {
        // 复制线程上下文信息
        SecurityContext originalContext = SecurityContextHolder.getContext();
        boolean isTransactionActive = TransactionSynchronizationManager.isActualTransactionActive();

        // 异步任务逻辑
        // ...

        // 还原线程上下文信息
        SecurityContextHolder.setContext(originalContext);
        if (isTransactionActive) {
            TransactionSynchronizationManager.initSynchronization();
        }
    }
}
```

关注 [@搬砖后端研发](https://www.zhihu.com/people/937d08239af02c9d15a5d69e2daa9643) 我分享更多有用干货及知识。