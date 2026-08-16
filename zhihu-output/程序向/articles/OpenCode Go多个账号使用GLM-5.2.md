---
id: "2052119367018717420"
title: "OpenCode Go多个账号使用GLM-5.2"
author: "人类的落日"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/2052119367018717420"
created: "2026-06-21 20:05"
updated: "2026-06-21 21:26"
collected: "2026-06-21 20:05"
downloaded: "2026-08-16"
---
> 众所周知，GLM5.2的coding plan实在是难搞，所以干脆自己用OpenCode Go的多个账号组建一个集群方便调用，OpenCode Go注册一个账号也就是五美元，只需要注册一点账号就好了。

OpenCode 如何接入多个 OpenCode Go 账号，并统一使用 GLM-5.2

> 嗯，要是有人能用我的邀请就好了，有需要的但还没有注册过的可以用这个链接进去，购买五美元的 OpenCode Go（可以用支付宝） ，这样你我可以各得到五美元的恢复额度。[https://opencode.ai/go?ref=E3XBATSBMQ](https://link.zhihu.com/?target=https%3A//opencode.ai/go%3Fref%3DE3XBATSBMQ)

  

最近折腾了一套比较顺手的方案：用 Sub2API 做本地中转，把多个 OpenCode Go 账号统一接进来，然后让 OpenCode 只面对一个 OpenAI-compatible 接口。这样 OpenCode 里只配置一个 provider，就可以让后端自动调度多个账号，模型默认走 `glm-5.2`。

这篇记录一下完整搭建思路。

  

### 最终效果

搭好之后，OpenCode 配置里只需要这样用：

```text
{
  "model": "sub2api/glm-5.2",
  "small_model": "sub2api/deepseek-v4-flash"
}
```

OpenCode 请求会先发到本地 Sub2API：

```text
http://你的本地地址:8080/v1
```

Sub2API 再从多个 OpenCode Go 账号里自动选择可用账号转发请求。

### 架构思路

整体链路是：

```text
OpenCode
  ↓
Sub2API 本地 OpenAI-compatible 接口
  ↓
多个 OpenCode Go API Key
  ↓
https://opencode.ai/zen/go/v1
```

好处是：

-   OpenCode 只需要配置一个 provider
-   多个账号可以统一放在一个账号池里
-   后续换 key、加 key、禁用 key，不需要反复改 OpenCode 配置
-   可以在 Sub2API 后台看到账号状态、请求量、token 消耗

### 准备工作

需要准备：

-   Windows + WSL，或者 Linux 服务器
-   PostgreSQL
-   Redis
-   Sub2API
-   OpenCode
-   多个 OpenCode Go API Key

本文用的是 WSL 方式。Docker 也可以，但如果本机没装 Docker，WSL 手动安装更直接。

### 安装依赖

进入 WSL：

```text
sudo apt update
sudo apt install -y postgresql redis-server curl jq ca-certificates
```

启动服务：

```text
sudo service postgresql start
sudo service redis-server start
```

创建数据库：

```text
sudo -u postgres psql
```

进入 psql 后执行：

```text
CREATE USER sub2api WITH PASSWORD 'sub2api';
CREATE DATABASE sub2api OWNER sub2api;
\q
```

### 安装 Sub2API

下载 Sub2API release 版本，例如：

```text
sudo mkdir -p /opt/sub2api
cd /opt/sub2api

curl -L -o sub2api.tar.gz https://github.com/Wei-Shaw/sub2api/releases/latest/download/sub2api_linux_amd64.tar.gz
tar -xzf sub2api.tar.gz
chmod +x sub2api
```

创建启动脚本：

```text
sudo nano /opt/sub2api/start-local.sh
```

内容示例：

```text
#!/usr/bin/env bash
set -e

sudo service postgresql start
sudo service redis-server start

export DATA_DIR=/opt/sub2api/data
export AUTO_SETUP=true
export RUN_MODE=simple
export SIMPLE_MODE_CONFIRM=true

export SERVER_HOST=0.0.0.0
export SERVER_PORT=8080

export DATABASE_HOST=127.0.0.1
export DATABASE_PORT=5432
export DATABASE_USER=sub2api
export DATABASE_PASSWORD=sub2api
export DATABASE_NAME=sub2api

export REDIS_HOST=127.0.0.1
export REDIS_PORT=6379

export ADMIN_EMAIL=admin@sub2api.local
export ADMIN_PASSWORD=请换成你自己的密码

mkdir -p /opt/sub2api/data /var/log/sub2api

/opt/sub2api/sub2api
```

赋权并启动：

```text
sudo chmod +x /opt/sub2api/start-local.sh
/opt/sub2api/start-local.sh
```

检查健康状态：

```text
curl http://127.0.0.1:8080/health
```

如果 Windows 访问不了 WSL 的 `127.0.0.1`，可以查 WSL IP：

```text
hostname -I
```

然后在 Windows 里访问：

```text
http://WSL_IP:8080/
```

### 初始化 Sub2API

打开管理后台：

```text
http://WSL_IP:8080/
```

使用启动脚本里设置的管理员账号登录。

建议先创建一个分组：

```text
名称: OpenCode Go
平台: openai
状态: active
```

然后添加多个账号。

账号类型选择：

```text
platform: openai
type: apikey
```

账号凭据大致是：

```text
{
  "api_key": "sk-你的-opencode-go-key",
  "base_url": "https://opencode.ai/zen/go/v1",
  "openai_capabilities": ["chat_completions"]
}
```

把所有 OpenCode Go key 都加入同一个 `OpenCode Go` 分组。

### 创建本地调用 Key

在 Sub2API 里创建一个给 OpenCode 使用的平台 key，例如：

```text
sk-sub2api-opencode-local-test
```

这个 key 不是 OpenCode Go 上游 key，而是 OpenCode 调用 Sub2API 的本地入口 key。

最终 OpenCode 要填的是：

```text
Base URL: http://WSL_IP:8080/v1
API Key: sk-sub2api-opencode-local-test
```

### 配置 OpenCode

可以配置全局文件：

```text
~/.config/opencode/opencode.jsonc
```

也可以配置项目级文件：

```text
项目目录/.opencode/opencode.json
```

示例：

```text
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "sub2api": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Sub2API Local",
      "options": {
        "baseURL": "http://WSL_IP:8080/v1",
        "apiKey": "sk-sub2api-opencode-local-test"
      },
      "models": {
        "glm-5.2": {
          "name": "GLM-5.2 via Sub2API",
          "limit": {
            "context": 400000,
            "output": 128000
          },
          "options": {
            "store": false
          }
        },
        "deepseek-v4-flash": {
          "name": "DeepSeek V4 Flash via Sub2API",
          "limit": {
            "context": 128000,
            "output": 32000
          },
          "options": {
            "store": false
          }
        },
        "minimax-m3": {
          "name": "MiniMax M3 via Sub2API",
          "limit": {
            "context": 1000000,
            "output": 80000
          },
          "options": {
            "store": false
          }
        }
      }
    }
  },
  "model": "sub2api/glm-5.2",
  "small_model": "sub2api/deepseek-v4-flash"
}
```

注意把 `WSL_IP` 换成自己的地址，例如：

```text
172.xx.xx.xx
```

### 测试调用

先用 curl 测 Sub2API：

```text
curl http://WSL_IP:8080/health
```

再用 OpenCode 测：

```text
opencode run --model sub2api/minimax-m3 "用一句中文回复：Sub2API 接入 OpenCode 测试成功。"
```

如果返回正常，就说明链路通了。

之后日常使用直接：

```text
opencode
```

默认模型会走：

```text
sub2api/glm-5.2
```

### 查看运行和消耗

OpenCode 自己可以看统计：

```text
opencode stats --days 1 --models
```

Sub2API 后台也可以看：

-   账号状态
-   是否可调度
-   最后使用时间
-   今日请求数
-   token 消耗
-   费用估算

也可以看日志：

```text
tail -f /var/log/sub2api/sub2api.log
```

如果想确认后端有没有轮询多个账号，可以观察日志里的 `account_id`，或者在后台看每个账号的 `last_used_at`。

### 常见问题

### 1\. 为什么后台显示“注册功能暂时关闭”？

这是普通用户自助注册入口关闭，不影响管理员使用。直接用安装时设置的管理员账号登录即可。

### 2\. Sub2API 账号测试失败，但实际调用正常？

Sub2API 内置的 OpenAI 账号测试有时会默认用 `gpt-5.4` 之类模型。如果你的 OpenCode Go 上游不支持这个模型，就可能显示测试失败。

这种情况不一定是 key 有问题。可以直接用真实模型测试，例如：

```text
opencode run --model sub2api/minimax-m3 "hello"
```

或者直接请求 OpenCode Go 的 `/models` 接口确认 key 是否有效。

### 3\. WSL IP 会变怎么办？

WSL 重启后 IP 可能变化。最简单做法是重新执行：

```text
hostname -I
```

然后改 OpenCode 配置里的 `baseURL`。

也可以用 Windows 管理员权限配置 `netsh portproxy`，把 `127.0.0.1:8080` 转发到 WSL IP。不过不建议随便写自启动代理脚本，容易被杀毒软件启发式误报。

### 4\. 多账号真的会自动切换吗？

只要多个账号都在同一个分组里，状态是 `active`，并且 `schedulable=true`，Sub2API 就可以调度它们。可以通过后台的最后使用时间、今日统计、日志里的 `account_id` 来确认。

### 总结

这套方案的核心是：不要让 OpenCode 直接管理多个 key，而是把多个 OpenCode Go key 放进 Sub2API，由 Sub2API 统一调度。OpenCode 只需要配置一个 OpenAI-compatible provider。

最终体验上就是：

```text
OpenCode 使用 sub2api/glm-5.2
Sub2API 自动选择多个 OpenCode Go 账号
后台统一看状态和消耗
```

对于想长期使用 OpenCode Go、又有多个账号需要切换的人来说，这种方式会比手动改 key 顺很多。