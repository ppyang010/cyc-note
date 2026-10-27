---
title: DSH工具栏侧聊接入侧边对话维护记录
date: 2026-10-27
tags:
  - dsh
  - 插件维护
  - 侧边对话
aliases:
  - 工具栏侧聊改用侧边对话
summary_model: grok-4.7
status: 已在当前 GUI 验证
---

# DSH工具栏侧聊接入侧边对话维护记录

> [!info] 整理说明
> 本文记录 2026-10-27 对本地 DSH Desktop 插件的修改。总结模型：`grok-4.7`。DeepSeek Harness 是运行工具，不是模型名称。本文没有外部原作者；涉及的插件作者以上游仓库为准。

## 目录

- [[#目的]]
- [[#改动范围]]
- [[#实现方式]]
  - [[#打开侧边对话]]
  - [[#把引用放进输入框]]
  - [[#工具栏调用顺序]]
- [[#修改文件]]
- [[#验证结果]]
- [[#维护边界]]
- [[#升级后的恢复方法]]
- [[#回滚方法]]

## 目的

选中回答后出现的工具栏原来有三个按钮：复制、引用、侧聊追问。原先「侧聊追问」打开的是 `dsh-prompt-history` 自己的实验侧聊。

本次改动让这个按钮改用图中 `dsh-better-sidebar` 的「侧边对话(beta)」。选中文本仍作为 Markdown 引用放进侧边对话输入框，不自动发送。

## 改动范围

涉及两个已安装插件：

| 插件 | 版本 | 作用 |
|---|---|---|
| `dsh-prompt-history` | 1.6.5 | 提供选中文本工具栏和「侧聊追问」按钮 |
| `dsh-better-sidebar` | 0.28.1 | 提供图中的「侧边对话(beta)」 |

安装位置：

- `/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-prompt-history`
- `/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-better-sidebar`

当前 GUI 实际加载的是两个插件的 `lib/client.js`，不是 `src/`。因此源码和运行产物都已修改。

## 实现方式

两个插件之间不增加硬依赖。`dsh-better-sidebar` 在页面上发布一个函数，`dsh-prompt-history` 调用它。

### 打开侧边对话

`dsh-better-sidebar` 发布：

```javascript
window.__dshBetterSidebarOpenSideChat
```

函数收到引用文本后：

1. 文本为空时直接返回。
2. `sidechat` 标签类型被设置禁用时返回失败。
3. 读取当前会话 ID。
4. 把引用文本按会话放入内存队列。
5. 调用 `service.openTab({ type: "sidechat" }, { sessionId })`。
6. 打开失败时撤回刚刚入队的文本。

### 把引用放进输入框

侧边对话标签挂载时，`SideChatView` 调用 `takeSidechatPrompt(sessionId)` 取出队列中的下一条文本。

取出的文本写入侧边对话 composer：

- 输入框为空时直接填入。
- 输入框已有内容时，用一个空行隔开后追加。
- 填入后聚焦输入框。
- 不调用发送接口。

### 工具栏调用顺序

「侧聊追问」不再受 `dsh-prompt-history` 的实验侧聊开关限制。点击后：

1. 读取当前选中文本。
2. 格式化成 Markdown 引用。
3. 优先调用 `window.__dshBetterSidebarOpenSideChat`。
4. 成功后显示「已把引用送入侧聊，输入你的问题即可」。
5. 只有原生侧边对话不可用时，才回退到旧实验侧聊。
6. 两者都不可用时，仍显示原来的禁用提示。

## 修改文件

源码：

- `dsh-better-sidebar/src/client/sidechat-bridge.ts`：新增桥接和待填队列。
- `dsh-better-sidebar/src/client/index.tsx`：插件激活时安装桥接，卸载时清理。
- `dsh-better-sidebar/src/client/SideChatView.tsx`：挂载侧边对话时消费队列。
- `dsh-prompt-history/src/client/bridge.ts`：优先调用原生侧边对话。
- `dsh-prompt-history/src/client/useClipboard.ts`：工具栏按钮始终提供侧聊动作。

当前 GUI 实际加载的产物：

- `dsh-better-sidebar/lib/client.js`
- `dsh-prompt-history/lib/client.js`

`lib/client-registry.js` 未改。当前包导出 `./client` 指向 `lib/client.js`，本次验证加载的是这个文件。

## 验证结果

2026-10-27 在当前 GUI `http://127.0.0.1:43120` 验证：

- 页面中的 `window.__dshBetterSidebarOpenSideChat` 已是新函数。
- 函数内部调用的是 `service.openTab({ type: "sidechat" })`。
- 用测试文本 `> 工具栏侧聊验证引用` 调用后，右侧出现「新对话」标签。
- 标签创建完成后，侧边对话输入框内容为 `> 工具栏侧聊验证引用`。
- 没有发送测试消息。
- 随后页面快照中测试引用和测试标签均已消失。
- 两个 `lib/client.js` 均通过 `node --check`。

未完成的验证：

- 没有在真实选区上逐按钮点击「复制」「引用」「侧聊追问」。
- 没有重新构建插件，因为安装包内没有 `tsc`、`tsdown` 和构建配置。运行产物是按源码改动手工同步的。

## 维护边界

这次改动位于已安装插件目录，不属于 DSH Desktop 应用本体。

插件升级、重装或 `pnpm install` 覆盖 `node_modules` 后，修改会丢失。届时需要按本文重新同步，或把改动整理成独立补丁。

旧实验侧聊没有删除。原生侧边对话缺失或打开失败时，它仍是回退路径。

## 升级后的恢复方法

升级后先确认版本和入口：

```bash
node -p "require('/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-better-sidebar/package.json').version"
node -p "require('/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-prompt-history/package.json').version"
node -p "require('/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-better-sidebar/package.json').exports['./client'].default"
```

然后检查三个标记：

```bash
rg -n "__dshBetterSidebarOpenSideChat" \
  "/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-better-sidebar" \
  "/Users/ccy/.dsh/profiles/desktop/node_modules/dsh-prompt-history"
```

三个位置都应有命中：

- `dsh-better-sidebar` 发布函数。
- `dsh-better-sidebar` 的 `SideChatView` 消费队列。
- `dsh-prompt-history` 优先调用该函数。

缺任一命中，就说明升级覆盖了对应改动。

## 回滚方法

回滚时删除以下行为：

- 删除 `sidechat-bridge.ts`。
- 移除 `index.tsx` 中对 `installSidechatPromptBridge` 的安装。
- 移除 `SideChatView.tsx` 中的 `takeSidechatPrompt` 消费。
- 让 `sendToSideChat` 恢复为直接调用旧 `openSideChat`。
- 让工具栏按钮恢复为仅在实验侧聊开关开启时出现。
- 同步回滚两个 `lib/client.js`。

回滚后刷新 DSH GUI，确认 `window.__dshBetterSidebarOpenSideChat` 不再存在。
