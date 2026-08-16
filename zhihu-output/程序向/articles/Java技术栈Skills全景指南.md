---
id: "2046226789802981256"
title: "Java技术栈Skills全景指南"
author: "Li鱼鱼"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2046226789802981256"
created: "2026-06-05 13:48"
updated: "2026-06-05 13:48"
collected: "2026-06-05 13:48"
downloaded: "2026-08-16"
---
## 一、后端基础设施类 Skills

### 1.1 Redis 官方 Agent Skill（⭐ Redis 官方出品）

| 维度 | 说明 |
| ----- | ----- |
| 来源 | Redis 官方博客（http://redis.io） |
| 功能 | 教 AI Agent 正确使用 Redis，涵盖缓存、限流、会话管理、向量搜索、语义缓存、Pub/Sub、Streams |
| 核心内容 | 数据结构选型（Hashes vs JSON vs Sorted Sets vs Vector Sets）、反模式防护（禁止 KEYS 循环、禁止无界 Key 增长）、生产级默认配置（连接池、Pipeline、集群兼容、错误处理） |
| 核心理念 | “MCP 提供工具，Skills 教如何使用” |
| 安装 | 通过 npx skills add或手动放置到 skills 目录 |

**核心价值**：Redis 官方团队亲自编写的 Skill，确保 Agent 写出的 Redis 代码是"正确的方式"，而不是模型训练数据中的过时做法。

### 1.2 Antigravity Awesome Skills 中的数据库/中间件 Skills

以下 Skills 来自 [https://github.com/sickn33/antigravity-awesome-skills](https://link.zhihu.com/?target=https%3A//github.com/sickn33/antigravity-awesome-skills)（⭐ 38.9k，1,480+ Skills），与 Java 后端基础设施直接相关：

| Skill 名称 | 说明 | 适用场景 |
| ----- | ----- | ----- |
| database-designer | 模式分析、ERD 生成、索引优化、迁移生成器 | 数据库设计阶段 |
| database-schema-designer | 需求 → 迁移文件、类型定义、种子数据、RLS 策略 | 新项目初始化 |
| migration-architect | 迁移规划、兼容性检查、回滚生成 | 数据库版本管理 |
| postgres-best-practices | Supabase 出品的 PostgreSQL 最佳实践 | PostgreSQL 项目 |
| postgresql | 数据库设计：类型、索引、约束、性能模式、高级特性 | 通用 PostgreSQL 设计 |
| postgresql-optimization | 查询调优、索引策略、性能分析、生产数据库管理 | 数据库优化 |
| sql-optimization-patterns | 慢查询优化、索引设计、执行计划分析 | SQL 性能调优 |
| redis | Redis 数据结构使用规范、缓存策略、连接管理 | Redis 开发（如官方 Skill 未安装） |
| message-queue-patterns | 消息队列架构、RabbitMQ/Kafka 模式、重试与幂等 | MQ 队列设计 |
| kafka-expert | Kafka Producer/Consumer 配置、分区策略、Exactly-Once 语义 | Kafka 消息系统 |
| mysql-best-practices | MySQL 设计规范、索引策略、事务隔离、连接池优化 | MySQL 项目 |

**安装**：`npx antigravity-awesome-skills --claude`

## 二、前端开发 Skills（Vue / React / TailwindCSS / UI 组件库）

### 2.1 Patterns.dev Skills（⭐ 58 个 Skills，官方维护）

Patterns.dev 出品，是目前最完整的前端 Skills 集合，覆盖 JavaScript、React、Vue 三大技术栈。

| 维度 | 说明 |
| ----- | ----- |
| 仓库 | https://github.com/PatternsDev/skills |
| 规模 | 58 个独立 Skills |
| 兼容 | Claude Code、Cursor、Codex、Gemini CLI、Antigravity、OpenCode |
| 安装 | npx skills add PatternsDev/skills --skill <skill-name> |

### React Skills（18 个）

| Skill | 类型 | 说明 |
| ----- | ----- | ----- |
| hooks-pattern | 设计 | 使用函数在多个组件间复用有状态逻辑 |
| hoc-pattern | 设计 | 将可复用逻辑通过 props 传递给组件 |
| compound-pattern | 设计 | 创建多个组件协同完成单一任务 |
| render-props-pattern | 设计 | 通过 props 传递 JSX 元素 |
| presentational-container-pattern | 设计 | 视图与应用逻辑分离 |
| ai-ui-patterns | 设计 | 构建 AI 驱动的界面（聊天机器人、智能助手） |
| react-2026 | 设计 | 2026 现代 React 技术栈（Vitest、Vite SSR、React Compiler） |
| react-composition-2026 | 设计 | React 19 组合模式：复合组件、Slots、多态性 |
| client-side-rendering | 渲染 | 客户端渲染模式 |
| server-side-rendering | 渲染 | 服务端渲染模式 |
| static-rendering | 渲染 | 静态生成模式 |
| incremental-static-rendering | 渲染 | 增量静态再生（ISR） |
| streaming-ssr | 渲染 | 流式 SSR |
| progressive-hydration | 渲染 | 渐进式水合 |
| react-server-components | 渲染 | React Server Components |
| react-selective-hydration | 渲染 | 选择性水合 |
| react-render-optimization | 性能 | Vite/SPA 渲染优化：组件边界、延迟渲染、布局抖动 |
| react-data-fetching | 性能 | TanStack Query、Suspense、React.cache、延迟 Promise |

### Vue Skills

| Skill | 类型 | 说明 |
| ----- | ----- | ----- |
| vue-composition-api | 设计 | Vue 3 Composition API 最佳实践 |
| vue-performance | 性能 | Vue 应用性能优化：懒加载、虚拟滚动、计算属性优化 |
| vue-ssr | 渲染 | Vue 3 SSR 指南：Nuxt 集成、水合策略、流式渲染 |

### JavaScript Skills（29 个）

| Skill | 类型 | 说明 |
| ----- | ----- | ----- |
| js-performance-patterns | 性能 | JavaScript 性能模式（2026 新增） |
| vite-bundle-optimization | 性能 | Vite 打包优化（2026 新增） |
| design-patterns | 设计 | 经典设计模式（单例、观察者、策略等） |
| islands-architecture | 渲染 | 孤岛架构：在服务端页面中渲染小块交互 |
| view-transitions | 渲染 | View Transitions API 页面转场动画 |

### 2.2 Vercel Labs 前端 Skills（⭐ 安装量 148,900+）

以下 Skills 由 Vercel Labs 出品，是目前安装量最高的前端开发 Skills。

| Skill 名称 | 安装量 | 说明 | 安装方式 |
| ----- | ----- | ----- | ----- |
| react-best-practices | 148,900+ | React Hooks、组合模式、性能优化 | npx skills add vercel-labs/agent-skills/react-best-practices |
| web-design-guidelines | 112,700+ | 全面的 Web 设计标准，打造精致界面 | npx skills add vercel-labs/agent-skills/web-design-guidelines |
| composition-patterns | 48,400+ | 复合组件与可扩展组合模式 | npx skills add vercel-labs/agent-skills/react-composition |
| next-best-practices | — | Next.js 最佳实践（App Router、Server Components） | npx skills add vercel-labs/next-skills/next-best-practices |
| react-native-skills | 34,300+ | React Native 性能与架构 | npx skills add vercel-labs/agent-skills/react-native-skills |

### 2.3 TailwindCSS / shadcn/ui 相关 Skills

### TailwindCSS 相关

| Skill 名称 | 作者 | 说明 | 安装方式 |
| ----- | ----- | ----- | ----- |
| frontend-design | Anthropic 官方 | 大胆、有意图的 UI 设计，避免"AI 味"外观 | npx skills add anthropics/skills/frontend-design |
| web-design-guidelines | Vercel Labs | 全面的 Web 设计标准，包含 Tailwind 设计系统模式 | npx skills add vercel-labs/agent-skills/web-design-guidelines |

Tailwind 目前没有官方独立 Skill，但 `frontend-design`和 `web-design-guidelines`已包含完整的 Tailwind 设计系统指导，包括 Token-based 颜色和间距系统、组件变体模式、响应式工具类组织、Dark mode 实现、一致的动画模式。

### shadcn/ui 相关

| Skill 名称 | 作者 | 说明 |
| ----- | ----- | ----- |
| shadcn-ui | Google Labs（Stitch） | shadcn/ui 组件库模式：复制粘贴模型、自定义模式、无障碍集成 |

## 三、全栈综合 Skills 集合

### 3.1 Jeffallan/claude-skills（⭐ 66 个全栈 Skills）

| 维度 | 说明 |
| ----- | ----- |
| 仓库 | https://github.com/Jeffallan/claude-skills |
| 规模 | 66 个专业 Skills |
| 覆盖领域 | 前端（React、Vue、TypeScript）、后端（Node.js、Python）、数据库、DevOps、安全、AI/ML |
| 安装 | 克隆到 skills 目录 |

包含的 Spring Boot / Java 相关 Skills：

-   `java-springboot`：Spring Boot 最佳实践（项目结构、依赖注入、配置管理、Web 层、Service 层、数据访问、日志）
-   `database-designer`：数据库架构设计
-   `api-design`：API 设计模式

### 3.2 alirezarezvani/claude-skills（51 + 78 个 Skills）

| 维度 | 说明 |
| ----- | ----- |
| 仓库 | https://github.com/alirezarezvani/claude-skills |
| 规模 | 129 个 Skills（51 Core + 78 POWERFUL） |
| 安装 | 通过安装脚本 ./scripts/install.sh --tool <tool> --target . |
| 兼容 | Cursor、Aider、Kilo Code、Windsurf、OpenCode、Augment、Antigravity、Hermes Agent、Mistral Vibe |

与 Java/Spring Boot 前端开发相关的 Skills：

-   `database-designer`：模式分析、ERD 生成、索引优化
-   `database-schema-designer`：需求 → 迁移、类型定义、种子数据
-   `migration-architect`：迁移规划、兼容性检查、回滚生成
-   `ci-cd-pipeline-builder`：分析技术栈 → 生成 CI/CD 配置
-   `agent-designer`：多 Agent 编排、工具 schema、性能评估

## 四、如何为 Java 后端框架编写自定义 Skill

### 4.1 MyBatis-Plus 自定义 Skill 示例

```text
# 创建 skill 目录
mkdir -p .claude/skills/mybatis-plus

# 创建 SKILL.md
cat > .claude/skills/mybatis-plus/SKILL.md << 'EOF'
---
name: mybatis-plus
description: MyBatis-Plus 开发规范与最佳实践。当用户要求创建 Mapper、Service 或编写数据库查询时自动激活。
---

# MyBatis-Plus 开发指南

## 触发条件
- 创建新的 Mapper 接口
- 编写 Service 层数据库操作
- 设计 Entity / DTO 映射

## 核心规则
1. Mapper 继承 BaseMapper<T>，不写 XML 除非必须
2. Service 继承 IService<T>，实现ServiceImpl<M, T>
3. 使用 @TableName 标注表名，@TableId 标注主键
4. 逻辑删除使用 @TableLogic，配置在 application.yml 中
5. 分页使用 Page<T> 对象，配置 MybatisPlusInterceptor
6. 条件构造器统一使用 LambdaQueryWrapper，避免字符串字段名

## 项目约定
- Entity 放在 entity/ 包，DTO 放在 dto/ 包
- Mapper XML 放在 resources/mapper/ 目录
- 主键策略：ASSIGN_ID（雪花算法）
- 表名前缀：t_
EOF

# 创建参考文件
mkdir -p .claude/skills/mybatis-plus/references
```

### 4.2 Redis 自定义 Skill 示例（配合官方 Skill 使用）

```text
mkdir -p .claude/skills/redis-project
cat > .claude/skills/redis-project/SKILL.md << 'EOF'
---
name: redis-project
description: 本项目 Redis 使用规范，覆盖缓存、Session、分布式锁等场景。
---

# 项目 Redis 使用规范

## 触发条件
- 使用 Redis 作为缓存
- 实现分布式锁
- 配置 Redis 连接池

## 核心规则
1. 使用 Spring Data Redis + Lettuce 客户端
2. Key 命名规范：{module}:{business}:{id}，如 user:profile:12345
3. 过期时间统一在配置中定义，禁止硬编码
4. 分布式锁使用 Redisson，禁止自实现 SETNX
5. 缓存穿透：使用布隆过滤器 + 空值缓存
6. 缓存雪崩：过期时间加随机偏移
EOF
```

## 五、推荐的 AI Agent Skills 全栈工作流

### 5.1 标准全栈工作流

```text
1. 数据库设计阶段：加载 database-designer + migration-architect
2. 后端开发阶段：加载 Spring Boot Skills + MyBatis/Redis Skills
3. 前端开发阶段：加载 Vue/React Skills + Tailwind/设计指南 Skills
4. API 联调阶段：加载 api-design-principles
5. 测试阶段：加载 tdd-mastery + 前端测试 Skills
6. 部署阶段：加载 ci-cd-pipeline-builder
```

### 5.2 多 Agent 协作模式

对于复杂全栈项目：

| Agent 角色 | 职责 | 推荐 Skill |
| ----- | ----- | ----- |
| 数据库架构师 | 数据库设计、迁移规划 | database-designer + migration-architect |
| 后端开发者 | Spring Boot + MyBatis + Redis 开发 | spring-boot-engineer + 自定义 MyBatis Skill |
| 前端开发者 | Vue/React + UI 组件库开发 | Patterns.dev React/Vue Skills + web-design-guidelines |
| 安全审计 | 安全漏洞扫描 | security-hardening |
| DevOps 工程师 | CI/CD、部署 | ci-cd-pipeline-builder |