---
id: "3332834266"
title: "数据库里创建时间字段用create_time、created_at还是created_time更适合？"
author: "Snowflyt"
type: zhihu-answer
source: "https://www.zhihu.com/question/265155157/answer/3332834266"
created: "2023-12-20 21:26"
updated: "2024-07-03 11:16"
collected: "2023-12-20 21:26"
downloaded: "2026-08-16"
---
对于日期时间我从来不用 time，我的观点很明确，datetime 表示日期时间、date 表示日期、time 只能用来表示不带日期的纯时间……所以我会命名为 `creationDateTime`……

我不止一次见别人嫌弃我这么写太长了，所以后来我又养成了一种习惯，如果是那种基本上每个 Entity 都会带的用来记录元数据的字段，我就命名为 `createdAt`、`updatedAt` 这种。对于这类 `xxxAt`，我只会在 datetime 的情况下使用，并且只在应用频繁与广泛的时候使用它们，避免其他人读我代码的时候乍一看没搞明白这个 `At` 指 datetime、date 还是 time——毕竟大家看到 `createdAt` 和 `updatedAt` 这种，应该可以无异议地认为这东西是个 datetime 的，不会产生歧义，在其他情况下就不一定了。

* * *

挺有意思一件事，起初我只是简单陈述我的观点，没想到遇到了这么多不理解。那我就简单讲一下我习惯于这么干的考量——当然，你总是能归根结底说一句“不就是强迫症”，那就没什么聊的必要了。

有人认为几乎在所有场景下都会使用 datetime，而 date 和 time 使用较少，因此这么命名算是纯纯折磨自己。我倒觉得不见得，在我经手的很多系统内，都会存在一些类似“任务管理模块”的东西，它们有些只是给人工管理任务做一些 CRUD，有些涉及自动任务执行。在这样的系统中，date 格式是比较常见的——许多时候会将一些任务或相关实体直接按日期归类，或者有些干脆就是按日期查询的。如果对这种情况有人还质疑其合理性的话，那么对于定时任务情况，要表示一个从某个起始日期到某个结束日期，每天在某些时间点执行的任务，就一定要结合 date 和 time 了，不可能只用 datetime 就表示的——除非直接生成好所有可能的 datetime 直接存数据库里，那你还挺天才的。再说说不可能有人不曾经练手过、或者至少在教程中看到过的“教务管理系统”模板，假如课表灵活一些，不定死在某些时间段中，也是必须要用 time 存时间段的。

按日期直接归类其实是挺自然和直接的，在我接触过的一些系统里 date 出现得并不少——也许总量比起 datetime 要少得多，但存在感是不低的。

有人提到，类型信息本身就能表明字段的意义——你说得没错，但你大概没有考虑过前端的体验，他们可通常只有个啥都能放的 `Date` 同时表示 datetime 和 time，即使第三方时间处理库也通常这么做（我希望前端还没有被开除程序员籍）。为前端考虑的话，区分 datetime 和 date 显然是最容易一眼看出来的解决方案。当然，写文档无论是 JavaDoc 还是 JSDoc 都能让你在鼠标悬浮在属性上时看到它的信息，所以有人提议写注释上得了——这就看个人习惯了，我只是习惯于写得更容易看到一些。

另外在传输时，日期时间这类通常没有一个专门的类型用来区分。在 JSON 中，datetime 和 date 显然都只能写成字符串，有些人为了偷懒会直接 serialize 成 ISO 8061 格式的日期时间，导致在调试 Payload 时不方便寻思后边时分秒全是零的到底是 datetime 还是 date. 并且还是考虑前端的问题，`Date` 这东西要做自动 serialize 的话可没法区分 datetime 还是 date，只能全部 serialize 成 datetime——当然，让前端每次手动 serialize 一下也是个方法，就是稍嫌麻烦。

实话实说，我做的系统里前后端的全部日期时间相关的通信都是采用 ISO 8061 格式的 UTC 时间的，精确到毫秒，比如 `2023-12-21T09:59:28.661Z`，这是 JS 中 `Date` 默认的 serialize 格式。我认为带时区的时间格式永远是最精确的，即使这系统暂时看来没有任何走出国门的可能我也要这么做，很多东西就是要在一开始打好地基，因为我有严重的强迫症。

*另外，显然用时间戳可以解决时区问题，代价是不好看，不方便调试。*

对于 Java 后端程序员，我贴心地准备了一个工具类用来解析这东西——我知道很多人在 Java 里处理时区相关问题时总是弄不利索，最后只会手动小时 `+8` 解决：

```java
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.regex.Pattern;

public class DateTimeStringUtils {
    private static final ZoneId SYSTEM_DEFAULT_ZONE_ID = ZoneId.systemDefault();

    private static final Pattern ISO_8061_DATE_TIME_STRING_PATTERN = Pattern.compile(
            "^\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d((:[0-5]\\d)|(:[0-5]\\d\\.\\d+))?(Z|[+-]\\d{2}:\\d{2})?$");
    private static final Pattern SIMPLE_DATE_TIME_STRING_PATTERN = Pattern
            .compile("^\\d{4}-[01]\\d-[0-3]\\d [0-2]\\d:[0-5]\\d((:[0-5]\\d)|(:[0-5]\\d\\.\\d+))?$");
    private static final Pattern ZONED_DATE_TIME_STRING_PATTERN = Pattern.compile(".+(Z|[+-]\\d{2}:\\d{2})$");

    private DateTimeStringUtils() {
    }

    /**
     * Check if a string is a valid ISO 8061 date time string or a simple date time
     * string.
     * 
     * <pre>
     * {@code
     * validate("2018-01-01T00:00"); // -> true
     * validate("2018-01-01T00:00Z"); // -> true
     * validate("2018-01-01T00:00+09:00"); // -> true
     * 
     * validate("2018-01-01T00:00:00"); // -> true
     * validate("2018-01-01T00:00:00Z"); // -> true
     * validate("2018-01-01T00:00:00+09:00"); // -> true
     * 
     * validate("2018-01-01T00:00:00.000"); // -> true
     * validate("2018-01-01T00:00:00.000Z"); // -> true
     * validate("2018-01-01T00:00:00.000+09:00"); // -> true
     * 
     * validate("2018-01-01 00:00"); // -> true
     * validate("2018-01-01 00:00:00"); // -> true
     * validate("2018-01-01 00:00:00.000"); // -> true
     * 
     * validate("2018-01-01"); // -> false
     * }
     * </pre>
     * 
     * @param str
     * @return
     */
    public static boolean validate(String str) {
        return ISO_8061_DATE_TIME_STRING_PATTERN.matcher(str).matches()
                || SIMPLE_DATE_TIME_STRING_PATTERN.matcher(str).matches();
    }

    /**
     * Base implementation of {@link #isZoned(String)} without validation.
     * 
     * @param str
     * @return
     */
    private static boolean baseIsZoned(String str) {
        return ZONED_DATE_TIME_STRING_PATTERN.matcher(str).matches();
    }

    /**
     * Check if a date time string is a zoned date time string.
     * 
     * <pre>
     * {@code
     * isZoned("2018-01-01T00:00:00"); // -> false
     * isZoned("2018-01-01T00:00:00Z"); // -> true
     * isZoned("2018-01-01T00:00:00+09:00"); // -> true
     * }
     * </pre>
     * 
     * @param str
     * @return
     * 
     * @throws IllegalArgumentException if the string is not a valid date time
     *                                  string
     */
    public static boolean isZoned(String str) {
        if (!validate(str))
            throw new IllegalArgumentException("Invalid date time string: " + str);
        return baseIsZoned(str);
    }

    /**
     * Base implementation of {@link #toISO8061(String)} without validation.
     * 
     * @param str
     * @return
     */
    private static String baseToISO8061(String str) {
        if (SIMPLE_DATE_TIME_STRING_PATTERN.matcher(str).matches())
            return str.substring(0, 10) + "T" + str.substring(11);
        return str;
    }

    /**
     * Replace space with `T` if it is a simple date time string.
     * 
     * <pre>
     * {@code
     * toISO8061("2018-01-01 00:00"); // -> "2018-01-01T00:00"
     * toISO8061("2018-01-01 00:00:00"); // -> "2018-01-01T00:00:00"
     * toISO8061("2018-01-01 00:00:00.000"); // -> "2018-01-01T00:00:00.000"
     * }
     * </pre>
     * 
     * @param str
     * @return
     * 
     * @throws IllegalArgumentException if the string is not a valid date time
     *                                  string
     */
    public static String toISO8061(String str) {
        if (!validate(str))
            throw new IllegalArgumentException("Invalid date time string: " + str);
        return baseToISO8061(str);
    }

    /**
     * Base implementation of {@link #parse(String)} without validation.
     * 
     * @param str
     * @return
     */
    private static LocalDateTime baseParse(String str) {
        String normalized = baseToISO8061(str);

        if (!baseIsZoned(normalized))
            return LocalDateTime.parse(normalized);

        return ZonedDateTime.parse(normalized).withZoneSameInstant(SYSTEM_DEFAULT_ZONE_ID).toLocalDateTime();
    }

    /**
     * Parse a date time string to {@link LocalDateTime}.
     * 
     * <pre>
     * {@code
     * parse("2018-01-01 00:00"); // -> 2018-01-01T00:00
     * parse("2018-01-01 00:00:00"); // -> 2018-01-01T00:00
     * parse("2018-01-01 00:00:00.000"); // -> 2018-01-01T00:00
     * 
     * parse("2018-01-01T00:00"); // -> 2018-01-01T00:00
     * parse("2018-01-01T00:00Z"); // -> 2018-01-01T08:00
     * parse("2018-01-01T00:00+09:00"); // -> 2017-12-31T23:00
     * 
     * parse("2018-01-01T00:00:00"); // -> 2018-01-01T00:00
     * parse("2018-01-01T00:00:00Z"); // -> 2018-01-01T08:00
     * parse("2018-01-01T00:00:00+09:00"); // -> 2017-12-31T23:00
     * 
     * parse("2018-01-01T00:00:00.000"); // -> 2018-01-01T00:00
     * parse("2018-01-01T00:00:00.000Z"); // -> 2018-01-01T08:00
     * parse("2018-01-01T00:00:00.000+09:00"); // -> 2017-12-31T23:00
     * }
     * </pre>
     * 
     * @param str
     * @return
     * 
     * @throws IllegalArgumentException if the string is not a valid date time
     *                                  string
     */
    public static LocalDateTime parse(String str) {
        if (!validate(str))
            throw new IllegalArgumentException("Invalid date time string: " + str);
        return baseParse(str);
    }

    public static void main(String[] args) {
        System.out.println(parse("2018-01-01 00:00")); // 2018-01-01T00:00
        System.out.println(parse("2018-01-01 00:00:00")); // 2018-01-01T00:00
        System.out.println(parse("2018-01-01 00:00:00.000")); // 2018-01-01T00:00

        System.out.println(parse("2018-01-01T00:00")); // 2018-01-01T00:00
        System.out.println(parse("2018-01-01T00:00Z")); // 2018-01-01T08:00
        System.out.println(parse("2018-01-01T00:00+09:00")); // 2017-12-31T23:00

        System.out.println(parse("2018-01-01T00:00:00")); // 2018-01-01T00:00
        System.out.println(parse("2018-01-01T00:00:00Z")); // 2018-01-01T08:00
        System.out.println(parse("2018-01-01T00:00:00+09:00")); // 2017-12-31T23:00

        System.out.println(parse("2018-01-01T00:00:00.000")); // 2018-01-01T00:00
        System.out.println(parse("2018-01-01T00:00:00.000Z")); // 2018-01-01T08:00
        System.out.println(parse("2018-01-01T00:00:00.000+09:00")); // 2017-12-31T23:00
    }
}
```

* * *

评论区的一些观点拓展了我的思路，正好借机会谈谈关于“规范”的问题。

程序员中总有一些神秘的圣战问题——我该用几个空格当缩进还是用 Tab？我该用 snake\_case 还是 camelCase 还是小众些的 kebab-case（大多数语言不支持）？我花括号该写在上一行末尾还是另起一行或者仅在函数/类定义时才另起一行？人们的观点五花八门，谁也说服不了谁。顺便我支持二空格缩进、camelCase（如果支持 kebab-case 我就换成 kebab-case）和花括号永远写在上一行末尾。

但是如果我这时跳出来说——我支持用三个空格缩进，用 Foo\_Bar\_Baz 命名——大多数人就会感到非常震撼甚至开始讨厌我。只是因为这种“独特”的说法挑战了多数人的认知而已，但仔细想象三个空格作为缩进有什么不对呢？比二空格看着层次更清楚一点，但如果回调函数太多又比四空格看着舒服一些；Foo\_Bar\_Baz 也很清楚，每个单词都用下划线分隔得清清楚楚，如果遇到字母缩写如 HTML 和 XML 也可以直接就全大写字母写上去，不比 snake\_case 多占字符而且反而更加清楚，有什么不好呢？同理 Foo-Bar-Baz 也没什么不好。

我还可以和大家讲讲我的其他常规命名约定。例如我也习惯于区分 path 和 pathname，前者更多表示目录路径而后者表示文件路径——尽管在几乎所有编程语言的标准库设计中都没怎么考虑区分这两者，但我会尽量在代码中用命名表示我的用意。如果你是第一次看到这种说法，或许会和突然有个人冒出来说他喜欢用三个空格当缩进一样困惑——但这种约定并没有显而易见的坏处，甚至和区分 date 与 datetime 一样还有一些微妙的好处，有什么不可接受的呢？

但这并不意味着我一定要和已有系统中的某些设计过不去。我要写 Rust 我就不至于写 camelCase 和所有人过不去，特别是造轮子时——就像我给 Python 造轮子也总是用四空格作为缩进和 snake\_case，尽管实话说有些作者不那么在意 PEP 8. 即使是我比较讨厌 Go 用 Tab 作为缩进的设计，我写 Go 时也肯定用 Tab. 这并不是说我人格分裂，而是我认同有一份社区一致约定的代码规范就要遵守它，就算我不认可它我也会尝试去遵守，要不然大家都不认可各自的代码就总会千奇百怪，这对编程语言社区来说不是一件好事，一点也不是。

同样的，如果我接手的一个系统已经用了 date 当作 datetime 的简称，那我说什么也不会打破这个惯例——除非这个系统允许搞点微服务出来，那我可能考虑在微服务里推广我的约定和惯例。在同一个系统里维持不同的约定和规范肯定也不是一件好事，一致性永远要优先于其他一切。

但是大家显然也能从我的偏好中发现我自身的一套命名逻辑，即尽可能考虑更多情况以消除潜在歧义——当然这不能太过分，例如我命名变量从不会考虑匈牙利命名法，我认为在名称里带上额外的类型信息这是相当多余和干扰视觉的。实际上 date 和 datetime 这套逻辑稍微有点“越界”的意思了，因为在 Java 这样的编程语言中是使用不同的类区分它们的，但对于字符串来说这样的区分仍然是有必要的，所以我还是习惯于这么设计。说实话，对于 Java 或 C# 中的 interface 我一般的观点也是不该加那个 I 前缀，因为它们在代码里都充当 type 而且是可以直接区分的，加 I 其实不太利于抽象，但我写 C# 也仍会愿意遵照微软那套规范加个 I 前缀。

归根结底只是约定不同。如果你读着不认同我也没什么意见，你可以当又学习了人类的多样性然后吐槽一句“第一次见有人这么用的，感觉有点怪”，这也没什么问题。