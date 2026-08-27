[一份 AGENTS.md，让 AI 代码规范率从 60% 飙升到 95%一份 AGENTS.md，让 AI 代码规范率从 - 掘金](https://juejin.cn/post/7639561816260886571?utm_source=gold_browser_extension) 

 > 前端 AI Skill 体系 · 实战篇
> 
> 5 分钟写一份 AGENTS.md，让 AI 从此按你的规矩写代码。

### 目录

*   [从评论区最多的一个问题说起](#%E4%BB%8E%E8%AF%84%E8%AE%BA%E5%8C%BA%E6%9C%80%E5%A4%9A%E7%9A%84%E4%B8%80%E4%B8%AA%E9%97%AE%E9%A2%98%E8%AF%B4%E8%B5%B7 "#%E4%BB%8E%E8%AF%84%E8%AE%BA%E5%8C%BA%E6%9C%80%E5%A4%9A%E7%9A%84%E4%B8%80%E4%B8%AA%E9%97%AE%E9%A2%98%E8%AF%B4%E8%B5%B7")
*   [AGENTS.md 到底是什么](#agentsmd-%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88 "#agentsmd-%E5%88%B0%E5%BA%95%E6%98%AF%E4%BB%80%E4%B9%88")
*   [没有 AGENTS.md vs 有 AGENTS.md](#%E6%B2%A1%E6%9C%89-agentsmd-vs-%E6%9C%89-agentsmd "#%E6%B2%A1%E6%9C%89-agentsmd-vs-%E6%9C%89-agentsmd")
    *   [场景 1：写一个复制按钮组件](#%E5%9C%BA%E6%99%AF-1%E5%86%99%E4%B8%80%E4%B8%AA%E5%A4%8D%E5%88%B6%E6%8C%89%E9%92%AE%E7%BB%84%E4%BB%B6 "#%E5%9C%BA%E6%99%AF-1%E5%86%99%E4%B8%80%E4%B8%AA%E5%A4%8D%E5%88%B6%E6%8C%89%E9%92%AE%E7%BB%84%E4%BB%B6")
    *   [场景 2：调用一个 API 接口](#%E5%9C%BA%E6%99%AF-2%E8%B0%83%E7%94%A8%E4%B8%80%E4%B8%AA-api-%E6%8E%A5%E5%8F%A3 "#%E5%9C%BA%E6%99%AF-2%E8%B0%83%E7%94%A8%E4%B8%80%E4%B8%AA-api-%E6%8E%A5%E5%8F%A3")
    *   [场景 3：提交代码](#%E5%9C%BA%E6%99%AF-3%E6%8F%90%E4%BA%A4%E4%BB%A3%E7%A0%81 "#%E5%9C%BA%E6%99%AF-3%E6%8F%90%E4%BA%A4%E4%BB%A3%E7%A0%81")
*   [手把手教你写一份 AGENTS.md](#%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E5%86%99%E4%B8%80%E4%BB%BD-agentsmd "#%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E4%BD%A0%E5%86%99%E4%B8%80%E4%BB%BD-agentsmd")
    *   [第一章：技术栈声明](#%E7%AC%AC%E4%B8%80%E7%AB%A0%E6%8A%80%E6%9C%AF%E6%A0%88%E5%A3%B0%E6%98%8E%E5%BF%85%E5%A1%AB "#%E7%AC%AC%E4%B8%80%E7%AB%A0%E6%8A%80%E6%9C%AF%E6%A0%88%E5%A3%B0%E6%98%8E%E5%BF%85%E5%A1%AB")
    *   [第二章：目录结构](#%E7%AC%AC%E4%BA%8C%E7%AB%A0%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84%E5%BF%85%E5%A1%AB "#%E7%AC%AC%E4%BA%8C%E7%AB%A0%E7%9B%AE%E5%BD%95%E7%BB%93%E6%9E%84%E5%BF%85%E5%A1%AB")
    *   [第三章：编码规范](#%E7%AC%AC%E4%B8%89%E7%AB%A0%E7%BC%96%E7%A0%81%E8%A7%84%E8%8C%83%E5%BF%85%E5%A1%AB "#%E7%AC%AC%E4%B8%89%E7%AB%A0%E7%BC%96%E7%A0%81%E8%A7%84%E8%8C%83%E5%BF%85%E5%A1%AB")
    *   [第四章：构建命令](#%E7%AC%AC%E5%9B%9B%E7%AB%A0%E6%9E%84%E5%BB%BA%E5%91%BD%E4%BB%A4%E5%BB%BA%E8%AE%AE%E5%86%99 "#%E7%AC%AC%E5%9B%9B%E7%AB%A0%E6%9E%84%E5%BB%BA%E5%91%BD%E4%BB%A4%E5%BB%BA%E8%AE%AE%E5%86%99")
    *   [第五章：Never 规则](#%E7%AC%AC%E4%BA%94%E7%AB%A0never-%E8%A7%84%E5%88%99%E6%9C%80%E9%87%8D%E8%A6%81 "#%E7%AC%AC%E4%BA%94%E7%AB%A0never-%E8%A7%84%E5%88%99%E6%9C%80%E9%87%8D%E8%A6%81")
    *   [第六章：约定与协作](#%E7%AC%AC%E5%85%AD%E7%AB%A0%E7%BA%A6%E5%AE%9A%E4%B8%8E%E5%8D%8F%E4%BD%9C%E5%9B%A2%E9%98%9F%E9%A1%B9%E7%9B%AE%E5%BB%BA%E8%AE%AE%E5%86%99 "#%E7%AC%AC%E5%85%AD%E7%AB%A0%E7%BA%A6%E5%AE%9A%E4%B8%8E%E5%8D%8F%E4%BD%9C%E5%9B%A2%E9%98%9F%E9%A1%B9%E7%9B%AE%E5%BB%BA%E8%AE%AE%E5%86%99")
*   [通用模板：5 分钟开箱即用](#%E9%80%9A%E7%94%A8%E6%A8%A1%E6%9D%BF5-%E5%88%86%E9%92%9F%E5%BC%80%E7%AE%B1%E5%8D%B3%E7%94%A8 "#%E9%80%9A%E7%94%A8%E6%A8%A1%E6%9D%BF5-%E5%88%86%E9%92%9F%E5%BC%80%E7%AE%B1%E5%8D%B3%E7%94%A8")
*   [进阶技巧](#%E8%BF%9B%E9%98%B6%E6%8A%80%E5%B7%A7 "#%E8%BF%9B%E9%98%B6%E6%8A%80%E5%B7%A7")
*   [效果数据](#%E6%95%88%E6%9E%9C%E6%95%B0%E6%8D%AE "#%E6%95%88%E6%9E%9C%E6%95%B0%E6%8D%AE")
*   [常见问题](#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98 "#%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98")

* * *

### 从评论区最多的一个问题说起

上篇文章[《基于四层 Skill 体系的前端团队 AI 提效 50%》](https://juejin.cn/post/7632121609760243748 "https://juejin.cn/post/7632121609760243748")发出后，评论区问得最多的问题是：

> "AGENTS.md 到底怎么写？能不能给个模板？"

今天安排。

但在给模板之前，我想先回答一个更根本的问题——

**为什么一个 Markdown 文件，就能让 AI 写出的代码质量发生质变？**

* * *

### AGENTS.md 到底是什么

一句话定义：

> **AGENTS.md 是写给 AI 编程助手看的项目规范文件。** 

你可以把它类比成：

| 文件 | 给谁看 | 管什么 |
| --- | --- | --- |
| `.eslintrc` | 给 ESLint 看 | 代码风格 |
| `.prettierrc` | 给 Prettier 看 | 格式化规则 |
| `tsconfig.json` | 给 TypeScript 看 | 类型检查 |
| **`AGENTS.md`** | **给 AI 看** | **项目规范、目录结构、编码约定、禁止事项** |

`.eslintrc` 让 ESLint 知道"用单引号还是双引号"。

`AGENTS.md` 让 AI 知道"组件放哪个目录、样式用什么方案、哪些文件绝对不能动"。

**没有它，AI 就是一个能力很强但不知道团队规矩的新人。** 

有了它，AI 知道你的规矩，按你的规矩来。

* * *

### 一份真实的 AGENTS.md 长什么样

以下是我从实际项目中提取的 AGENTS.md（已脱敏），你可以直接感受它的结构：

```markdown
# AGENTS.md

- 本项目为 React 19 + TypeScript 前端应用
- 包管理器：yarn，Node >= 22.12.0
- 样式方案：Less + CSS Modules
- UI 组件库：antd v6

## Project Structure

src/
├── components/     # 通用组件（PascalCase）
├── pages/          # 页面组件
├── hooks/          # 自定义 Hooks
├── services/       # API 请求封装
├── models/         # 全局状态
├── utils/          # 工具函数
├── typings/        # 类型定义
└── constants/      # 常量

- Never edit src/.umi/ — 框架自动生成
- Never edit dist/ — 构建产物

## Coding Style

- 使用 interface 定义 Props
- 组件命名：PascalCase，文件名 index.tsx
- Never 使用 any 类型
- Never 使用内联样式

## Build Commands

yarn serve    # 开发服务器
yarn build    # 生产构建
yarn lint     # 格式化

```

看起来很简单对吧？就是一个 Markdown 文件。

**但它的效果是惊人的。** 

* * *

### 没有 AGENTS.md vs 有 AGENTS.md

我用三个真实场景给你看差距。

#### 场景 1：写一个复制按钮组件

**❌ 没有 AGENTS.md 时，AI 写的代码：** 

```tsx
export default function CopyBtn({ text }: any) {
  return (
    <button 
      style={{ color: 'blue', padding: '4px 8px' }}
      onClick={() => navigator.clipboard.writeText(text)}
    >
      Copy
    </button>
  )
}

```

问题清单：

*   ❌ `any` 类型——完全没有类型定义
*   ❌ 内联样式——团队用的是 CSS Modules
*   ❌ `CopyBtn` 命名——团队规范是完整的 `CopyButton`
*   ❌ 没有用 antd 的 `message` 组件做成功提示
*   ❌ 文件没有放在 `src/components/CopyButton/` 目录下

**✅ 有 AGENTS.md 后，AI 写的代码：** 

```tsx

import React, { useCallback } from 'react'
import { message } from 'antd'
import styles from './index.less'

interface CopyButtonProps {
  text: string
  onSuccess?: () => void
}

const CopyButton: React.FC<CopyButtonProps> = ({ text, onSuccess }) => {
  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(text)
    message.success('已复制')
    onSuccess?.()
  }, [text, onSuccess])

  return (
    <button className={styles['copy-button']} onClick={handleCopy}>
      复制
    </button>
  )
}

export default CopyButton

```

差距一目了然：

*   ✅ 明确的 `interface` 定义 Props
*   ✅ CSS Modules 引入样式
*   ✅ 用了 antd 的 `message` 组件
*   ✅ `CopyButton` 完整命名
*   ✅ 放在正确的目录 `src/components/CopyButton/`

> **后者像团队里有 3 年经验的同事写的代码，前者像实习生第一天写的。** 

#### 场景 2：调用一个 API 接口

**❌ 没有 AGENTS.md 时：** 

```tsx

const [data, setData] = useState(null)

useEffect(() => {
  fetch('/api/customers')
    .then(res => res.json())
    .then(data => setData(data))
}, [])

```

**✅ 有 AGENTS.md 后：** 

```tsx

import { request } from 'umi'

export async function fetchCustomerList(
  params: API.CustomerListParams
): Promise<API.Response<API.Customer[]>> {
  return request('/api/customers', { params })
}


import { fetchCustomerList } from '@/services/customer'

const { data, loading } = useRequest(fetchCustomerList)

```

区别：

*   ✅ API 调用封装在 `src/services/` 下
*   ✅ 使用框架提供的 `request` 而非裸 `fetch`
*   ✅ 有完整的 TypeScript 类型定义
*   ✅ 使用 `useRequest` Hook 管理请求状态

#### 场景 3：提交代码

**❌ 没有 AGENTS.md 时：** 

```bash
git commit -m "fix button"

```

**✅ 有 AGENTS.md 后：** 

```bash
git commit -m "fix(components): 修复 CopyButton 在 Safari 下复制失败的问题"

```

一个随意的描述 vs 一个符合 Conventional Commits 规范的 commit message。

* * *

### 手把手教你写一份 AGENTS.md

看完效果，现在教你怎么写。

一份合格的 AGENTS.md 包含 **6 个核心章节**。逐个教你写，每个章节都有模板。

#### 第一章：技术栈声明（必填）

这是 AGENTS.md 的"开场白"，告诉 AI 你的项目用了什么。

```markdown
# AGENTS.md

- 本项目为 React 19 + TypeScript 前端应用
- 包管理器：yarn
- 样式方案：Less + CSS Modules
- UI 组件库：antd v6
- 构建工具：类 umi 框架

```

**写法要点**：

*   用**列表**而非段落——AI 解析列表的准确率更高
*   写明**版本号**——React 18 和 React 19 的写法不同
*   写明**包管理器**——否则 AI 可能给你 `npm install` 而不是 `yarn add`

**适配不同技术栈**：

```markdown
# Vue 3 项目
- 本项目为 Vue 3 + TypeScript 前端应用
- 构建工具：Vite 5
- 状态管理：Pinia
- UI 组件库：Ant Design Vue 4

# Next.js 项目
- 本项目为 Next.js 14 + TypeScript 全栈应用
- 路由方案：App Router
- 样式方案：Tailwind CSS v3

```

#### 第二章：目录结构（必填）

AI 最需要的信息之一——知道文件放哪里。

```markdown
## Project Structure

src/
├── components/     # 通用组件（PascalCase 命名）
├── pages/          # 页面组件
├── hooks/          # 自定义 Hooks
├── services/       # API 请求封装
├── models/         # 状态管理
├── utils/          # 工具函数
├── typings/        # 类型定义
└── constants/      # 常量

```

**写法要点**：

*   每个目录后面**加注释**说明用途
*   只列到**一级目录**就够了——太深了 AI 反而会困惑
*   写清楚**命名规范**——比如"PascalCase"

#### 第三章：编码规范（必填）

告诉 AI "在这个项目里，代码该怎么写"。

```markdown
## Coding Style

**TypeScript/React**
- 使用 interface 定义 Props 类型
- 组件使用 React.FC<Props>
- 组件命名：PascalCase，文件名 index.tsx

**样式（Less + CSS Modules）**
- 正确用法：import styles from './index.less'
- 使用方式：className={styles['my-class']}

**路径别名**
- @/* → src/*

```

**写法要点**：

*   **越具体越好**——不要写"遵循最佳实践"，要写"使用 interface 不用 type"
*   **给出正确用法示例**——AI 读示例比读规则更准确

#### 第四章：构建命令（建议写）

```markdown
## Build Commands

yarn serve    # 启动开发服务器
yarn build    # 生产构建
yarn lint     # 代码格式化

```

AI 帮你调试问题时可能需要运行命令。如果它不知道你用 `yarn serve` 而不是 `npm start`，就会给你错误的指导。

#### 第五章：Never 规则（最重要！）

这是 AGENTS.md 中**价值最高的章节**。

`Never` 规则告诉 AI "绝对不能做什么"——这比告诉它"应该怎么做"更重要。

```markdown
## Never 规则

- Never 修改 src/.umi/ 或 src/.umi-production/ 目录
- Never 修改 dist/ 目录
- Never 在组件内使用 any 类型
- Never 使用内联样式（style={{ }}），除非需要动态计算
- Never 在 Less 中使用硬编码颜色值——使用主题变量
- Never 在渲染路径中执行耗时操作
- Never 在列表渲染中省略 key 属性
- Never 在 node_modules/ 中安装依赖
- Never 修改 lock 文件
- Never 使用 git stash
- Never 切换分支


```

**为什么 Never 规则如此重要？**

因为 AI 犯错的成本远高于人类。

人类改错了 `src/.umi/`，会很快意识到"哦，这个目录不应该改"。但 AI 不会——它会认认真真地把自动生成的代码改了，然后你下次构建就炸了。

> **一条 Never 规则，能避免一次灾难性的误操作。** 

我的建议是：

> **每次 AI 犯了一个你不希望它犯的错，就往 Never 规则里加一条。** 

这是一个**持续演进**的过程。我现在的 Never 规则有 11 条，都是从真实踩坑中积累出来的。

#### 第六章：约定与协作（团队项目建议写）

```markdown
## Commit 规范

- 格式：type(scope): description
- 类型：feat / fix / docs / style / refactor / test / chore

## 多 Agent 并发

- 禁止 git stash
- 禁止切换分支
- 只 commit 自己修改的文件

```

* * *

### 通用模板：5 分钟开箱即用

如果你不想从零写，这里有一份通用模板，覆盖 React + TypeScript 项目的最常见场景。

**直接复制到你的项目根目录，改掉 `[方括号]` 里的内容就行**：

```markdown
# AGENTS.md

- 本项目为 [React/Vue/Next.js] + TypeScript 前端应用
- 包管理器：[yarn/pnpm/npm]
- 样式方案：[Less/Sass/Tailwind CSS] + CSS Modules
- UI 组件库：[antd/Arco Design/Element Plus] v[版本号]

## Project Structure

src/
├── components/     # 通用组件（PascalCase 命名）
├── pages/          # 页面组件
├── hooks/          # 自定义 Hooks
├── services/       # API 请求封装
├── models/         # 状态管理
├── utils/          # 工具函数
├── typings/        # 类型定义
└── constants/      # 常量

## Coding Style

**TypeScript**
- 使用 interface 定义 Props
- 组件使用 React.FC<Props> 或函数声明
- Never 使用 any 类型

**样式**
- import styles from './index.less'
- Never 使用内联样式
- Never 硬编码颜色值

**路径别名**
- @/* → src/*

## Build Commands

[你的开发命令]    # 启动开发服务器
[你的构建命令]    # 生产构建
[你的格式化命令]  # 代码格式化

## Never 规则

- Never 修改框架自动生成的目录
- Never 修改 dist/ 构建产物
- Never 在组件内使用 any 类型
- Never 使用内联样式
- Never 在渲染路径中执行耗时操作
- Never 在列表渲染中省略 key
- Never 硬编码敏感信息
- Never 修改 lock 文件

## Commit 规范

- 格式：type(scope): description
- 类型：feat / fix / docs / style / refactor / test / chore

```

* * *

### 进阶技巧

#### 技巧 1：DESIGN.md 联动视觉规范

`AGENTS.md` 管的是"代码怎么写"，`DESIGN.md` 管的是"UI 长什么样"：

```markdown
# DESIGN.md

## 品牌色
- 主色：#1677FF
- 主色悬浮：#4096FF
- 主色背景：rgba(22, 119, 255, 0.1)

## 文字色
- 主文字：rgba(0, 0, 0, 0.88)
- 次要文字：rgba(0, 0, 0, 0.65)

## 间距系统
- 基础单位：8px
- 组件间距：16px / 24px

```

有了 DESIGN.md，AI 在写样式时就不会用 `color: blue` 这种硬编码颜色值。

#### 技巧 2：AGENTS.local.md 个人偏好

创建一个 `AGENTS.local.md`（加入 `.gitignore`），写你的个人偏好：

```markdown
# AGENTS.local.md（不入仓库）

- 回复语言：中文
- 代码注释语言：中文
- 组件写法偏好：函数声明
- 类型定义偏好：interface

```

AI 会同时读取项目规范和你的个人偏好，输出更符合你习惯的代码。

#### 技巧 3：Never 规则的持续演进

我的建议是维护一个 **Never 规则演进日志**：

```yaml
2026-04-15  新增：Never 修改 src/.umi/ 目录
            原因：AI 把自动生成的路由配置改了，构建报错

2026-04-18  新增：Never 在 Less 中硬编码颜色值
            原因：AI 用了 

2026-04-22  新增：Never 使用 git stash
            原因：多 Agent 并发时，一个 Agent stash 了另一个的改动

```

> **每一条 Never 规则背后，都是一个真实的踩坑故事。** 

* * *

### 效果数据

| 指标 | 没有 AGENTS.md | 有 AGENTS.md | 变化 |
| --- | --- | --- | --- |
| AI 代码规范遵循率 | ~60% | **95%+** | ↑ 35% |
| AI 代码一次通过率 | ~40% | **80%+** | ↑ 40% |
| 每次手动修正时间 | ~8 分钟 | **~1 分钟** | ↓ 87.5% |
| 新人上手时间 | 3-5 天 | **1 天** | ↓ 70%+ |

> 以上数据基于实际项目 3 周使用期间，对 50+ 次 AI 代码生成的人工抽检统计。不同项目和技术栈可能有差异。

最后一个数据可能出乎意料——**AGENTS.md 对新人也有用**。

因为它不仅是给 AI 看的，也是一份精简的项目开发规范。新人读 AGENTS.md，5 分钟就知道项目的技术栈、目录结构、编码规范和禁止事项。

> **它是项目文档的一个超级浓缩版。** 

* * *

### 常见问题

#### Q1：AGENTS.md 放在哪里？

**项目根目录。**  和 `package.json`、`tsconfig.json` 同级。

但不同工具读取方式不同： `AGENTS.md` 更适合作为统一规范源文件；

*   Cursor 用 Rules 接入
*   Claude Code 用 `CLAUDE.md` 引用，
*   GitHub Copilot 用 `.github/copilot-instructions.md`，
*   Windsurf 用 Rules / `.windsurfrules`。

AI 编程助手会自动扫描项目根目录读取。

#### Q2：需要提交到 Git 吗？

**需要。**  团队共享的规范文件。但 `AGENTS.local.md`（个人偏好）应该加入 `.gitignore`。

#### Q3：写多长合适？

*   **最小可用版本**：30 行（技术栈 + 目录 + 3 条 Never 规则）
*   **推荐长度**：60-100 行
*   **不建议超过**：200 行

#### Q4：多个 AI 工具都能识别吗？

已验证：Cursor ✅ | Claude ✅ | GitHub Copilot ✅ | Windsurf ✅

更准确地说，`AGENTS.md` 是统一规范源文件，不是所有工具都原生直接读取它。不同工具需要接入自己的规则入口：Cursor 用 Rules，Claude Code 用 `CLAUDE.md`，GitHub Copilot 用 `copilot-instructions.md`。

#### Q5：已有项目怎么加？

在项目根目录创建 `AGENTS.md`，复制本文模板，5 分钟填好，提交。**不需要改任何代码，不需要安装任何工具。** 

* * *

### 一个彩蛋

如果你觉得手动写还是太麻烦——下篇教程我会分享如何《[用一行命令自动生成 AGENTS.md + DESIGN.md](https://juejin.cn/post/7647519391916556294 "https://juejin.cn/post/7647519391916556294")》，脚本会读取 `package.json` 自动识别技术栈、UI 库、包管理器，5 秒搞定。

但即使不用任何工具，**手写的 AGENTS.md 也能达到 80% 的效果。** 

工具只是让最后的 20% 更自动化。核心永远是那个 Markdown 文件本身。

* * *

### 总结

| 你可能在想 | 我的回答 |
| --- | --- |
| "一个 Markdown 文件真能有这么大效果？" | 是的，AI 缺的不是能力，是上下文 |
| "写起来会不会很复杂？" | 6 个章节，30-100 行，5 分钟 |
| "团队不愿意用怎么办？" | 提交到 Git 就行，团队无需额外操作 |
| "要花多少时间维护？" | 初次 5 分钟，之后每踩一个坑加一条 Never 规则 |

> **与其每次手动修正 AI 写的代码，不如花 5 分钟告诉它规矩。** 

* * *

如果你按照本文的方法创建了 AGENTS.md，欢迎在评论区分享你的效果数据——特别是"规范遵循率"和"一次通过率"的变化。

也欢迎分享你踩过的坑和总结出的 Never 规则，我会整理一份**社区版 Never 规则大全** 👇

觉得有用？点个赞 👍 收藏一下，后面我会继续分享 DESIGN.md 的深度用法——如何让 AI 写出的 UI 不再"一眼 AI 味"。