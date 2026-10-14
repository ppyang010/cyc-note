---
title: DSH 插件清单
date: 2026-09-30
updated: 2026-09-30
tags:
  - dsh
  - plugin
  - config
  - sync
aliases:
  - DeepSeek Harness 插件清单
  - DSH plugins
status: active
---

# DSH 插件清单

> [!abstract] 这份笔记做什么
> 记录本机 DeepSeek Harness（DSH Desktop）实际装了哪些插件、从哪装、装到哪一版。换 DSH 版本、重装、或新机器同步时，优先对照这里，而不是凭记忆点市场。

相关笔记：[[dsh提示词]]

## 盘点快照

| 项 | 值 |
|---|---|
| 盘点时间 | 2026-09-30（按本机 `package.json` / lockfile 修改时间） |
| DSH Desktop | `2.0.9`（`/Applications/DSH Desktop.app`） |
| 配置根目录 | `~/.dsh` |
| 当前主 profile | `desktop`（本 GUI 实际在用） |
| 次 profile | `web`（插件更少，多了 `dsh-file-mentions`） |
| 市场区域 | china（`~/.dsh/profiles/desktop/.dsh-market/state.json`） |

> [!warning] 不要把密钥写进这篇笔记
> MCP 的 token、app-secret、Confluence PAT 只存在 `cordis.patch.yml` 和本机环境变量里。同步配置时单独拷贝该文件，不要粘到 Obsidian。

## 配置落点

换版本时，插件“装了什么”和“怎么挂上”是两层：

| 作用 | 路径 | 说明 |
|---|---|---|
| 插件依赖与 bundle 列表 | `~/.dsh/profiles/desktop/package.json` | **主清单**。`dependencies` 决定装什么，`dsh.profile.bundles` 决定启动时挂哪些 |
| 锁定版本 | `~/.dsh/profiles/desktop/pnpm-lock.yaml` | GitHub 源的 commit 以这里为准 |
| 热挂载 / MCP / 压缩参数 | `~/.dsh/profiles/desktop/cordis.patch.yml` | live reload 只监视这个文件；含 MCP 密钥 |
| 空根，不要手改 | `~/.dsh/profiles/desktop/cordis.yml` | 官方说明：编辑 patch，不编辑这个 |
| 插件设置、模型、默认权限 | `~/.dsh/settings.yaml` | 不含插件安装列表，但含 sidebar / model-picker / sidebarqa 等配置 |
| web profile 对照 | `~/.dsh/profiles/web/package.json` | 另一套更瘦的安装，换版本时不要和 desktop 混拷 |

官方自带、不用重装的 bundle：

- `@deepseek-ai/dsh-base`
- `@deepseek-ai/dsh-web-app`

## Desktop 已装插件（主清单）

来源：`~/.dsh/profiles/desktop/package.json`。`spec` 是写入依赖的安装源，`resolved` 是 `node_modules` 里实际版本，`pin` 是 lockfile 里的 GitHub commit（无则表示走 registry 版本号）。

| 包名 | 作用 | spec | resolved | pin / 锁定 | 仓库 |
|---|---|---|---|---|---|
| `dsh-better-sidebar` | VS Code 风格右侧栏（资源管理器 / 编辑器 / 终端 / git / 浏览器），按会话隔离 | `0.19.0` | `0.19.0` | registry | [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) |
| `dsh-context` | 上下文看板与 context 命令 | `0.49.3` | `0.49.3` | registry | [bowenliang123/dsh-context](https://github.com/bowenliang123/dsh-context) |
| `dsh-provider-model-configurator` | 可视化增删改 provider 模型条目 | `github:LiangYin233/dsh-provider-model-configurator#v0.3.9` | `0.3.9` | `70f88112c7d92fadeb93e46f5dcb8b1f3ae6eba3` | [LiangYin233/dsh-provider-model-configurator](https://github.com/LiangYin233/dsh-provider-model-configurator) |
| `dsh-workbuddy-connect` | 把 WorkBuddy 桌面 App 的模型自动接到 DSH | `^0.3.2` | `0.3.2` | registry | [corrinehu/dsh-workbuddy-connect](https://github.com/corrinehu/dsh-workbuddy-connect) |
| `dsh-sidebar-qa` | 划词后在右侧追问，另开会话，不打断主对话 | `github:ChenRuoT/dsh-sidebar-qa` | `0.5.0` | `a2e689c19eb7cfd2c024618c707761c23d8046f0` | [ChenRuoT/dsh-sidebar-qa](https://github.com/ChenRuoT/dsh-sidebar-qa) |
| `@dsh-external/dsh-sentinel` | 哨兵：文件 / 进程 / 端口 / 命令条件唤醒 agent | `github:fuhefei/dsh-sentinel#v0.7.0` | `0.7.0` | `a9527073b95930f8c557704ad0f2821651d124c2` | [fuhefei/dsh-sentinel](https://github.com/fuhefei/dsh-sentinel) |
| `dsh-reference-anything` | 统一 `@` 引用：技能、工作区文件、会话、本地 agent 记录、网盘、网页聊天 | `0.4.0` | `0.4.0` | registry | [Chael-Chael/dsh-reference-anything](https://github.com/Chael-Chael/dsh-reference-anything) |
| `@deepseek-ai/dsh-llm-pi-ai-antigravity` | Google Anti Gravity / Cloud Code Assist provider | `github:OpenSaozi/dsh-antigravity#1cb901002683cb7517b910a25a466d400b2429aa` | `0.1.0-rc.5` | `1cb901002683cb7517b910a25a466d400b2429aa` | [OpenSaozi/dsh-antigravity](https://github.com/OpenSaozi/dsh-antigravity) |
| `dsh-pin` | 会话置顶：工作区内置顶 / 全局置顶托盘 | `^0.2.1` | `0.2.1` | registry | [Yu-tao-Li/dsh-pin](https://github.com/Yu-tao-Li/dsh-pin) |
| `dsh-model-picker` | 搜索优先的模型选择器 + 独立思考档；fork 默认 medium 并按模型记忆 | `github:ppyang010/dsh-model-picker` | `1.18.0` | `2ae43d093b5af1477a4bd9c5a690af8fe919aa64` | [ppyang010/dsh-model-picker](https://github.com/ppyang010/dsh-model-picker)（上游 [ttmouse/dsh-model-picker](https://github.com/ttmouse/dsh-model-picker)） |
| `dsh-prompt-history` | 输入框 Up/Down 历史、Ctrl+R、引用、聊天 TOC | `^1.2.15` | `1.2.15` | registry | [Xiaofei-fei/dsh-prompt-history](https://github.com/Xiaofei-fei/dsh-prompt-history) |
| `dsh-better-display` | 更干净的阅读视图：进程细节、实时推理、最终回答 | `github:aa2246740/dsh-better-display#v0.1.1` | `0.1.1` | `daccf37ef14798316bc291a42eb25f749f12ff34` | [aa2246740/dsh-better-display](https://github.com/aa2246740/dsh-better-display) |
| `dsh-ego-browser` | ego-lite 浏览器工具（`ego_*`）+ 实时 watch 面板 | `github:Fisfzy/ego-browser` | `0.8.5` | `2d9ad51b813d351e7201c20703032ac2522c48be` | [Fisfzy/ego-browser](https://github.com/Fisfzy/ego-browser) / [Fisfzy/dsh-ego-browser](https://github.com/Fisfzy/dsh-ego-browser) |
| `dsh-all-usage` | 用量看板：模型 / provider / 工作区 / cache / 余额 / CSV | `github:ParticleLight/dsh-all-usage` | `1.1.10` | `4e42883ca3d9cfd4d71442252c0531e87d6f27d8` | [ParticleLight/dsh-all-usage](https://github.com/ParticleLight/dsh-all-usage) |
| `@linxin666/dsh-session-archive` | 会话归档、批量恢复、级联删除、自动清理 | `^0.3.24` | `0.3.24` | registry | npm：`@linxin666/dsh-session-archive` |

`dsh.profile.bundles` 顺序（启动挂载顺序，官方 base 在最前）：

```text
@deepseek-ai/dsh-base
@deepseek-ai/dsh-web-app
dsh-better-sidebar
dsh-context
dsh-provider-model-configurator
dsh-workbuddy-connect
dsh-sidebar-qa
@dsh-external/dsh-sentinel
dsh-reference-anything
@deepseek-ai/dsh-llm-pi-ai-antigravity
dsh-pin
dsh-model-picker
dsh-prompt-history
dsh-better-display
dsh-ego-browser
dsh-all-usage
@linxin666/dsh-session-archive
```

## Web profile 已装插件（对照）

来源：`~/.dsh/profiles/web/package.json`。日常以 Desktop 为准；只有跑 `dsh web` 独立 profile 时才需要对齐这里。

| 包名 | spec | resolved | pin | 相对 desktop |
|---|---|---|---|---|
| `@dsh-external/dsh-sentinel` | `github:fuhefei/dsh-sentinel#v0.7.0` | `0.7.0` | `a9527073…` | 两边都有 |
| `dsh-all-usage` | `github:ParticleLight/dsh-all-usage` | `1.1.10` | `4e42883c…` | 两边都有 |
| `dsh-better-sidebar` | `github:omdsh-dev/DSH-better-sidebar#v0.19.0` | `0.19.0` | `754974af…` | desktop 走 registry `0.19.0`，web 钉 GitHub tag |
| `dsh-file-mentions` | `github:a903067276-rgb/dsh-file-mentions#main` | `1.2.2` | `fe5d77c8ecf4c323c01c14c6d712416174e62eec` | **仅 web**。回复里的路径可点击打开 |
| `dsh-provider-model-configurator` | `github:LiangYin233/dsh-provider-model-configurator#v0.3.9` | `0.3.9` | `70f88112…` | 两边都有 |
| `dsh-sidebar-qa` | `github:ChenRuoT/dsh-sidebar-qa` | `0.5.0` | `a2e689c1…` | 两边都有 |

## MCP（不是插件市场包，但是同步配置的一部分）

Desktop `cordis.patch.yml` 里用 `@deepseek-ai/dsh-mcp-client` 挂了 4 个 stdio MCP。换机器时要连同命令路径一起核，**不要把密钥抄进笔记**。

| id | serverName | 启动方式（不含密钥） |
|---|---|---|
| `mcp-api-mocker` | `api-mocker` | `npx -y @dxy/api-mocker-mcp-server` |
| `mcp-bb-browser` | `bb-browser` | `node ~/.codex/mcp/bb-browser/node_modules/bb-browser/dist/mcp.js` |
| `mcp-dxy-wiki` | `dxy-wiki` | `uvx mcp-atlassian` |
| `mcp-skywalking` | `skywalking` | `~/.codex/mcp/skywalking-mcp/bin/swmcp stdio --read-only` |

另外还有非 MCP 的 patch：

- `compaction-basic`：`thresholdRatio: 0.75`，`retainRatio: 0.16`
- 多个 `*-hot` 条目：给当前已启动进程热挂新 bundle。完整重启后官方 bundle id 会先挂上，这些 hot 条目会因同包名自动 `disabled`，避免重复加载
- `ui-reference` 被显式 `disabled: true`（改由 `dsh-reference-anything` 提供）

## 和插件相关的 settings（无密钥）

`~/.dsh/settings.yaml` 里需要一起带走的插件配置块：

- `dsh-better-sidebar`：标题栏方案、`agentOpenTools`
- `sidebarqa`：追问用的 provider / 模型
- `model-picker-augmented`：隐藏 / 置顶模型
- `agent-default-model`、`subagent-model-selection`、`permission.defaultPreset`
- `llm-pi-ai.providers`：模型目录本身（体积大，换版本时整文件备份即可）

## 换 DSH 版本时怎么同步

> [!tip] 推荐顺序
> 先备份，再升级 DSH，再按 `package.json` 重装插件，最后拷回 `cordis.patch.yml` 和 `settings.yaml`。不要只拷 `node_modules`。

1. **升级前备份这 4 个文件**
   - `~/.dsh/profiles/desktop/package.json`
   - `~/.dsh/profiles/desktop/pnpm-lock.yaml`
   - `~/.dsh/profiles/desktop/cordis.patch.yml`
   - `~/.dsh/settings.yaml`
2. **升级 / 重装 DSH Desktop**，确认新版本能启动、官方市场能打开。
3. **优先用 GUI 插件市场**按上表重装；市场找不到的用 GitHub spec（`github:owner/repo#tag或commit`）。
4. 装完后核对 `package.json` 的 `dependencies` 和 `dsh.profile.bundles` 是否与本笔记一致。缺 bundle 的插件装了也不会挂载。
5. 把备份的 `cordis.patch.yml` 合回去：
   - MCP 段可以整段保留
   - `*-hot` 段只在“当前进程还没重启、需要立刻热挂”时有用；完整重启后可删，避免长期堆积
6. 恢复 `settings.yaml` 前先看新版本 schema 有没有改 key；冲突时以新版本结构为准，只迁回插件相关块。
7. **完整退出并重启 DSH Desktop**。live reload 只监视 `cordis.patch.yml`，改 `package.json` 通常要重启。
8. 抽查：better-sidebar 右侧栏、model-picker、sentinel、ego-browser 工具、MCP 工具列表是否出现。

> [!example] 最小可复制依赖块（desktop）
> 市场不好用时，把下面写回 `package.json` 的 `dependencies`，再让 DSH 重装 profile。GitHub 浮动源（没写 tag 的）建议同时保留 lockfile，否则会漂到最新 commit。

```json
{
  "@deepseek-ai/dsh-llm-pi-ai-antigravity": "github:OpenSaozi/dsh-antigravity#1cb901002683cb7517b910a25a466d400b2429aa",
  "@dsh-external/dsh-sentinel": "github:fuhefei/dsh-sentinel#v0.7.0",
  "@linxin666/dsh-session-archive": "^0.3.24",
  "dsh-all-usage": "github:ParticleLight/dsh-all-usage",
  "dsh-better-display": "github:aa2246740/dsh-better-display#v0.1.1",
  "dsh-better-sidebar": "0.19.0",
  "dsh-context": "0.49.3",
  "dsh-ego-browser": "github:Fisfzy/ego-browser",
  "dsh-model-picker": "github:ppyang010/dsh-model-picker",
  "dsh-pin": "^0.2.1",
  "dsh-prompt-history": "^1.2.15",
  "dsh-provider-model-configurator": "github:LiangYin233/dsh-provider-model-configurator#v0.3.9",
  "dsh-reference-anything": "0.4.0",
  "dsh-sidebar-qa": "github:ChenRuoT/dsh-sidebar-qa",
  "dsh-workbuddy-connect": "^0.3.2"
}
```

## 以后怎么更新这篇笔记

装、卸、换插件后，用本机真实文件刷新，不要凭聊天记忆改：

```bash
# 主清单
cat ~/.dsh/profiles/desktop/package.json

# 实际版本
python3 - <<'PY'
import json
from pathlib import Path
root = Path.home()/".dsh/profiles/desktop"
deps = json.loads((root/"package.json").read_text())["dependencies"]
for name, spec in deps.items():
    p = root/"node_modules"/name/"package.json"
    ver = json.loads(p.read_text())["version"] if p.exists() else "?"
    print(f"{name}\tspec={spec}\tresolved={ver}")
PY
```

核对项：

- [ ] `dependencies` 与表格一致
- [ ] `dsh.profile.bundles` 含全部第三方插件
- [ ] GitHub 源的 lock commit 有没有漂
- [ ] `cordis.patch.yml` 的 MCP id 有没有增删（仍不把密钥写入笔记）
- [ ] 改 `updated` 日期

## 已知差异 / 坑

- Desktop 和 Web 不是同一套插件。`dsh-file-mentions` 只在 web；session-archive / ego-browser / pin / prompt-history 等只在 desktop。
- `dsh-better-sidebar` desktop 钉 registry `0.19.0`，web 钉 GitHub `v0.19.0`（commit `754974af…`）。换版本时不要混。
- `dsh-model-picker`、`dsh-all-usage`、`dsh-ego-browser`、`dsh-sidebar-qa` 的 spec **没有 tag**，重装会跟到当时的默认分支 HEAD。要复现今天的行为，用表格里的 pin。
- `dsh-ego-browser` 的 lock 是 `git+ssh://git@github.com/Fisfzy/ego-browser.git#2d9ad51…`，没配 GitHub SSH 的机器可能装不上。
- `cordis.patch.yml` 里的 `*-hot` 是给“没重启的当前进程”用的权宜之计，不是长期清单。
- 官方自带 bundle 不要写进“我安装的插件”。
