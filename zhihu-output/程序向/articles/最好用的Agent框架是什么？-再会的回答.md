---
id: "2011030916038955090"
title: "最好用的Agent框架是什么？"
author: "再会"
type: zhihu-answer
source: "https://www.zhihu.com/question/1962250618908410064/answer/2011030916038955090"
created: "2026-02-28 10:52"
updated: "2026-03-03 17:03"
collected: "2026-02-28 10:52"
downloaded: "2026-08-16"
---
如果你刚学 LangGraph，大概率会跟我一样有个错觉：

“AgentExecutor 用得好好的，为什么要换？”

然后真进了生产环境，立马被打脸。

**想加个人工确认？加不了。想看中间调了几次工具？看不到。想改个重试逻辑？得重写整个黑盒。**

我折腾完 LangGraph 全链路后，最大的体会就一条：**AgentExecutor 是玩具，LangGraph 才是生产工具。**

* * *

### 一、AgentExecutor 这个黑盒，我忍了很久

最开始我用LangChain里的 AgentExecutor 构建了能调工具、查知识、记历史的 Agent。看起来挺全能，但有个致命问题：

**你看不到中间发生了什么。**

有次用户说”删除项目数据”，Agent 直接调了 delete 工具。我想加个”删除前确认”，查了半天文档，发现 AgentExecutor 不支持。

**LangGraph 怎么解决的？**

一行 `interrupt_before=["tools"]` 搞定。在进入 tools 节点前暂停，等人工确认后再继续。

```python
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"]  # 就这行
)
```

**这事的教训：黑盒用起来爽，出事了你连怎么死的都不知道。**

* * *

### 二、State、Node、Edge，三要素我一开始也懵

教程说 LangGraph 就三个核心元素：

| 组件 | 作用 | 类比 |
| ----- | ----- | ----- |
| State | 存储整个流程的共享数据 | 一张所有人都能读写的白板 |
| Node | 执行具体任务的函数 | 一个工人，干完活写回白板 |
| Edge | 定义执行顺序的规则 | 工头喊：”A 干完，B 上！” |

**但我一开始理解错了。**

我以为 State 就是个普通字典，随便定义。结果有次我定义了个 `messages` 字段，节点返回时直接覆盖了之前的消息，记忆全丢了。

**后来才知道：**

```text
from langgraph.graph import MessagesState

class State(MessagesState):  # 继承这个
    user_id: str
    session_data: dict
```

`MessagesState` 里的 `messages` 字段有特殊处理，节点返回新消息时会自动**追加**而不是覆盖。我自己定义的字段没这个待遇。

**踩坑两小时，就为搞懂这个。**

* * *

### 三、LangSmith 这个调试工具，不用真的瞎

LangGraph 提供内置的流程图生成功能：

```text
with open('workflow.png', 'wb') as f:
    f.write(app.get_graph().draw_mermaid_png())
```

但这只是**静态架构图**，看不到运行时状态。

**真正有用的是 LangSmith。**

注册个账号，配三个环境变量：

```text
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "my_demo"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
```

运行后，每次 `app.invoke()` 都会生成一条 Trace 记录。点进去能看到：

-   每一步的输入/输出
-   LLM 的 prompt 和 token 消耗
-   工具调用的参数和返回
-   错误堆栈直接标红

**有次我的 Agent 陷入无限循环，本地调试半天没头绪。** 打开 LangSmith 一看，`should_continue` 函数永远返回”tools”，因为 tool\_calls 判断逻辑写反了。

**这工具省了我至少一半调试时间。** 建议从第一个 LangGraph 项目就启用，别等出问题了再补。

* * *

### 四、thread\_id 和 session\_id，这俩名字把我坑惨了

LangChain 里用 `session_id` 标识会话，LangGraph 里用 `thread_id`。

我一开始没注意，代码里全写的 `session_id`：

```text
config = {
    "configurable": {"session_id": "user123"}  # 错了！
}
```

跑起来记忆功能完全失效。查了半天文档才发现，**LangGraph 必须用 `thread_id`**。

```text
config = {
    "configurable": {"thread_id": "user123"}  # 对了
}
```

**这俩名字太像了，真的容易混。** 我的建议：LangGraph 代码里看到 session\_id 就改成 thread\_id，别犹豫。

* * *

### 五、系统提示词这么写，不然会污染历史

多轮对话里加系统提示词，我一开始是这么写的：

```text
inputs = {
    "messages": [
        SystemMessage(content=sys_prompt),
        HumanMessage(content=user_input)
    ]
}
```

结果每轮对话都重复插入 SystemMessage，历史记录越来越长，token 疯涨。

**正确做法：**

```text
def call_model(state: MessagesState):
    # 仅在 LLM 调用时临时拼接，不写入状态
    message_for_llm = [SystemMessage(content=sys_prompt)] + state["messages"]
    response = llm_with_tools.invoke(message_for_llm)
    return {"messages": [response]}  # 只返回 AI 回复，不包含 prompt
```

**系统提示词只影响当前推理，不保存到历史记录。**这才能确保历史记录流转合理。

* * *

### 六、人工干预这个功能，生产环境必开

刚看到 Human-in-the-Loop时，还觉得“自动化这么方便，干嘛还得一个个对命令手工确认，费事儿”。

后来用agent帮我编程，而且给了他删改权限。等他执行完我傻眼了：我的代码被他改的乱七八糟，找不出一点我之前代码的影子。吓得我赶紧回滚，幸好commit记录还在。从这之后我只给它只读权限，如果涉及真正的代码处理，必须、一定要人工确认！

**现在我的做法：**

```text
app = workflow.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tools"]
)

# 运行时判断哪些工具需要审批
if tool_name == "analyze_server_logs":
    # 查询类工具，自动放行
    inputs = None
elif tool_name == "restart_service":
    # 高危操作，人工确认
    approval = input("是否批准？(yes/no): ")
    if approval == "yes":
        inputs = None
    else:
        break
```

**查询类工具自动过，写操作人工批。** 这样既安全又不影响效率。

* * *

### 七、Graph-as-a-Tool，这个设计我真服

有次我要做个”带重试的 API 调用”工具。一开始直接写函数：

```text
@tool
def call_api(query):
    try:
        return api_call(query)
    except:
        return api_call(query)  # 重试一次
```

后来需求变了，要支持”最多重试 3 次”“指数退避”“失败后通知”……函数越写越长，最后 200 行，根本没法维护。

**LangGraph 的解法：把子流程也做成图。**

```text
# 子图：带重试的 API 调用
retry_workflow = StateGraph(RetryState)
retry_workflow.add_node("call_api", call_unstable_api)
retry_workflow.add_conditional_edges("call_api", should_retry, {...})
retry_app = retry_workflow.compile()

# 封装为 tool
@tool
def create_order(query: str) -> str:
    result = retry_app.invoke({"query": query, "attempt": 1})
    return result["result"]
```

**主图看不到子图内部逻辑，只知道调用个工具。** 子图里爱怎么重试、怎么退避都行，主流程不受影响。

**这个设计有点像微服务。** 大系统拆小模块，每个模块自己管好自己，对外只暴露接口。

* * *

### 八、Multi-Agent 编排，单 Agent 真的会崩

我之前习惯让一个 Agent 干所有活：查文档、搜网页、写代码、回邮件……

后来项目大了，问题全来了：

-   Prompt 太长，LLM 经常忽略指令
-   记忆爆炸，上下文飞速扩张
-   工具混杂，模型容易误调用

**LangGraph 的解法：多专家 + 总控。**

```text
# 专家节点
def rag_expert(state):  # 只查私有知识
def web_research(state):  # 只搜公开信息
def code_writer(state):  # 只写代码

# 总控节点
def supervisor(state):  # 只负责调度
    # 根据任务类型指派专家
    return {"next_speaker": "rag_expert"}
```

**测试过，同样任务，单 Agent 要 1500 token，多 Agent 只要 800。** 因为每个专家只关注自己那摊事，不用背全局上下文。不仅总token少了，每个Agent只需负责自己的上下文，总上下文开销与注意力保持也能更好。

* * *

### 九、条件边的两种写法，我一开始也分不清

LangGraph 的条件边有两种写法：

**动态路由（函数直接返回节点名）：**

```text
def route_supervisor(state):
    return state["next_speaker"]  # 可能返回任何专家名字

workflow.add_conditional_edges("supervisor", route_supervisor)
```

**静态映射（字典指定分支）：**

```text
def should_continue(state):
    if has_tool_calls:
        return "tools"
    return "supervisor"

workflow.add_conditional_edges(
    "member",
    should_continue,
    {"tools": "tools", "supervisor": "supervisor"}  # 显式映射
)
```

**区别在哪？**

动态路由适合目标不确定的情况（Supervisor 可能指派任何专家）；静态映射适合结构固定的场景（二选一或三选一）。

**我一开始全用的动态路由，结果有次拼错节点名，报错信息又看不懂，查了两小时。** 后来固定结构的地方全改静态映射，至少能提前发现拼写错误。

* * *

### 十、一条我走过来的学习路径

我会建议按这个顺序走：

1.  先跑通最小 LangGraph（State + Node + Edge）
2.  接入 LangSmith，学会看 Trace
3.  用 LangGraph 复现 ReAct 循环（替代 AgentExecutor）
4.  加持久化记忆（checkpointer=MemorySaver()）
5.  加人工干预（interrupt\_before）
6.  学 Graph-as-a-Tool（子图封装）
7.  搞 Multi-Agent 编排（总控 + 专家）

你会发现，LangGraph 学习的本质不是”背 API”，而是：

-   **状态驱动意识**（State 是核心，节点只是状态转换器）
-   **流程可视化意识**（能用 LangSmith 就别盲猜）
-   **分层抽象意识**（主图管决策，子图管执行）

* * *

### 最后说一句

**LangGraph 最难的从来不是”画流程图”，而是”理解状态怎么流转”。**

State 怎么定义？节点返回什么？边怎么连？这些事教程不会细讲，只能自己踩。

我把自己走的这条路整理成了一个系列，13 篇，从最基础的手写 Agent 到最后的可视化界面，每篇博客都有配套可运行代码。LangGraph 基础和进阶篇的代码都在 Github 上，开箱即用，仅需配置 API\_KEY。

**agent-craft:**

[https://github.com/Annyfee/agent-craft](https://link.zhihu.com/?target=https%3A//github.com/Annyfee/agent-craft)

不是标准答案，只是一条走过来的路。有帮到你的话，欢迎给个 star，一起交流学习。