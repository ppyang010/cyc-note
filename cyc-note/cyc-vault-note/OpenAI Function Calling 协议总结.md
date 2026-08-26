# OpenAI Function Calling 协议总结

**核心机制**：模型不执行函数，只输出结构化调用意图；你的应用执行后把结果回传，循环直到模型给出最终文本。整个过程就是三个阶段：

> 你给菜单（定义工具）→ 模型点菜（模型发起调用）→ 你做好菜端上去（回传结果）

---

## 阶段一：定义工具（你 → 模型）

发请求时告诉模型「你有哪些工具可用」：工具名、用途描述、参数 JSON Schema。模型只看说明，不会真的执行。

| | Responses API（新） | Chat Completions（旧） |
|---|---|---|
| 形态 | 扁平：`{type:"function", name, description, parameters, strict}` | 包一层：`{type:"function", function:{name, parameters}}` |

**例：定义一个执行 bash 命令的工具**

```json
{
  "type": "function",
  "name": "run_bash",
  "description": "在本机执行一条 bash 命令，返回 stdout/stderr 和退出码。",
  "parameters": {
    "type": "object",
    "properties": {
      "command": { "type": "string", "description": "要执行的完整命令，如 ls -la" },
      "workdir": { "type": ["string", "null"], "description": "工作目录，可选" }
    },
    "required": ["command", "workdir"],
    "additionalProperties": false
  },
  "strict": true
}
```

**例：定义一个运行 CLI 的工具（Chat Completions 旧形态）**

```json
{
  "type": "function",
  "function": {
    "name": "run_cli",
    "description": "运行一条 CLI，如 git / gh / npm。",
    "parameters": {
      "type": "object",
      "properties": {
        "argv": {
          "type": "array",
          "items": { "type": "string" },
          "description": "参数数组，例如 [\"git\",\"status\",\"-sb\"]，不要走 shell 拼接"
        }
      },
      "required": ["argv"]
    }
  }
}
```

---

## 阶段二：模型发起调用（模型 → 你）

用户说「列出当前目录文件」，模型返回一张结构化「调用单」。**命令此时还没执行。**

| | Responses API（新） | Chat Completions（旧） |
|---|---|---|
| 位置 | `output[]` 中 `{type:"function_call", call_id, name, arguments}` | `message.tool_calls[]` 中 `{id, function:{name, arguments}}` |

**例：bash 调用单（Responses）**

```json
{
  "type": "function_call",
  "call_id": "call_01",
  "name": "run_bash",
  "arguments": "{\"command\":\"ls -la\",\"workdir\":null}"
}
```

**例：CLI 调用单（Chat Completions）**

```json
{
  "role": "assistant",
  "tool_calls": [{
    "id": "call_cli_1",
    "type": "function",
    "function": {
      "name": "run_cli",
      "arguments": "{\"argv\":[\"git\",\"status\",\"-sb\"]}"
    }
  }]
}
```

---

## 阶段三：回传结果（你 → 模型）

你拿到调用单，在自己机器上真正执行（`bash -lc 'ls -la'` 或 `git status -sb`），把输出发回，并用 `call_id` / `tool_call_id` 对齐。模型看到结果后继续生成最终回答，或再开下一张单子（循环阶段二三）。

| | Responses API（新） | Chat Completions（旧） |
|---|---|---|
| 形态 | `{type:"function_call_output", call_id, output}` | `{role:"tool", tool_call_id, content}` |

**例：bash 执行结果回传（Responses）**

```json
{
  "type": "function_call_output",
  "call_id": "call_01",
  "output": "{\"exit_code\":0,\"stdout\":\"total 48\\ndrwxr-xr-x  8 ccy  staff  256 Aug 24 10:00 .\\n...\",\"stderr\":\"\"}"
}
```

**例：CLI 执行结果回传（Chat Completions）**

```json
{
  "role": "tool",
  "tool_call_id": "call_cli_1",
  "content": "## main\n M README.md"
}
```

---

## 应用侧执行代码（把阶段二接阶段三）

```python
import json, subprocess

def run_bash(command, workdir=None):
    p = subprocess.run(
        ["bash", "-lc", command],
        cwd=workdir or None,
        capture_output=True,
        text=True,
    )
    return json.dumps({
        "exit_code": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
    })

# 收到 function_call 后
args = json.loads(item.arguments)      # 解析模型给的参数
output = run_bash(**args)              # 真正执行
# 再把 function_call_output 塞回下一轮 input
```

---

## 关键规则

- `arguments` 始终是 JSON **字符串**，需自己 `JSON.parse` / `json.loads`
- `parameters` 是标准 JSON Schema；`strict:true` 要求 `additionalProperties:false` + 所有字段进 `required`
- `tool_choice`: `auto` / `required` / `none` / 指定函数；支持并行多张「调用单」
- 结果格式自由（字符串即可）；无返回值的工具回传 `"success"` 之类即可
- 工具定义占 input token；实践建议一次暴露 < 20 个工具、CLI 优先用 `argv` 数组而非 shell 拼接
