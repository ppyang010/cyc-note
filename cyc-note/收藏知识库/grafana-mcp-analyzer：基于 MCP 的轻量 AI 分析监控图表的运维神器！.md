---
Title: "grafana-mcp-analyzer：基于 MCP 的轻量 AI 分析监控图表的运维神器！"
Url: "https://blog.csdn.net/qq_37834631/article/details/148473620?spm=1001.2014.3001.5501"
Author: "qq_37834631"
Origin: "qq_37834631"
Description: "文章浏览阅读3.3k次，点赞12次，收藏29次。grafana-mcp-analyzer是一个开源项目，通过MCP协议将AI助手与Grafana监控平台连接，实现自然语言分析监控数据。它能自动读取Grafana仪表盘，提供专业运维分析和优化建议。主要特点：支持多种AI助手（ChatGPT/Claude/Cursor）30秒快速配置，支持curl命令和HTTP API两种方式全面分析监控数据并提供可执行建议轻量级部署，支持多种数据源安装只需3分钟：npm安装工具配置Grafana连接集成AI助手通过自然语言查询获取专业分析_grafana-mcp-analyzer"
Tags:
  - "grafana"
  - "人工智能"
  - "运维"
  - "node.js"
  - "typescript"
Created: "2026-08-12 16:40:00"
Cover: "https://csdnimg.cn/release/blogv2/dist/pc/img/newHeart2023Active.png"
---

还在深夜盯着 Grafana 图表手动排查问题？今天推荐一个让 **AI 能“读图说话”的开源神器** —— [`grafana-mcp-analyzer`](https://github.com/SailingCoder/grafana-mcp-analyzer)。

#### 想象一下这样的场景：

- 凌晨3点，服务器告警响起。。。
- 你睁着惺忪的眼睛盯着复杂的监控图表 😵💫
- 花了30分钟才找到问题根源…

**现在，仅需一句话就能搞定：**

> 👤 “AI，帮我看看服务器出什么问题了？”
> 
> 🤖 AI立即回复：“CPU突增85%，主要是订单处理服务的内存泄漏导致，建议…”

![](https://i-blog.csdnimg.cn/direct/ca8b55fae3df4f3b8249c332ad7c0175.webp#pic_center)

### 项目简介：什么是 grafana-mcp-analyzer？

`grafana-mcp-analyzer` 是一个开源项目，基于 **Model Context Protocol (MCP)** 协议，提供了一套桥接 **AI 助手** （如 ChatGPT、Claude）与 **Grafana 监控平台** 的中间层服务。它能让 AI 助手实时读取你的 Grafana 仪表盘数据，并用自然语言做出判断、分析以及建议。

| 功能亮点 | 技术优势 | 实际价值 |
| --- | --- | --- |
| **自然语言查询** | 基于MCP协议，支持Claude/ChatGPT/Cursor | 零学习成本，说人话就能分析 |
| **一键curl配置** | 快速配置，浏览器复制即用 | 30秒完成复杂查询配置 |
| **多层级分析** | 支持单个图表精准分析，也支持整个Dashboard聚合分析，支持 **大体量数据** 分析 | 灵活的分析粒度 |
| **全数据源支持** | Prometheus、ES、MySQL… | 统一所有监控数据 |
| **专业DevOps建议** | 不只是展示数据，更提供可执行的优化方案 | 比人工更快发现潜在问题 |
| **超轻量部署** | 超小体积，快速集成部署 | 生产环境零负担 |

一句话总结： ***让 AI 自动分析 Grafana 指标，做你身边的智能运维专家。***

### 🚀 快速配置：从配置到使用全程不到3分钟

#### 第一步：极速安装（30秒）

```bash
npm install -g grafana-mcp-analyzer
bash1
```

> MCP 依赖 `Node.js 18+` 环境，推荐安装方式详见： [Node.js 快速安装最全指南](https://blog.csdn.net/qq_37834631/article/details/148457021?spm=1001.2014.3001.5501)

#### 第二步：AI 助手集成（30秒）

**Cursor设置** → **“MCP”** → **服务配置** （以Cursor为例）

```json
{
  "mcpServers": {
    "grafana": {
      "command": "grafana-mcp-analyzer",
      "env": {
        "CONFIG_PATH": "https://raw.githubusercontent.com/SailingCoder/grafana-mcp-analyzer/main/config/grafana-config-play.js"
      }
    }
  }
}
json12345678910
```

注：CONFIG_PATH支持绝对路径、远程路径，推荐使用远程路径快速体验。

#### 第二步：智能配置（1分钟）

如果你需要连接自己的数据，请在 `CONFIG_PATH` 路径下创建一个名为 `grafana-config-play.js` 的配置文件。

> 如果你只想快速体验示例，可跳过此步骤，直接执行第四步。

```javascript
/**
 * 基于Grafana Play演示实例的配置文件
 * 数据源(狗狗币OHLC数据)：https://play.grafana.org/d/candlesticksss/candlestick2?orgId=1&from=2021-07-13T22:13:30.740Z&to=2021-07-13T22:46:18.921Z&timezone=utc
 * 以下配置文件内容来源：https://raw.githubusercontent.com/SailingCoder/grafana-mcp-analyzer/main/config/grafana-config-play.js
 * Request 配置方式：支持 http api 和 curl
 */
const config = {
  // Grafana服务器地址
  baseUrl: 'https://play.grafana.org',
  
  // 默认请求头
  defaultHeaders: {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*'
  },

  // 健康检查配置
  healthCheck: {
    url: 'api/health'
  },

  // 查询定义
  queries: {
    // 第一个查询 - 使用curl格式（面板2的狗狗币数据）
    // dogecoin_panel_2 ....

    // 第二个查询 - 使用HTTP API格式（面板7的狗狗币数据）
    'dogecoin_panel_7': {
      url: 'api/ds/query',
      method: 'POST',
      params: {
        ds_type: 'grafana-testdata-datasource',
        requestId: 'SQR109'
      },
      headers: {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'x-datasource-uid': '9cY0WtPMz',
        'x-grafana-org-id': '1',
        'x-panel-id': '7',
        'x-panel-plugin-id': 'candlestick',
        'x-plugin-id': 'grafana-testdata-datasource'
      },
      data: {
        queries: [{
          csvFileName: "ohlc_dogecoin.csv",
          datasource: {
            type: "grafana-testdata-datasource",
            uid: "9cY0WtPMz"
          },
          refId: "A",
          scenarioId: "csv_file",
          datasourceId: 153,
          intervalMs: 2000,
          maxDataPoints: 1150
        }],
        from: "1626214410740",
        to: "1626216378921"
      },
      systemPrompt: \`您是金融市场技术分析专家，专注于加密货币市场分析。

**分析重点**：
1. 市场趋势和动量分析 - 识别主要趋势方向和动量变化
2. 价格模式识别 - 识别头肩顶、双底、三角形等经典形态
3. 成交量与价格关系 - 分析成交量对价格走势的支撑
4. 市场情绪评估 - 基于技术指标评估市场情绪状态
5. 短期和长期投资策略建议 - 提供不同时间周期的投资建议

**输出要求**：
- 基于实际数据进行分析，提供具体数值解读
- 识别关键的价格模式和趋势变化
- 给出明确的交易建议和风险提示
- 提供可操作的投资策略

请提供详细的技术分析报告。\`
    },
    overall_cpu_utilization100: {
      curl: \`curl 'https://play.grafana.org/api/ds/query?ds_type=prometheus&requestId=SQR371' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -b '_ga=GA1.2.387525048.1751712678; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX191kw8iAnoyFkv6jbIl3EOkbSdK21uFLwGid2zCBcXWXVl4rK8kP9uB; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2FQpNd4Fbr7FgBG8YeyeoTAiBUO993bC9E%3D; _gid=GA1.2.354949503.1752935466; rl_group_id=RudderEncrypt%3AU2FsdGVkX1%2Fyd5jy%2Bq5XZfeqcDGhXMhz56ANft0NLCo%3D; rl_group_trait=RudderEncrypt%3AU2FsdGVkX1%2F9hmHjbWlb%2F%2B2RP0JlMRymkg9QBgUw3oE%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX19JQD0l8hbD8ApQMSbVisxyXCEuam7wcYtcnfywOO67gQc7EjkFm0bW%2BNZjB%2BsmRZnHy5ccbyeoHQ%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX18s9kRPf%2BwQSRIaYGd9O5kGPmZh%2FQhoq4LyI63CRJNoBrh7Cc06OuAO; rl_trait=RudderEncrypt%3AU2FsdGVkX1%2B%2FhZugE4qfWyjSTEFKcsYs0DwcOyfdazoJfVtGv4x0q%2BOFxbqHDD0r%2BLWcg%2F6CceMFQH3dJIa3C0WyF0hWoBLLwV%2BiQB4077KEHTtX%2BkJxjJ4X6czXwpsh%2FsV9e8l4ptVfz%2FgyJLh1qw%3D%3D; _gat=1; _ga_Y0HRZEVBCW=GS2.2.s1752935474$o2$g1$t1752935591$j38$l0$h0; rl_session=RudderEncrypt%3AU2FsdGVkX1%2BUhBGRm24hqUS5TRKZrN31aK8t518MW16GZKplO6iFClFnqmpYiglWbXqKgnDZz8o%2FaGxuQouIM%2BN0BBr8Nh3HY6chGRtVUEeRSRXAAQiiH30%2Bp6%2F57AoqhwV3k0jqvIikr69S9sDpCg%3D%3D' \
  -H 'origin: https://play.grafana.org' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://play.grafana.org/d/cNMLIAFK/cpu-utilization-details-cores?var-interval=$__auto&orgId=1&from=now-3h&to=now&timezone=browser&var-host=faro-shop-control-plane&var-cpu=$__all&refresh=5s&editPanel=22&inspect=22&inspectTab=query' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' \
  -H 'x-dashboard-title: CPU Utilization Details (Cores)' \
  -H 'x-dashboard-uid: cNMLIAFK' \
  -H 'x-datasource-uid: grafanacloud-prom' \
  -H 'x-grafana-device-id: 2b0db28108a0a56f4a0dcf3d59537fe7' \
  -H 'x-grafana-org-id: 1' \
  -H 'x-panel-id: 22' \
  -H 'x-panel-plugin-id: timeseries' \
  -H 'x-panel-title: $host - Overall CPU Utilization' \
  -H 'x-plugin-id: prometheus' \
  --data-raw $'{"queries":[{"calculatedInterval":"2s","datasource":{"type":"prometheus","uid":"grafanacloud-prom"},"datasourceErrors":{},"errors":{},"expr":"clamp_max((avg by (mode) ( (clamp_max(rate(node_cpu_seconds_total{instance=\\"faro-shop-control-plane\\",mode\u0021=\\"idle\\"}[1m]),1)) or (clamp_max(irate(node_cpu_seconds_total{instance=\\"faro-shop-control-plane\\",mode\u0021=\\"idle\\"}[5m]),1)) )),1)","format":"time_series","hide":false,"interval":"1m","intervalFactor":1,"legendFormat":"{{mode}}","metric":"","refId":"A","step":300,"exemplar":false,"requestId":"22A","utcOffsetSec":28800,"scopes":[],"adhocFilters":[],"datasourceId":171,"intervalMs":60000,"maxDataPoints":778},{"datasource":{"type":"prometheus","uid":"grafanacloud-prom"},"expr":"clamp_max(max by () (sum  by (cpu) ( (clamp_max(rate(node_cpu_seconds_total{instance=\\"faro-shop-control-plane\\",mode\u0021=\\"idle\\",mode\u0021=\\"iowait\\"}[5m]),1)) or (clamp_max(irate(node_cpu_seconds_total{instance=\\"faro-shop-control-plane\\",mode\u0021=\\"idle\\",mode\u0021=\\"iowait\\"}[5m]),1)) )),1)","format":"time_series","hide":false,"interval":"1m","intervalFactor":1,"legendFormat":"Max Core Utilization","refId":"B","exemplar":false,"requestId":"22B","utcOffsetSec":28800,"scopes":[],"adhocFilters":[],"datasourceId":171,"intervalMs":60000,"maxDataPoints":778}],"from":"1752924823337","to":"1752935623337"}'\`,
      systemPrompt: \`您是系统性能分析专家，专注于CPU使用率数据分析。

**核心任务**：直接回答用户的问题："我的服务器现在怎么样？"

**必须回答的问题**：
当前CPU使用率是多少？（具体数值）

**输出格式**：
## 服务器状态概览
**直接结论**：服务器CPU使用率 [具体数值]%，状态 [正常/偏高/异常]

## 详细数据
- **当前使用率**：[数值]%
- **平均使用率**：[数值]%
- **峰值使用率**：[数值]%
- **主要使用模式**：[user/system/iowait等]

## 风险评估
[基于数据的具体风险分析]

## 行动建议
[具体的可执行建议]

**重要**：如果无法获取到实际数据，请明确说明"无法获取实际数据"，并解释可能的原因。不要基于假设进行分析！\`
    },
  }
};

module.exports = config;
javascript运行123456789101112131415161718192021222324252627282930313233343536373839404142434445464748495051525354555657585960616263646566676869707172737475767778798081828384858687888990919293949596979899100101102103104105106107108109110111112113114115116117118119120121122123124125126127128129130131132133
```

**配置获取技巧：** （推荐 curl）

1、curl命令配置

在Grafana中执行查询 → 按F12打开开发者工具 → Network标签页 -> 找到查询请求 → 右键 → Copy as cURL → 粘贴到配置文件的curl字段

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8cfd76741c90413b990228a9171abf54.png)

2、HTTP API配置

- **获取 Data 传参**：进入图表 → “Query Inspector” → "JSON"解析 → 拷贝请求体(request)
- **获取 Url 和 Headers Token**：通过 Network 面板查看请求参数，手动构造 HTTP 配置。

在线转 JSON 地址： [https://www.json.cn/jsononline/](https://www.json.cn/jsononline/)

#### 第四步：开始对话

完全重启Cursor。  
  
然后体验智能分析：

> 👤 您：分析overall_cpu_utilization100数据  
> 🤖 AI：正在连接Grafana并分析…

> 👤 您：聚合分析dogecoin_panel_2、dogecoin_panel_7的数据  
> 🤖 AI：同时查询多个指标并进行综合关联分析…

一句话总结： ***AI 不再只是“聊天”，现在它也能读懂你的监控图表了。***

### 技术实现原理

项目基于 MCP 协议（Model Context Protocol）进行 任务拆解，将 Grafana 图表查询（无论是 PromQL、ES、SQL）统一抽象为结构化数据，提供给 AI 模型进行分析。（简单来说就是 MCP 协议 + Grafana HTTP API）

```
+------------------+     ask("CPU 怎么样？")     +---------------------+
|   ChatGPT 等 AI  |  <---------------------->  | MCP Analyzer 中间服务 |
+------------------+                            +---------------------+
                                                        |
                                                        | 查询转发
                                                        v
                                              +------------------------+
                                              |   Grafana HTTP API     |
                                              +------------------------+
123456789
```

核心优势在于：

- 与数据源（数据查询语句）解耦，支持多种格式统一接入；
- Prompt 可定制，适配不同分析场景；
- 部署简单，生产可落地；
- 适配各种支持 MCP 协议的 AI 工具/平台；
- 核心Resources，支持 **大数据量** 分析，高效智能 **全量** 数据分析；

当前局限：

- 更适用于中小规模数据分析：当前分析能力主要聚焦在中小体量的监控数据，适合日常巡检、局部异常定位等场景，基本可覆盖常规运维需求；
- 大数据量场景仍存挑战：在处理大规模监控数据时，受限于现阶段 AI 模型的上下文处理能力。但随着后续新/老模型能力的加强，这种模型上下文的误差也会消失。

### 结语：让监控系统听得懂人话

随着 AI 的能力越来越强，传统运维的工具链也在悄然升级。如果说过去我们是 ***「人看图 → 手动分析 → 手动决策」***，那么今天，我们已经可以迈入 ***「说句话 → AI 理解 → 给出建议」*** 的智能时代。

[`grafana-mcp-analyzer`](https://github.com/SailingCoder/grafana-mcp-analyzer) 只是个开始。它展示了 AI 与传统监控（Grafana）融合的潜力。如果你正在用 Grafana，又对 AI 感兴趣，这个值得一试。

📎 项目地址： [https://github.com/SailingCoder/grafana-mcp-analyzer](https://github.com/SailingCoder/grafana-mcp-analyzer)  
📫 欢迎留言、点赞、分享，让更多人知道这个项目！