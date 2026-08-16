---
id: "3518507166"
title: "如何看待mybatis-plus这个cve漏洞及声明？"
author: "廖雪峰"
type: zhihu-answer
source: "https://www.zhihu.com/question/657590809/answer/3518507166"
created: "2024-06-03 10:54"
updated: "2025-10-08 17:42"
collected: "2024-06-03 10:54"
downloaded: "2026-08-16"
---
这就是mybatis-plus自己傻B，啥需求都敢接。

明明是SaaS应该自己完成的事，非要搞到db框架层自动加talentId。

这些垃圾需求让第三方自己写。

话说回来，大家是怎么能忍受这种写法的？

```text
List<User> userList = userMapper.selectList(
        new QueryWrapper<User>()
                .lambda()
                .ge(User::getAge, 18)
);
```

我自己封装一个jdbc-template不到1000行代码的

[https://github.com/michaelliao/warpdb](https://link.zhihu.com/?target=https%3A//github.com/michaelliao/warpdb)

写法1:

```text
List<User> users = warpdb.from(User.class).where("age>?", 18);
```

写法2:

```text
List<User> users = warpdb.query("select * from User where age>?", 18);
```

* * *

很多人简直就是本末倒置，为了让IDE重构方便就宁愿写一大坨层层嵌套的lambda，也不愿意直接用更有强大表达能力的SQL。

对于CRUD来说，insert/update/delete都不是问题，因为Java类型系统加上一点jpa注解就能实现，复杂的地方其实就是如何构造查询。

查询结果转换Java类是非常简单的，因为SQL查询会返回metadata，主要的复杂问题都是如何构造复杂查询。

类似 where (age < 20 or age > 60) and (state = 1 or state = 2)用sql写非常自然，参数按位置填写或者类似js的template string：

where("(age < ? or age > ?) and (state = ? or state = ?)", 20, 60, 1, 2)

你用querymapper封装完还得把sql写到注释里，而且lambda嵌套错了业务逻辑就错了，编译器检查通过了又有什么用？

mybatis-plus官网的示例代码：

```text
LambdaQueryWrapper<User> lambdaQueryWrapper = new LambdaQueryWrapper<>();
lambdaQueryWrapper.allEq((field, value) -> field.contains("a"), Map.of("id", 1, "name", "老王", "age", null));

// SELECT * FROM user WHERE id = 1 AND name = '老王' AND age IS NULL
```

他们自己都没跑过 age is NULL 应该怎么生成，Map.of()是会抛异常的。is NULL查询不是传参的条件查询。如果我来写会这么写：

```text
where("id = ? and name = ? and age is NULL", 1, "老王");
```

用字符串做where条件其实就一个问题，没有编译期检查，比如jooq的这种写法：

```text
Query query = create.select(field("BOOK.TITLE"), field("AUTHOR.FIRST_NAME"), field("AUTHOR.LAST_NAME"))
                    .from(table("BOOK"))
                    .join(table("AUTHOR"))
                    .on(field("BOOK.AUTHOR_ID").eq(field("AUTHOR.ID")))
                    .where(field("BOOK.PUBLISHED_IN").eq(1948));
// 这个代码其实也挺烦，加个table,field毫无意义，不如直接传字符串
```

要编译检查就得生成代码，多这一步其实很麻烦：

```text
Query query = create.select(BOOK.TITLE, AUTHOR.FIRST_NAME, AUTHOR.LAST_NAME)
                    .from(BOOK)
                    .join(AUTHOR)
                    .on(BOOK.AUTHOR_ID.eq(AUTHOR.ID))
                    .where(BOOK.PUBLISHED_IN.eq(1948));
```

限于java语法，用 where("age > ? and age < ?", 20, 30) 完全是可以接受的。

如果一个系统大多数是简单查询，直接写sql简单明了，比lambda表达式可读性强太多；

如果一个系统大多数是复杂查询，还需要dba优化的那种，那更需要直接写sql了，因为sql本身就够复杂了，再转成嵌套的lambda看的人不得疯了。

绝大多数系统根本没有迁移数据库的需求，针对数据库特定的sql优化如果必不可少，不写sql难道写个插件？

* * *

如果有足够的时间，可以写一个maven插件，用antlr解析sql语法，配合类型+jpa注解，检查字段名称就可以放在编译期：

```text
List<User> list = db.from(User.class)
                    .where("email=? and passwd=?", email, password)
                    .first();
```

* * *

最后吐槽一下很多Java开发的执念：

-   SQL必须在XML中，Java代码中不得出现SQL。
-   改SQL只需要改XML，不用动Java代码。
-   不得以任何字符串方式在Java代码中写SQL，务必写成lambda。

还好go/node/python/rust/...这些语言压根就不考虑XML，人家直接把SQL写到代码里。