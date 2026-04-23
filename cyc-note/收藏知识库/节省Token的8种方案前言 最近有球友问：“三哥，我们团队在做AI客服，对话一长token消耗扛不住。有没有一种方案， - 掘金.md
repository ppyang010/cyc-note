---
Title: 节省Token的8种方案前言 最近有球友问：“三哥，我们团队在做AI客服，对话一长token消耗扛不住。有没有一种方案， - 掘金
Url: "https://juejin.cn/post/7628442107121598479?utm_source=gold_browser_extension"
Author: 
Origin: juejin.cn
Description: 前言 最近有球友问：“三哥，我们团队在做AI客服，对话一长token消耗扛不住。有没有一种方案，既能保留完整上下文记忆，又能省token？” 这位朋友的问题，恰恰戳中了当下AI应用开发最头疼的痛点。
Tags:
  - 后端中文技术社区
  - 前端开发社区
  - 前端技术交流
  - 前端框架教程
  - JavaScript 学习资源
  - CSS 技巧与最佳实践
  - HTML5 最新动态
  - 前端工程师职业发展
  - 开源前端项目
  - 前端技术趋势
Created: "2026-04-23 22:37:03"
Cover: "https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b2b6df4306a942bc919c8733ae4d419a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1777429681&x-signature=cBdsdpalXaWg6Cq8%2Fshl2X6Ftt8%3D"
---
## 前言

最近有球友问：“三哥，我们团队在做AI客服，对话一长token消耗扛不住。有没有一种方案，既能保留完整上下文记忆，又能省token？”

这位朋友的问题，恰恰戳中了当下AI应用开发最头疼的痛点。

**既要马儿跑得快，又要马儿不吃草。**

这听起来像是矛盾，但经过这两年的摸索，我发现在某些条件下，确实存在“相对两全”的解法。

今天这篇文章就专门跟大家一起聊聊这个话题，希望对你会有所帮助。

更多项目实战在Java突击队网：susan.net.cn

## 一、为什么记忆必然消耗token？

很多小伙伴可能觉得，大模型就像一个人，你说过的话它应该天然记得住。

**错！**

大模型本质上是一个 **无状态的函数。**

每次调用都是独立的，它没有任何“记忆细胞”。

为了让AI记住之前聊过什么，唯一的办法就是： **把历史对话拼接到下一次请求里**。

这就是所谓的“上下文注入”。

![image](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/b2b6df4306a942bc919c8733ae4d419a~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1777429681&x-signature=cBdsdpalXaWg6Cq8%2Fshl2X6Ftt8%3D)

看到没？

**第N次请求携带的历史，是前N-1轮的总和**。

token消耗随着对话轮数线性增长——更准确地说，是O(n)级别的增长。

但事情没这么简单。

Transformer模型的核心是 **自注意力机制**，它的计算复杂度是 **O(n²)**。

也就是说，输入长度翻一倍，计算量翻四倍。

更可怕的是，当输入过长时，模型会患上“中间迷失症”——位于长文本中间的信息被严重忽略。

所以，我们的真实困境是：

> **保留全部历史 → token爆炸 + 注意力稀释 → 又贵又笨**

> **丢弃历史 → 信息丢失 → AI变“金鱼脑”**

有没有一条中间道路？

有。

下面我会介绍8种方案，从简单到复杂，从廉价到智能，你可以根据自己的场景按需选择。

## 二、方案一：全量记忆

简单粗暴，但不推荐。

这是最直觉的实现：把所有对话都存下来，每次请求全部带上。

```bash
bash 体验AI代码助手 代码解读复制代码public class FullMemorySession {
    // 使用LinkedList存储全部对话轮次
    private List<Message> fullHistory = new ArrayList<>();
    
    public void addTurn(String userMsg, String assistantMsg) {
        fullHistory.add(new Message("user", userMsg));
        fullHistory.add(new Message("assistant", assistantMsg));
    }
    
    public String buildContext() {
        StringBuilder sb = new StringBuilder();
        for (Message msg : fullHistory) {
            sb.append(msg.getRole()).append(": ").append(msg.getContent()).append("\n");
        }
        return sb.toString();
    }
    
    // 消息实体
    static class Message {
        String role;
        String content;
        // 构造器、getter省略
    }
}
```

**代码解析**：逻辑非常直接—— `fullHistory` 列表保存所有消息， `buildContext()` 把它们全部拼接成字符串。没有任何优化。

**优点**：

- 信息零损失，完美保留每句话
- 实现极简单，5分钟写完

**缺点**：

- token消耗随轮数线性增长，100轮可能几万token
- 达到模型上下文上限后（比如8K/128K），旧消息会被截断
- 响应时间越来越慢，账单越来越高

**适用场景**：只适合Demo演示、调试测试，或者保证对话不超过10轮的极短场景。

**生产环境慎用**。

## 三、方案二：滑动窗口

省token，但记性差。

滑动窗口只保留最近N轮对话，超出窗口的直接丢弃。

```bash
bash 体验AI代码助手 代码解读复制代码public class SlidingWindowMemory {
    private final int windowSize;          // 窗口大小，比如5轮
    private final Queue<Message> window;   // 用队列自动淘汰旧数据
    
    public SlidingWindowMemory(int windowSize) {
        this.windowSize = windowSize;
        this.window = new ArrayDeque<>();
    }
    
    public void addTurn(String userMsg, String assistantMsg) {
        // 加入新消息
        window.offer(new Message("user", userMsg));
        window.offer(new Message("assistant", assistantMsg));
        // 如果超过窗口大小（注意：一轮=2条消息），就移除头部
        while (window.size() > windowSize * 2) {
            window.poll();
        }
    }
    
    public String buildContext() {
        return window.stream()
            .map(m -> m.getRole() + ": " + m.getContent())
            .collect(Collectors.joining("\n"));
    }
}
```

**代码解析**： `ArrayDeque` 作为队列， `offer()` 在尾部添加，当大小超出 `windowSize * 2` （因为一轮包含用户和助手两条消息）时， `poll()` 移除最旧的。

这样窗口始终保持固定大小。

**优点**：

- token消耗 **严格可控**，不会无限增长
- 实现简单，性能高
- 响应速度快

**缺点**：

- **早期信息永久丢失**。用户第一句说“我是VIP会员”，第20轮问“我的会员权益”，AI已经忘了
- 无法处理需要长期记忆的任务

**适用场景**：客服快速问答、闲聊机器人、临时对话——那些不需要记住早期信息的场景。

## 四、方案三：摘要压缩

让AI自己总结记忆。

这个方案的想法很巧妙：不保留原始对话，而是定期让大模型把旧对话“压缩”成一段摘要，只保留关键信息。

```bash
bash 体验AI代码助手 代码解读复制代码public class SummaryMemory {
    private String summary = "";                    // 历史摘要
    private List<Message> recentMessages = new ArrayList<>();  // 未压缩的新消息
    private final int compressThreshold;             // 触发压缩的token阈值
    private final LLMClient llm;                     // 大模型客户端
    
    public SummaryMemory(LLMClient llm, int compressThreshold) {
        this.llm = llm;
        this.compressThreshold = compressThreshold;
    }
    
    public void addTurn(String userMsg, String assistantMsg) {
        recentMessages.add(new Message("user", userMsg));
        recentMessages.add(new Message("assistant", assistantMsg));
        
        // 估算当前token数，超过阈值则触发压缩
        if (estimateTokenCount() > compressThreshold) {
            compress();
        }
    }
    
    private void compress() {
        // 构建待压缩的内容：旧摘要 + 新消息
        String toCompress = summary + "\n" + formatMessages(recentMessages);
        String prompt = """
            请将以下对话历史压缩成一段简洁的摘要，保留：
            1. 用户的关键信息（姓名、偏好、身份、已做出的决定）
            2. 重要的任务状态和上下文
            3. 任何后续对话可能需要的事实
            原始对话：
            %s
            摘要：
            """.formatted(toCompress);
        
        // 调用大模型生成摘要
        String newSummary = llm.chat(prompt);
        this.summary = newSummary;
        // 压缩后清空近期消息，但可以保留最后一轮作为锚点（防止断层）
        this.recentMessages.clear();
    }
    
    public String buildContext() {
        // 上下文 = 摘要 + 最近未压缩的消息
        if (summary.isEmpty()) {
            return formatMessages(recentMessages);
        }
        return "【历史摘要】\n" + summary + "\n\n【最近对话】\n" + formatMessages(recentMessages);
    }
    
    private int estimateTokenCount() {
        // 简单估算：中文1字≈2token，英文1词≈1.3token，这里粗略用字符数/2
        int totalChars = summary.length() + formatMessages(recentMessages).length();
        return totalChars / 2;
    }
    
    private String formatMessages(List<Message> msgs) {
        return msgs.stream()
            .map(m -> m.getRole() + ": " + m.getContent())
            .collect(Collectors.joining("\n"));
    }
}
```

**代码详解**：

- `summary` 字段存储压缩后的历史摘要，初始为空。
- `recentMessages` 存储尚未被压缩的新消息。
- 每次添加消息后，估算总token数（摘要+新消息），如果超过阈值，调用 `compress()`。
- 压缩时，将旧摘要和新消息一起发给大模型，让它生成一个新的、更精炼的摘要。
- 压缩完成后清空 `recentMessages`，但也可以选择保留最后1-2轮，防止摘要丢失近期细节。
- `buildContext()` 返回摘要+最近消息的拼接，作为下次请求的上下文。

**优点**：

- **压缩比极高**：100轮对话可能压缩成200字摘要，token节省90%以上
- 关键信息被提炼出来，比滑动窗口聪明得多
- 成本可控，摘要生成的调用次数不多（每隔N轮一次）

**缺点**：

- **摘要可能失真**：模型可能漏掉重要细节或产生幻觉
- 每次压缩需要额外调用LLM，增加几十毫秒延迟
- 摘要的“信息密度”随着压缩次数增加而下降（反复压缩会丢失细节）

**适用场景**：长周期对话（几十到几百轮），对信息完整性要求不是100%严谨的场景，比如教育辅导、角色扮演。

## 五、方案四：向量记忆（RAG）

检索相关而不是保留全部。

这是目前工业界最主流的方案。

思路是： **不保存全部历史，而是把历史消息向量化后存入数据库，每次只检索最相关的几条历史**。

```bash
bash 体验AI代码助手 代码解读复制代码public class VectorMemory {
    private final EmbeddingClient embeddingClient;  // 向量化模型，如OpenAI embedding
    private final VectorDatabase vectorDb;           // 向量数据库，如Milvus、Chroma
    private final int topK = 5;                      // 每次检索几条最相关的历史
    
    public VectorMemory(EmbeddingClient embeddingClient, VectorDatabase vectorDb) {
        this.embeddingClient = embeddingClient;
        this.vectorDb = vectorDb;
    }
    
    // 存储一条历史消息（每个消息单独存储，带上元数据）
    public void saveMessage(String role, String content, Map<String, Object> metadata) {
        // 1. 调用embedding接口，将文本转为向量
        float[] vector = embeddingClient.embed(content);
        // 2. 存入向量数据库
        VectorRecord record = new VectorRecord(vector, content, metadata);
        vectorDb.insert(record);
    }
    
    // 检索与当前问题最相关的历史记忆
    public List<Message> retrieveRelevantHistory(String currentQuestion) {
        // 将当前问题向量化
        float[] queryVector = embeddingClient.embed(currentQuestion);
        // 在数据库中做相似度搜索，返回topK条最相似的历史消息
        List<VectorRecord> results = vectorDb.search(queryVector, topK);
        // 转换成Message对象
        return results.stream()
            .map(r -> new Message((String)r.getMetadata().get("role"), r.getContent()))
            .collect(Collectors.toList());
    }
    
    // 构建上下文：检索结果 + 最近几轮（可选）
    public String buildContext(String userQuestion) {
        List<Message> relevantHistory = retrieveRelevantHistory(userQuestion);
        StringBuilder context = new StringBuilder("相关历史记忆：\n");
        for (Message msg : relevantHistory) {
            context.append(msg.getRole()).append(": ").append(msg.getContent()).append("\n");
        }
        return context.toString();
    }
}
```

**代码详解**：

- 每条消息单独存储，调用 `embeddingClient.embed()` 将其转为高维向量（比如1536维）。
- 向量数据库存储向量+原始文本+元数据（角色、时间戳等）。
- 当用户发来新问题时，同样将问题向量化，然后到数据库中做 **余弦相似度搜索**，找到最相似的 `topK` 条历史消息。
- 这些检索出的历史消息就是“与当前问题最相关的记忆”，拼接进上下文。

**优点**：

- **token消耗极低**：每次只带5-10条最相关的历史，而不是几百条
- **可以访问非常久远的记忆**：只要存储了，就能检索到，不受窗口限制
- **灵活性高**：可以混入知识库、FAQ等外部知识

**缺点**：

- **检索可能不准确**：如果embedding模型质量差，或者问题与历史的相关性未被捕捉到，就会漏掉关键信息
- **需要额外组件**：向量数据库、embedding服务，增加系统复杂度
- **有延迟**：embedding调用+向量检索，大约增加50-200ms

**适用场景**：绝大多数生产环境——智能客服、AI助手、个性化推荐等。

**这是目前最推荐的方案**。

## 六、方案五：分层混合记忆

它是工业级最强方案。

没有单一方案是完美的。真正的工业级系统，往往会 **组合多种策略**，形成分层记忆。

下面这张图展示了一个典型的混合记忆架构：

![image](https://p6-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/4a6ad6ef27cf4114bbaa1482f33a1417~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg6IuP5LiJ6K-05oqA5pyv:q75.awebp?rk3s=f64ab15b&x-expires=1777429681&x-signature=bZaAQpAt%2BaMJ%2FL7XzQcVSdMjUWM%3D)

Java实现的核心骨架：

```bash
bash 体验AI代码助手 代码解读复制代码public class HierarchicalMemory {
    private SlidingWindowMemory shortTerm;     // L1 短期
    private SummaryMemory midTerm;              // L2 中期摘要
    private VectorMemory longTerm;              // L3 长期向量
    
    private final int SUMMARY_INTERVAL = 10;    // 每10轮触发一次摘要压缩
    private int turnCount = 0;
    
    public HierarchicalMemory(LLMClient llm, EmbeddingClient embed, VectorDatabase db) {
        this.shortTerm = new SlidingWindowMemory(5);   // 保留最近5轮
        this.midTerm = new SummaryMemory(llm, 2000);    // token超2000压缩
        this.longTerm = new VectorMemory(embed, db);
    }
    
    public void addTurn(String userMsg, String assistantMsg) {
        turnCount++;
        
        // 存入三层记忆
        shortTerm.addTurn(userMsg, assistantMsg);
        midTerm.addTurn(userMsg, assistantMsg);
        longTerm.saveMessage("user", userMsg, Map.of("turn", turnCount));
        longTerm.saveMessage("assistant", assistantMsg, Map.of("turn", turnCount));
        
        // 每10轮额外触发一次摘要同步（可选）
        if (turnCount % SUMMARY_INTERVAL == 0) {
            midTerm.compress();  // 强制压缩
        }
    }
    
    public String buildContext(String currentQuestion) {
        // 1. 短期记忆（最近对话）—— 最重要，直接拼接
        String shortContext = shortTerm.buildContext();
        
        // 2. 检索长期记忆（基于当前问题）
        List<Message> longMemory = longTerm.retrieveRelevantHistory(currentQuestion);
        String longContext = formatMessages(longMemory);
        
        // 3. 中期摘要（如果摘要非空）
        String midContext = midTerm.getCurrentSummary();
        
        // 4. 按重要性组装：短期 > 检索结果 > 摘要
        StringBuilder finalContext = new StringBuilder();
        finalContext.append("【最近对话】\n").append(shortContext).append("\n");
        if (!longContext.isEmpty()) {
            finalContext.append("【相关历史】\n").append(longContext).append("\n");
        }
        if (midContext != null && !midContext.isEmpty()) {
            finalContext.append("【历史摘要】\n").append(midContext).append("\n");
        }
        return finalContext.toString();
    }
}
```

**代码解析**：

- **L1 短期**：滑动窗口保留最近5轮，保证对话连贯性，延迟最低。
- **L2 中期**：摘要压缩，当消息积累到一定程度（比如token超2000或每10轮）就压缩一次，保留全局脉络。
- **L3 长期**：向量数据库存储每条消息，支持按语义检索，解决“长尾记忆”问题。
- **构建上下文时**：优先保证短期（最可靠），然后加上向量检索出的相关历史（弥补窗口丢弃的），最后补充摘要（作为兜底）。

**优点**：

- **兼具短时连贯、长时检索、全局摘要**，覆盖几乎所有场景
- token消耗可控（短期固定+检索topK+摘要）
- 即使检索失败，摘要和短期窗口也能兜底

**缺点**：

- 实现复杂，需要维护多个组件
- 需要精细调参（窗口大小、摘要频率、检索数量）

**适用场景**：大型生产系统、企业级AI应用，对体验和成本都有高要求的场景。

## 七、方案六：状态变量提取

该方案需要极致的结构化压缩。

有些场景下，真正需要记忆的不是整个对话，而是 **几个关键状态变量**。

比如订票机器人只需要知道： `{目的地: "北京", 日期: "2026-05-01", 人数: 2}`。

```bash
bash 体验AI代码助手 代码解读复制代码public class StateVariableMemory {
    private Map<String, Object> state = new HashMap<>();  // 核心状态
    
    // 通过LLM从对话中提取结构化状态
    public void updateState(String userMsg, String assistantMsg, LLMClient llm) {
        String extractPrompt = """
            从以下对话中提取关键状态变量，以JSON格式输出。
            当前已有状态：%s
            用户最新消息：%s
            AI回复：%s
            请更新状态，只输出JSON，不要其他内容。
            """.formatted(toJson(state), userMsg, assistantMsg);
        
        String jsonResponse = llm.chat(extractPrompt);
        Map<String, Object> newState = parseJson(jsonResponse);
        state.putAll(newState);  // 合并更新
    }
    
    public String buildContext() {
        // 上下文只需要展示当前状态，而不是历史对话
        return "当前会话状态：" + toJson(state);
    }
}
```

**优点**：

- **极致省token**：几KB的状态就能代替几十KB的对话
- **结构化**，模型更容易理解

**缺点**：

- 只适合 **高度结构化** 的任务（订票、填表、参数收集）
- 提取状态本身需要调用LLM，有额外成本

**适用场景**：任务型对话、表单填写、配置向导。

## 八、方案七：工具/函数调用

把记忆“外包”给外部系统。

大模型不是万能的，记忆完全可以交给外部数据库。

模型只需要学会调用“保存记忆”和“查询记忆”的工具。

```bash
bash 体验AI代码助手 代码解读复制代码public class ToolBasedMemory {
    // 定义两个工具函数
    @Tool(name = "save_memory", description = "保存一条重要信息到长期记忆")
    public void saveMemory(String key, String value) {
        externalDB.put(key, value);
    }
    
    @Tool(name = "recall_memory", description = "根据关键词回忆之前保存的信息")
    public String recallMemory(String key) {
        return externalDB.get(key);
    }
    
    // 在对话循环中，让模型自主决定何时调用这些工具
}
```

这种方案让模型 **自主管理记忆** ——它觉得重要就存，需要就用。这是目前AI Agent的主流做法。

**优点**：极其灵活，模型可以按需存取；token消耗几乎为零（只传工具调用结果）。  
**缺点**：依赖模型自身的函数调用能力，容易出错或漏存。

**适用场景**：Agent系统、自主决策类应用。

## 九、终极对比

| 方案 | token节省效果 | 信息保留能力 | 实现复杂度 | 推荐指数 |
| --- | --- | --- | --- | --- |
| 全量记忆 | 0%（无节省） | 100% | ⭐ | ❌ 不推荐 |
| 滑动窗口 | 极高（固定） | 差（只留近期） | ⭐ | ⭐⭐ 短对话可用 |
| 摘要压缩 | 高（70-90%） | 中（可能失真） | ⭐⭐⭐ | ⭐⭐⭐⭐ 长对话 |
| 向量检索(RAG) | 高（每次topK） | 高（语义检索） | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ 首选 |
| 分层混合 | 高 | 极高 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ 工业级 |
| 状态变量 | 极高（近乎0） | 中（仅结构化） | ⭐⭐ | ⭐⭐⭐ 任务型 |
| 工具调用 | 极高 | 中（靠模型） | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ Agent场景 |

更多项目实战在Java突击队网：susan.net.cn

## 总结

回到最初的问题： **有没有方案既能保留上下文记忆，又能省token？**

我的答案是： **有，但不存在“免费午餐”。**

每一分token的节省，都换来了系统复杂度的增加或记忆精度的下降。

根据我的实战经验，给你几条直接的建议：

1. **如果你刚开始做MVP**：直接用 **滑动窗口（最近10轮）**，上线跑起来再说。先验证产品价值，再优化成本。
2. **如果你做的是通用客服/AI助手**：首选 **向量检索（RAG）**。这是当前最成熟、性价比最高的方案。配合一个小的滑动窗口（3-5轮）保证对话连贯性，效果已经很好了。
3. **如果你的对话轮次非常长（100+）且信息密度高**：上 **分层混合记忆**。短期窗口+中期摘要+长期向量，三者配合才能既省token又不丢信息。
4. **如果你做的是表单/订票/参数收集**： **状态变量提取** 是王道。几十个字段就能代表整个会话，token几乎不增长。
5. **永远不要在生产环境用全量记忆** ——除非你预算无限且用户只聊5句话。

posted @ [苏三说技术](https://link.juejin.cn/?target=https%3A%2F%2Fwww.cnblogs.com%2F12lisu "https://www.cnblogs.com/12lisu") 阅读(0) 评论(0) [MD](https://link.juejin.cn/?target=https%3A%2F%2Fwww.cnblogs.com%2F12lisu%2Fp%2F19869593.md "https://www.cnblogs.com/12lisu/p/19869593.md") [编辑](https://link.juejin.cn/?target=https%3A%2F%2Fi.cnblogs.com%2FEditPosts.aspx%3Fpostid%3D19869593 "https://i.cnblogs.com/EditPosts.aspx?postid=19869593") [收藏](https://link.juejin.cn/?target=) [举报](https://link.juejin.cn/?target=https%3A%2F%2Freport.cnblogs.com%2F%3FtargetLink%3Dhttps%253A%252F%252Fwww.cnblogs.com%252F12lisu%252Fp%252F19869593%26targetId%3D19869593%26targetType%3D0 "https://report.cnblogs.com/?targetLink=https%3A%2F%2Fwww.cnblogs.com%2F12lisu%2Fp%2F19869593&targetId=19869593&targetType=0")