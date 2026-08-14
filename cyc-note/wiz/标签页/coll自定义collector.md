---
Title: "coll自定义collector"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2023-06-05 19:04:45"
Cover: ""
WizGuid: "358c6397-5747-493e-9b26-7a411271f7c4"
WizType: ""
WizLocation: "/标签页/"
WizDataMd5: "805bb0fb20eadde78e4f14c1c8820141"
Modified: "2023-06-05 23:58:35"
WizSyncedAt: "2026-08-14 22:20:57"
---

[guava Collectors - Google 搜索](https://www.google.com/search?q=guava++Collectors&newwindow=1&sxsrf=APwXEde-ZQZMpMmzv0nkPDXhfuVXZP1T-A%3A1685957197853&ei=Tap9ZKDYM_HdseMP0ICGQA&ved=0ahUKEwjgson_56v_AhXxbmwGHVCAAQgQ4dUDCBA&uact=5&oq=guava++Collectors&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyBggAEAgQHjIGCAAQBRAeOgcIIxCwAxAnOgoIABBHENYEELADOgcIIxCKBRAnOgQIIxAnOgcIIxCxAhAnOgcIABCABBAKSgQIQRgAUIcRWLdaYKtfaANwAXgBgAGYA4gBxB6SAQcyLTMuNy4ymAEAoAEBoAECwAEByAEK&sclient=gws-wiz-serp#ip=1)
[Guava类库学习--Table(双键的Map)_guava 双键map_Bazingaea的博客-CSDN博客](https://blog.csdn.net/Bazingaea/article/details/51233969)
[你不知道的 Guava Collect，都在这了 - 掘金](https://juejin.cn/post/7156155294182014984)
[Guava类库学习--Table(双键的Map)_guava 双键map_Bazingaea的博客-CSDN博客](https://blog.csdn.net/Bazingaea/article/details/51233969)
[guava table 自定义collector - Google 搜索](https://www.google.com/search?q=+guava+table+%E8%87%AA%E5%AE%9A%E4%B9%89collector&newwindow=1&sxsrf=APwXEddjgdDX9tfkHqeKtYKntsR5KCiNkQ%3A1685956118433&ei=FqZ9ZLHvGZyPseMPjJq3qAc&ved=0ahUKEwix0q7846v_AhWcR2wGHQzNDXUQ4dUDCBA&uact=5&oq=+guava+table+%E8%87%AA%E5%AE%9A%E4%B9%89collector&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQogQyBQgAEKIEMgUIABCiBDoKCAAQRxDWBBCwAzoECCMQJ0oECEEYAFDkGFiyMmCiOGgCcAF4AIAB4wKIAd0HkgEFMi0xLjKYAQCgAQGgAQLAAQHIAQo&sclient=gws-wiz-serp)
[Java Stream 自定义Collector - cd_along - 博客园](https://www.cnblogs.com/cd-along/p/14702435.html)
[Java8 Stream 自定义收集器Collector - 腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/old/1710047)
[java 泛型 extends super - Google 搜索](https://www.google.com/search?q=java+%E6%B3%9B%E5%9E%8B+extends+super&oq=java+%E6%B3%9B%E5%9E%8B+&aqs=chrome.5.69i57j0i12i512l2j0i512j0i12i512j0i512l2j0i12i512l3.5095j0j1&sourceid=chrome&ie=UTF-8)
[Java泛型中extends和super的理解_Franco蜡笔小强的博客-CSDN博客](https://blog.csdn.net/w372426096/article/details/78081552)

[java 泛型详解-绝对是对泛型方法讲解最详细的，没有之一 - little fat - 博客园](https://www.cnblogs.com/coprince/p/8603492.html)

package cn.dxy.exam.ms.util; import com.google.common.collect.HashBasedTable; import java.util.Set; import java.util.function.BiConsumer; import java.util.function.BinaryOperator; import java.util.function.Function; import java.util.function.Supplier; import java.util.stream.Collector; /** * @author ccy * @description * @time 2023/6/5 17:16 */ public class TableCollectorsImpl<T, A, R> implements Collector<T, A, R> { private final Supplier<A> supplier; private final BiConsumer<A, T> accumulator; private final BinaryOperator<A> combiner; private final Function<A, R> finisher; private final Set<Characteristics> characteristics; public static <T, A, R> Collector <T, A, R> ofTableCollectors() { Supplier tableSupplier = HashBasedTable::create; return new TableCollectorsImpl(tableSupplier,null,null,null,null); } TableCollectorsImpl(Supplier<A> supplier, BiConsumer<A, T> accumulator, BinaryOperator<A> combiner, Function<A, R> finisher, Set<Characteristics> characteristics) { this.supplier = supplier; this.accumulator = accumulator; this.combiner = combiner; this.finisher = finisher; this.characteristics = characteristics; } @Override public Supplier<A> supplier() { return supplier; } @Override public BiConsumer<A, T> accumulator() { return accumulator; } @Override public BinaryOperator<A> combiner() { return combiner; } @Override public Function<A, R> finisher() { return finisher; } @Override public Set<Characteristics> characteristics() { return characteristics; } }

```
x
```

1

```
package cn.dxy.exam.ms.util;
```

2

```

```

3

```
import com.google.common.collect.HashBasedTable;
```

4

```

```

5

```
import java.util.Set;
```

6

```
import java.util.function.BiConsumer;
```

7

```
import java.util.function.BinaryOperator;
```

8

```
import java.util.function.Function;
```

9

```
import java.util.function.Supplier;
```

10

```
import java.util.stream.Collector;
```

11

```

```

12

```
/**
```

13

```
 * @author ccy
```

14

```
 * @description
```

15

```
 * @time 2023/6/5 17:16
```

16

```
 */
```

17

```
public class TableCollectorsImpl<T, A, R> implements Collector<T, A, R> {
```

18

```
    private final Supplier<A> supplier;
```

19

```
    private final BiConsumer<A, T> accumulator;
```

20

```
    private final BinaryOperator<A> combiner;
```

21

```
    private final Function<A, R> finisher;
```

22

```
    private final Set<Characteristics> characteristics;
```

23

```

```

24

```

```

25

```
    public static <T, A, R> Collector <T, A, R> ofTableCollectors() {
```

26

```
        Supplier tableSupplier = HashBasedTable::create;
```

27

```
        return new TableCollectorsImpl(tableSupplier,null,null,null,null);
```

28

```
    }
```

29

```

```

30

```

```

31

```
    TableCollectorsImpl(Supplier<A> supplier,
```

32

```
                        BiConsumer<A, T> accumulator,
```

33

```
                        BinaryOperator<A> combiner,
```

34

```
                        Function<A, R> finisher,
```

35

```
                        Set<Characteristics> characteristics) {
```

36

```
        this.supplier = supplier;
```

37

```
        this.accumulator = accumulator;
```

38

```
        this.combiner = combiner;
```

39

```
        this.finisher = finisher;
```

40

```
        this.characteristics = characteristics;
```

41

```
    }
```

42

```

```

43

```

```

44

```
    @Override
```

45

```
    public Supplier<A> supplier() {
```

46

```
        return supplier;
```

47

```
    }
```

48

```

```

49

```
    @Override
```

50

```
    public BiConsumer<A, T> accumulator() {
```

51

```
        return accumulator;
```

52

```
    }
```

53

```

```

54

```
    @Override
```

55

```
    public BinaryOperator<A> combiner() {
```

56

```
        return combiner;
```

57

```
    }
```

58

```

```

59

```
    @Override
```

60

```
    public Function<A, R> finisher() {
```

61

```
        return finisher;
```

62

```
    }
```

63

```

```

64

```
    @Override
```

65

```
    public Set<Characteristics> characteristics() {
```

66

```
        return characteristics;
```

67

```
    }
```

68

```
}
```

69

```

```
