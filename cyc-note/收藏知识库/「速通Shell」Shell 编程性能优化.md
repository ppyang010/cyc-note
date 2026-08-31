---
Title: "「速通Shell」Shell 编程性能优化"
Url: "https://juejin.cn/post/7678975240300773428"
Author: "柒号华仔"
Origin: "掘金"
Description: "前面几篇讲了 shell 的语言特性、错误处理、模块化、测试、信号处理，又用三篇讲了常用命令。脚本能跑、能维护、能上线，到这一步很多人就觉得够用了，但真正把脚本从能跑推到专业还有最后一关——性能。"
Tags:
  - "Shell中文技术社区"
  - "前端开发社区"
  - "前端技术交流"
  - "前端框架教程"
  - "JavaScript 学习资源"
  - "CSS 技巧与最佳实践"
  - "HTML5 最新动态"
  - "前端工程师职业发展"
  - "开源前端项目"
  - "前端技术趋势"
Created: "2026-08-31 16:35:28"
Cover: "https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7e994d7b558e46aaa1bbc33b88abcca1~tplv-k3u1fbpfcp-jj:160:120:0:0:q75.avis"
---

前面几篇讲了 shell 的语言特性、错误处理、模块化、测试、信号处理，又用三篇讲了常用命令。脚本能跑、能维护、能上线，到这一步很多人就觉得够用了，但 **真正把脚本从能跑推到专业还有最后一关——性能**。

很多人对 shell 性能有误解。一种觉得"shell 不就是跑命令嘛，能快到哪去"；另一种觉得"性能有问题就上 Python"。两种看法都不对，shell 脚本和 Python 性能差距没那么夸张，很多时候差的是写法。 **把"慢 shell 脚本"重写成"快 shell 脚本"，往往只是几个习惯的改变**。

这一篇我们系统讲 shell 性能优化的思路和具体技巧。读完你应该能做到：写脚本时心里有根弦，知道哪些写法是性能陷阱，知道怎么用 awk、bash 内置、并行化等手段加速。

## 一、shell 性能的基本法则

在讲具体技巧之前，先建立一个认知： **shell 性能问题的根源是 fork**。

什么是 fork？每当你调一个外部命令，shell 就要 fork 一个子进程去执行它。fork 本身的开销其实不大（微秒级），但 bash 里 fork 还要 exec 系统调用、加载动态库、初始化 stdio——整个过程通常要几毫秒。

这就带来了 shell 性能的第一法则： **避免不必要的 fork**。一个几毫秒的开销看起来不多，但脚本里如果有几千次循环，每次循环 fork 一次——几秒钟就过去了。

真实差距有多大？一个简单的例子：统计文件行数。

```bash
bash 代码解读复制代码# 写法一：wc
time wc -l bigfile.txt
# 0.005s
​
# 写法二：循环 read
time while read line; do ((count++)); done < bigfile.txt
# 0.8s
```

同一个文件，wc 比 bash 循环快 160 倍。这就是 fork 和不 fork 的差距。

理解了"fork 是慢的"这一点，下面的所有技巧都是围绕它展开的。

## 二、避免不必要的 fork

### 2.1 永远不要 cat file | grep

这是 shell 圈最经典的"反模式"：

```perl
perl 代码解读复制代码# 反模式：cat + 管道 + grep
time cat file.txt | grep "pattern" > result.txt
# 0.020s
​
# 正确：grep 直接读文件
time grep "pattern" file.txt > result.txt
# 0.010s
```

反模式创建了两个进程（cat + grep），正确写法只创建一个（grep）。 **性能提升 2 倍**。

类似的反模式还有：

```perl
perl 代码解读复制代码# 反模式：cat 多文件 + grep
time cat file1 file2 file3 | grep "pattern"
# 0.030s
​
# 正确：grep 接受多个文件
time grep "pattern" file1 file2 file3
# 0.012s
```

能用命令直接读文件，就不要 cat。

### 2.2 用 (<file)代替(<file) 代替 (cat file)

把文件内容读进变量：

```
ini 代码解读复制代码# 写法一：cat + 命令替换
content=$(cat file.txt)        # fork cat
# 0.020s
​
# 写法二：bash 内置
content=$(<file.txt)            # 无 fork
# 0.001s
```

`$(<file)` 是 bash 的"读文件到变量"语法，不调用任何外部命令，性能差 20 倍。

这个技巧在你需要把整个文件读进变量处理时特别有用。

### 2.3 用 read 代替 awk 取字段

如果只是按分隔符切几列， **用 `read` 比 awk 快**：

```bash
bash 代码解读复制代码# 写法一：awk
time awk -F: '{print $1}' /etc/passwd > users.txt
# 0.015s
​
# 写法二：read + bash 内置
time while IFS=: read -r user _; do echo "$user"; done < /etc/passwd > users.txt
# 0.030s
```

写法二反而更慢？这是因为 bash 循环的开销超过了 awk 一次调用的成本。awk 是用 C 写的，处理几百万行比 bash 循环快。

所以这个例子的真实结论是： **对大量数据用 awk，对少量数据用 read**。前面字符串那篇讲过这个权衡，这里再强调一次。

### 2.4 字符串处理用 bash 内置而不是 sed

简单的字符串操作，bash 内置比 sed 快很多：

```bash
bash 代码解读复制代码# 写法一：sed
time echo "hello world" | sed 's/world/shell/'
# 0.005s
​
# 写法二：bash 变量展开
time str="hello world"; str="${str/world/shell}"; echo "$str"
# 0.0001s
```

性能差 50 倍。 **简单的字符串替换、删除前后缀，bash 变量展开永远比 sed 快**。

复杂的正则匹配才用 sed/awk。判断标准：能用 `${var//pattern/replacement}` 解决的，就不要用 `echo "$var" | sed`。

### 2.5 数组长度用 ${#arr\[@\]} 而不是 wc

```bash
bash 代码解读复制代码# 写法一：wc
time echo "${arr[@]}" | wc -w
# 0.020s
​
# 写法二：bash 内置
time echo "${#arr[@]}"
# 0.0001s
```

`${#arr[@]}` 是 bash 内置的数组长度——不 fork 任何进程。

### 2.6 测试用 \[\[ \]\] 而不是 \[ \]

```lua
lua 代码解读复制代码# 写法一：[ ]（test 命令）
time for i in {1..1000}; do [ "$i" -gt 500 ] && true; done
# 0.300s
​
# 写法二：[[ ]]（bash 内置）
time for i in {1..1000}; do [[ "$i" -gt 500 ]] && true; done
# 0.005s
```

`[ ]` 实际上是 fork 一个 test 进程； `[[ ]]` 是 bash 内置关键字。1000 次循环差了 60 倍。

日常用 \[\[ \]\]，\[ \]\` 只在需要 POSIX 兼容时用。

## 三、bash 内置 vs 外部命令

shell 命令分两类：bash 内置和外部命令。

- 内置：bash 自身实现，不 fork。cd、echo、read、test、printf、declare、set、export、let、local 都是。
- 外部命令：独立可执行文件，每次调用都 fork。ls、cat、grep、sed、awk、wc、sort 都是。

**原则：能用内置就用内置**。下面是常见的内置替身对照表：

| 操作 | 外部命令（慢） | bash 内置（快） | 性能差 |
| --- | --- | --- | --- |
| 字符串长度 | `echo "$s" \| wc -c` | `${#s}` | 100x |
| 数组长度 | `echo "${arr[@]}" \| wc -w` | `${#arr[@]}` | 100x |
| 子串提取 | `echo "$s" \| cut -c1-5` | `${s:0:5}` | 50x |
| 字符串替换 | `echo "$s" \| sed 's/a/b/'` | `${s/a/b}` | 50x |
| 数值计算 | `expr $a + $b` | `$((a + b))` | 20x |
| 条件测试 | `[ "$a" -gt 0 ]` | `[[ "$a" -gt 0 ]]` | 60x |
| 读文件 | `$(cat file)` | `$(<file)` | 20x |
| 文件存在 | `[ -f file ]` | `[[ -f file ]]` | 50x |

记住这张表，写脚本时优先用内置。

## 四、awk/sed 是性能加速器

前面说"用 bash 内置比外部命令快"，但awk 是例外。

awk 一次调用就能完成 bash 循环 + 多次命令调用的事。 **对大量数据，awk 几乎总是比 bash 循环快一个数量级**。

### 4.1 awk 替代循环

```bash
bash 代码解读复制代码# 写法一：bash 循环统计
time while read line; do ((count++)); done < bigfile.txt
# 2.5s
​
# 写法二：awk
time awk 'END{print NR}' bigfile.txt
# 0.05s
```

awk 跑了几十倍快。这是 awk 用 C 写的 + 一次调用处理整个文件的红利。

再看一个例子——按列求和：

```bash
bash 代码解读复制代码# 写法一：bash 循环
time awk '{sum += $3} END {print sum}' data.txt > result.txt
# 写法二：纯 bash
time sum=0; while read -r a b c rest; do ((sum += c)); done < data.txt; echo $sum > result.txt
# 写法一：0.05s
# 写法二：2.0s
```

awk 快了 40 倍。

### 4.2 什么时候用 awk

**awk 适合**：

- 处理大文件（MB 级别以上）
- 按列处理数据
- 需要做统计（计数、求和、平均）
- 复杂的字段操作

**awk 不适合**：

- 简单的字段切分（小文件用 read 就够）
- 复杂的逻辑判断（bash 写起来更清晰）
- 需要调用大量其他命令的场景

一般来说，1000 行以下 bash 循环能搞定，1000 行以上用 awk。

### 4.3 sed 适合什么

sed 适合"按行批量修改"—— `s/old/new/g`、 `d` 删除、 `p` 打印。 **对于模式匹配的替换，sed 比 bash 循环快得多**。

```bash
bash 代码解读复制代码# 写法一：bash 循环 + 字符串替换
time while read line; do echo "${line/old/new}"; done < file.txt
# 写法二：sed
time sed 's/old/new/g' file.txt
# 写法一：2.0s
# 写法二：0.05s
```

## 五、避免循环里的重复工作

很多时候脚本慢不是因为单个操作慢，而是循环里的小开销被放大了一千次。

### 5.1 缓存常用的命令结果

```bash
bash 代码解读复制代码# 反模式：每次循环都算一次
for file in *.log; do
    today=$(date +%Y%m%d)
    count=$(wc -l < "$file")
    echo "$file: $count lines, today: $today"
done
​
# 优化：提到循环外
today=$(date +%Y%m%d)
for file in *.log; do
    count=$(wc -l < "$file")
    echo "$file: $count lines, today: $today"
done
```

`date` 调用一次 0.005s，1000 个文件就 5s。提到循环外省 5s。

类似的还有：

- 配置文件读一次，不要每个函数都重读
- 常量字符串用变量，不要每次拼接
- 路径解析一次，不要每次都 cd + pwd

### 5.2 用关联数组替代 grep

判断"某个值在不在列表里"：

```bash
bash 代码解读复制代码# 写法一：每次都 grep
time for name in "${names[@]}"; do
    if grep -q "^$name$" allowed.txt; then
        echo "$name allowed"
    fi
done
# 5s
​
# 写法二：先把 allowed 读进关联数组
time declare -A allowed
while read -r line; do allowed[$line]=1; done < allowed.txt
for name in "${names[@]}"; do
    if [[ -n "${allowed[$name]}" ]]; then
        echo "$name allowed"
    fi
done
# 0.5s
```

O(N\*M) 变成 O(N+M)，性能差 10 倍。

### 5.3 减少文件 IO

文件读写是相对慢的操作， **能一次读的就不要分多次读**：

```bash
bash 代码解读复制代码# 反模式：每次循环都读文件
for id in "${ids[@]}"; do
    name=$(grep "^$id:" /etc/passwd | cut -d: -f5)
    echo "$id: $name"
done
​
# 优化：一次读完整个文件
declare -A names
while IFS=: read -r id _ _ _ name _; do
    names[$id]=$name
done < /etc/passwd
​
for id in "${ids[@]}"; do
    echo "$id: ${names[$id]:-unknown}"
done
```

文件读一次比读 1000 次快得多。

## 六、并行化

如果脚本里有独立的任务，需要处理多个文件、调多个 API、查多个数据库，并行化能把多核机器的性能充分利用起来。

### 6.1 & + wait：基础并行

```bash
bash 代码解读复制代码# 串行：5 个任务各 1 秒
time for host in web1 web2 web3 web4 web5; do
    ssh "$host" uptime
done
# 5s
​
# 并行：5 个任务并发
time for host in web1 web2 web3 web4 web5; do
    ssh "$host" uptime &
done
wait
# 1s
```

`&` 把任务放后台， `wait` 等所有后台任务完成。 **5 倍提速**。

### 6.2 xargs -P：更可控的并行

xargs 的 `-P` 参数指定并行进程数， **比手写 & 灵活**：

```perl
perl 代码解读复制代码# 8 个进程并行处理
time find . -name "*.jpg" | xargs -P 8 -I {} convert {} -resize 50% {}.small.jpg
# 串行：40s
# 并行（8 核）：5s
```

**8 倍提速**。 `xargs -P` 适合"批量独立任务"，每个任务处理一个文件。

### 6.3 GNU parallel：最强大的并行

GNU parallel 是 xargs 的超集，支持并行、进度显示、结果合并。

```perl
perl 代码解读复制代码# 安装
apt install parallel    # Debian/Ubuntu
yum install parallel    # CentOS
​
# 并行压缩所有 .log
time find . -name "*.log" | parallel gzip {}
# 8 倍提速
​
# 显示进度
find . -name "*.log" | parallel --progress gzip {}
​
# 收集结果到文件
find . -name "*.log" | parallel --result output/ gzip {}
```

**parallel vs xargs -P**：

- xargs 简单、轻量、内置
- parallel 功能多、显示进度、跨平台一致性更好

日常用 xargs 够用，复杂场景上 parallel。

### 6.4 并行化的几个坑

**坑一：输出会乱**。多个进程同时输出到 stdout，结果会交错。 **解决：每个任务输出到独立文件，最后合并**：

```bash
bash 代码解读复制代码for host in web1 web2 web3; do
    ssh "$host" uptime > "/tmp/uptime_$host.txt" &
done
wait
cat /tmp/uptime_*.txt
rm /tmp/uptime_*.txt
```

**坑二：进程数太多反而慢**。100 个并发把 CPU 跑满、磁盘 IO 拥堵。 **经验：CPU 密集用 N=核数，IO 密集用 N=10-50**。

**坑三：日志混乱**。多个任务同时写同一个日志文件，输出会错乱。 **每个任务独立日志**。

## 七、性能分析工具

优化之前要先知道"哪里慢"。这一节讲几个常用的性能分析工具。

### 7.1 time：基本计时

```shell
shell 代码解读复制代码time ./script.sh
# real    0m5.123s    # 实际耗时
# user    0m3.456s    # 用户态 CPU 时间
# sys     0m0.234s    # 内核态 CPU 时间
```

`real` 是实际等待时间， `user + sys` 是 CPU 占用时间。如果 real 远大于 user + sys，说明在等 IO（网络/磁盘）。

### 7.2 strace：追踪系统调用

```bash
bash 代码解读复制代码# 看脚本调用了哪些系统调用
strace -c ./script.sh
​
# 看具体的调用
strace -e trace=open,read,write ./script.sh
```

strace 能告诉你脚本在等什么，是 fork 太多、还是磁盘 IO、还是网络。

### 7.3 perf：CPU 性能分析

```bash
bash 代码解读复制代码# 记录 CPU 事件
perf record ./script.sh
perf report
```

perf 能告诉你CPU 时间花在了哪些函数上。对 shell 脚本来说，主要看 awk、grep 这些外部命令的调用次数。

### 7.4 bash 内置的时间

```
ini 代码解读复制代码# bash 内置的 time，精度更高
TIMEFORMAT='real %3R, user %3U, sys %3S'
time ./script.sh
```

这个 time 是 shell 关键字，不会 fork /usr/bin/time。

## 八、实例：把一个慢脚本加速

我们看一个真实的慢脚本案例，看怎么一步步优化。

**原始版本** （处理 1000 个日志文件，统计错误数）：

```bash
bash 代码解读复制代码#!/bin/bash
for file in *.log; do
    count=$(cat "$file" | grep "ERROR" | wc -l)
    echo "$file: $count errors"
done
```

**性能**：1000 个文件，每文件 0.05s，总共 50s。

**优化第一步：去 cat**

```bash
bash 代码解读复制代码for file in *.log; do
    count=$(grep -c "ERROR" "$file")    # grep -c 直接计数
    echo "$file: $count errors"
done
```

**性能**：每文件 0.04s，总共 40s，提速 1.25x。

**优化第二步：循环里避免重复的 cat**

```bash
bash 代码解读复制代码total=0
for file in *.log; do
    count=$(grep -c "ERROR" "$file")
    echo "$file: $count errors"
    total=$((total + count))
done
echo "总计: $total"
```

**性能**：基本没变化，但 **代码更清晰**。

**优化第三步：并行化**

```bash
bash 代码解读复制代码total=0
for file in *.log; do
    (
        count=$(grep -c "ERROR" "$file")
        echo "$file: $count errors" >> /tmp/results.txt
        echo "$count"
    ) &
done > /tmp/counts.txt
​
# 等所有任务完成
wait
​
# 汇总
total=$(awk '{s+=$1} END {print s}' /tmp/counts.txt)
echo "总计: $total"
rm -f /tmp/results.txt /tmp/counts.txt
```

**性能**：8 核机器，6.25s，提速 8x。

**优化第四步：换思路，整个流程用 awk**

```bash
bash 代码解读复制代码# 一次 awk 调用处理所有文件
total=0
for file in *.log; do
    count=$(awk '/ERROR/{c++} END{print c+0}' "$file")
    total=$((total + count))
    echo "$file: $count errors"
done
echo "总计: $total"
```

**性能**：每文件 0.05s，总共 50s。awk 一次只处理一个文件，没有优势。

**真正的优化：批处理**

```bash
bash 代码解读复制代码# 把所有日志合并后一次处理
cat *.log | awk '/ERROR/{count++} END{print "总计:", count+0}'
```

但这样拿不到每个文件的统计——所以保留每个文件单独统计 + 并行化是最佳方案。

最终性能对比：

总提速 8x。这就是 shell 性能优化的实际效果，主要靠并行化，单点优化收益有限。

## 九、总结

shell 性能优化是个细节活，核心思路是：

- **避免不必要的 fork**：能内置就别调外部命令
- **bash 内置优先**：变量展开、 `[[ ]]`、 `${#arr[@]}` 都很便宜
- **awk 适合处理大数据**：一次调用处理整文件
- **并行化是最大提速**：CPU 密集任务用核数倍并行
- **先 profile 再优化**：用 time/strace/perf 找瓶颈

shell 性能问题通常不是shell 语言慢，而是用法不对，很多慢脚本改改写法就快 10 倍。

性能优化聊完，整个 shell 编程系列的主题到这里就比较完整了。从语言特性到工程实践，从常用命令到性能调优，shell 编程需要掌握的核心内容基本覆盖了。