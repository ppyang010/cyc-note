---
Title: OpenSpec框架实现原理源码级剖析OpenSpec 的核心在于 Artifact Graph，将文档创建过程建模为有 - 掘金
Url: "https://juejin.cn/post/7600670487409492020"
Author: 
Origin: juejin.cn
Description: OpenSpec 的核心在于 Artifact Graph，将文档创建过程建模为有向无环图（DAG），并通过拓扑排序计算构建顺序。
Tags:
  - 源码中文技术社区
  - 前端开发社区
  - 前端技术交流
  - 前端框架教程
  - JavaScript 学习资源
  - CSS 技巧与最佳实践
  - HTML5 最新动态
  - 前端工程师职业发展
  - 开源前端项目
  - 前端技术趋势
Created: "2026-04-27 17:31:35"
Cover: "https://lf-web-assets.juejin.cn/obj/juejin-web/xitu_juejin_web/58aaf1326ac763d8a1054056f3b7f2ef.svg"
---
## OpenSpec 实现原理总结

本文档是 OpenSpec 深度技术文档的快速参考指南。 **完整文档索引：** [implementation/README.md](https://link.juejin.cn/?target=https%3A%2F%2Flink.zhihu.com%2F%3Ftarget%3Dhttps%253A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2Fimplementation%2FREADME.md "https://link.zhihu.com/?target=https%3A//github.com/wenxiaoyu/openspec-doc/blob/main/implementation/README.md")

### 📁 文档位置

完整的技术文档位于 `docs/implementation/` 目录：

```perl
perl 体验AI代码助手 代码解读复制代码implementation/
├── README.md                          # 文档索引和导航
├── 00-overview.md                     # 概览和前置知识
├── 01-architecture.md                 # 架构总览
├── 02-artifact-graph.md               # Artifact Graph 系统
├── 03-schema-system.md                # Schema 系统
├── 04-state-management.md             # 状态管理
└── 05-instruction-generation.md       # 指令生成系统
```

### 🎯 核心概念速查

#### 1\. Artifact Graph（工件依赖图）

**位置：** `docs/implementation/02-artifact-graph.md`

**核心思想：** 将文档创建过程建模为有向无环图（DAG）

**关键算法：**

- **拓扑排序** - 计算构建顺序（Kahn's Algorithm）
- **依赖检测** - 查找可执行的下一步
- **循环检测** - DFS 检测环

**代码位置：** `src/core/artifact-graph/graph.ts`

```typescript
typescript 体验AI代码助手 代码解读复制代码// 核心 API
graph.getBuildOrder()              // 获取构建顺序
graph.getNextArtifacts(completed)  // 查找可执行工件
graph.isComplete(completed)        // 检查是否完成
graph.getBlocked(completed)        // 查找阻塞工件
```

#### 2\. Schema 系统

**位置：** `./implementation/03-schema-system.md`

**核心思想：** 声明式工作流定义

**三层解析优先级：**

```sql
sql 体验AI代码助手 代码解读复制代码Project-local > User-global > Package-builtin
```

**代码位置：** `src/core/artifact-graph/schema.ts`, `resolver.ts`

```yaml
yaml 体验AI代码助手 代码解读复制代码# Schema 定义示例
name: spec-driven
version: 1
artifacts:
  - id: proposal
    generates: proposal.md
    requires: []
  - id: specs
    requires: [proposal]
```

#### 3\. 状态管理

**位置：** `./implementation/04-state-management.md`

**核心思想：** 状态即文件（State as Files）

**设计原则：**

- 工件完成状态 = 文件是否存在
- 支持 Glob 模式（ `specs/**/*.md`）
- 无需数据库

**代码位置：** `src/core/artifact-graph/state.ts`

```typescript
typescript 体验AI代码助手 代码解读复制代码// 核心 API
detectCompleted(graph, changeDir)  // 检测完成状态
loadChangeContext(...)             // 加载变更上下文
formatChangeStatus(context)        // 格式化状态
```

#### 4\. 指令生成

**位置：** `./implementation/05-instruction-generation.md`

**核心思想：** 为 AI 生成结构化指令

**指令组成：**

- `context` - 项目背景（约束）
- `rules` - 工件规则（约束）
- `template` - 输出结构
- `dependencies` - 依赖信息
- `instruction` - 创建指导

**代码位置：** `src/core/artifact-graph/instruction-loader.ts`

```typescript
typescript 体验AI代码助手 代码解读复制代码// 核心 API
generateInstructions(context, artifactId)  // 生成工件指令
generateApplyInstructions(...)             // 生成 Apply 指令
loadTemplate(schemaName, templatePath)     // 加载模板
```

### 🔄 数据流示例

#### 创建新变更

```csharp
csharp 体验AI代码助手 代码解读复制代码用户: openspec new change add-auth
  ↓
CLI 解析和验证
  ↓
创建目录: openspec/changes/add-auth/
  ↓
写入元数据: .openspec.yaml { schema: 'spec-driven' }
  ↓
输出: "Created change 'add-auth'"
```

#### 生成指令

```makefile
makefile 体验AI代码助手 代码解读复制代码用户: openspec instructions proposal --change add-auth
  ↓
加载上下文:
  ├─ 解析 Schema
  ├─ 构建依赖图
  └─ 检测完成状态
  ↓
生成指令:
  ├─ 加载模板
  ├─ 读取配置
  ├─ 收集依赖
  └─ 组装指令
  ↓
输出: 结构化的 XML 格式指令
```

#### 检测状态

```csharp
csharp 体验AI代码助手 代码解读复制代码用户: openspec status --change add-auth
  ↓
加载上下文
  ↓
检测完成状态:
  ├─ 检查 proposal.md 是否存在
  ├─ 检查 specs/**/*.md 是否有文件
  ├─ 检查 design.md 是否存在
  └─ 检查 tasks.md 是否存在
  ↓
格式化输出:
  ✓ proposal
  ✓ specs
  → design
  ○ tasks (blocked by: design)
```

### 🏗️ 架构层次

```
scss 体验AI代码助手 代码解读复制代码┌─────────────────────────────────────┐
│         CLI 层 (Commander.js)       │  ← 命令解析、路由
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│         命令层 (Commands)           │  ← 用户交互、输出格式化
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│      核心引擎层 (Core)              │  ← 业务逻辑
│  ┌──────────────────────────────┐  │
│  │   Artifact Graph Engine      │  │  ← 依赖管理
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │   Instruction Loader         │  │  ← 指令生成
│  └──────────────────────────────┘  │
└────────────────┬────────────────────┘
                 │
┌────────────────▼────────────────────┐
│         数据层 (Data)               │  ← 文件系统、Schema
└─────────────────────────────────────┘
```

### 📊 关键指标

#### 时间复杂度

| 操作 | 复杂度 | 说明 |
| --- | --- | --- |
| 拓扑排序 | O(V + E) | V=工件数, E=依赖边数 |
| 状态检测 | O(V) | 检查所有工件 |
| 依赖查询 | O(V × D) | D=平均依赖数 |

#### 空间复杂度

| 数据结构 | 复杂度 |
| --- | --- |
| 依赖图 | O(V + E) |
| 完成状态 | O(V) |
| 指令缓存 | O(1) per artifact |

### 🎨 设计模式

#### 1\. 工厂模式

```typescript
typescript 体验AI代码助手 代码解读复制代码// ArtifactGraph 创建
ArtifactGraph.fromYaml(filePath)
ArtifactGraph.fromYamlContent(content)
ArtifactGraph.fromSchema(schema)
```

#### 2\. 适配器模式

```typescript
typescript 体验AI代码助手 代码解读复制代码// 多工具适配
interface ToolCommandAdapter {
  getFilePath(id): string
  formatFile(content): string
}
```

#### 3\. 策略模式

```typescript
typescript 体验AI代码助手 代码解读复制代码// 不同的输出格式
printStatusText(status)      // 文本格式
JSON.stringify(status)       // JSON 格式
```

#### 4\. 模板方法模式

```typescript
typescript 体验AI代码助手 代码解读复制代码// Schema 定义模板，引擎执行流程
artifacts.forEach(artifact => {
  loadTemplate(artifact.template)
  generateInstructions(artifact)
  createArtifact(artifact)
})
```

### 🔧 扩展点

#### 1\. 自定义 Schema

**位置：** `openspec/schemas/<name>/`

**文件：**

- `schema.yaml` - 工作流定义
- `templates/` - 模板文件

#### 2\. 项目配置

**位置：** `openspec/config.yaml`

**内容：**

- `context` - 项目背景
- `rules` - 工件规则

#### 3\. 工具适配器

**位置：** `src/core/command-generation/adapters/`

**实现：** `ToolCommandAdapter` 接口

### 📚 学习路径

#### 初学者

1. 阅读 [架构总览](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2Fimplementation%2F01-architecture.md "https://github.com/wenxiaoyu/openspec-doc/blob/main/implementation/01-architecture.md")
2. 理解 [Artifact Graph](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2Fimplementation%2F02-artifact-graph.md "https://github.com/wenxiaoyu/openspec-doc/blob/main/implementation/02-artifact-graph.md")
3. 学习 [Schema 系统](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2Fimplementation%2F03-schema-system.md "https://github.com/wenxiaoyu/openspec-doc/blob/main/implementation/03-schema-system.md")

#### 进阶

1. 深入 [状态管理](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2F%2Fimplementation%2F04-state-management.md "https://github.com/wenxiaoyu/openspec-doc/blob/main//implementation/04-state-management.md")
2. 掌握 [指令生成](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2F%2Fimplementation%2F05-instruction-generation.md "https://github.com/wenxiaoyu/openspec-doc/blob/main//implementation/05-instruction-generation.md")
3. 研究源码实现

#### 扩展开发

1. 创建自定义 Schema
2. 添加工具适配器
3. 贡献核心功能

### 🔗 相关资源

- **完整文档：** `docs/implementation/`
- **源代码：** `src/core/`
- **测试用例：** `test/core/`
- **用户文档：** `docs/`

### 💡 关键要点

1. **Artifact Graph** 是核心 - 理解它就理解了整个系统
2. **状态即文件** - 简单但强大的设计
3. **声明式 Schema** - 灵活的工作流定义
4. **结构化指令** - AI 集成的关键
5. **适配器模式** - 支持多工具的秘诀

### 🎯 下一步

- 运行项目，跟踪完整工作流
- 阅读源码，理解实现细节
- 创建自定义 Schema，实践扩展
- 贡献代码，参与开发

---

**完整文档索引：** [implementation/README.md](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2Fwenxiaoyu%2Fopenspec-doc%2Fblob%2Fmain%2Fimplementation%2FREADME.md "https://github.com/wenxiaoyu/openspec-doc/blob/main/implementation/README.md")