DSH 配置推理等级显示：

请帮我为本机 DSH（DeepSeek Harness）配置模型推理等级，直接修改配置并校验，不要只给操作说明。

目标：为全局配置中所有已显式列出的 llm-pi-ai 模型添加以下可选等级：

reasoningEfforts:
  low: low
  medium: medium
  high: high
  xhigh: xhigh
  max: max

操作要求：
1. 先确定实际 DSH 配置目录。优先检查 DSH_HOME；未设置时检查 ~/.dsh/settings.yaml。读取当前配置，不要直接覆盖整份文件。
2. 检查本机安装的 DSH / llm-pi-ai 版本及配置 schema，确认支持 reasoningEfforts，以及 low、medium、high、xhigh、max 五个键。不支持时停止修改并说明原因。
3. 当前版本若没有全局或 provider 级 reasoningEfforts 默认字段，就逐一添加到：
   llm-pi-ai.providers.<provider>.models[] 的每个模型条目中。
   不要把 reasoningEfforts 写到不支持的顶层位置。
4. 对已有 reasoningEfforts：
   - 若与上述配置一致，保持不变。
   - 若为 false 或存在不同的参数映射，先列出冲突并向我确认，不要静默覆盖。
5. 保持默认模型和默认推理等级不变。不要设置 reasoning: max 或 agent-default-model.reasoningEffort: max；我要的是“可以选择这五档”，不是“默认使用最高档”。
6. 修改前备份原文件。仅修改相关字段，保留其他配置，不输出 API Key 等凭据。
7. 修改后验证 YAML 可解析、字段符合当前版本 schema，并核对所有目标模型的配置。不要把 YAML 解析成功说成服务商支持验证成功。
8. 不要未经确认发起付费模型请求，也不要自动重启正在运行的 DSH。说明是否需要刷新页面或重启才能生效。
9. 最后报告：修改文件、备份位置、涉及的 provider 和模型数量、校验结果，以及未验证事项。

注意：
这是我明确要求统一声明的五档选项，并不代表所有模型或代理实际支持它们。请提醒我：不支持的档位可能被服务端拒绝或忽略，尤其是 xhigh 和 max。
如果只是给现有模型逐一添加，请明确说明以后新增模型不会自动继承。