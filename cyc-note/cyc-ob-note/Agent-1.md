
## 一个最基础的agent 流程


接受用户输入
保存消息上下文并尝试压缩上下文
for_start  (max_rounds) 最大循环次数50次(**到达次数退出**)
调用大模型
模型结果是否要调用工具
	否: 保存模型回复,并返回
	是: 判断是否一个工具调用 
		一个工具调用:串行执行
		多个工具调用:并行执行
		
	保存工具调用结果到上下文
	尝试压缩上下文
	再次调用大模型(把工具调用结果告诉大模型)
KeyboardInterrupt(***用户输入ctrl+c退出***)
for_end


这本质上是一个 ReAct 风格的 Agent 主循环：

模型思考 → 调用工具 → 获取结果 → 模型继续思考 → 最终回答



## 为什么是for循环 而不是while(true)
Claude Code 的循环写成 `while(true)`，靠内部的预算和错误恢复来退出。CoreCoder 这里写成 `for _ in range(self.max_rounds)`，`max_rounds` 默认 50。

这不是风格差异，是一道刹车。设想模型陷入一个它自己跳不出的循环：读文件、发现不对、再读、还是不对、再读。没有上限的话，它会一直烧你的 token，直到你手动 Ctrl+C 或者账单让你心疼。50 轮这个数字是经验值，正常任务远用不到，真撞到上限，循环会返回那句很克制的 `(reached maximum tool-call rounds)`，把控制权交还给你。

任何要把 LLM 放进循环的人，第一件事就该是给循环一个硬上限。这是最便宜的保险。


## 工具结果长什么样子


模型要工具，我们就得把执行结果以它认得的格式喂回去。OpenAI 的 function calling 协议规定，一个 `assistant` 消息如果带了 `tool_calls`，那么后面必须跟上数量相等、`tool_call_id` 一一对应的 `tool` 消息。CoreCoder 老老实实照办：

```python
result = self._exec_tool(tc)
self.messages.append({
    "role": "tool",
    "tool_call_id": tc.id,
    "content": result,
})
```



## 每个 agent 只认自己那套工具

  

注意上面用的是 `self._tool_by_name`，它在构造函数里建好：

```python

self._tool_by_name = {t.name: t for t in self.tools}

```  

是一个实例级的字典，不是全局表。这件事在主 agent 上看不出差别，但在[子 agent](05-parallel-and-subagents.md) 上很关键：主 agent 派生子 agent 时，会把工具集裁掉一部分（比如不让子 agent 再去开孙子 agent）。如果工具查找走的是全局表，这个裁剪就形同虚设，子 agent 还是能叫出被禁的工具。实例级字典保证了「这个 agent 能用哪些工具」是它自己的事，谁也越不过去。测试 `test_agent_tool_scope_is_per_instance` 盯的就是这个：一个只给了 `read_file` 的 agent，去叫 `bash` 会得到 `unknown tool 'bash'`，哪怕 `bash` 是个真实注册过的工具。

ps:派生子agent的时候可以管控子agent的工具