---
id: "387612085"
title: "你工作中最推荐的 C/C++ 程序库有哪些，为什么？"
author: "zydcom"
type: zhihu-answer
source: "https://www.zhihu.com/question/51134387/answer/387612085"
created: "2018-05-09 22:57"
updated: "2018-05-10 07:38"
collected: "2018-05-09 22:57"
downloaded: "2026-08-16"
---
做存储, 数据库系统方面的开发，主要用到

\* grpc/libevent/libev/libasio 实现高性能网络服务器

\* protobuf 数据结构序列化/反序列化，方便数据交换

\* LevelDB/RocksDB 嵌入式KV数据库

\* snappy/zlib/lz4 数据压缩，解压缩

\* jemalloc/tcmalloc 高效内存分配器，尤其多线程场景

\* jerasure Reed Solomon编解码，给存储系统实现erasure code

\* murmurhash… 实现hash摘要

\* crc32 数据存储或传输时的数据校验

\* cJSON 解析json格式配置文件

\* libBSON JSON序列化/反序列化，MongoDB使用这种格式存储数据

\* boost 功能丰富的C++基础库，轻度使用，C++11/14后基本不用了。

\* libRedis redis是一个数据库服务，并不是单独的库，但其代码精简，质量非常高，里面很多代码都可以拿出来直接复用，比如网络，各种数据结构的实现。