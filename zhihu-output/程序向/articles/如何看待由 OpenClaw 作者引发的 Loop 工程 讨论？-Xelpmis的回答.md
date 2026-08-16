---
id: "2048267036585940333"
title: "如何看待由 OpenClaw 作者引发的 \"Loop 工程\" 讨论？"
author: "Xelpmis"
type: zhihu-answer
source: "https://www.zhihu.com/question/2048003050531558553/answer/2048267036585940333"
created: "2026-06-11 04:55"
updated: "2026-06-11 04:55"
collected: "2026-06-11 04:55"
downloaded: "2026-08-16"
---
不想看了，挑一个你喜欢的去炒吧\[狗头\]

| Agent 工程 | 对标的软件/计算机概念 | 一句话本质 |
| ----- | ----- | ----- |
| Prompt engineering | 语句 / 表达式 | 单条指令怎么写,一行 print |
| Loop engineering | 控制流(for/while/递归) | 把单次调用变成迭代、重试、收敛 |
| Harness engineering | 运行时 / 解释器 / VM | agent 的 JVM,执行壳与 I/O 管道 |
| Context engineering | 内存管理 / 手动 GC | 上下文窗口是 RAM,手动 evict 和 compact |
| Memory engineering | 持久化 / 数据库 | 跨 session 落盘,INSERT INTO |
| Eval / Verifier engineering | 类型系统 / 断言 / 单元测试 | 校验 agent 的”返回值”对不对 |
| Orchestration engineering | 并发 / 多线程 / actor 模型 | 多 agent 调度、死锁、竞态 |
| Protocol engineering | FFI / ABI / 接口规范 | agent 间和工具间的调用约定(MCP) |
| Policy / Guardrail engineering | 权限模型 / 异常处理 | sudo + try/catch,哪些动作要人点头 |
| Tool engineering | 标准库 / API 设计 | 给 agent 造好用的工具和函数签名 |
| Retrieval engineering | 索引 / 查询优化 | RAG,怎么把对的资料喂进去 |
| Skill / Module engineering | 库 / 包 / 模块化 | 可复用的能力封装 |
| Router engineering | 调度器 / 负载均衡 | 把任务分给哪个模型/agent/路径 |
| State engineering | 状态机 / checkpoint | 显式管理状态转移与回滚 |
| Sandbox engineering | 虚拟化 / 容器 / 隔离 | 限制 agent 能碰什么,别 rm -rf / |
| Observability engineering | 日志 / trace / profiling | 看清每一步在干嘛、卡在哪 |
| Cost engineering | 性能剖析 + 经济学 | 每次求值都烧钱,复杂度换算成美元 |
| Caching engineering | 缓存(prompt / KV cache) | 别重复烧 token,命中率就是省钱 |
| Security engineering | 安全 / 注入防御 | prompt injection 是新版 SQL 注入 |
| Alignment / Spec engineering | 形式化规约 / 契约式设计 | 把”想要什么”精确钉死,防止跑偏 |
| Meta / Compiler engineering | 编译器 / 代码生成 | 把人类意图自动降级成上面所有层 |