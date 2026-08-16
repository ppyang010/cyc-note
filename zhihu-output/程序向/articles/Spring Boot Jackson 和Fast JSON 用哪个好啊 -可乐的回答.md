---
id: "3374600944"
title: "Spring Boot Jackson 和Fast JSON 用哪个好啊 ?"
author: "可乐"
type: zhihu-answer
source: "https://www.zhihu.com/question/501897937/answer/3374600944"
created: "2024-01-24 17:29"
updated: "2024-01-24 17:29"
collected: "2024-01-24 17:29"
downloaded: "2026-08-16"
---
我最近也遇到了这个问题，之前用的都是Fastjson的静态方法，很方便。但是Spring框架中都使用的是Jackson，我就想也试试Jacnson。

发现Jackson功能很强大，但是比较麻烦。刚开始使用的时候因为用惯了Fastjson的静态方法，十分不习惯，先要new一个ObjectMapper，因为它的方法都是抛出异常的，调用时还要用try-catch包住，不方便，就像这样。

```java
String subject;
try {
    subject = new ObjectMapper().writeValueAsString(new User());
} catch (JsonProcessingException e) {
    throw new RuntimeException("Serialization as json failed", e);
}
```

我就搜啊，看看网上有没有什么优雅的用法，并没有发现什么有价值的。

后来转变了思路，既然Spring里面都用这个，那就找找看Spring中怎么用的，后来真在框架中找到了这个类`AbstractJsonParser`，它里面是这样写的：

```java
package org.springframework.boot.json;

/**
 * Base class for parsers wrapped or implemented in this package.
 *
 * @author Anton Telechev
 * @author Phillip Webb
 * @since 2.0.1
 */
public abstract class AbstractJsonParser implements JsonParser {

    // ...省略不重要的

    protected final <T> T tryParse(Callable<T> parser, Class<? extends Exception> check) {
        try {
            return parser.call();
        }
        catch (Exception ex) {
            if (check.isAssignableFrom(ex.getClass())) {
                throw new JsonParseException(ex);
            }
            ReflectionUtils.rethrowRuntimeException(ex);
            throw new IllegalStateException(ex);
        }
    }

    // ... 省略不重要的
}
```

他在调用Jackson中需要try-catch的方法时，就变成了这样：

```java
    public List<Object> parseList(String json) {
        return tryParse(() -> getObjectMapper().readValue(json, LIST_TYPE), Exception.class);
    }
```

确实优雅！

根据他的思路，再把ObjectMapper封装成单例，创建一个工具类`JacksonUtil`

```java
import com.fasterxml.jackson.core.JacksonException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.boot.json.JsonParseException;

import java.util.concurrent.Callable;

public class JacksonUtil {

    private JacksonUtil(){
    }

    // 静态代码块单例
    private final static ObjectMapper OBJECT_MAPPER;

    static {
        OBJECT_MAPPER = new ObjectMapper();
    }

    public static ObjectMapper getObjectMapper(){
        return OBJECT_MAPPER;
    }

    public static <T> T tryParse(Callable<T> parser) {
        return tryParse(parser, JacksonException.class);
    }

    public static <T> T tryParse(Callable<T> parser, Class<? extends Exception> check) {
        try {
            return parser.call();
        } catch (Exception ex) {
            if (check.isAssignableFrom(ex.getClass())) {
                throw new JsonParseException(ex);
            }
            throw new IllegalStateException(ex);
        }
    }
}
```

调用时

```java
public class TestJacksonUtil {
    public static void main(String[] args) {
        // 1.普通json
        User user = JacksonUtil.tryParse(() -> JacksonUtil.getObjectMapper().readValue("{json}", User.class));
        List<User> users = JacksonUtil.tryParse(() -> JacksonUtil.getObjectMapper().readValue("{json}", new TypeReference<List<User>>() {}));


        // 2.有特殊要求的json
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.setDateFormat(new SimpleDateFormat("yyyy-MM-dd"));
        String json = JacksonUtil.tryParse(() -> objectMapper.writeValueAsString(new User()));
    }
}
```

他的这个方法既不影响ObjectMapper原有的api，又把异常捕捉了，还能适用于所有的方法，十分巧妙！牛！