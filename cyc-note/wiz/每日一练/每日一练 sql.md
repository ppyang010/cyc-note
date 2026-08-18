---
Title: "每日一练 sql"
Url: ""
Author: ""
Origin: "WizNote"
Description: ""
Tags: []
Created: "2017-07-25 18:21:03"
Cover: ""
WizGuid: "f6c67189-3a3b-41d7-9016-fafa82899d98"
WizType: "document"
WizLocation: "/每日一练/"
WizDataMd5: "b6d4165d3342d92839f0d798bf079015"
Modified: "2017-08-20 15:51:46"
WizSyncedAt: "2026-08-18 18:31:49"
---

[https://www.zhihu.com/question/19552975](https://www.zhihu.com/question/19552975)

![[attachments/102433281.png]]

# 创建表

关注表创建语句

表字段

if exists

drop table if exists student;

-- if not exists

create table student (

sno VARCHAR(3) NOT NULL PRIMARY KEY,

sname VARCHAR(4) NOT NULL,

ssex VARCHAR(2) NOT NULL,

sbirthday DATETIME,

class VARCHAR(5)

);

CREATE TABLE if not exists course

(cno VARCHAR(5) NOT NULL PRIMARY KEY,

cname VARCHAR(10) NOT NULL,

tno VARCHAR(10) NOT NULL);

CREATE TABLE score

(sno VARCHAR(3) NOT NULL,

cno VARCHAR(5) NOT NULL,

degree NUMERIC(10, 1) NOT NULL) ;

CREATE TABLE teacher

(tno VARCHAR(3) NOT NULL,

tname VARCHAR(4) NOT NULL, TSEX VARCHAR(2) NOT NULL,

tbirthday DATETIME NOT NULL, PROF VARCHAR(6),

depart VARCHAR(10) NOT NULL);

create table grade(low INT,

upp INT,

rank  VARCHAR(10));

# 练习语句

##1、 查询Student表中的所有记录的Sname、Ssex和Class列。

SELECT sname,ssex,class FROM student;

##2、 查询教师所有的单位即不重复的Depart列。

SELECT  DISTINCT depart from teacher;

##3、 查询Student表的所有记录。

SELECT * from student;

##4、 查询Score表中成绩在60到80之间的所有记录。

SELECT * from score where degree >=60 and degree <=80 ;

##5、 查询Score表中成绩为85，86或88的记录。

SELECT * from score WHERE degree in(85,86,88);

##6、 查询Student表中“95031”班或性别为“女”的同学记录。

SELECT * from student s WHERE s.ssex='女' or s.class='95031';

##7、 以Class降序查询Student表的所有记录。

SELECT * from student ORDER BY class DESC;

##8、 以Cno升序、Degree降序查询Score表的所有记录。

SELECT * from score ORDER BY cno asc ,degree desc;

##9、 查询“95031”班的学生人数。

SELECT * from student where class='95031';

##10、查询Score表中的最高分的学生学号和课程号。

SELECT  sno,cno from score where degree in (SELECT MAX(degree) from score);

##11、查询‘3-105’号课程的平均分。

SELECT AVG(degree) from score where cno='3-105';

##12、查询Score表中至少有5名学生选修的并以3开头的课程的平均分数。

SELECT AVG( degree),cno from score where cno in (

SELECT cno from score where cno like '3%' GROUP BY cno HAVING COUNT(sno)>=5);

##13、查询最低分大于70，最高分小于90的Sno列。

SELECT sno from score where degree >=70 and degree<=90;

##14、查询所有学生的Sname、Cno和Degree列。

SELECT sname,cno,degree from student t LEFT JOIN score s ON t.sno=s.sno;

##15、查询所有学生的Sno、Cname和Degree列。

SELECT t.sno,cno,degree from student t LEFT JOIN score s ON t.sno=s.sno;

##16、查询所有学生的Sname、Cname和Degree列。

SELECT t.sname,cname,degree from student t LEFT JOIN score s ON t.sno=s.sno LEFT JOIN course c on s.cno=c.cno;

##17、查询“95033”班所选课程的平均分。

SELECT AVG(degree) from student t LEFT JOIN score s ON t.sno=s.sno where t.class;

##18.现查询所有同学的Sno、Cno和rank列。

SELECT s.sno,s.cno from score s ,grade g

where s.degree BETWEEN g.low and g.upp

ORDER BY sno, rank ;

##19查询选修“3-105”课程的成绩高于“109”号同学成绩的所有同学的记录。

SELECT *

FROM score a

LEFT JOIN score b on b.sno='109' and b.cno='3-105'

WHERE  a.cno='3-105'  and a.degree>b.degree;

##另一解法：

SELECT A.* FROM SCORE A  WHERE A.CNO='3-105' AND

A.DEGREE>ALL(SELECT DEGREE FROM

SCORE B WHERE B.SNO='109' AND B.CNO='3-105');

##20、查询score中选学一门以上课程的同学中分数为非最高分成绩的记录。

SELECT A.sno ,A.degree FROM SCORE A where EXISTS(

SELECT s.sno  from score s WHERE s.sno=A.sno

GROUP BY s.sno HAVING count(s.cno) > 1

)

and  A.degree not in (

SELECT MAX(degree) from score c where c.sno=A.sno

)

GROUP BY sno;

##21、查询成绩高于学号为“109”、课程号为“3-105”的成绩的所有记录。

SELECT a.*,b.* from score a LEFT JOIN score b on b.sno='109' and b.cno='3-105' where a.cno='3-105' and a.degree >b.degree;

##方案2

select * from score a WHERE a.cno='3-105' and a.degree >All(SELECT b.degree from score b where b.sno='109' and b.cno='3-105');

##22、查询和学号为108的同学同年出生的所有学生的Sno、Sname和Sbirthday列。

SELECT a.* from student a where EXISTS (

SELECT 1 from student b where b.sno='108' and a.Sbirthday=b.Sbirthday

) and a.sno !='108';

##23、查询“张旭“教师任课的学生成绩。

SELECT s.* from score s LEFT JOIN course c on s.cno=c.cno LEFT JOIN teacher t on t.tno =c.tno where t.tname='张旭';

##24、查询选修某课程的同学人数多于5人的教师姓名。

select t.tname from score s left JOIN course c on s.cno=c.cno LEFT JOIN teacher t on c.tno=t.tno GROUP BY s.cno HAVING count(*)>5;

##25、查询95033班和95031班全体学生的记录。

select * from student s where s.class='95033' or s.class='95031' ORDER BY s.class;

##26、查询存在有85分以上成绩的课程Cno.

SELECT DISTINCT s.cno  from score s where s.degree >85;

##27、查询出“计算机系“教师所教课程的成绩表。

SELECT * from score s LEFT JOIN course c on s.cno=c.cno LEFT JOIN teacher t on c.tno=t.tno where t.depart='计算机系';

##28、查询“计算机系”与“电子工程系“不同职称的教师的Tname和Prof。 查询计算机系中与电子工程系职称不同的教师

SELECT * from teacher a where a.PROF not in (

SELECT b.prof FROM teacher b WHERE b.depart='电子工程系'

) and a.depart ='计算机系';

##答案2

SELECT * from teacher a where NOT EXISTS (

SELECT * FROM teacher b WHERE b.depart='电子工程系' and b.prof=a.PROF

) and a.depart ='计算机系';

##29、查询选修编号为“3-105“课程的学升且成绩至少高于一位选修编号为“3-245”的同学的Cno、Sno和Degree,并按Degree从高到低次序排序。

SELECT a.* from score a where a.cno='3-105' and a.degree > ANY(SELECT b.degree from score b where b.cno='3-245' );

##30、查询选修编号为“3-105”且成绩高于所有选修编号为“3-245”课程的同学的Cno、Sno和Degree.

SELECT a.* from score a where a.cno='3-105' and a.degree > ALL(SELECT b.degree from score b where b.cno='3-245' );

##31、查询所有教师和同学的name、sex和birthday.

select s.sname as name ,s.ssex as sex ,s.sbirthday as birthday  from student s

UNION

SELECT t.tname as name ,t.tsex as sex ,t.tbirthday as birthday from teacher t;

##32、查询所有“女”教师和“女”同学的name、sex和birthday.

select s.sname as name ,s.ssex as sex ,s.sbirthday as birthday  from student s WHERE s.ssex='女'

UNION

SELECT t.tname as name ,t.tsex as sex ,t.tbirthday as b

irthday from teacher t WHERE t.tsex='女';

##33、查询成绩比该课程平均成绩低的同学的成绩表。

SELECT b.* from score b where b.degree < (SELECT AVG(a.degree) from score a where a.cno=b.cno  GROUP BY a.cno);

##SELECT AVG(a.degree),a.cno from score a   GROUP BY a.cno;

##34、查询所有任课教师的Tname和Depart.

SELECT * from teacher t  JOIN course c on t.tno=c.tno;

SELECT * from teacher t where  EXISTS (

SELECT * from course c where c.tno=t.tno

);

##35  查询所有未讲课的教师的Tname和Depart.

SELECT * from teacher t where not EXISTS (

SELECT * from course c where c.tno=t.tno

);

##36、查询至少有2名男生的班号。

SELECT s.class from student s where s.ssex='男' GROUP BY s.class HAVING COUNT(s.sno) >=2;

##37、查询Student表中不姓“王”的同学记录。

SELECT * from student s where s.sname not like '王%';

##38、查询Student表中每个学生的姓名和年龄。

SELECT sname,YEAR(NOW())-YEAR(sbirthday) as age from student;

##39、查询Student表中最大和最小的Sbirthday日期值。

(SELECT * from student ORDER BY sbirthday DESC LIMIT 0,1)

UNION

(SELECT * from student ORDER BY sbirthday  LIMIT 0,1);

##40、以班号和年龄从大到小的顺序查询Student表中的全部记录。

SELECT * from student ORDER BY class DESC ,sbirthday asc;

##解法2

SELECT * ,YEAR(NOW())-YEAR(sbirthday) as age from student ORDER BY class DESC , age desc;

##41、查询“男”教师及其所上的课程。

SELECT * from teacher t  JOIN course c on t.tno=c.tno where t.tsex='男';

##42、查询最高分同学的Sno、Cno和Degree列。

SELECT * from score s where s.degree = (SELECT MAX(b.degree) FROM score b);

##43、查询和“李军”同性别的所有同学的Sname.

SELECT a.sname from student a where EXISTS (SELECT 1 from student b where b.sname='李军'  and b.ssex=a.ssex ) and a.sname != '李军';

##44、查询和“李军”同性别并同班的同学Sname.

SELECT a.sname from student a where EXISTS (SELECT 1 from student b where b.sname='李军' and b.class=a.class and b.ssex=a.ssex ) and a.sname != '李军';

##45、查询所有选修“计算机导论”课程的“男”同学的成绩表

SELECT a.* FROM score a LEFT JOIN course b on a.cno=b.cno LEFT JOIN student c on a.sno=c.sno where b.cname='操作系统' and c.ssex='男';

# 函数

注意目前确定可以用函数的地方 为select 和haveing

#### 1字符串与时间互相转换

[mysql 时间与字符串 互相转换](wiz://open_document?guid=600310cb-9cf7-4f03-9a65-af392f2b671b&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

str_to_date  date_format

#### 2时间操作

获取 比较 加减

时间比较 转为为时间格式  然后就可以直接比较  dA between dB and dc

[mysql 日期操作 增减天数、时间转换、时间戳](wiz://open_document?guid=71856163-5ae4-4f15-a4fe-7ab6fea46afa&kbguid=&private_kbguid=d80cc495-0821-48fc-87d8-265551858bc2)

[http://www.cnblogs.com/wenzichiqingwa/archive/2013/03/05/2944485.html](http://www.cnblogs.com/wenzichiqingwa/archive/2013/03/05/2944485.html)

#### 3字符串拼接 与其他 操作

sql string转换成int型 sql截取字符串

select cast(SUBSTRING('ddd25844', PATINDEX('%[0-9]%', 'ddd25844'), 4 )as int)

string转换成int型

cast('字符串型数字' as int)

sql 截取字符串

substring('要截取的字符串','开始截取的索引',截取的个数)

获取字符串特定位置的索引

patindex('匹配的表达式','被取的字符串')

__concat__将两个字段记录合并成一个，即字符串链接；

__SUBSTR__来进行字符串截取字符串函数；

__TRIM__用来去除字符串前后的空白字符；

#### 4去重关键字

DISTINCT

#### 5  IN、ANY、SOME 和 ALL 操作符的使用

MySQL 列子查询及

列子查询是指子查询返回的结果集是 N 行一列，该结果通常来自对表的某个字段查询返回。

一个列子查询的例子如下：

SELECT * FROM article WHERE uid IN(SELECT uid FROM user WHERE status=1)

IN：在指定项内，同 IN(项1,项2,…)。

ANY：与比较操作符联合使用，表示与子查询返回的任何值比较为 TRUE ，则返回 TRUE 。

SOME：ANY 的别名，较少使用。

ALL：与比较操作符联合使用，表示与子查询返回的所有值比较都为 TRUE ，则返回 TRUE 。

[http://www.5idev.com/p-mysql_volumn_subquery.shtml](http://www.5idev.com/p-mysql_volumn_subquery.shtml)

6.WHERE与HAVING的区别

```
FROM：对FROM子句中的前两个表执行笛卡尔积（Cartesian product)(交叉联接），生成虚拟表VT1ON：对VT1应用ON筛选器。只有那些使<join_condition>为真的行才被插入VT2。OUTER(JOIN)：如 果指定了OUTER JOIN（相对于CROSS JOIN 或(INNER JOIN),保留表（preserved table：左外部联接把左表标记为保留表，右外部联接把右表标记为保留表，完全外部联接把两个表都标记为保留表）中未找到匹配的行将作为外部行添加到 VT2,生成VT3.如果FROM子句包含两个以上的表，则对上一个联接生成的结果表和下一个表重复执行步骤1到步骤3，直到处理完所有的表为止。WHERE：对VT3应用WHERE筛选器。只有使<where_condition>为true的行才被插入VT4.GROUP BY：按GROUP BY子句中的列列表对VT4中的行分组，生成VT5.CUBE|ROLLUP：把超组(Suppergroups)插入VT5,生成VT6.HAVING：对VT6应用HAVING筛选器。只有使<having_condition>为true的组才会被插入VT7.SELECT：处理SELECT列表，产生VT8.DISTINCT：将重复的行从VT8中移除，产生VT9.ORDER BY：将VT9中的行按ORDER BY 子句中的列列表排序，生成游标（VC10).TOP：从VC10的开始处选择指定数量或比例的行，生成表VT11,并返回调用者。
```

由上术可知

先执行where

然后group by 在对where之后的结果进行分组

这个结果集中每一行代表一组（一组中其实有多个数据 但是显示的时候处理了）

having 条件

这个条件对上个结果集中每一组进行条件判断  符合的显示 也是每一行代表一组（如果一组中是多个数据但是显示的时候会处理 ）

不过这里一办就对每组进行条件判断或者聚合函数计算 显示想要的哪一行

#### 6mysql datetime、date、time、timestamp区别

我们看看这几个数据库中（mysql、oracle和sqlserver）如何表示时间

mysql数据库：它们分别是 date、datetime、time、timestamp和year。date ：“yyyy-mm-dd”格式表示的日期值 time ：“hh:mm:ss”格式表示的时间值 datetime： “yyyy-mm-dd hh:mm:ss”格式 timestamp： “yyyymmddhhmmss”格式表示的时间戳值 year： “yyyy”格式的年份值。
