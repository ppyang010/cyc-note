---
id: "2027870778918486485"
title: "你的openclaw都装了哪些skill？"
author: "猩纪猿"
type: zhihu-answer
source: "https://www.zhihu.com/question/2019693913921835490/answer/2027870778918486485"
created: "2026-04-15 22:07"
updated: "2026-04-15 22:07"
collected: "2026-04-15 22:07"
downloaded: "2026-08-16"
---
作为一个日常用 Claude Code 搬砖的开发者，分享一下我目前在用的 skill 配置：

**日常开发类：**

-   **init** - 初始化项目时自动生成 CLAUDE.md 文档，省得每次手动写
-   **simplify** - 写完代码自动审查，检查复用性、质量和效率，堪称代码洁癖福音
-   **review** - 直接在终端里 review PR，不用切到网页端

**安全与质量：**

-   **security-review** - 对当前分支做安全审计，上线前必跑一遍

**配置管理类：**

-   **update-config** - 管理 settings.json，配权限、环境变量、hooks 一把梭
-   **keybindings-help** - 自定义快捷键
-   **statusline** - 配置状态栏 UI

**效率工具：**

-   **loop** - 定时轮询任务，比如每5分钟检查一下部署状态
-   **claude-api** - 开发 Anthropic SDK 应用时的专属辅助

**团队协作：**

-   **team-onboarding** - 帮新同事快速上手 Claude Code
-   **insights** - 生成使用报告，复盘效率

说实话，**simplify** 和 **review** 是我用得最多的，强烈推荐。