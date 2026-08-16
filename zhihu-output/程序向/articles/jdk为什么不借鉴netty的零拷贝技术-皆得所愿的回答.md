---
id: "2055028705924325888"
title: "jdk为什么不借鉴netty的零拷贝技术?"
author: "皆得所愿"
type: zhihu-answer
source: "https://www.zhihu.com/question/498972987/answer/2055028705924325888"
created: "2026-06-29 20:43"
updated: "2026-06-29 20:43"
collected: "2026-06-29 20:43"
downloaded: "2026-08-16"
---
**​  
JAVA的产品**Aeron / Chronicle Queue / Disruptor 能够达到纳秒-微秒级性能就是采用零拷贝技术。是否采用零拷贝是对底层机制的理解和设计的选择，和JDK的设计无关。

**零拷贝（Zero-Copy）​**​ 是指在数据传输过程中，避免数据在内核空间和用户空间之间来回拷贝，从而减少 CPU 占用、降低延迟、提升吞吐量的技术。

* * *

### 一、传统方式的问题（非零拷贝）

假设你要把一个文件从磁盘读出，通过网络发给客户端：

```text
应用程序 read()  →  内核读磁盘 → 内核缓冲区 → 拷贝到用户缓冲区
应用程序 write() →  拷贝到内核socket缓冲区 → 网卡发送
```

**发生了两次数据拷贝：**

1.  内核缓冲区 → 用户缓冲区（CPU 参与拷贝）
2.  用户缓冲区 → 内核 Socket 缓冲区（CPU 参与拷贝）

还有四次上下文切换（用户态↔内核态），CPU 大量时间花在搬数据上。

* * *

### 二、零拷贝做了什么？

**零拷贝让数据直接从内核缓冲区进入网卡，绕开用户空间：**

```text
sendfile(file_fd, socket_fd)

磁盘 → 内核页缓存 → DMA → 网卡
```

​**只有一次 DMA 拷贝（硬件完成，不消耗 CPU）**​，没有 CPU 参与的拷贝。

* * *

### 三、Aeron 中的零拷贝

Aeron 的零拷贝体现在两个方面：

### 1\. 接收端：直接从共享内存读取，不进堆

```text
// Aeron FragmentHandler 收到的 DirectBuffer 指向共享内存
FragmentHandler handler = (buffer, offset, length, header) -> {
    // buffer 底层是 mmap 出来的堆外内存，不是 JVM 堆上的 byte[]
    double price = buffer.getDouble(offset);  // 直接从共享内存读，零拷贝
};
```

-   传统做法：`byte[] data = new byte[length]; buffer.getBytes(offset, data);`→ 发生一次拷贝
-   Aeron 做法：直接用\*\* **`buffer.getXxx(offset)`从共享内存读取 →** \*\***零拷贝**

### 2\. 发送端：直接写共享内存，不进堆

```text
UnsafeBuffer buf = new UnsafeBuffer(BufferUtil.allocateDirectAligned(128, 64));
buf.putDouble(0, price);       // 直接写到堆外内存
buf.putBytes(8, symBytes);
pub.offer(buf, 0, length);     // Aeron 直接引用这片内存发送，不拷贝
```

* * *

### 四、Chronicle Queue 中的零拷贝

Chronicle Queue 基于\*\* **​**内存映射文件（mmap）\*\*​：

```text
// 写入时，数据直接写入 mmap 区域，等价于写磁盘（OS 异步刷盘）
appender.writeDocument(tick);

// 读取时，直接读 mmap 区域，不经过 byte[] 拷贝
tailer.readDocument(tick);
```

**​效果：​**​ 写入和读取都不产生 Java 堆内的 byte\[\] 对象，没有 GC 压力，也没有 CPU 拷贝。

* * *

### 五、零拷贝的几种常见实现

| 技术 | 原理 | 典型场景 |
| ----- | ----- | ----- |
| ​mmap（内存映射文件）​​ | 文件直接映射到进程地址空间 | Chronicle Queue、Kafka 日志段 |
| sendfile​ | 内核态直接将数据从文件描述符传到 socket | Nginx 静态文件、Tomcat 文件下载 |
| ​DMA（直接内存访问）​​ | 硬件直接在外设和内存间传输 | 网卡、磁盘控制器 |
| RDMA​ | 绕过双方操作系统，远程直接读内存 | 高性能计算、分布式存储 |
| ​DirectBuffer（堆外内存）​​ | JVM 直接操作 OS 分配的内存 | Aeron、Netty、Disruptor |

* * *

### 六、直观类比

想象你要把一本书的内容复印给另一个人：

-   ​**非零拷贝**​：你把书从书架上拿出来（磁盘→内核），抄到笔记本上（内核→用户），再把笔记本递给别人（用户→内核），别人再抄一遍（内核→用户）。你抄了两遍。
-   ​**零拷贝**​：你直接把书架上的那页纸撕下来递给对方。没有抄写动作。

* * *

### 七、为什么对低延迟系统重要？

```text
传统方式（非零拷贝）：
  接收消息 → 内核拷贝到 byte[] → GC 回收 byte[] → 延迟抖动 10-100μs

零拷贝方式：
  接收消息 → 直接读共享内存 → 无 GC → 延迟稳定在亚微秒级
```

在高频交易系统中，每微秒的抖动都可能导致滑点损失。零拷贝消除了 GC 暂停和 CPU 拷贝这两个主要的延迟不稳定因素，是 Aeron / Chronicle Queue / Disruptor 能够达到纳秒-微秒级性能的关键原因之一。