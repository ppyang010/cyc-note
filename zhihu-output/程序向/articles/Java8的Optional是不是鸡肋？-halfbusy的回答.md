---
id: "2246870053"
title: "Java8的Optional是不是鸡肋？"
author: "halfbusy"
type: zhihu-answer
source: "https://www.zhihu.com/question/382242885/answer/2246870053"
created: "2021-11-28 18:53"
updated: "2021-12-10 00:07"
collected: "2021-11-28 18:53"
downloaded: "2026-08-16"
---
哈哈，鸡肋是食之无味，弃之可惜。但现在用很多Java API， optional 已经成标准输入输出类型了，想不用都难。稍稍看看 java.util 集合API：Interface Collection<E>，Interface List<E>等，都增加了optional operation。

关于空指针异常处理，出过好几种方案，optional是一种，注解是一种，空对象模式是一种，JSR-303规则也有空检查说明，JSR-303 是 JAVA EE 6 中的一项子规范，在字段是增加一层过滤器验证，可以保证数据的合法性。Spring MVC 3.x 之中也大力支持 JSR-303。

Java 6的时候，我是通过引入第三方包google guava中使用optional，Java 8之后将optional拥入怀中，Java 9还对Optional改进了，Java 11又对optional加强了。 看java版本进化的态度，optional应该是鸡腿，而不是鸡肋。

Java对象编程，空对象主要是MVC层、数据层外部引入，比如上传了一个空对象，或数据层查询出来一个空对象。防御性编程是良好的编程习惯，《代码整洁之道》中推荐的，任何方法不要传递null，不要返回null。所以，在使用“外部引入”的对象之前，提前进行校验。spring mvc， spring jpa中新版本的API就有不少使用到Optional。

spring mvc三段代码可以对比一下：

```jsp
@Controller
public class EmployeeController {

  @RequestMapping("/employee")
  @ResponseBody
  public String getEmployeeByDept (@RequestParam("dept") String deptName) {
      return "test response for dept: " + deptName;
  }
    .............
}
```

上面的代码，如果没有请求dept查询参数，会报400错误。

为了避免注入失败，400错误，通过注解 required =false，表示dept查询参数可忽略，不会报错。

```java
@Controller
public class EmployeeController {
    .............
  @RequestMapping("/employee2")
  @ResponseBody
  public String getEmployeeByDept2 (@RequestParam(value = "dept", required = false)
                                              String deptName) {
      return "test response for dept: " + deptName;
  }
    .............
}
```

  
引入Optional之后，可以替换 required，其实这也是spring 向标准的Java SE/EE API 看齐。

```jsp
@Controller
public class EmployeeController {
    .............
  @RequestMapping("/employee3")
  @ResponseBody
  public String getEmployeeByDept3 (@RequestParam("dept") Optional<String> deptName) {
      return "test response for dept: " + (deptName.isPresent() ? deptName.get() :
                "using default dept");
  }
}
```

  

在Spring Data JPA 2.0 的CrudRepository、SimpleJpaRepository的API

```text
Optional<T>	findById(ID id) 
<S extends T>Optional<S>	findOne(Example<S> example) 
Optional<T>	findOne(Specification<T> spec)
```