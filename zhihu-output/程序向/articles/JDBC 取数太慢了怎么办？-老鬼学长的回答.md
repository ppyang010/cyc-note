---
id: "96667796756"
title: "JDBC 取数太慢了怎么办？"
author: "老鬼学长"
type: zhihu-answer
source: "https://www.zhihu.com/question/495924098/answer/96667796756"
created: "2025-02-09 17:52"
updated: "2025-02-09 17:52"
collected: "2025-02-09 17:52"
downloaded: "2026-08-16"
---
谢邀。

说实话，给JDBC提提速这事儿，我他妈能喷出血泪经验：你们这帮崽子是不是还在用DriverManager.getConnection这种原始人操作？

## 第一刀先砍连接池！

烂大街的破铜烂铁（比如DBCP）赶紧扔，上HikariCP这种超跑级别选手：

```text
// 直接给你看企业级配置
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:mysql://localhost:3306/your_db?useUnicode=true&characterEncoding=utf8&useSSL=false");
config.setUsername("root");
config.setPassword("别他妈用root了行不行");
config.addDataSourceProperty("cachePrepStmts", "true");
config.addDataSourceProperty("prepStmtCacheSize", "250");
config.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
config.setMaximumPoolSize(20); // 连接池大小按业务来，别设成100当土豪

HikariDataSource dataSource = new HikariDataSource(config);
```

这配置一上，连接复用直接告别“创建-销毁”的死亡循环，性能至少提三成！

## 第二刀砍SQL写法

你们这帮人取数就知道无脑全捞！分页不用limit用内存过滤？活该慢得跟驴拉磨似的！

给看正确姿势：

```text
// 分页别在Java内存里搞（Volcano式查询原地爆炸）
String sql = "SELECT id,name FROM big_table LIMIT ? OFFSET ?";
try(PreparedStatement ps = connection.prepareStatement(sql)){
    ps.setInt(1, pageSize);
    ps.setInt(2, (pageNum-1)*pageSize);
    ResultSet rs = ps.executeQuery();
    // 处理结果集
}
```

如果数据实在大得离谱？加个覆盖索引覆盖查询字段，直接骑脸输出性能提升。

## 第三刀必须祭出批量操作大法

一条条insert就是在侮辱数据库尊严，试试Batch猛男套餐：

```text
try(PreparedStatement ps = connection.prepareStatement("INSERT INTO user(name) VALUES (?)")){
    connection.setAutoCommit(false); // 关键！关闭自动提交
    for(int i=0;i<10000;i++){
        ps.setString(1, "用户"+i);
        ps.addBatch();
        if(i % 1000 == 0){
            ps.executeBatch(); // 分批次提交
            ps.clearBatch();
        }
    }
    ps.executeBatch();
    connection.commit(); // 手动提交
}
```

这效率能从10分钟干到3秒信不信？但记住MySQL得在url加上rewriteBatchedStatements=true才能激活真·批量模式！

## 终极暴击：ResultSet调优

别他妈一次性加载全部数据到内存：

```text
Statement stmt = connection.createStatement(
    ResultSet.TYPE_FORWARD_ONLY, 
    ResultSet.CONCUR_READ_ONLY
);
stmt.setFetchSize(100); // 每次从数据库拿100条，而不是全捞
```

就跟打游戏读进度条似的——分段加载才不会被内存撑炸。

喷个警钟：数据库不是ATM机不能瞎取钱！能用索引解决的问题别上JOIN，能查10行别取100行，谁TM让你用select \*的？

最后，分享一个不错的编程导航网站，里面有大量的免费教程供你学习：

[https://www.j301.cn/](https://link.zhihu.com/?target=https%3A//www.j301.cn/)