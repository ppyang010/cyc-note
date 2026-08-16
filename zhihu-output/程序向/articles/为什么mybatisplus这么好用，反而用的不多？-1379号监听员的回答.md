---
id: "3282783134"
title: "为什么mybatisplus这么好用，反而用的不多？"
author: "1379号监听员"
type: zhihu-answer
source: "https://www.zhihu.com/question/314745062/answer/3282783134"
created: "2023-11-09 16:39"
updated: "2025-09-10 10:45"
collected: "2023-11-09 16:39"
downloaded: "2026-08-16"
---
大部分接触到mybatis-plus的人都有几个误区

1.  用了mybatis-plus，就不应该用mybatis了
2.  用了mybatis-plus，service层就必须继承BaseService，造成sql操作侵入service层
3.  用了mybatis-plus，就必须写QueryWrapper或LambdaQueryWrapper

其实

1.  mybatis-plus是用来增强mybatis的，其提供的单表操作很方便，两者要配合起来使用
2.  如果不希望mybatis-plus侵入service层，就在团队里约定好service层不要继承BaseService就行了
3.  基础的单表操作，用BaseMapper中封装好的方法。  
    BaseMapper中没有的简单的单表操作可以写QueryWrapper或LambdaQueryWrapper等，而且可以在Mapper接口中写default方法，不用写实现类和xml代码。  
    另外，复杂的单表操作和多表联查依然写到mybatis的xml里。

这才是mybatis-plus的最佳实践