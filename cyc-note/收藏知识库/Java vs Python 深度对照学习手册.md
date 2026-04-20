好的，这是一份专门为 Java 开发者定制的深度对比学习资料。我将从**语法基础**、**核心特性**、**面向对象**、**异常处理**、**并发编程**等多个维度进行逐行代码级的对比解析。

---

# Java vs Python 深度对照学习手册

## 🎯 核心理念差异

在开始代码对比前，首先要理解两者设计哲学的根本不同，这将决定你的编码风格：

| 特性 | Java | Python |
| :--- | :--- | :--- |
| **类型系统** | **静态类型** (Static Typing)<br>变量必须先定义类型，编译期检查。 | **动态类型** (Dynamic Typing)<br>变量类型在运行时确定，无需声明。 |
| **运行机制** | **编译型** (Compile to Bytecode)<br>源码 -> .class 字节码 -> JVM 运行。 | **解释型** (Interpreted)<br>源码 -> Python 解释器逐行执行（底层也有 .pyc 字�节码）。 |
| **编程范式** | **面向对象** (Strict OOP)<br>一切皆对象，所有代码必须在类中。 | **多范式** (Multi-paradigm)<br>面向对象、函数式、过程式混合，脚本化程度高。 |
| **语法风格** | **显式冗长** (Verbose)<br>强调结构清晰，代码量大。 | **简洁优雅** (Concise)<br>强调可读性，代码量通常少 1/3 到 1/5。 |
| **代码块** | **大括号** `{}` | **缩进** (Indentation)<br>缩进代表层级，强制代码整洁。 |

---

## 模块一：基础语法与数据类型

### 1. 变量声明与类型

**Java (强类型，显式声明)**
```java
// 必须指定类型
int a = 10;
String name = "Alice";
double price = 99.9;
boolean isValid = true;

// 类型错误在编译期报错
// a = "Hello"; // 编译失败
```

**Python (动态类型，自动推断)**
```python
# 无需指定类型，解释器自动推断
a = 10
name = "Alice"
price = 99.9
is_valid = True  # 注意首字母大写

# 动态改变类型（合法，但不推荐滥用）
a = "Hello" # 现在a变成了字符串

# 类型提示 (Type Hints) - Python 3.5+ 新增，类似 TypeScript
# 这只是注释，不强制运行，但 IDE 会提示
age: int = 25 
```

**💡 关键点：** Java 变量是“盒子”，定义了只能装什么；Python 变量是“标签”，可以随时贴在不同的对象上。

### 2. 基本数据类型对照表

| 类别 | Java | Python | 备注 |
| :--- | :--- | :--- | :--- |
| **整数** | `byte`, `short`, `int`, `long` | `int` | Python 整数无精度限制，不会溢出。 |
| **浮点数** | `float`, `double` | `float` | Python 默认双精度。 |
| **布尔** | `boolean` (`true`/`false`) | `bool` (`True`/`false`) | Python 首字母大写。 |
| **空值** | `null` | `None` | Python 用 `is None` 判断。 |
| **字符串** | `String` (引用类型) | `str` | Python 单引号 `'...'` 和双引号 `"..."` 效果相同。 |
| **字符** | `char` | 无 (`str` 长度为1) | Python 无单独字符类型。 |

### 3. 字符串操作详解

**Java**
```java
String s1 = "Hello";
String s2 = new String("World");

// 拼接
String result = s1 + " " + s2;

// 格式化
String formatted = String.format("Name: %s, Age: %d", "Alice", 25);

// 多行字符串 (Java 15+ Text Block)
String json = "{\n  \"name\": \"Alice\"\n}";

// 字符串操作
s1.equals(s2); // 比较内容
s1.length();   // 长度
s1.split(" "); // 分割
```

**Python**
```python
s1 = "Hello"
s2 = 'World' # 单双引号通用

# 拼接 (推荐 f-string)
result = f"{s1} {s2}"  # 格式化字符串

# 多行字符串 (原生支持)
json_str = """
{
  "name": "Alice"
}
"""

# 字符串操作
s1 == s2        # 比较内容 (Python 直接用 == 比较值，而非 is)
len(s1)         # 长度 (内置函数，而非方法)
s1.split(" ")   # 分割
s1.upper()      # 大写
",".join(['a', 'b']) # Join操作
```

### 4. 运算符差异

| 运算符 | Java | Python | 说明 |
| :--- | :--- | :--- | :--- |
| **整除** | `/` (整数相除得整数) | `//` | Python `/` 总得浮点数，`//` 得整数。 |
| **幂运算** | `Math.pow(2, 3)` | `2 ** 3` | Python 原生支持幂运算符。 |
| **逻辑非** | `!true` | `not True` | Python 使用英文关键字。 |
| **逻辑与/或** | `&&`, `||` | `and`, `or` | Python 使用英文关键字。 |
| **三元运算** | `a > b ? a : b` | `a if a > b else b` | Python 语法结构不同。 |

---

## 模块二：控制流

### 1. 条件判断

**Java**
```java
int score = 85;
if (score >= 90) {
    System.out.println("A");
} else if (score >= 60) {
    System.out.println("B");
} else {
    System.out.println("C");
}
```

**Python**
```python
score = 85
# 注意：条件后必须有冒号 :
if score >= 90:
    print("A")
elif score >= 60: # else if 缩写为 elif
    print("B")
else:
    print("C")
```

**💡 Python 特性：链式比较**
```python
# Java: if (x >= 0 && x <= 10)
x = 5
if 0 <= x <= 10:  # Python 支持数学写法
    print("在范围内")
```

### 2. 循环结构

**Java (灵活但繁琐)**
```java
// 1. 经典 For 循环
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}

// 2. 增强 For 循环
int[] arr = {1, 2, 3};
for (int num : arr) {
    System.out.println(num);
}
```

**Python (高度抽象)**
```python
# 1. for-in 循环 (类似 Java 增强 for)
# range(5) 生成序列 [0, 1, 2, 3, 4]
for i in range(5):
    print(i)

# range(start, end, step)
for i in range(0, 10, 2): # 0, 2, 4, 6, 8
    print(i)

# 2. 遍历列表
arr = [1, 2, 3] # Python 列表
for num in arr:
    print(num)

# 3. 同时获取索引和值 (类似 Java 的 fori + arr[i])
for index, value in enumerate(arr):
    print(f"Index: {index}, Value: {value}")
```

### 3. Switch vs Match

**Java (JDK 8 之前)**
```java
String day = "MON";
switch (day) {
    case "MON":
    case "TUE":
        System.out.println("工作日");
        break;
    case "SUN":
        System.out.println("休息日");
        break;
    default:
        System.out.println("未知");
}
```
*(注：Java 12+ 引入了 Switch 表达式，更接近函数式风格)*

**Python (3.10+ Match-Case)**
```python
day = "MON"
match day:
    case "MON" | "TUE": # 多个值匹配
        print("工作日")
    case "SUN":
        print("休息日")
    case _: # 类似 default
        print("未知")
```

---

## 模块三：数据结构（集合框架）

这是 Java 开发者最容易产生“文化冲击”的地方。Python 内置了极其强大的数据结构。

### 1. 列表 vs Java List

**Java List**
```java
import java.util.ArrayList;
import java.util.List;

List<String> list = new ArrayList<>();
list.add("A");
list.add("B");
String first = list.get(0);
list.remove(0);
```

**Python List (内置类型)**
```python
# 创建
my_list = ["A", "B", "C"]

# 增
my_list.append("D")       # 末尾添加
my_list.insert(0, "Start") # 指定位置插入

# 删
my_list.remove("A")       # 删除元素 "A"
del my_list[0]            # 删除索引 0
last = my_list.pop()      # 弹出最后一个

# 查/改
first = my_list[0]        # 索引访问
my_list[0] = "New"        # 修改

# 切片 (Slice) - Java 不具备的强大特性
sub = my_list[1:3]        # 获取索引 1 到 2 的子列表
last_two = my_list[-2:]   # 获取最后两个元素
```

### 2. 字典 vs Java Map

**Java Map**
```java
import java.util.HashMap;
import java.util.Map;

Map<String, Integer> map = new HashMap<>();
map.put("Alice", 25);
int age = map.get("Alice"); // 25
map.containsKey("Bob");     // false
```

**Python Dict (内置类型)**
```python
# 创建
person = {"name": "Alice", "age": 25}

# 增/改
person["city"] = "Beijing" # 自动添加
person["age"] = 26         # 自动覆盖

# 查
print(person["name"])      # 直接取值，不存在会报错
print(person.get("salary", 0)) # 推荐方式，不存在返回默认值 0

# 删
del person["city"]
val = person.pop("age")    # 删除并返回值

# 遍历
for key, val in person.items():
    print(f"{key}: {val}")
```

### 3. 集合 vs Java Set

**Java**
```java
Set<String> set = new HashSet<>();
set.add("A");
set.add("A"); // 重复元素自动去重
```

**Python**
```python
# 创建 (注意空集合只能用 set()，因为 {} 是空字典)
s = {"A", "B"}
s = set([1, 2, 3, 3]) # {1, 2, 3}

s.add("C")
s.remove("A")
```

### 4. 元组 - Java 没有的不可变序列

Python 特有，类似于不可变的 List，常用于函数返回多个值。

```python
point = (10, 20) # 用圆括号定义
x, y = point     # 解包
# point[0] = 5   # 报错！元组不可修改
```

---

## 模块四：函数定义

### 1. 基本定义

**Java**
```java
public int add(int a, int b) {
    return a + b;
}
// 调用
int result = add(1, 2);
```

**Python**
```python
def add(a, b):
    return a + b

# 调用
result = add(1, 2)
```

### 2. 参数的高级用法 (Python 核心优势)

**Java (通过方法重载实现灵活性)**
```java
// 需要定义多个方法来实现默认参数效果
public String greet(String name) {
    return greet(name, "Hello");
}
public String greet(String name, String greeting) {
    return greeting + ", " + name;
}
```

**Python (默认参数 & 关键字参数)**
```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Alice"))                   # 使用默认值
print(greet("Bob", greeting="Hi"))      # 指定关键字参数
```

### 3. 可变参数

**Java**
```java
public void printAll(String... args) {
    for (String s : args) {
        System.out.println(s);
    }
}
```
好的，我们继续深入对比。上一部分讲到了函数的可变参数，我们从这里接着讲。

---

## 模块四（续）：函数的高级参数与特性

### 3. 可变参数

**Java (使用 `Type...`)**
```java
// Java 可变参数本质是数组
public void printNames(String... names) {
    for (String name : names) {
        System.out.println(name);
    }
}
// 调用
printNames("A", "B", "C");
```

**Python (`*args` 和 `**kwargs`)**
这是 Python 极其强大的特性，Java 没有直接对应的机制。

```python
# *args 接收任意数量的位置参数，打包成元组
def print_names(*names):
    for name in names:
        print(name)

print_names("A", "B", "C") 
# 输出: A B C

# **kwargs 接收任意数量的关键字参数，打包成字典
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")

print_info(name="Alice", age=25)
# 输出: name = Alice
#      age = 25

# 混合使用顺序：普通参数 -> *args -> 默认参数 -> **kwargs
def complex_func(a, b, *args, **kwargs):
    print(f"a={a}, b={b}")
    print(f"args={args}")
    print(f"kwargs={kwargs}")

complex_func(1, 2, 3, 4, name="Bob", age=30)
# a=1, b=2
# args=(3, 4)
# kwargs={'name': 'Bob', 'age': 30}
```

### 4. Lambda 表达式与函数式编程

**Java (引入 Stream API 后支持)**
```java
// Java Lambda 需要函数式接口支持
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// map/filter/reduce
List<Integer> squares = numbers.stream()
    .map(x -> x * x)
    .collect(Collectors.toList());

// 多行 Lambda 需要大括号和 return
numbers.forEach(x -> {
    int result = x * 2;
    System.out.println(result);
});
```

**Python (原生支持，语法更简洁)**
```python
numbers = [1, 2, 3, 4, 5]

# Python Lambda 是单行表达式，不能包含复杂语句
squares = list(map(lambda x: x * x, numbers))

# 但 Python 更推荐使用列表推导式 - 极其重要！
# 这是 Python 最具代表性的写法，替代 Java 的 Stream map/filter
squares = [x * x for x in numbers]            # map
evens = [x for x in numbers if x % 2 == 0]    # filter

# 字典推导式
scores = {"Alice": 90, "Bob": 60, "Charlie": 85}
passed = {name: score for name, score in scores.items() if score >= 60}
```

### 5. 闭包与装饰器

**Java**
Java 实现类似功能通常需要继承或实现接口，或者使用 AOP 框架。Java 8+ 的 Lambda 实现了简单的闭包，但被 `final`（或 effectively final）限制。

**Python (装饰器 Decorator)**
Python 的装饰器是高阶函数的语法糖，可以在不修改原函数代码的情况下增加功能。**这是 Java 开发者必须掌握的高级特性**。

```python
# 定义一个装饰器（类似 Java 的 AOP 切面）
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs) # 执行原函数
        end = time.time()
        print(f"函数 {func.__name__} 运行耗时: {end - start:.2f}s")
        return result
    return wrapper

# 使用装饰器 (语法糖 @)
@timer
def long_running_task():
    time.sleep(1)
    print("任务完成")

# 调用
long_running_task()
# 输出:
# 任务完成
# 函数 long_running_task 运行耗时: 1.00s
```
**对比理解：** 装饰器模式在 Java 中需要设计模式来实现，而在 Python 中是语言内置特性，常用于日志记录、权限校验、性能测试等。

---

## 模块五：面向对象编程 (OOP) 深度对比

### 1. 类的定义与构造函数

**Java**
```java
public class User {
    // 私有属性
    private String name;
    private int age;

    // 构造函数
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // Getter/Setter...
    public String getName() { return name; }
}
```

**Python**
```python
class User:
    # 构造函数 (初始化方法)
    # self 相当于 Java 的 this，必须显式写在第一个参数
    def __init__(self, name, age):
        # 动态绑定属性，无需提前声明
        self.name = name
        self.age = age
  
    # 方法定义
    def introduce(self):
        # 访问属性使用 self.
        print(f"I am {self.name}, {self.age} years old.")

# 实例化 (不需要 new 关键字)
user = User("Alice", 25)
user.introduce()
```

### 2. 访问控制

**Java**
严格依赖 `public`, `protected`, `private`, `default` 关键字。编译器强制检查。

**Python**
Python 没有强制访问修饰符，依靠**命名约定**。
*   `var`: 公有。
*   `_var`: 受保护，提示外部不要直接访问（约定俗成，非强制）。
*   `__var`: 私有，Python 会进行名称重整，实际上改名为 `_ClassName__var`，使得外部难以直接访问。

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner        # 公有
        self._rate = 0.05         # 受保护 (约定)
        self.__balance = balance  # 私有 (名称重整)

    def get_balance(self):
        return self.__balance

acc = BankAccount("Bob", 1000)

print(acc.owner)          # OK
print(acc._rate)          # OK (IDE可能会警告)
# print(acc.__balance)    # 报错: AttributeError
# 但其实还是能访问到，只是名字变了（不推荐这样做）：
print(acc._BankAccount__balance) # 1000
```

### 3. 继承与多态

**Java (单继承 + 接口实现)**
```java
class Animal {
    public void speak() { System.out.println("..."); }
}

class Dog extends Animal {
    @Override
    public void speak() { System.out.println("Woof"); }
}
```

**Python (支持多继承)**
```python
class Animal:
    def speak(self):
        print("...")

# Python 支持多继承
class Dog(Animal):
    # 重写父类方法
    def speak(self):
        print("Woof")

# 多态示例：Python 的多态是“鸭子类型”
# 不需要继承关系，只要有 speak 方法即可
class Car:
    def speak(self):
        print("Beep")

def make_noise(obj):
    # 只要 obj 有 speak 方法就能调用
    # Java 需要依赖接口或父类引用
    obj.speak()

make_noise(Dog())
make_noise(Car())
```

### 4. 接口 vs 抽象基类

**Java**
Java 有 `interface` 和 `abstract class`。

**Python**
Python 没有强制的 `interface` 关键字（通常用带有空方法的类模拟）。Python 3.4+ 引入了 `abc` 模块来实现抽象基类。

```python
from abc import ABC, abstractmethod

# 定义抽象基类 (类似 Java 接口或抽象类)
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

# 必须实现所有抽象方法才能实例化
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
  
    def area(self):
        return 3.14 * self.radius ** 2
  
    def perimeter(self):
        return 2 * 3.14 * self.radius

# c = Shape() # 报错: Can't instantiate abstract class
c = Circle(5)
```

### 5. 魔术方法
Python 的类有一系列以双下划线开头和结尾的方法，用于实现特定的语法功能。**这是 Java 不具备的强大特性**。

| 魔术方法 | 触发场景 | Java 类比 |
| :--- | :--- | :--- |
| `__init__` | 对象初始化 | 构造函数 |
| `__str__` | `print(obj)` 或 `str(obj)` | `toString()` |
| `__eq__` | `obj1 == obj2` | `equals()` |
| `__hash__` | `hash(obj)` | `hashCode()` |
| `__len__` | `len(obj)` | 实现集合接口的 `size()` |
| `__getitem__` | `obj[key]` | 实现 Map/List 接口的 `get()` |
| `__iter__` | `for x in obj` | 实现 Iterable 接口 |
| `__enter__`/`__exit__` | `with obj:` | `try-with-resources` |

**示例：实现自定义容器**
```python
class MyList:
    def __init__(self):
        self.data = []
  
    def append(self, item):
        self.data.append(item)
  
    # 实现 len()
    def __len__(self):
        return len(self.data)
  
    # 实现 obj[index] 访问
    def __getitem__(self, index):
        return self.data[index]
  
    # 实现 print 显示
    def __str__(self):
        return str(self.data)

ml = MyList()
ml.append(1)
print(len(ml))   # 调用 __len__ -> 1
print(ml[0])     # 调用 __getitem__ -> 1
print(ml)        # 调用 __str__ -> [1]
```

---

## 模块六：异常处理机制

### 1. 异常层次结构

*   **Java**: 所有异常继承自 `Throwable`，分为 `Error` 和 `Exception`。`RuntimeException` 及其子类为非检查型异常，其余为检查型异常（必须 `try-catch` 或 `throws`）。
*   **Python**: 所有异常继承自 `BaseException`。Python **没有检查型异常**，这意味着编译器不会强制你捕获异常，代码更简洁但风险需开发者自担。

### 2. 语法对比

**Java**
```java
try {
    // 可能出错的代码
    int result = 10 / 0;
} catch (ArithmeticException e) {
    // 异常处理
    System.out.println("Error: " + e.getMessage());
} catch (Exception e) {
    // 兜底
    System.out.println("Unknown error");
} finally {
    // 清理资源 (总是执行)
    System.out.println("Cleanup");
}
```

**Python**
```python
try:
    result = 10 / 0
except ZeroDivisionError as e: # 使用 as 关键字捕获异常对象
    print(f"Error: {e}")
except Exception as e:
    print(f"Unknown error: {e}")
else:
    # Python 特有：如果没有发生异常，执行这里
    print("Success!")
finally:
    print("Cleanup")

# 常见的异常类型对应关系：
# NullPointerException   -> AttributeError (属性不存在) 或 TypeError (NoneType)
# IndexOutOfBoundsException -> IndexError
# FileNotFoundException    -> FileNotFoundError
```

### 3. 资源管理

**Java (JDK 7+ try-with-resources)**
```java
// 自动关闭资源，类必须实现 AutoCloseable
try (BufferedReader br = new BufferedReader(new FileReader("file.txt"))) {
    System.out.println(br.readLine());
} // 自动调用 close()
```

**Python (上下文管理器 with)**
```python
# with 语句自动管理资源，类需实现 __enter__ 和 __exit__
with open("file.txt", "r", encoding="utf-8") as f:
    print(f.read())
# 离开缩进块后自动关闭文件，即使中间发生异常
```

### 4. 自定义异常

**Java**
```java
class MyException extends Exception {
    public MyException(String msg) {
        super(msg);
    }
}
throw new MyException("Something wrong");
```

**Python**
```python
# 自定义异常通常直接继承 Exception
class MyException(Exception):
    # 可以很简单，不需要写构造函数
    pass

# 或者增加自定义属性
class InvalidAgeError(Exception):
    def __init__(self, age, msg="Age must be positive"):
        self.age = age
        self.msg = msg
        super().__init__(f"{msg}: {age}")

raise InvalidAgeError(-1)
```

---

## 模块七：并发编程

这是 Java 开发者转型 Python 最大的思维难点：**GIL (Global Interpreter Lock)**。

### 1. 线程模型差异

*   **Java**: 真正的多线程。利用多核 CPU 并行计算。适合 CPU 密集型任务。
*   **Python**: 由于 GIL，同一时刻只能有一个线程在 CPU 上执行 Python 字节码。
    *   **CPU 密集型任务**：Python 多线程**无法**利用多核，甚至比单线程慢（因为有切换开销）。建议使用**多进程**。
    *   **I/O 密集型任务**：Python 多线程非常有效，因为 I/O 操作会释放 GIL（如网络请求、文件读写）。

### 2. 线程创建

**Java**
```java
new Thread(() -> {
    System.out.println("Thread running");
}).start();

// 线程池
ExecutorService executor = Executors.newFixedThreadPool(4);
executor.submit(() -> System.out.println("Task"));
```

**Python**
```python
import threading

def task():
    print("Thread running")

t = threading.Thread(target=task)
t.start()
t.join()

# 线程池 (Python 3.2+ concurrent.futures，类似 Java ExecutorService)
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    future = executor.submit(task)
    result = future.result()
```

### 3. 异步编程

Java 有 `CompletableFuture`，Python 3.4+ 引入了 `asyncio` 库，通过 `async/await` 语法实现协程。这是现代 Python 高并发编程的首选。

**Java (Reactive/Spring WebFlux 风格)**
```java
CompletableFuture.supplyAsync(() -> fetchData())
    .thenAccept(data -> process(data));
```

**Python (Async/Await)**
```python
import asyncio
import time

# 定义协程函数
async def say_after(delay, what):
    await asyncio.sleep(delay) # 模拟 I/O，非阻塞等待
    print(what)

async def main():
    # 并发执行两个协程
    print(f"started at {time.strftime('%X')}")
  
    # gather 类似于 Java 的 allOf
    await asyncio.gather(
        say_after(1, 'hello'),
        say_after(2, 'world')
    )
  
    print(f"finished at {time.strftime('%X')}")

# 运行
asyncio.run(main())
# 结果：总共耗时 2秒 (并发)，而不是 3秒 (串行)
```

### 4. 多进程

如果你需要利用多核 CPU 进行计算（如图像处理、数据分析），Python 必须使用多进程。

```python
from multiprocessing import Pool

def heavy_calculation(x):
    return x * x

if __name__ == '__main__':
    # 进程池
    with Pool(4) as p:
        results = p.map(heavy_calculation, [1, 2, 3, 4, 5])
        print(results)
```

---

## 模块八：工程化与生态 (工具链)

### 1. 包管理

| 功能 | Java | Python |
| :--- | :--- | :--- |
| **构建工具** | Maven, Gradle | setuptools, poetry |
| **依赖文件** | `pom.xml` / `build.gradle` | `requirements.txt` / `pyproject.toml` |
| **仓库** | Maven Central | PyPI (Python Package Index) |
| **安装命令** | (Maven 自动下载) | `pip install requests` |
| **虚拟环境** | (较少用，通常依赖 IDE 配置) | **非常重要**: `venv`, `virtualenv`, `conda` |

**Python 虚拟环境最佳实践：**
Java 项目通常依赖 IDE 或 Maven 管理依赖版本。Python 项目必须使用虚拟环境隔离不同项目的依赖。

```bash
# 创建虚拟环境
python -m venv myenv

# 激活
# Windows:
myenv\Scripts\activate
# Linux/Mac:
source myenv/bin/activate

# 安装库
pip install requests

# 导出依赖
pip freeze > requirements.txt

# 安装现有依赖
pip install -r requirements.txt
```

### 2. 常用库对照表 (必须掌握)

作为 Java 开发，你需要知道 Python 领域对应的“标准库”或“事实标准库”。

| 领域 | Java 库 | Python 库 | 说明 |
| :--- | :--- | :--- | :--- |
| **Web 开发** | Spring Boot | **Django** (全功能) / **FastAPI** (高性能) / **Flask** (轻量) | Django 像 Spring 全家桶，FastAPI 像 Spring WebFlux。 |
| **HTTP 客户端** | Apache HttpClient / OkHttp | **requests** | "HTTP for Humans"，比 Java 简单无数倍。 |
| **JSON 处理** | Jackson / Gson | **json** (内置) | Python 的字典/列表天然对应 JSON 结构。 |
| **数据处理** | 无法直接对比 | **Pandas** | Excel/SQL 级别的数据处理能力，Java 没有同级别的单一库。


好的，我继续补充更多深度内容！

---

## 模块九：文件 I/O 与资源管理

### 1. 文件读取详解

**Java (传统方式)**
```java
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.BufferedReader;
import java.io.FileReader;

// 方式1：NIO (JDK 7+)
String content = new String(Files.readAllBytes(Paths.get("file.txt")));
List<String> lines = Files.readAllLines(Paths.get("file.txt"));

// 方式2：传统 BufferedReader (大文件推荐)
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
}
```

**Python (极其简洁)**
```python
from pathlib import Path

# 一次性读取 (小文件)
content = Path("file.txt").read_text(encoding="utf-8")

# 逐行读取 (大文件，推荐)
with open("file.txt", "r", encoding="utf-8") as f:
    for line in f:  # 迭代器，逐行读取，不占大量内存
        print(line.strip())

# 读取所有行到列表
lines = Path("file.txt").read_text().splitlines()
# 或
with open("file.txt") as f:
    lines = f.readlines()
```

### 2. 文件写入

**Java**
```java
try (BufferedWriter writer = new BufferedWriter(
        new FileWriter("output.txt"))) {
    writer.write("Hello");
    writer.newLine();
}
```

**Python**
```python
# 覆盖写入
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
    f.writelines(["line1\n", "line2\n"])

# 追加写入
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")
```

### 3. 路径操作

**Java**
```java
import java.nio.file.Path;
import java.nio.file.Paths;

Path path = Paths.get("dir", "subdir", "file.txt");
path.getFileName();    // file.txt
path.getParent();      // dir/subdir
path.toAbsolutePath(); // 绝对路径
Files.exists(path);
Files.isDirectory(path);
Files.list(path);      // 遍历目录
```

**Python (pathlib 是 Python 3.4+ 推荐的路径库)**
```python
from pathlib import Path

path = Path("dir") / "subdir" / "file.txt"  # 支持 / 运算符连接路径
path.name          # file.txt
path.parent        # dir/subdir
path.suffix        # .txt
path.exists()
path.is_dir()
path.is_file()

# 目录操作
Path("new_dir").mkdir(parents=True, exist_ok=True)
Path("old_dir").rmdir()

# 遍历目录
for p in Path(".").iterdir():
    print(p.name)
```

---

## 模块十：类型系统进阶

### 1. 类型提示 (Type Hints)

Python 3.5+ 引入了类型提示，这是**可选的**，不会强制执行，但在 IDE（如 PyCharm）和工具（如 mypy）的支持下，可以实现类似 Java 静态类型的检查效果。

```python
# 基本类型提示
name: str = "Alice"
age: int = 25
prices: list[float] = [1.5, 2.0, 3.5]

# 函数参数和返回值
def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! " * times).strip()

# 复杂类型
from typing import List, Dict, Optional, Union, Callable

# List[int] vs list[int] (Python 3.9+ 支持直接用内置类型)
def process(numbers: list[int]) -> int:
    return sum(numbers)

# Optional 相当于 Java 的 @Nullable
def find_user(user_id: int) -> Optional[dict]:
    # 可能返回 dict 或 None
    if user_id > 0:
        return {"id": user_id, "name": "User"}
    return None

# Union 多种可能类型
def parse_input(value: str) -> Union[int, float, str]:
    # ...

# Callable 函数类型
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# 类型别名
UserDict = Dict[str, Union[str, int]]
def create_user(name: str, age: int) -> UserDict:
    return {"name": name, "age": age}
```

### 2. 泛型对比

**Java (编译时泛型，类型擦除)**
```java
// 泛型类和泛型方法
public class Box<T> {
    private T content;
  
    public void set(T content) { this.content = content; }
    public T get() { return content; }
}

// 限制泛型类型
public class NumberBox<T extends Number> {
    private T value;
    public double toDouble() { return value.doubleValue(); }
}
```

**Python (运行时动态，typing 库模拟)**
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, content: T):
        self.content = content
  
    def get(self) -> T:
        return self.content
  
    def set(self, content: T):
        self.content = content

# 使用
int_box = Box[int](42)
str_box = Box[str]("Hello")

# 约束类型 (有限制，但不强制)
from typing import TypeVar, Union

Number = Union[int, float]
def double(n: Number) -> Number:
    return n * 2
```

### 3. 运行时类型检查

**Java** 依赖编译时检查。

**Python (使用 dataclasses 和 Pydantic)**
```python
# 传统方式
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# Python 3.7+ dataclasses (简化 POJO)
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str = ""  # 默认值

user = User("Alice", 25)
print(user)  # User(name='Alice', age=25)
# 自动生成 __eq__, __repr__, __hash__

# Pydantic (推荐，用于 API 请求/响应验证)
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    age: int
    email: str
  
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v

# 自动验证类型，从字典创建
user = User(**{"name": "Bob", "age": "30", "email": "bob@test.com"})
# age 会自动从字符串转换为 int
print(user.age)  # 30 (类型已转换)
```

---

## 模块十一：常用标准库深度对比

### 1. 日期与时间

**Java**
```java
import java.time.*;

LocalDate today = LocalDate.now();
LocalDateTime now = LocalDateTime.now();
Instant timestamp = Instant.now();

// 格式化
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String formatted = now.format(formatter);

// 解析
LocalDate parsed = LocalDate.parse("2024-01-15");

// 计算
LocalDate nextWeek = today.plusWeeks(1);
Duration duration = Duration.between(start, end);
```

**Python**
```python
from datetime import datetime, date, timedelta, timezone
import time

# 日期时间
now = datetime.now()
today = date.today()

# 格式化
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

# 解析
parsed = datetime.strptime("2024-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")

# 计算
next_week = today + timedelta(weeks=1)
yesterday = now - timedelta(days=1)

# 时区
utc_now = datetime.now(timezone.utc)
```

### 2. 正则表达式

**Java**
```java
import java.util.regex.*;

Pattern pattern = Pattern.compile("^\\w+@\\w+\\.\\w+$");
Matcher matcher = pattern.matcher("test@example.com");

if (matcher.matches()) {
    System.out.println("Valid email");
}

// 提取
String text = "Price: $99.99";
Pattern p = Pattern.compile("\\$(\\d+\\.\\d+)");
Matcher m = p.matcher(text);
if (m.find()) {
    System.out.println(m.group(1)); // 99.99
}
```

**Python**
```python
import re

# 匹配
pattern = r"^\w+@\w+\.\w+$"
if re.match(pattern, "test@example.com"):
    print("Valid email")

# 提取
text = "Price: $99.99"
match = re.search(r"\$(\d+\.\d+)", text)
if match:
    print(match.group(1))  # 99.99

# 替换
result = re.sub(r"\$(\d+)", r"¥\1", text)  # Price: ¥99.99

# 分割
parts = re.split(r"[,\s]+", "a,b c,d")

# 查找所有
emails = re.findall(r"\w+@\w+\.\w+", text_with_emails)

# 编译复用
compiled = re.compile(r"\d+")
numbers = compiled.findall("123 abc 456")
```

### 3. 数学与随机数

**Java**
```java
import java.util.Random;
import java.lang.Math;

Math.max(1, 2);
Math.sqrt(16);
Math.pow(2, 3);
Math.random();  // 0.0 ~ 1.0

Random rand = new Random();
rand.nextInt(100);        // 0 ~ 99
rand.nextInt(1, 100);    // Java 17+
rand.nextGaussian();
```

**Python**
```python
import random
import math

max(1, 2)
math.sqrt(16)
math.pow(2, 3)
random.random()           # 0.0 ~ 1.0

random.randint(1, 100)    # 整数 1 ~ 100
random.choice(['a', 'b', 'c'])
random.shuffle(my_list)
random.sample(population, k=3)

# 统计/数学
math.sin(math.pi/2)
math.log(math.e)
math.floor(3.7)   # 3
math.ceil(3.2)   # 4
```

### 4. 序列化

**Java (JSON 常用 Jackson)**
```java
import com.fasterxml.jackson.databind.ObjectMapper;

ObjectMapper mapper = new ObjectMapper();

// Java对象转JSON字符串
String json = mapper.writeValueAsString(user);

// JSON字符串转Java对象
User u = mapper.readValue(json, User.class);

// 格式化输出
String pretty = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(user);

// Map/List 转 JSON
Map<String, Object> map = Map.of("name", "Alice", "age", 25);
String jsonMap = mapper.writeValueAsString(map);
```

**Python (内置 json 模块)**
```python
import json

data = {"name": "Alice", "age": 25, "scores": [90, 85, 88]}

# Python字典直接序列化
json_str = json.dumps(data, indent=2, ensure_ascii=False)

# 反序列化
parsed = json.loads(json_str)

# 文件操作
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)

# 自定义序列化
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
  
    def toJSON(self):
        return {"name": self.name, "age": self.age}
```

---

## 模块十二：单元测试完整对比

### 1. 测试框架

| Java | Python | 说明 |
| :--- | :--- | :--- |
| JUnit 4 | unittest | 经典测试框架 |
| JUnit 5 (Jupiter) | pytest | 现代主流 |

### 2. JUnit 5 vs pytest

**Java**
```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

@DisplayName("计算器测试")
class CalculatorTest {
  
    Calculator calc;
  
    @BeforeEach
    void setUp() {
        calc = new Calculator();
    }
  
    @Test
    @DisplayName("加法测试")
    void testAdd() {
        assertEquals(5, calc.add(2, 3));
        assertEquals(0, calc.add(-1, 1));
    }
  
    @Test
    void testDivideByZero() {
        assertThrows(ArithmeticException.class, () -> calc.divide(1, 0));
    }
  
    @ParameterizedTest
    @CsvSource({
        "1, 2, 3",
        "0, 0, 0",
        "-1, 1, 0"
    })
    void testAddParam(int a, int b, int expected) {
        assertEquals(expected, calc.add(a, b));
    }
}
```

**Python (pytest)**
```python
import pytest

# 简单测试函数，以 test_ 开头
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# 异常测试
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError) as exc:
        divide(1, 0)
    assert "division by zero" in str(exc.value)

# 参数化测试 (pytest 语法更简洁)
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_param(a, b, expected):
    assert add(a, b) == expected

# Fixtures (类似 @BeforeEach)
@pytest.fixture
def calculator():
    return Calculator()

def test_multiply(calculator):
    assert calculator.multiply(3, 4) == 12
```

### 3. Mock 对比

**Java (Mockito)**
```java
import static org.mockito.Mockito.*;

@Test
void testService() {
    UserRepository mockRepo = mock(UserRepository.class);
    when(mockRepo.findById(1)).thenReturn(new User("Alice"));
  
    UserService service = new UserService(mockRepo);
    User user = service.getUser(1);
  
    assertEquals("Alice", user.getName());
    verify(mockRepo).findById(1);
}
```

**Python (unittest.mock)**
```python
from unittest.mock import Mock, patch, MagicMock

def test_service():
    # 创建 Mock 对象
    mock_repo = Mock()
    mock_repo.find_by_id.return_value = User("Alice")
  
    service = UserService(mock_repo)
    user = service.get_user(1)
  
    assert user.name == "Alice"
    mock_repo.find_by_id.assert_called_once_with(1)

# 模拟类方法
@patch('module.ClassName')
def test_with_patch(mock_class):
    mock_class.return_value.method.return_value = 42
    # ...
```

---

## 模块十三：数据库操作

### 1. JDBC vs Python 数据库操作

**Java (JDBC)**
```java
import java.sql.*;

String url = "jdbc:mysql://localhost:3306/mydb";
String sql = "SELECT * FROM users WHERE age > ?";

try (Connection conn = DriverManager.getConnection(url, user, pass);
     PreparedStatement stmt = conn.prepareStatement(sql)) {
  
    stmt.setInt(1, 18);
  
    try (ResultSet rs = stmt.executeQuery()) {
        while (rs.next()) {
            System.out.println(rs.getString("name"));
        }
    }
}
```

**Python (原生 DB-API)**
```python
import sqlite3  # SQLite 为例，其他数据库类似

conn = sqlite3.connect('mydb.db')
cursor = conn.cursor()

# 查询
cursor.execute("SELECT * FROM users WHERE age > ?", (18,))  # 参数化查询
rows = cursor.fetchall()

for row in rows:
    print(row[0])  # 或 row['name']

conn.close()
```

### 2. ORM 对比

**Java (Spring Data JPA)**
```java
// 实体
@Entity
@Table(name = "users")
public class User {
    @Id @GeneratedValue
    private Long id;
  
    @Column(nullable = false)
    private String name;
  
    private Integer age;
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<User> findByAgeGreaterThan(int age);
    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);
}

// 使用
@Service
public class UserService {
    @Autowired
    private UserRepository repo;
  
    public List<User> getAdults() {
        return repo.findByAgeGreaterThan(18);
    }
}
```

**Python (SQLAlchemy)**
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
  
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
  
    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"

# 创建连接
engine = create_engine('sqlite:///mydb.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# CRUD 操作
new_user = User(name='Alice', age=25)
session.add(new_user)
session.commit()

# 查询
adults = session.query(User).filter(User.age > 18).all()
alice = session.query(User).filter_by(name='Alice').first()

# 修改
alice.age = 26
session.commit()

# 删除
session.delete(alice)
session.commit()
```

---

## 模块十四：网络编程

### 1. HTTP 客户端

**Java (OkHttp / Apache HttpClient)**
```java
// OkHttp
OkHttpClient client = new OkHttpClient();
Request request = new Request.Builder()
    .url("https://api.example.com/data")
    .build();

try (Response response = client.newCall(request).execute()) {
    if (response.isSuccessful()) {
        String body = response.body().string();
        // 解析 JSON...
    }
}

// POST 请求
MediaType JSON = MediaType.parse("application/json");
String json = "{\"name\": \"Alice\"}";
RequestBody body = RequestBody.create(json, JSON);
Request request = new Request.Builder()
    .url("https://api.example.com/users")
    .post(body)
    .build();
```

**Python (requests 库 - 极其简洁)**
```python
import requests

# GET 请求
response = requests.get("https://api.example.com/data")
if response.status_code == 200:
    data = response.json()  # 自动解析 JSON

# POST 请求
payload = {"name": "Alice", "age": 25}
response = requests.post("https://api.example.com/users", json=payload)

# 请求头、超时等
headers = {"Authorization": "Bearer token"}
response = requests.get(url, headers=headers, timeout=30)
```

### 2. 异步 HTTP (asyncio + aiohttp)

**Java (WebClient - Project Reactor)**
```java
WebClient client = WebClient.create();
Mono<String> result = client.get()
    .uri("https://api.example.com/data")
    .retrieve()
    .bodyToMono(String.class);
```

**Python (aiohttp)**
```python
import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/data') as response:
            return await response.json()

async def main():
    # 并发请求多个 URL
    urls = ['url1', 'url2', 'url3']
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

asyncio.run(main())
```

---

## 模块十五：设计模式实现对比

### 1. 单例模式

**Java**
```java
public class Singleton {
    private static final Singleton INSTANCE = new Singleton();
  
    private Singleton() { }
  
    public static Singleton getInstance() {
        return INSTANCE;
    }
}

// 枚举单例 (最佳实践)
public enum SingletonEnum {
    INSTANCE;
    public void doSomething() { }
}
```

**Python**
```python
# 方式1：模块变量（Python 最自然的单例）
# my_singleton.py
class Singleton:
    def __init__(self):
        self.value = None

_instance = None

def get_instance():
    global _instance
    if _instance is None:
        _instance = Singleton()
    return _instance

# 方式2：装饰器
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Config:
    pass
```

### 2. 工厂模式

**Java**
```java
interface Shape {
    void draw();
}

class Circle implements Shape {
    public void draw() { System.out.println("Circle"); }
}

class Square implements Shape {
    public void draw() { System.out.println("Square"); }
}

class ShapeFactory {
    public Shape create(String type) {
        return switch (type) {
            case "circle" -> new Circle();
            case "square" -> new Square();
            default -> throw new IllegalArgumentException();
        };
    }
}
```

**Python**
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        print("Circle")

class Square(Shape):
    def draw(self):
        print("Square")

# Python 工厂函数
def shape_factory(shape_type: str) -> Shape:
    shapes = {
        "circle": Circle,
        "square": Square,
    }
    if shape_type not in shapes:
        raise ValueError(f"Unknown shape: {shape_type}")
    return shapes[shape_type]()

# 使用
shape = shape_factory("circle")
shape.draw()
```

---

## 模块十六：内存管理与垃圾回收

### 对比

| 方面 | Java | Python |
| :--- | :--- | :--- |
| **内存分配** | JVM 堆，运行时分配 | 私有堆，引用计数 + 循环垃圾回收 |
| **GC 机制** | 分代收集 (Young/Old/Perm) | 引用计数 (主要) + GC 模块 (循环引用) |
| **手动干预** | 有限 (`System.gc()`) | 可手动触发 (`gc.collect()`) |
| **内存泄漏检测** | JProfiler, VisualVM | `tracemalloc`, `objgraph` |
| **循环引用** | JVM GC 可以处理 | Python 引用计数无法处理，但 GC 模块会处理 |

```python
# Python 内存分析示例
import tracemalloc

tracemalloc.start()

# 你的代码
data = [i for i in range(100000)]

current, peak = tracemalloc.get_traced_memory()
print(f"Current memory: {current / 1024 / 1024:.2f} MB")
print(f"Peak memory: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

---

## 模块十七：Python 特有高级特性

### 1. 装饰器 (Decorator) - 进阶

```python
import functools
import time

# 装饰器带参数
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)  # 保留原函数信息
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=5, delay=2)
def unreliable_api_call():
    # 失败重试逻辑
    pass

# 类装饰器
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.calls = 0
        functools.update_wrapper(self, func)
  
    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(f"Call #{self.calls}")
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    print("Hello!")
```

### 2. 上下文管理器 (Context Manager)

```python
# 类实现
class DatabaseConnection:
    def __enter__(self):
        print("Connecting to DB...")
        return self
  
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        return False  # 不压制异常

with DatabaseConnection() as conn:
    print("Executing queries...")

# 函数实现 (contextlib)
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    try:
        connection.begin()
        yield connection
        connection.commit()
    except:
        connection.rollback()
        raise

with transaction(conn):
    conn.execute("INSERT ...")
```

### 3. 生成器 (Generator)

```python
# 生成器函数 - 按需生成值，不占用大量内存
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 使用
for num in fibonacci(1000):
    print(num)  # 逐个处理，内存占用极小

# 生成器表达式 (类似列表推导式)
squares = (x * x for x in range(1000000))  # 内存高效
print(list(squares)[:10])  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# yield from - 委托生成
def generator():
    yield from [1, 2, 3]
    yield from "abc"
```

### 4. 迭代器协议

```python
# 实现自定义迭代器
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0
  
    def __iter__(self):
        return self
  
    def __next__(self):
        if self.current >= self.limit:
            raise StopIteration
        self.current += 1
        return self.current

for num in Counter(5):
    print(num)  # 1, 2, 3, 4, 5
```

---

## 模块十八：项目结构与最佳实践

### 1. 标准项目结构

**Java Maven 项目**
```
my-java-app/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── config/
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       └── model/
│   │   └── resources/
│   │       └── application.yml
│   └── test/
│       └── java/...
└── target/
```

**Python 项目 (类 Django 风格)**
```
my-python-app/
├── src/                    # 或直接用包名
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_services/
├── docs/
├── pyproject.toml          # 现代项目配置
├── requirements.txt
├── .gitignore
└── README.md
```

### 2. 配置管理

**Java (application.yml)**
```yaml
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: secret

app:
  name: my-app
  version: 1.0.0
```

**Python (多种方式)**
```python
# 方式1：环境变量 + python-dotenv
# .env 文件
# DATABASE_URL=postgresql://user:pass@localhost/db
# SECRET_KEY=your-secret-key

from dotenv import load_dotenv
import os

load_dotenv()  # 加载 .env 文件

db_url = os.getenv("DATABASE_URL")
secret = os.getenv("SECRET_KEY")

# 方式2：Pydantic Settings (推荐)
# pip install pydantic-settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
  
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
print(settings.database_url)

# 方式3：YAML 配置
import yaml

with open("config.yml") as f:
    config = yaml.safe_load(f)
```

### 3. 日志配置

**Java (Logback/SLF4J)**
```xml
<!-- logback.xml -->
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
  
    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
    </root>
  
    <logger name="com.example" level="DEBUG"/>
</configuration>
```

**Python**
```python
import logging
import logging.config

# 方式1：基础配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 方式2：YAML 配置
# logging.yml
"""
version: 1
disable_existing_loggers: false

formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    formatter: detailed
  file:
    class: logging.FileHandler
    filename: app.log
    formatter: detailed

root:
  level: INFO
  handlers: [console, file]
"""

with open('logging.yml') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
```

---

## 附录：Java 开发者速查表

### 语法速查

| Java | Python | 说明 |
| :--- | :--- | :--- |
| `String s = "hello";` | `s = "hello"` | 字符串 |
| `int[] arr = {1,2,3};` | `arr = [1, 2, 3]` | 数组/列表 |
| `arr.length` | `len(arr)` | 长度 |
| `arr[i]` | `arr[i]` | 索引访问 |
| `List<String> list = new ArrayList<>();` | `my_list = []` 或 `list()` | 列表 |
| `list.add(x)` | `my_list.append(x)` | 添加元素 |
| `list.get(0)` | `my_list[0]` | 获取元素 |
| `list.remove(0)` | `del my_list[0]` 或 `my_list.pop(0)` | 删除元素 |
| `Map<K,V>` | `dict` | 字典 |
| `map.put(k, v)` | `d[k] = v` | 设置键值 |
| `map.get(k)` | `d.get(k, default)` | 获取值 |
| `for (int i=0; i<n; i++)` | `for i in range(n):` | 循环 |
| `for (T t : list)` | `for item in list:` | 遍历 |
| `if (condition)` | `if condition:` | 条件 |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` | 逻辑运算 |
| `a ? b : c` | `b if a else c` | 三元表达式 |
| `public void method()` | `def method(self):` | 方法定义 |
| `public static void main(String[] args)` | `if __name__ == "__main__":` | 程序入口 |
| `this.x = x;` | `self.x = x` | 引用自身 |
| `null` | `None` | 空值 |
| `instanceof` | `isinstance()` | 类型检查 |
| `getClass().getName()` | `type(obj).__name__` | 获取类型名 |
| `toString()` | `__str__()` | 字符串表示 |
| `equals()` | `__eq__()` | 相等比较 |
| `hashCode()` | `__hash__()` | 哈希值 |
| `public` | (无下划线) | 公有成员 |
| `protected` | `_protected` | 受保护成员 |
| `private` | `__private` | 私有成员 |
| `throw new Exception()` | `raise Exception()` | 抛出异常 |
| `try { } catch (Exception e)` | `try: except Exception as e:` | 异常捕获 |
| `synchronized` | `threading.Lock` | 同步 |
| `volatile` | (不需要) | 线程可见性 |
| `interface` | `ABC` + `@abstractmethod` | 抽象接口 |
| `abstract class` | `ABC` + `@abstractmethod` | 抽象类 |
| `extends` | `(class Child(Parent):)` | 继承 |
| `implements` | (不需要显式声明) | 接口实现 |
| `final` | (使用约定: 全大写命名) | 常量 |
| `static` | (模块级变量或类变量) | 静态成员 |

### 内置函数对照

| 功能 | Java 方法 | Python 函数 |
| :--- | :--- | :--- |
| 打印 | `System.out.println()` | `print()` |
| 获取输入 | `Scanner` | `input()` |
| 字符串转整数 | `Integer.parseInt()` | `int()` |
| 字符串转浮点 | `Double.parseDouble()` | `float()` |
| 转字符串 | `String.valueOf()` | `str()` |
| 取绝对值 | `Math.abs()` | `abs()` |
| 取最大值 | `Math.max()` | `max()` |
| 取最小值 | `Math.min()` | `min()` |
| 开方 | `Math.sqrt()` | `math.sqrt()` |
| 幂运算 | `Math.pow()` | `**` 或 `pow()` |
| 随机数 | `Math.random()` | `random.random()` |
| 数组排序 | `Arrays.sort()` | `sorted()` |
| 集合排序 | `Collections.sort()` | `list.sort()` |
| 二分搜索 | `Arrays.binarySearch()` | `bisect.bisect()` |

### 常用模块导入

| 场景 | Python 导入 |
| :--- | :--- |
| 列表/字典/集合 | 无需导入 |
| 数学运算 | `import math` |
| 随机数 | `import random` |
| 日期时间 | `from datetime import datetime, timedelta` |
| 系统参数 | `import sys, os` |
| 正则表达式 | `import re` |
| JSON | `import json` |
| CSV | `import csv` |
| HTTP 请求 | `import requests` |
| 命令行参数 | `import argparse` |
| 类型提示 | `from typing import List, Dict, Optional` |

---

## 学习路线总结

```
┌─────────────────────────────────────────────────────────────────┐
│                    Java → Python 学习路线                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第1阶段：语法适应 (1-2周)                                        │
│  ├── 动态类型 vs 静态类型                                         │
│  ├── 缩进语法 vs 大括号                                           │
│  ├── 内置数据结构 (list, dict, set, tuple)                         │
│  └── 控制流语法 (if/for/while/try-except)                         │
│                                                                 │
│  第2阶段：核心特性 (2-3周)                                        │
│  ├── 函数定义与参数 (*args, **kwargs, lambda)                     │
│  ├── 面向对象 (类, 继承, 魔术方法)                                 │
│  ├── 列表/字典推导式                                              │
│  └── 异常处理与文件 I/O                                           │
│                                                                 │
│  第3阶段：工程化 (1-2周)                                          │
│  ├── 虚拟环境与包管理 (pip, poetry)                               │
│  ├── 单元测试 (pytest)                                           │
│  ├── 日志配置                                                     │
│  └── 项目结构规范                                                 │
│                                                                 │
│  第4阶段：框架实践 (2-3周)                                        │
│  ├── FastAPI/Flask Web 开发                                      │
│  ├── SQLAlchemy ORM                                               │
│  ├── Pandas 数据处理                                              │
│  └── requests HTTP 客户端                                         │
│                                                                 │
│  第5阶段：高级特性 (持续学习)                                      │
│  ├── 装饰器与元编程                                               │
│  ├── 异步编程 (asyncio)                                          │
│  ├── 并发与多进程                                                 │
│  └── 类型提示与代码规范 (mypy)                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

这份资料涵盖了 Java 开发者学习 Python 需要掌握的几乎所有核心内容。建议按照学习路线逐步深入，每完成一个模块就动手编写代码练习。掌握这些内容后，你就能熟练使用 Python 进行日常开发工作了！

有任何具体问题欢迎随时提问！ 🚀