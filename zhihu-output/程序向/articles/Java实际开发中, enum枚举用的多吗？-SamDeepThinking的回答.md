---
id: "2013160036134834695"
title: "Java实际开发中, enum枚举用的多吗？"
author: "SamDeepThinking"
type: zhihu-answer
source: "https://www.zhihu.com/question/1913219325743067883/answer/2013160036134834695"
created: "2026-03-06 07:52"
updated: "2026-04-08 10:40"
collected: "2026-03-06 07:52"
downloaded: "2026-08-16"
---
> 日常业务开发的话，使用Enum的普通用法就可以了，不需要什么很高明的用法。但是翻开 Tomcat、Spring Boot、RocketMQ的源码，你会发现枚举可以玩的花样还蛮多的，比如 策略模式、状态机、函数式编程、领域建模。枚举能做的事比你想象的多得多。

我从 Tomcat 7、Spring Boot 2.7、RocketMQ 4.9.8源码中摘抄出10个案例，让大家看看技术大神的enum用法。

* * *

## 流行框架中的Enum用法

### 枚举内嵌函数式接口

> 来源：Tomcat `org.apache.coyote.http2.FrameType`

HTTP/2 协议有多种帧类型（DATA、HEADERS、SETTINGS…），每种帧对 payload 大小有不同的校验规则。Tomcat 怎么做的？在枚举内部定义了一个函数式接口 ***`IntPredicate`***，每个常量持有不同的验证谓词：

```java
enum FrameType {
    DATA          (0, false, true,  null,             false),
    HEADERS       (1, false, true,  null,              true),
    PRIORITY      (2, false, true,  equals(5),        false),  // payload必须=5
    RST           (3, false, true,  equals(4),        false),  // payload必须=4
    SETTINGS      (4, true,  false, dividableBy(6),    true),  // payload必须是6的倍数
    PUSH_PROMISE  (5, false, true,  greaterOrEquals(4), true), // payload>=4
    PING          (6, true,  false, equals(8),        false),  // payload必须=8
    WINDOW_UPDATE (8, true,  true,  equals(4),         true);

    private final IntPredicate payloadSizeValidator;  // 每个帧类型自带验证器

    // 校验方法：直接调用谓词
    void check(int streamId, int payloadSize) throws Http2Exception {
        if (payloadSizeValidator != null && !payloadSizeValidator.test(payloadSize)) {
            throw new ConnectionException(..., Http2Error.FRAME_SIZE_ERROR);
        }
    }

    // 枚举内部定义函数式接口
    private interface IntPredicate {
        boolean test(int x);
    }

    // 工厂方法创建不同的谓词
    private static IntPredicate equals(final int y) {
        return x -> x == y;
    }
    private static IntPredicate dividableBy(final int y) {
        return x -> x % y == 0;
    }
    private static IntPredicate greaterOrEquals(final int y) {
        return x -> x >= y;
    }
}
```

特别的地方在哪呢?

FrameType可以理解成一张配置表，每行一种帧类型的完整规则。验证逻辑不是写在 `if-else` 里，而是**作为字段存在常量上**。新增帧类型时只需加一行，不用改任何验证代码。

* * *

### 枚举驱动状态机

> 来源：Tomcat `org.apache.tomcat.util.http.parser.HttpParser.DomainParseState`

解析 HTTP 域名时，Tomcat 用枚举实现了一个完整的**有限状态自动机**。每个状态知道自己能接受什么字符，以及转移到哪个状态：

```java
private enum DomainParseState {
    //               mayContinue  allowsHyphen  allowsPeriod  allowsEnd
    NEW     (true,   false,        false,        false,  "...atStart"),
    ALPHA   (true,   true,         true,         true,   "...afterLetter"),
    NUMERIC (true,   true,         true,         true,   "...afterNumber"),
    PERIOD  (true,   false,        false,        true,   "...afterPeriod"),
    HYPHEN  (true,   true,         false,        false,  "...afterHyphen"),
    COLON   (false,  false,        false,        false,  "...afterColon"),
    END     (false,  false,        false,        false,  "...atEnd");

    private final boolean mayContinue;
    private final boolean allowsHyphen;
    private final boolean allowsPeriod;
    private final boolean allowsEnd;
    private final String errorMsg;

    // 核心：状态转移方法
    public DomainParseState next(int c) {
        if (c == -1) {
            if (allowsEnd) return END;
            else throw new IllegalArgumentException(errorMsg);
        } else if (isAlpha(c)) {
            return ALPHA;
        } else if (isNumeric(c)) {
            return NUMERIC;
        } else if (c == '.') {
            if (allowsPeriod) return PERIOD;
            else throw new IllegalArgumentException(errorMsg);
        } else if (c == '-') {
            if (allowsHyphen) return HYPHEN;
            else throw new IllegalArgumentException(errorMsg);
        }
        // ...
    }
}
```

状态转移规则**全部编码在枚举常量的布尔字段里**。`next()` 方法根据当前状态的字段决定能否转移。不需要 `switch(currentState)` 的大块代码，每个状态”自己知道”该怎么转移。这是状态模式和枚举的完美结合。

* * *

### 枚举错误升级器

> 来源：Tomcat `org.apache.coyote.ErrorState`

网络编程中经常遇到错误升级问题：先发生了一个小错误，后面又出了一个更严重的，最终应该按最严重的错误来处理。Tomcat 给错误状态枚举加了一个 `getMostSevere()` 方法：

```java
public enum ErrorState {
    NONE                (false, 0, true,  true),   // 无错误
    CLOSE_CLEAN         (true,  1, true,  true),   // 完成当前响应后关连接
    CLOSE_NOW           (true,  2, false, true),   // 立刻关闭流/通道
    CLOSE_CONNECTION_NOW(true,  3, false, false);   // 立刻关闭底层网络连接

    private final boolean error;
    private final int severity;          // 严重度数值
    private final boolean ioAllowed;
    private final boolean connectionIoAllowed;

    // 比较器：返回更严重的那个
    public ErrorState getMostSevere(ErrorState input) {
        if (input.severity > this.severity) {
            return input;
        } else {
            return this;
        }
    }
}

// 使用场景：错误逐级升级
errorState = errorState.getMostSevere(newError);
```

`severity` 字段让枚举常量之间建立了**偏序关系**。`getMostSevere()` 相当于一个 `max()` 操作。这比用 `if (newError.ordinal() > currentError.ordinal())` 这种脆弱的写法好很多，ordinal 依赖声明顺序，severity 是显式的。

* * *

### 枚举常量自带私有方法和私有字段

> 来源：Spring Boot `org.springframework.boot.cloud.CloudPlatform`

Spring Boot 自动检测运行环境是哪个云平台。每个平台的检测逻辑完全不同，有的查一个环境变量，有的要查多个，有的还需要遍历所有环境变量：

```java
public enum CloudPlatform {
    NONE {
        @Override
        public boolean isDetected(Environment environment) {
            return false;
        }
    },

    CLOUD_FOUNDRY {
        @Override
        public boolean isDetected(Environment environment) {
            return environment.containsProperty("VCAP_APPLICATION")
                || environment.containsProperty("VCAP_SERVICES");
        }
    },

    KUBERNETES {
        // 枚举常量可以有自己的私有静态字段！
        private static final String KUBERNETES_SERVICE_HOST = "KUBERNETES_SERVICE_HOST";
        private static final String SERVICE_HOST_SUFFIX = "_SERVICE_HOST";
        private static final String SERVICE_PORT_SUFFIX = "_SERVICE_PORT";

        @Override
        public boolean isDetected(Environment environment) {
            if (environment instanceof ConfigurableEnvironment) {
                return isAutoDetected((ConfigurableEnvironment) environment);
            }
            return false;
        }

        // 枚举常量可以有自己的私有方法！
        private boolean isAutoDetected(ConfigurableEnvironment environment) {
            PropertySource<?> source = environment.getPropertySources()
                .get(StandardEnvironment.SYSTEM_ENVIRONMENT_PROPERTY_SOURCE_NAME);
            if (source != null && source.containsProperty(KUBERNETES_SERVICE_HOST)) {
                return true;
            }
            // 兜底：遍历所有环境变量查找 xxx_SERVICE_HOST + xxx_SERVICE_PORT 的组合
            // ...
        }
    },

    AZURE_APP_SERVICE {
        private final List<String> azureEnvVariables = Arrays.asList(
            "WEBSITE_SITE_NAME", "WEBSITE_INSTANCE_ID",
            "WEBSITE_RESOURCE_GROUP", "WEBSITE_SKU");

        @Override
        public boolean isDetected(Environment environment) {
            // 函数式：所有变量都存在才算Azure
            return this.azureEnvVariables.stream()
                .allMatch(environment::containsProperty);
        }
    };

    public abstract boolean isDetected(Environment environment);

    // 公共方法：先查配置，再自动检测
    public boolean isActive(Environment environment) {
        String platformProperty = environment.getProperty("spring.main.cloud-platform");
        return isEnforced(platformProperty) || (platformProperty == null && isDetected(environment));
    }
}
```

每个枚举常量不只是重写了一个抽象方法，KUBERNETES 常量还有自己的**私有静态字段**和**多个私有方法**，俨然一个”微型类”。AZURE\_APP\_SERVICE 用了 `Stream.allMatch()` + 方法引用。这种写法把每个平台的检测逻辑完全内聚在各自的常量里，绝不会互相干扰。

* * *

### 嵌套枚举持有 Function 字段

> 来源：Spring Boot `org.springframework.boot.convert.DurationStyle`

Spring Boot 配置文件里可以写 `timeout=30s` 或 `timeout=PT30S`（ISO8601格式）。`DurationStyle` 枚举负责自动识别格式并解析。它的嵌套枚举 `Unit` 更有意思，\*\*每个时间单位持有一个 \*`***Function<Duration, Long>***`\* 字段\*\*：

```java
public enum DurationStyle {

    SIMPLE("^([+-]?\\d+)([a-zA-Z]{0,2})$") {
        @Override
        public Duration parse(String value, ChronoUnit unit) {
            Matcher matcher = matcher(value);
            Assert.state(matcher.matches(), "Does not match simple duration pattern");
            String suffix = matcher.group(2);
            return (StringUtils.hasLength(suffix) ? Unit.fromSuffix(suffix) : Unit.fromChronoUnit(unit))
                .parse(matcher.group(1));
        }
        @Override
        public String print(Duration value, ChronoUnit unit) {
            return Unit.fromChronoUnit(unit).print(value);
        }
    },

    ISO8601("^[+-]?[pP].*$") {
        @Override
        public Duration parse(String value, ChronoUnit unit) {
            return Duration.parse(value);
        }
        @Override
        public String print(Duration value, ChronoUnit unit) {
            return value.toString();
        }
    };

    private final Pattern pattern;  // 每种style持有自己的正则

    public abstract Duration parse(String value, ChronoUnit unit);
    public abstract String print(Duration value, ChronoUnit unit);

    // 嵌套枚举：时间单位
    enum Unit {
        NANOS  (ChronoUnit.NANOS,   "ns", Duration::toNanos),
        MICROS (ChronoUnit.MICROS,  "us", (d) -> d.toNanos() / 1000L),
        MILLIS (ChronoUnit.MILLIS,  "ms", Duration::toMillis),
        SECONDS(ChronoUnit.SECONDS, "s",  Duration::getSeconds),
        MINUTES(ChronoUnit.MINUTES, "m",  Duration::toMinutes),
        HOURS  (ChronoUnit.HOURS,   "h",  Duration::toHours),
        DAYS   (ChronoUnit.DAYS,    "d",  Duration::toDays);

        private Function<Duration, Long> longValue;  // 方法引用作为字段！

        Unit(ChronoUnit chronoUnit, String suffix, Function<Duration, Long> toUnit) {
            this.longValue = toUnit;
        }

        public long longValue(Duration value) {
            return this.longValue.apply(value);  // 调用函数
        }

        public String print(Duration value) {
            return longValue(value) + this.suffix;  // 10s, 500ms
        }
    }
}
```

两层枚举嵌套 – 外层 `DurationStyle` 每个常量重写 parse/print 抽象方法，内层 `Unit` 每个常量持有 `Function<Duration, Long>` 方法引用。`Duration::toMillis` 这样的方法引用直接作为构造参数传入，运行时调用 `longValue.apply(duration)` 就完成了转换。这就是函数式编程和枚举的深度融合。

* * *

### 枚举的模板方法模式

> 来源：Spring Boot `org.springframework.boot.jdbc.DatabaseDriver`

Spring Boot 支持 20+ 种数据库。`DatabaseDriver` 枚举用**模板方法模式**处理各数据库的差异：基类提供默认行为，个别数据库常量重写 protected 方法：

```java
public enum DatabaseDriver {
    UNKNOWN(null, null),  // Null Object 模式
    H2("H2", "org.h2.Driver", "org.h2.jdbcx.JdbcDataSource", "SELECT 1"),
    MYSQL("MySQL", "com.mysql.cj.jdbc.Driver", ..., "/* ping */ SELECT 1"),

    // HANA 的URL前缀不是 "hana"，是 "sap"
    HANA("HDB", "com.sap.db.jdbc.Driver", ...) {
        @Override
        protected Collection<String> getUrlPrefixes() {
            return Collections.singleton("sap");  // 覆盖默认行为
        }
    },

    // SQL Server 的产品名有两种写法
    SQLSERVER("Microsoft SQL Server", ...) {
        @Override
        protected boolean matchProductName(String productName) {
            return super.matchProductName(productName)
                || "SQL SERVER".equalsIgnoreCase(productName);
        }
    },

    // Firebird 同时支持两种URL前缀
    FIREBIRD("Firebird", ...) {
        @Override
        protected Collection<String> getUrlPrefixes() {
            return Arrays.asList("firebirdsql", "firebird");
        }
    };

    // 默认行为：用枚举名的小写作为URL前缀
    protected Collection<String> getUrlPrefixes() {
        return Collections.singleton(name().toLowerCase(Locale.ENGLISH));
    }

    protected boolean matchProductName(String productName) {
        return this.productName != null && this.productName.equalsIgnoreCase(productName);
    }

    // 静态工厂方法：从 JDBC URL 识别数据库类型
    public static DatabaseDriver fromJdbcUrl(String url) {
        String urlWithoutPrefix = url.substring("jdbc".length()).toLowerCase();
        for (DatabaseDriver driver : values()) {
            for (String urlPrefix : driver.getUrlPrefixes()) {
                if (driver != UNKNOWN && urlWithoutPrefix.startsWith(":" + urlPrefix + ":")) {
                    return driver;
                }
            }
        }
        return UNKNOWN;  // 找不到就返回 UNKNOWN，不是 null
    }
}
```

-   **模板方法模式** ，`getUrlPrefixes()` 和 `matchProductName()` 是 protected 方法，大部分数据库用默认实现，少数（HANA、SQL Server、Firebird）重写它们；
-   **Null Object 模式** ， `UNKNOWN` 常量作为”找不到”的返回值，调用方不用判空；
-   20+ 种数据库的差异**全部内聚在各自的枚举常量里**。

* * *

### 枚举持有Lambda

> 来源：Spring Boot `org.springframework.boot.jdbc.EmbeddedDatabaseConnection`

Spring Boot 需要判断一个 JDBC URL 是否指向内嵌数据库。每种内嵌数据库的判断规则不同，用 `Predicate<String>` Lambda 来表达：

```java
public enum EmbeddedDatabaseConnection {
    NONE  (null, null, null, (url) -> false),
    H2    (EmbeddedDatabaseType.H2,    ..., (url) -> url.contains(":h2:mem")),
    DERBY (EmbeddedDatabaseType.DERBY, ..., (url) -> true),
    HSQLDB(EmbeddedDatabaseType.HSQL,  ..., (url) -> url.contains(":hsqldb:mem:"));

    private final Predicate<String> embeddedUrl;  // Lambda 字段

    boolean isEmbeddedUrl(String url) {
        return this.embeddedUrl.test(url);  // 调用 Predicate
    }

    // 运行时自动探测可用的内嵌数据库
    public static EmbeddedDatabaseConnection get(ClassLoader classLoader) {
        for (EmbeddedDatabaseConnection candidate : values()) {
            if (candidate != NONE
                && ClassUtils.isPresent(candidate.getDriverClassName(), classLoader)) {
                return candidate;
            }
        }
        return NONE;
    }
}
```

`Predicate<String>` Lambda 直接写在枚举常量的构造参数里。H2 检查 URL 里有没有 `:h2:mem`，HSQLDB 检查 `:hsqldb:mem:`，Derby 无条件返回 true（它的所有 URL 都是内嵌的）。每个常量的判断规则一目了然，不需要任何 if-else 分支。

* * *

### 8\. 枚举的纯策略模式

> 来源：Spring Boot `org.springframework.boot.context.config.ConfigDataNotFoundAction`

配置文件找不到时怎么办？Spring Boot 用两行枚举实现了经典的策略模式：

```java
public enum ConfigDataNotFoundAction {

    FAIL {
        @Override
        void handle(Log logger, ConfigDataNotFoundException ex) {
            throw ex;   // 直接抛异常，启动失败
        }
    },

    IGNORE {
        @Override
        void handle(Log logger, ConfigDataNotFoundException ex) {
            logger.trace(LogMessage.format("Ignoring missing config data %s",
                ex.getReferenceDescription()));   // 记日志，继续启动
        }
    };

    abstract void handle(Log logger, ConfigDataNotFoundException ex);
}
```

这是你能见到的最精简的策略模式实现。传统做法需要一个 `Strategy` 接口 + `FailStrategy` 类 + `IgnoreStrategy` 类 + 一个工厂。用枚举？**一个文件，两个常量，一个抽象方法**，完事。

* * *

### 枚举实现接口 + 工厂方法返回匿名实现

> 来源：Tomcat `javax.websocket.CloseReason.CloseCodes`

WebSocket 关闭码有标准定义的（1000-1015），也有用户自定义的（3000-4999）。枚举能覆盖标准码，但自定义码怎么办？Tomcat 的方案：**枚举实现接口，工厂方法对标准码返回枚举常量，对自定义码返回匿名实现**：

```java
public interface CloseCode {
    int getCode();
}

public enum CloseCodes implements CloseReason.CloseCode {
    NORMAL_CLOSURE(1000),
    GOING_AWAY(1001),
    PROTOCOL_ERROR(1002),
    // ... 更多标准码

    public static CloseCode getCloseCode(final int code) {
        // 自定义码范围：返回匿名实现
        if (code > 2999 && code < 5000) {
            return new CloseCode() {
                @Override
                public int getCode() {
                    return code;
                }
            };
        }
        // 标准码：返回枚举常量
        switch (code) {
            case 1000: return NORMAL_CLOSURE;
            case 1001: return GOING_AWAY;
            // ...
            default: throw new IllegalArgumentException("Invalid close code: [" + code + "]");
        }
    }
}
```

枚举实现接口后，返回类型用接口（`CloseCode`）而不是枚举类型。这样工厂方法既能返回预定义的枚举常量，又能返回运行时创建的匿名实现。**有限的枚举和无限的自定义值共存**，类型系统完全统一。

* * *

### 枚举的多维度转换 + 版本兼容

> 来源：RocketMQ `org.apache.rocketmq.common.compression.CompressionType`

RocketMQ 的压缩类型枚举展示了一个实际问题：**协议演进中的向后兼容**。

```java
public enum CompressionType {
    LZ4(1),
    ZSTD(2),
    ZLIB(3);

    private final int value;

    // 维度1：字符串名称 -> 枚举
    public static CompressionType of(String name) {
        switch (name.trim().toUpperCase()) {
            case "LZ4":  return LZ4;
            case "ZSTD": return ZSTD;
            case "ZLIB": return ZLIB;
            default: throw new RuntimeException("Unsupported: " + name);
        }
    }

    // 维度2：数值 -> 枚举（注意版本兼容！）
    public static CompressionType findByValue(int value) {
        switch (value) {
            case 1: return LZ4;
            case 2: return ZSTD;
            case 0: // 旧版本没有压缩类型字段，默认值0，兼容处理
            case 3: return ZLIB;
            default: throw new RuntimeException("Unknown value: " + value);
        }
    }

    // 维度3：枚举 -> 系统标志位
    public int getCompressionFlag() {
        switch (value) {
            case 1: return MessageSysFlag.COMPRESSION_LZ4_TYPE;
            case 2: return MessageSysFlag.COMPRESSION_ZSTD_TYPE;
            case 3: return MessageSysFlag.COMPRESSION_ZLIB_TYPE;
            default: throw new RuntimeException("Unsupported flag: " + value);
        }
    }
}
```

一个枚举要在三个维度间转换：字符串名称、数值编码、系统标志位。`findByValue` 里 `case 0` 兼容旧版本的处理方式值得学习。 **协议升级时枚举也得向后兼容**，这一招在真的精妙，我也是第一见到。

* * *

## 总结

上面提到的这些enum用法，我们日常开发中会用到吗? 估计不太会哦，大家就当是一种知识补充就可以了。

如果你有疑惑，想微信单对单跟我沟通一下，也可以的。我最近刚开了知识星球，感兴趣的可以加入。具体星球有什么内容以及它已经帮到了什么人，可以看一下下面两篇：

-   [做了17年Java开发，我能帮到你什么](https://zhuanlan.zhihu.com/p/2023356820547184529)
-   [最近几天我帮职场人解决了什么问题](https://zhuanlan.zhihu.com/p/2024530597503145397)

目前我的星球有优惠活动，链接如下:

-   [老码头的技术浮生录](https://link.zhihu.com/?target=https%3A//t.zsxq.com/GOrJK)

![](images/135_001.jpg)