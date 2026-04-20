# Java 开发者 Python 对照学习计划

## 📋 学习计划总览

| 周次 | 主题 | 重点 |
|------|------|------|
| 第1周 | 基础语法 & 数据类型 | 语法差异、内置类型 |
| 第2周 | 控制流 & 函数 | 缩进、参数、返回值 |
| 第3周 | 面向对象编程 | 类定义、继承、多态 |
| 第4周 | 异常处理 & 文件操作 | try-except、文件I/O |
| 第5周 | 集合 & 泛型 | 列表、字典、集合推导式 |
| 第6周 | 并发编程 | threading、asyncio |
| 第7周 | 测试 & 工程化 | pytest、logging |
| 第8周 | 常用框架 | Django/Flask、数据处理 |

---

## 📅 第1周：基础语法 & 数据类型

### 核心概念对照

| 概念    | Java                   | Python                |
| ----- | ---------------------- | --------------------- |
| 输出    | `System.out.println()` | `print()`             |
| 变量声明  | `int a = 1;`           | `a = 1` (动态类型)        |
| 常量    | `final int PI = 3.14;` | `PI = 3.14` (约定)      |
| 类型注释  | 不需要                    | `a: int = 1` (3.5+可选) |
| 字符串引号 | 双引号                    | 双引号或单引号均可             |
| 注释    | `//` 或 `/* */`         | `#` 或 `"""`           |

### 代码对比

```python
# ============ Java ============
public class Hello {
    public static void main(String[] args) {
        // 变量声明必须指定类型
        int age = 25;
        String name = "Alice";
      
        System.out.println("Hello, " + name);
        System.out.printf("Age: %d%n", age);
    }
}

# ============ Python ============
# 无需类型声明，动态类型
age = 25
name = "Alice"

print(f"Hello, {name}")           # f-string (Python 3.6+)
print("Age:", age)                # 自动空格分隔

# 多行字符串
description = """
这是一个多行
字符串
"""
```

### 内置数据类型对照

| Java 类型 | Python 类型 | 说明 |
|-----------|-------------|------|
| `int` | `int` | 整数（无上限） |
| `double` | `float` | 浮点数 |
| `boolean` | `bool` | 布尔值 |
| `char` | `str` (单字符) | 字符串 |
| `String` | `str` | 字符串 |

### Python 特有类型

```python
# None 等价于 Java 的 null
result = None

# 布尔值：True / False (首字母大写)
is_valid = True

# 类型检查
print(type(age))        # <class 'int'>
print(isinstance(age, int))  # True

# 类型提示 (类似 TypeScript)
def greet(name: str, age: int) -> str:
    return f"Hello {name}, age {age}"
```

### 🏋️ 练习任务

1. 创建变量存储：姓名、年龄、身高(m)、是否学生
2. 使用 f-string 格式化输出自我介绍
3. 体验 Python 的动态类型：在同一声明中先赋整数再赋字符串

---

## 📅 第2周：控制流 & 函数

### 控制结构对照

```python
# ============ Java ============
public class ControlDemo {
    public static void main(String[] args) {
        // if-else
        int score = 85;
        if (score >= 90) {
            System.out.println("A");
        } else if (score >= 60) {
            System.out.println("B");
        } else {
            System.out.println("C");
        }
      
        // for 循环
        for (int i = 0; i < 5; i++) {
            System.out.println(i);
        }
      
        // for-each
        String[] fruits = {"apple", "banana"};
        for (String fruit : fruits) {
            System.out.println(fruit);
        }
      
        // while
        int j = 0;
        while (j < 3) {
            System.out.println(j++);
        }
    }
}

# ============ Python ============
score = 85

# if-elif-else (注意：elif 连写)
if score >= 90:
    print("A")
elif score >= 60:
    print("B")
else:
    print("C")

# for 循环 - 更像 Java 的增强for
fruits = ["apple", "banana"]
for fruit in fruits:
    print(fruit)

# range() 等价于 Java 的 IntStream.range()
for i in range(5):        # 0,1,2,3,4
    print(i)

for i in range(1, 6):     # 1,2,3,4,5 (起始,结束-1)
    print(i)

for i in range(0, 10, 2): # 0,2,4,6,8 (步长)
    print(i)

# while
j = 0
while j < 3:
    print(j)
    j += 1

# switch 等价于 match (Python 3.10+)
status = "active"
match status:
    case "active":
        print("运行中")
    case "pending":
        print("等待中")
    case _:
        print("未知状态")
```

### 函数定义对照

```python
# ============ Java ============
public class FunctionDemo {
    // 方法必须写在类中
    public static int add(int a, int b) {
        return a + b;
    }
  
    public static void printMessage(String message) {
        System.out.println(message);
    }
  
    // 可变参数
    public static int sum(int... numbers) {
        int total = 0;
        for (int n : numbers) {
            total += n;
        }
        return total;
    }
}

# ============ Python ============
# 函数定义更简洁，不需要在类中
def add(a: int, b: int) -> int:
    """加法函数"""
    return a + b

# 默认参数 (类似 Java 的重载)
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!

# 可变参数 (*args 类似 varargs)
def sum(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum(1, 2, 3))             # 6
print(sum(1, 2, 3, 4, 5))       # 15

# 关键字参数 (**kwargs)
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Beijing")

# Lambda 表达式 (类似 Java 的箭头函数)
square = lambda x: x ** 2
print(square(5))                # 25

# 高阶函数
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### 🏋️ 练习任务

1. 编写函数：`is_prime(n)` 判断素数
2. 编写函数：接收不定参数，返回最大值
3. 使用 lambda 和 map/filter 实现：过滤偶数并平方
4. 实现斐波那契数列生成器（用 yield）

---

## 📅 第3周：面向对象编程

### 类定义对照

```python
# ============ Java ============
public class Person {
    private String name;
    private int age;
  
    // 构造器
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
  
    // Getter/Setter
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
  
    // 方法
    public void introduce() {
        System.out.println("I am " + name + ", " + age + " years old");
    }
  
    // toString
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}

// 继承
public class Student extends Person {
    private String school;
  
    public Student(String name, int age, String school) {
        super(name, age);
        this.school = school;
    }
}

# ============ Python ============
class Person:
    """人物类"""
  
    # 类属性 (类似 Java static 变量)
    species = "Human"
  
    def __init__(self, name: str, age: int):
        """构造方法"""
        self.name = name      # 实例属性
        self.age = age
        self._private = 0    # 约定：单下划线表示私有
  
    # 属性装饰器 (类似 Getter)
    @property
    def name(self):
        return self._name
  
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value
  
    # 实例方法
    def introduce(self):
        print(f"I am {self.name}, {self.age} years old")
  
    # 魔术方法
    def __str__(self):
        return f"Person(name='{self.name}', age={self.age})"
  
    def __repr__(self):
        return f"Person('{self.name}', {self.age})"
  
    # 运算符重载
    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name and self.age == other.age
        return False
  
    def __len__(self):
        return self.age

# 继承
class Student(Person):
    def __init__(self, name: str, age: int, school: str):
        super().__init__(name, age)  # 调用父类构造器
        self.school = school
  
    def introduce(self):
        # 方法重写
        super().introduce()  # 调用父类方法
        print(f"I study at {self.school}")

# 多继承
class Flyable:
    def fly(self):
        print("Flying!")

class SuperHero(Student, Flyable):
    pass
```

### 访问修饰符对照

| Java | Python | 说明 |
|------|--------|------|
| `public` | `public` (无下划线) | 公有属性 |
| `protected` | `_protected` | 子类可见（约定） |
| `private` | `__private` | 名称重整实现私有 |

```python
class Demo:
    def __init__(self):
        self.public = "everyone"
        self._protected = "subclass"
        self.__private = "only me"
  
    def __secret_method(self):
        print("This is private")

# 外部访问
demo = Demo()
print(demo.public)           # OK
print(demo._protected)       # 可访问，但不推荐
# print(demo.__private)      # 报错！
print(demo._Demo__private)   # 语法上可以，但不推荐
```

### 抽象类 & 接口对照

```python
# Java 接口
public interface Drawable {
    void draw();
}

public interface Moveable {
    void move();
}

// 类实现多个接口
public class Circle implements Drawable, Moveable {
    public void draw() { }
    public void move() { }
}

# Python 实现接口 (用 ABC)
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Moveable(ABC):
    @abstractmethod
    def move(self):
        pass

# Python 不需要显式声明实现接口，只要实现方法即可
class Circle(Drawable, Moveable):
    def draw(self):
        print("Drawing circle")
  
    def move(self):
        print("Moving circle")
```

### 特殊方法（魔术方法）

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
  
    def __add__(self, other):      # +
        return Vector(self.x + other.x, self.y + other.y)
  
    def __sub__(self, other):      # -
        return Vector(self.x - other.x, self.y - other.y)
  
    def __mul__(self, scalar):     # *
        return Vector(self.x * scalar, self.y * scalar)
  
    def __getitem__(self, index):  # []
        if index == 0: return self.x
        if index == 1: return self.y
        raise IndexError()
  
    def __call__(self):            # 对象()调用
        return f"({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)         # (4, 6)
print(v1 * 3)          # (3, 6)
print(v1[0])           # 1
print(v1())            # (1, 2)
```

### 🏋️ 练习任务

1. 实现一个 `BankAccount` 类：存款、取款、查余额、利息计算
2. 用 `@property` 实现只读属性
3. 实现运算符重载：复数类的加减乘除
4. 创建抽象类 `Animal` 和实现类 `Dog`、`Cat`

---

## 📅 第4周：异常处理 & 文件操作

### 异常处理对照

```python
# ============ Java ============
public class ExceptionDemo {
    public static void main(String[] args) {
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Division by zero: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Other error: " + e.getMessage());
        } finally {
            System.out.println("Always executed");
        }
      
        // 抛出异常
        throw new IllegalArgumentException("Invalid input");
    }
}

# ============ Python ============
# 异常处理
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Division by zero: {e}")
except Exception as e:
    print(f"Other error: {e}")
else:
    print("No exception occurred")  # try中没有异常时执行
finally:
    print("Always executed")

# 抛出异常
raise ValueError("Invalid input")

# 自定义异常
class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

raise ValidationError("email", "Invalid format")
```

### 常见异常类型

| Java | Python | 说明 |
|------|--------|------|
| `NullPointerException` | `AttributeError` / `TypeError` | 空引用 |
| `IndexOutOfBoundsException` | `IndexError` | 索引越界 |
| `IllegalArgumentException` | `ValueError` | 参数不合法 |
| `NoSuchElementException` | `KeyError` | 键不存在 |
| `IOException` | `IOError` / `OSError` | IO异常 |

### 文件操作对照

```java
// ============ Java ============
import java.io.*;
import java.nio.file.*;

public class FileDemo {
    public static void main(String[] args) throws IOException {
        // 读取文件
        String content = Files.readString(Path.of("file.txt"));
      
        // 写入文件
        Files.writeString(Path.of("output.txt"), "Hello World");
      
        // 按行读取
        try (BufferedReader reader = new BufferedReader(
                new FileReader("file.txt"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        }
    }
}
```

```python
# ============ Python ============
# 推荐方式：with 语句自动关闭资源
from pathlib import Path

# 读取文件
path = Path("file.txt")
content = path.read_text()           # 读取全部内容
lines = path.read_text().splitlines()  # 按行分割

# 写入文件
path.write_text("Hello World")

# 逐行读取 (大文件推荐)
with open("file.txt", "r", encoding="utf-8") as f:
    for line in f:                   # 迭代器，逐行读取
        print(line.strip())

# 写入 (覆盖)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Line 1\n")
    f.writelines(["Line 2\n", "Line 3\n"])

# 追加模式
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")

# JSON 文件操作
import json

data = {"name": "Alice", "age": 25}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

# CSV 文件操作
import csv

with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 25})
    writer.writerow({"name": "Bob", "age": 30})

with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

### 🏋️ 练习任务

1. 实现文件复制功能（带异常处理）
2. 读取 CSV 文件，计算某列的平均值
3. 实现日志记录器，支持不同级别输出到文件
4. JSON 配置文件的读取和更新

---

## 📅 第5周：集合框架 & 推导式

### 集合类型对照

| Java | Python | 说明 |
|------|--------|------|
| `List<T>` | `list` | 有序列表 |
| `Set<T>` | `set` | 无序去重集合 |
| `Map<K,V>` | `dict` | 键值对映射 |
| `Queue<T>` | `deque` | 队列（collections） |
| `Stack<T>` | `list` | 栈（用 append/pop） |

### 列表操作

```python
# ============ Python List ============
# 创建
numbers = [1, 2, 3, 4, 5]
fruits = list(["apple", "banana"])
empty = []

# 索引 (支持负数)
print(numbers[0])      # 1
print(numbers[-1])     # 5 (最后一个)
print(numbers[1:4])    # [2, 3, 4] (切片)
print(numbers[::2])    # [1, 3, 5] (步长2)

# 常用方法
numbers.append(6)      # 末尾添加
numbers.insert(0, 0)   # 指定位置插入
numbers.extend([7, 8]) # 合并列表
numbers.pop()          # 移除末尾元素
numbers.pop(0)          # 移除指定位置
numbers.remove(3)      # 移除第一个匹配的
del numbers[0]         # 删除指定位置

# 列表推导式 (类似 Java Stream)
squares = [x**2 for x in range(10)]           # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# 带条件
names = ["Alice", "Bob", "Charlie"]
long_names = [n for n in names if len(n) > 3]  # ['Alice', 'Charlie']

# 嵌套推导
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]

# 解包 (类似 Java 14+ 的 record)
a, b, c = [1, 2, 3]
first, *rest, last = [1, 2, 3, 4, 5]  # first=1, rest=[2,3,4], last=5
```

### 字典操作

```python
# ============ Python Dict ============
# 创建
user = {"name": "Alice", "age": 25}
user = dict(name="Alice", age=25)     # 关键字参数
empty = {}

# 访问
print(user["name"])                   # Alice
print(user.get("email", "N/A"))       # 默认值

# 添加/修改
user["email"] = "alice@example.com"
user.update({"city": "Beijing", "age": 26})

# 删除
del user["email"]
email = user.pop("email", None)      # 带默认值

# 遍历
for key in user:
    print(f"{key}: {user[key]}")

for key, value in user.items():
    print(f"{key}: {value}")

for value in user.values():
    print(value)

# 字典推导式
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 过滤
filtered = {k: v for k, v in user.items() if k != "email"}
```

### 集合操作

```python
# ============ Python Set ============
# 创建
colors = {"red", "green", "blue"}
empty = set()  # 注意：{} 创建的是字典

# 操作
colors.add("yellow")
colors.remove("green")    # 不存在会报错
colors.discard("black")   # 不存在不报错

# 集合运算
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

union = set1 | set2           # {1, 2, 3, 4, 5, 6}
intersection = set1 & set2    # {3, 4}
difference = set1 - set2      # {1, 2}
symmetric_diff = set1 ^ set2  # {1, 2, 5, 6}

# 集合推导式
squares_set = {x**2 for x in range(-5, 6)}
```

### 对比：Java Stream vs Python 推导式

```java
// Java Stream
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)
    .map(n -> n * n)
    .collect(Collectors.toList());
```

```python
# Python 推导式
numbers = [1, 2, 3, 4, 5]
result = [n * n for n in numbers if n % 2 == 0]
# [4, 16]
```

```python
# 复杂场景用 filter/map (类似 Java Stream)
from functools import reduce

result = list(map(lambda x: x * x, 
              filter(lambda x: x % 2 == 0, numbers)))

# 求和 (类似 reduce)
total = reduce(lambda x, y: x + y, numbers, 0)
```

### 🏋️ 练习任务

1. 统计字符串中每个字符出现的频率
2. 实现词频统计器（读取文件，输出 Top 10 高频词）
3. 用推导式实现：两个列表的笛卡尔积
4. 实现集合运算演示器

---

## 📅 第6周：并发编程

### 线程对照

```java
// ============ Java ============
public class ThreadDemo extends Thread {
    @Override
    public void run() {
        System.out.println("Running in thread");
    }
  
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new ThreadDemo();
        thread.start();
        thread.join();
    }
}

// 实现 Runnable
Runnable task = () -> {
    System.out.println("Running");
};
Thread thread = new Thread(task);
thread.start();

// ExecutorService
ExecutorService executor = Executors.newFixedThreadPool(4);
Future<Integer> future = executor.submit(() -> {
    return 42;
});
executor.shutdown();
```

```python
# ============ Python ============
import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future

# 方式1：继承 Thread
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
  
    def run(self):
        print(f"Thread {self.name} starting")
        time.sleep(1)
        print(f"Thread {self.name} finished")

thread = MyThread("A")
thread.start()
thread.join()

# 方式2：传入函数
def task(n):
    time.sleep(1)
    return n * n

threads = []
for i in range(3):
    t = threading.Thread(target=task, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# 线程安全
counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:  # 自动获取和释放锁
        counter += 1

# ThreadPoolExecutor (推荐)
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task, i) for i in range(5)]
  
    for future in futures:
        print(f"Result: {future.result()}")  # 阻塞等待结果
```

### 异步编程对照

```java
// Java CompletableFuture
CompletableFuture.supplyAsync(() -> fetchData())
    .thenApply(data -> process(data))
    .thenAccept(result -> System.out.println(result))
    .exceptionally(ex -> {
        ex.printStackTrace();
        return null;
    });
```

```python
# Python asyncio (Python 3.5+)
import asyncio

async def fetch_data(url: str) -> str:
    # 模拟异步 I/O
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    # 并发执行
    urls = ["http://example1.com", "http://example2.com", "http://example3.com"]
  
    # gather: 并发等待多个协程
    results = await asyncio.gather(*[fetch_data(url) for url in urls])
    print(results)

# 运行
asyncio.run(main())

# 顺序执行
async def sequential():
    for url in urls:
        result = await fetch_data(url)
        print(result)
```

### 同步原语对照

| Java | Python | 说明 |
|------|--------|------|
| `synchronized` | `Lock`, `RLock` | 互斥锁 |
| `ReentrantLock` | `RLock` | 可重入锁 |
| `Semaphore` | `Semaphore` | 信号量 |
| `CountDownLatch` | `threading.Barrier` | 屏障 |
| `AtomicInteger` | `queue.Queue` | 线程安全队列 |
| `volatile` | - | (Python GIL 不需要) |

### 🏋️ 练习任务

1. 实现多线程下载文件模拟器
2. 用 asyncio 实现并发 HTTP 请求（aiohttp 库）
3. 实现生产者-消费者问题
4. 实现线程安全的计数器

---

## 📅 第7周：测试 & 工程化

### 测试对照

```java
// Java JUnit 5
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    Calculator calc = new Calculator();
  
    @Test
    void testAdd() {
        assertEquals(5, calc.add(2, 3));
    }
  
    @BeforeEach
    void setUp() { }
  
    @AfterEach
    void tearDown() { }
}
```

```python
# Python pytest
import pytest

# 基础测试
def test_add():
    assert add(2, 3) == 5

# 使用 pytest fixtures (类似 JUnit @BeforeEach)
@pytest.fixture
def calculator():
    return Calculator()

def test_multiply(calculator):
    assert calculator.multiply(3, 4) == 12

# 参数化测试 (类似 JUnit @ParameterizedTest)
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_params(a, b, expected):
    assert add(a, b) == expected

# 异常测试
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

# Mock (类似 Mockito)
from unittest.mock import Mock, patch

@patch('module.ClassName')
def test_mock(mock_class):
    mock_class.return_value.method.return_value = 42
    # ...
```

### 日志对照

```java
// Java logging
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MyClass {
    private static final Logger log = LoggerFactory.getLogger(MyClass.class);
  
    public void doSomething() {
        log.debug("Debug message");
        log.info("Info message");
        log.warn("Warning message");
        log.error("Error message");
    }
}
```

```python
# Python logging
import logging

# 配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def do_something():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")

# 高级配置
import logging.config

config = {
    'version': 1,
    'formatters': {
        'detailed': {'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'detailed'
        }
    },
    'loggers': {
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG'
        }
    }
}
logging.config.dictConfig(config)
```

### 包管理 & 虚拟环境

```bash
# ============ Python 环境管理 ============
# 创建虚拟环境
python -m venv myenv

# 激活 (Windows)
myenv\Scripts\activate

# 激活 (Linux/Mac)
source myenv/bin/activate

# 安装依赖
pip install requests
pip install -r requirements.txt

# 导出依赖
pip freeze > requirements.txt

# 使用 pipenv (更现代)
pip install pipenv
pipenv install requests
pipenv install --dev pytest
pipenv shell  # 进入虚拟环境

# 使用 poetry (推荐)
pip install poetry
poetry init
poetry add requests
poetry add --dev pytest
poetry shell
```

### 项目结构（类比 Maven）

```
myproject/
├── src/                      # 源代码
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/                     # 测试
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils/
├── docs/                     # 文档
├── pyproject.toml            # 项目配置 (Poetry)
├── requirements.txt          # pip freeze
├── setup.py                  # 安装配置
└── README.md
```

### 🏋️ 练习任务

1. 为之前练习的类编写完整测试用例
2. 配置日志，按级别输出到不同文件
3. 使用 Poetry 创建项目并配置依赖
4. 实现测试覆盖率报告

---

## 📅 第8周：常用框架 & 生态

### Web 框架对照

| Java 框架 | Python 框架 | 定位 |
|-----------|-------------|------|
| Spring Boot | Django | 全功能框架 |
| Spark Java | Flask/FastAPI | 轻量微框架 |
| - | FastAPI | 现代高性能 |

```python
# ============ FastAPI (推荐) ============
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 数据模型 (类似 DTO)
class Item(BaseModel):
    name: str
    price: float
    tags: List[str] = []
    description: Optional[str] = None

# 模拟数据库
items = {}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items/")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"item_id": item_id, "item": item}

# 运行: uvicorn main:app --reload
```

```python
# ============ Flask ============
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello World"})

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    return jsonify({"id": item_id, "name": "Item"})

# 运行: flask run
```

### 数据处理库

```python
# ============ NumPy: 数值计算 ============
import numpy as np

# 创建数组
arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros((3, 3))      # 3x3 零矩阵
range_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# 数组操作
arr.mean()    # 平均值
arr.sum()     # 求和
arr.std()     # 标准差
arr.reshape(2, 3)  # 改变形状

# 矩阵运算
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
C = A @ B  # 矩阵乘法

# ============ Pandas: 数据分析 ============
import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85.5, 90.0, 78.5]
})

# 基本操作
df.head()           # 前5行
df.describe()       # 统计描述
df['age'].mean()    # 列平均值
df[df['age'] > 28]  # 筛选

# CSV 操作
df.to_csv('output.csv', index=False)
df = pd.read_csv('input.csv')

# 聚合
grouped = df.groupby('age').agg({'score': 'mean'})
```

### ORM 对照

| Java | Python | 说明 |
|------|--------|------|
| JPA/Hibernate | SQLAlchemy | ORM 框架 |
| MyBatis | - | 半自动映射 |

```python
# ============ SQLAlchemy ============
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
  
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)

engine = create_engine('sqlite:///test.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# CRUD
new_user = User(name='Alice', email='alice@example.com', age=25)
session.add(new_user)
session.commit()

# 查询
users = session.query(User).filter(User.age > 20).all()
for user in users:
    print(user.name)
```

### 🏋️ 练习任务

1. 用 FastAPI 创建 REST API：增删改查用户
2. 用 Pandas 分析 CSV 数据并生成报告
3. 用 SQLAlchemy 实现博客数据库操作
4. 完成一个完整的小项目

---

## 📚 学习资源推荐

### 官方文档
- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/)
- [FastAPI 文档](https://fastapi.tiangolo.com/zh/)
- [Pandas 文档](https://pandas.pydata.org/docs/)

### 书籍
- 《Python 编程：从入门到实践》
- 《流畅的 Python》（进阶）
- 《Python Cookbook》

### 在线学习
- [Real Python](https://realpython.com/)
- [LeetCode Python 题解](https://github.com/cy69855522/Interview-Boost)

---

## 🎯 关键差异总结

```
┌─────────────────────────────────────────────────────────────────┐
│                     Java vs Python 核心差异                      │
├─────────────────────────────────────────────────────────────────┤
│  1. 动态类型 vs 静态类型    │ Python 无需声明类型                 │
│  2. 缩进语法               │ Python 用缩进代替大括号             │
│  3. 多继承                 │ Python 支持多继承                   │
│  4. 鸭子类型               │ Python 关注"能做什么"而非"是什么"   │
│  5. GIL 限制               │ 多线程受 GIL 限制，需用多进程/异步   │
│  6. 列表即集合             │ Python 列表可做队列/栈/集合/队列     │
│  7. 函数式特性             │ Lambda、推导式、高阶函数原生支持    │
│  8. 解释型语言             │ 无需编译，直接运行                  │
└─────────────────────────────────────────────────────────────────┘
```

---

有什么具体主题需要我深入讲解吗？