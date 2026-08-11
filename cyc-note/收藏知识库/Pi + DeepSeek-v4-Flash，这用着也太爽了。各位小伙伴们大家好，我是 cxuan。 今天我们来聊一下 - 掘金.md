[Pi + DeepSeek-v4-Flash，这用着也太爽了。各位小伙伴们大家好，我是 cxuan。 今天我们来聊一下 - 掘金](https://juejin.cn/post/7671964740780785670) 

 各位小伙伴们大家好，我是 cxuan。

今天我们来聊一下 Pi ，Pi 这个 Agent 我也是想写很久了。

如果你刚接触 Pi，就暂且可以先把它理解成一个运行在 CLI 里的 Coding Agent，它的设计逻辑就是四个字 --- 极简内核。

极简到像是只有内核的 Linux 0.11 。

Pi 本身只有最基础的 `read`、`bash`、`edit`、`write` 等基础工具。

如果你需要 skill 和 MCP ，你得自己装。

这篇文章我就先跟大家聊聊 Pi ，然后说一下如何接入 DeepSeek，再根据一个我实际的场景跑一下 Pi + DeepSeek-v4-Flash 的能力。

Pi 是什么？
-------

Pi 的官方定位是 **minimal terminal coding harness**，也就是最小化的 Coding Agent 。Pi 的重点在于 harness：它负责运行模型、提供工具、保存会话，并允许你替换或扩展几乎所有工作环节。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806060937325.png)

一个最基础的 Pi session 的工作流如下：

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806084506363.png)

Pi 的核心只提供少量文件和 Shell 工具。很多 Coding Agent 有的 Plan Mode、Subagent、浏览器自动化、WebSearch 和自定义状态栏等能力，需要通过 Extension、Skill 或 Package 来进行添加。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/14-pi-ecosystem-illustration.png)

Pi 的这种设计与 VS Code 有些相似：优先提供编辑和运行框架，想要啥自己通过插件的方式进行拓展。

### 五分钟搞定 Pi 的安装

废话说的有点说了，下面直接跟大家说如何安装。 一句命令的事儿：

```css
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

```

进入项目后启动：

```bash
cd your-project
pi

```

就完事儿了。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260805230847199.png)

你看看这个主页，真 TM 极简了，连个 Logo 都没有。。。

第一次启动可以执行：

```bash
/login       登录模型供应商或订阅
/model       选择模型
/settings    设置主题、thinking 和消息模式
/hotkeys     查看快捷键

```

几个最常用的操作：

*   `Shift+Tab`：切换 thinking level。
*   `Ctrl+L`：选择模型。
*   `Escape`：中止当前运行。
*   `Ctrl+O`：展开或折叠工具输出。
*   输入 `@`：引用项目文件。
*   `/resume`：恢复以前的会话。
*   `/tree`：回到会话中的任意节点并创建新分支。

刚开始时不需要安装任何插件，直接先上手体验。

为什么要使用 Pi
---------

现在市面上的 Coding Agent 太多了，为啥要用 Pi 呢？它有啥优势？

我给大家列举了几点：

首先就是**模型选择自由**，多 Provider 支持已经不是啥新鲜事了，不过这仍然是 Pi 的优势，因为很多 Coding Agent 本身不支持其他模型，需要借助外部工具来支持。

**工作流由自己决定**，Pi 不强制使用内置的 Plan、Subagent ，你可以通过 Skill 和 Extension 按需组合，这就保证了高自由度，但代价是配置和维护也要自己负责。

**可以嵌入自己的系统**，除了终端交互之外，Pi 还提供了 JSON、RPC 和 TypeScript SDK。它既能作为 Coding Agent 使用，也能成为内部机器人、自动审查或专用工作台的基础组件。

**Skill 可以跨工具复用**，Pi 支持 Agent Skills 标准，可以复用 `.agents/skills`、Claude Code 和 Codex 的 Skill。不用为每个 Coding Agent 都配置自己的 skills 了。

### 那 Pi、Codex CLI、Claude Code 和 Gemini CLI 该怎么选

这些区别只有一个：**官方 CLI 更省事，Pi 更自由。** 

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/15-cli-choice-illustration.png)

*   主要使用 OpenAI，希望沙箱和审批开箱即用：选 **Codex CLI**。
*   主要使用 Claude，希望 Agent、Plan、IDE 和插件体验完整：选 **Claude Code**。
*   主要使用 Gemini 或 Google Cloud：选 **Gemini CLI**（Gemini 真是不想说了）
*   经常切换模型、使用代理网关，或者想自己改造工作流：选 **Pi**。

如果你不想折腾，官方 CLI 通常更合适；如果你受不了工具替你决定模型和工作流，Pi 对你来说才有吸引力。

所有如果你是新手或者小白，通常不建议你使用 Pi，Pi 更适合老油子，想要自己折腾的 Geek 。

这让我想到之前写 DeepSeek-v4-Flash 本地部署的文章时，有个评论区的人说：

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806072142293.png)

只能说生命不息，折腾不止。。。

把 DeepSeek-v4-Flash 接入 Pi
-------------------------

Pi 的自定义 provider 都写在 `~/.pi/agent/models.json`，往 `providers` 里加一个 `deepseek` 就行，支持 OpenAI 兼容 API：

```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com/v1",
      "api": "openai-completions",
      "apiKey": "sk-你的key",
      "authHeader": true,
      "compat": {
        "supportsStore": false,
        "supportsReasoningEffort": true
      },
      "models": [
        {
          "id": "deepseek-v4-flash",
          "name": "DeepSeek V4 Flash",
          "reasoning": true,
          "input": ["text"],
          "contextWindow": 1000000,
          "maxTokens": 65536,
          "thinkingLevelMap": {
            "off": null,
            "low": "high",
            "medium": "high",
            "high": "high",
            "xhigh": "max",
            "max": "max"
          }
        }
      ]
    }
  }
}

```

`thinkingLevelMap` 是精髓：DeepSeek 只有 high/max 档，Pi 的 low/medium/high 都会映射到 high，xhigh/max 映射到 max。

apikey 可以像我一样从钥匙串里面来读：

```json
"apiKey": "!security find-generic-password -a lx -s pi-deepseek-api-key -w"

```

把 key 存进钥匙串就一行：

```csharp
security add-generic-password -a lx -s pi-deepseek-api-key -w 'sk-你的key'

```

然后 `~/.pi/agent/settings.json` 把默认值改成 DeepSeek ，之后每次开 Pi 就是 DeepSeek：

```json
{
  "defaultProvider": "deepseek",
  "defaultModel": "deepseek-v4-flash",
  "defaultThinkingLevel": "xhigh"
}

```

保存后重启 Pi，用 `/model`（或 Ctrl+L）就能在 DeepSeek 和 GPT 之间一键切换，不用改任何配置。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806080058068.png)

上手干了第一个任务，就是排查 Codex Plus 的用量问题，用 DeepSeek 排查 Codex 的用量问题。。。。xs 。

我发现最近 Codex plus 的额度非常不够用，自从我没有用 Codex app ，用上 Pi + CPA 接入 GPT-5.6 以来，在一堂大课的时间，我就夯满了一个 plus 号的周额度。

我非常纳闷，为什么会这么费额度？我一度让我怀疑是被人偷额度了，于是我让 DeepSeek 排查了一下原因。

最终排查结果：**没被盗，就是我一个半小时自己烧完的**。

整个排查过程让我感觉很好的一点是，DeepSeek-v4-Flash 会自动识别路径依赖，自动判断这条路是否正确，不会走的太深，判断错了自动更正。

下面就是一个它当时自动判断的真实思考过程。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806083124683.png)

DeepSeek-v4-Flash 的完整报告如下。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806075435405.png)

这次排查过程还是真香，一顿排查花了 20 M token，费用才不到 1 块钱。而且速度还快。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806073517971.png)

我想到了之前有人在知乎上提到了一个问题，我的回答是：

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/image-20260806090208547.png)

说几个 Pi + DeepSeek-v4-Flash 用的顺手的地方：

1.  **便宜到可以随便跑**：20M token 不到 1 块钱，同样的排查量级，GPT 那边是直接烧掉半个 plus 号的周额度；
2.  **1M 上下文**：支持长项目和长报告。
3.  **路径自纠错**：干活的适合发现走错路会自动退回来换一条，不会一条路走到黑，这有点像真实人类的排查过程了。
4.  **Pi 上无缝切换**：支持多 Provider 和模型切换。

我觉得以后 GPT 的号就留着干重活，然后我的日常基座就是 Pi + DeepSeek-v4-Flash 了。

这个日常只截止到 DeepSeek-v4-Pro 的发布之前 ：）

本来这篇文章写完就要发了，然后看到 DeepSeek 的消息 ，要涨价了。

![](https://cdn.jsdelivr.net/gh/doggaifan/picbed/ea1e0a9cb93c8c44b807c678415bf5b9.jpg)

尼玛。。。。。。

这篇文章我现在撤回还来得及么？