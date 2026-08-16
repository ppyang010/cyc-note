---
id: "3167739710"
title: "如何在Java中直接使用Hystrix?"
author: "搬砖后端研发"
type: zhihu-answer
source: "https://www.zhihu.com/question/617323283/answer/3167739710"
created: "2023-08-16 11:04"
updated: "2023-08-16 11:04"
collected: "2023-08-16 11:04"
downloaded: "2026-08-16"
---
**1、添加依赖**

在 Java 项目中添加 Hystrix 的依赖，可以使用 Maven 或 Gradle 来管理依赖。

举个Maven 的示例：

```text
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-core</artifactId>
    <version>版本号</version>
</dependency>
```

**步骤 2：创建 Hystrix 命令**

使用 Hystrix 最常见的方式是创建一个继承自 `HystrixCommand` 类的命令类。在这个类中，可以定义需要进行容错处理的逻辑。

示例：

```text
import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

public class MyHystrixCommand extends HystrixCommand<String> {

    private final String name;

    public MyHystrixCommand(String name) {
        super(HystrixCommandGroupKey.Factory.asKey("ExampleGroup"));
        this.name = name;
    }

    @Override
    protected String run() throws Exception {
        return "Hello, " + name + "!";
    }
}
```

**执行 Hystrix 命令**

可以创建并执行自定义 Hystrix 命令。

示例：

```text
public class Main {
    public static void main(String[] args) {
        String result = new MyHystrixCommand("banzhuanhouduanyanfa").execute();
        System.out.println(result); // 输出 "Hello, banzhuanhouduanyanfa!"
    }
}
```

各位看官点点关注，点点赞呀。