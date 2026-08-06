Subagent 刚开始流行的时候，很多人都会很兴奋。

这很正常。

一个 Agent 已经能写代码了，那多个 Agent 一起干，是不是就更像一个研发团队？

一个负责[需求分析](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E9%9C%80%E6%B1%82%E5%88%86%E6%9E%90&zhida_source=entity)。

一个负责技术方案。

一个负责写代码。

一个负责补测试。

一个负责 Review。

一个负责安全检查。

听起来很合理。

甚至很像人类团队协作：产品、[架构师](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%9E%B6%E6%9E%84%E5%B8%88&zhida_source=entity)、开发、测试、Reviewer、安全同学各司其职。

但用久了会发现，subagent 不是这么简单。

很多时候，多拆几个 subagent，效果不但没有更好，反而更差。

原因也很直接：Agent 不是人类同事。Subagent 不是坐在你旁边、共享全部上下文、理解项目背景、能随时追问的工程师。

它通常是一个新的上下文窗口。你给它一个任务，它在自己的上下文里执行，最后把结果总结回来。

这带来好处，也带来成本。

好处是隔离噪声、并行探索、避免主会话被大量中间[信息污染](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E4%BF%A1%E6%81%AF%E6%B1%A1%E6%9F%93&zhida_source=entity)。

成本是上下文要重新传，任务要重新解释，结果要重新整合，错误也更难归因。

所以，多 Agent 协作不是多开几个窗口。

它需要很清楚地判断：什么时候该拆，什么时候不该拆。

\## 一、为什么大家容易高估 subagent

大家高估 subagent，主要是因为用了人类团队的类比。

人类团队里，拆工通常能提升效率。

一个人查问题，一个人写代码，一个人补测试，一个人 review。大家有共同背景，有长期协作经验，有上下文记忆，也能随时开会对齐。

但 subagent 没有这些天然条件。

它不知道主会话里完整讨论过什么。

它不知道用户之前否定过哪些方案。

它不知道某个项目里的[隐性规则](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E9%9A%90%E6%80%A7%E8%A7%84%E5%88%99&zhida_source=entity)，除非你传给它。

它不知道另一个 subagent 正在改哪里。

它做完以后通常只返回一个摘要，而不是完整思考过程和所有中间证据。

这就导致一个问题：你每拆一个 subagent，都要支付一次[上下文传输成本](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E4%B8%8A%E4%B8%8B%E6%96%87%E4%BC%A0%E8%BE%93%E6%88%90%E6%9C%AC&zhida_source=entity)。

任务背景要传。

目标要传。

约束要传。

相关文件要传。

禁止事项要传。

输出格式要传。

验证方式要传。

如果传少了，它做错。

如果传多了，成本上升，还可能把它带偏。

所以，subagent 不是免费并行。

它是带成本的隔离执行。

\## 二、subagent 最大的成本是上下文重传

很多人第一次用 subagent，会忽略这个成本。

主 Agent 已经读了十几个文件，理解了需求，知道了[项目约束](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E9%A1%B9%E7%9B%AE%E7%BA%A6%E6%9D%9F&zhida_source=entity)。然后它派一个 subagent 去“实现这个功能”。

问题是，subagent 未必知道主 Agent 刚刚读过什么。

父 Agent 必须把关键信息重新组织给它。

如果父 Agent 只说：

“帮我实现批量导入成员功能。”

subagent 就会从零开始探索。

它可能读错文件、重复查找、漏掉约束，甚至和主 Agent 前面已经确认过的方案冲突。

如果父 Agent 说得很详细：

“需求是这样，技术方案是这样，允许改这些文件，不能改这些文件，测试命令是这些，已有组件在这里，错误处理规范在这里……”

那上下文传输就很重。

这就是 subagent 的基本矛盾：它隔离了上下文，也丢失了上下文。

隔离让它不污染主会话。

丢失让它需要重新获得关键事实。

所以，subagent 最适合的任务，往往不是“接着主 Agent 的复杂推理继续做”，而是“拿一个边界清楚的小任务独立完成”。

\## 三、subagent 会重复探索

第二个成本是重复探索。

比如主 Agent 已经知道导入弹窗在 \`member-management/import-dialog.tsx\`，测试在 \`\_\_tests\_\_/member-import.test.tsx\`，接口在 \`services/member.ts\`。

如果 subagent 没拿到这些信息，它会重新搜索。

这不只是浪费 token 和时间。

更大的问题是，它可能搜到另一套相似但不相关的代码。

大仓库里经常有多个类似实现：

旧页面。

新页面。

移动端版本。

实验版本。

废弃组件。

另一个业务线的相似组件。

主 Agent 前面已经判断了哪个是正确入口，但 subagent 重新探索时可能走到另一条路。

这会导致输出不稳定。

所以，派 subagent 之前，必须明确它的起点。

不要让它“帮我找一下相关代码”这种模糊任务和“帮我实现这个功能”混在一起。

如果任务是探索，就让它只探索。

如果任务是实现，就把探索结果传给它。

不要让每个 subagent 都重新走一遍大仓库迷宫。

\## 四、subagent 会增加合并成本

多 Agent 协作还有一个很现实的问题：结果要合并。

人类团队里，大家可以通过代码 review、会议、设计文档对齐。

Agent 之间通常没有这么强的协商机制。

比如你开了三个 subagent：

一个改 API。

一个改 UI。

一个补测试。

看起来分工明确。

但真实情况可能是：

API subagent 改了返回类型。

UI subagent 按旧类型写了状态。

测试 subagent mock 的是第三种[数据结构](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84&zhida_source=entity)。

最后主 Agent 要回来合并，发现三者不一致。

如果任务边界没有设计好，多 Agent 并行会制造更多冲突。

尤其是写代码任务，只要多个 subagent 可能改同一组文件，就要非常小心。

同一个文件被两个 Agent 改，不只是 merge conflict。更麻烦的是语义冲突：代码能合并，但逻辑不一致。

所以，并行 subagent 适合文件边界清楚、模块边界清楚、输出可独立验证的任务。

不适合高度耦合的实现任务。

\## 五、subagent 会让责任边界变模糊

还有一个问题：责任边界。

一个 Agent 做错了，你可以回看它读了什么、改了什么、为什么这么改。

多个 subagent 协作时，错误可能来自很多地方：

父 Agent 任务拆错。

父 Agent 传少了上下文。

subagent 误解了任务。

另一个 subagent 输出了错误假设。

合并时主 Agent 没发现冲突。

测试没有覆盖到。

最后出问题时，很难判断是哪一层的问题。

所以，多 Agent 工作流必须有清晰交付物。

每个 subagent 不能只说“完成了”。

它应该输出：

做了什么。

看了哪些文件。

基于哪些假设。

改了哪些文件。

哪些地方不确定。

跑了哪些验证。

需要主 Agent 注意什么。

否则主 Agent 拿到几个模糊总结，很难负责整合。

\## 六、什么时候应该用 subagent

说了这么多成本，不代表 subagent 没用。

它很有用，但要用在合适场景。

我认为有几类任务适合。

第一类，研究型任务。

比如：

“找出项目里所有调用旧支付接口的地方。”

“分析这个模块有哪些入口。”

“调研升级某个依赖会影响哪些文件。”

“比较两套实现的差异。”

这类任务会产生大量搜索、阅读和中间判断。放在主会话里会污染上下文，交给 subagent 很合适。

第二类，只读 Review 任务。

比如让 subagent 读 PR diff，输出 P0/P1 风险。

它不需要改文件，也不需要和主 Agent 共享很多实现状态。只要给它任务 spec、diff 和测试结果就够。

第三类，安全检查。

比如检查敏感信息、[权限边界](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%9D%83%E9%99%90%E8%BE%B9%E7%95%8C&zhida_source=entity)、危险依赖、CI 是否被绕过。

这种任务有明确 checklist，适合专门 subagent。

第四类，独立模块实现。

比如一个需求拆成两个完全不同模块，文件边界清楚。一个 subagent 负责 A 模块，另一个负责 B 模块。

前提是[接口契约](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%8E%A5%E5%8F%A3%E5%A5%91%E7%BA%A6&zhida_source=entity)先定好。

第五类，噪声很大的任务。

比如跑大量[日志分析](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%97%A5%E5%BF%97%E5%88%86%E6%9E%90&zhida_source=entity)、读很多文件、搜索很多候选点。这些中间过程不应该挤占主会话上下文。

第六类，可并行验证任务。

比如一个 subagent 跑前端测试，一个跑后端测试，一个做 lint/typecheck 失败分析。它们不改同一批文件，只返回结果。

这些场景里，subagent 的收益大于成本。

\## 七、什么时候不应该用 subagent

也有很多场景不适合。

第一，需求还不清楚时。

如果连目标、验收标准、边界都没定，拆 subagent 只会让混乱扩散。

第二，任务高度耦合时。

比如一个[状态流](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E7%8A%B6%E6%80%81%E6%B5%81&zhida_source=entity)贯穿多个组件、接口、hook、测试。拆给多个 subagent 很容易不一致。

第三，主上下文非常关键时。

如果任务依赖用户前面大量讨论、多个限制条件、历史决策，subagent 很可能拿不到完整背景。

第四，文件冲突风险高时。

多个 subagent 会改同一组文件，最好不要并行。

第五，输出难验证时。

比如“帮我优化架构”“帮我提升代码质量”。这种任务边界模糊，subagent 输出很难判断对错。

第六，只是为了显得流程高级。

如果一个主 Agent 能清楚完成，就没必要拆。

Subagent 不是 KPI。

\## 八、一个判断公式

我自己会用一个简单公式判断是否拆 subagent：

收益是否大于三类成本。

收益包括：

能否并行节省时间。

能否隔离噪声。

能否使用专门 checklist。

能否避免主会话被污染。

能否让任务边界更清晰。

成本包括：

上下文重传成本。

[重复探索成本](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E9%87%8D%E5%A4%8D%E6%8E%A2%E7%B4%A2%E6%88%90%E6%9C%AC&zhida_source=entity)。

[结果合并成本](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E7%BB%93%E6%9E%9C%E5%90%88%E5%B9%B6%E6%88%90%E6%9C%AC&zhida_source=entity)。

如果一个任务只是多了一个人设，但这三类成本都很高，那就不要拆。

比如“实现一个跨前后端的复杂功能”，通常不应该一上来拆五个 subagent。

应该先由主 Agent 做需求分析和技术方案，明确边界，再决定哪些部分能独立出去。

\## 九、正确的 subagent 工作流

如果要用 subagent，我建议按这个流程。

第一步，主 Agent 先建立任务共识。

明确目标、验收标准、改动范围、关键上下文。

第二步，主 Agent 决定哪些任务可独立。

不是按角色拆，而是按边界拆。

第三步，给 subagent 明确任务包。

任务包要包括：

目标。

背景。

输入材料。

允许做什么。

不能做什么。

输出格式。

验证要求。

第四步，subagent 输出[结构化](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E7%BB%93%E6%9E%84%E5%8C%96&zhida_source=entity)结果。

不要只给一句总结。要给证据、文件、风险和建议。

第五步，主 Agent 统一整合。

主 Agent 负责判断冲突、合并结论、决定下一步。

第六步，用测试和 CI 验证。

不要相信多个 subagent 的自我总结。最终还是要靠验证。

这套流程比“开几个 subagent 一起干”麻烦，但稳定得多。

\## 十、subagent 的任务包应该怎么写

一个 subagent 任务包可以这样：

\`\`\`  
任务：只读分析成员导入功能相关代码，不要修改文件。

背景：  
我们要实现 CSV 批量导入成员的行级错误展示。

你需要回答：  
1\. 当前导入入口在哪里。  
2\. 是否已有类似导入实现。  
3\. 当前错误处理规范是什么。  
4\. 相关测试在哪里。  
5\. 有哪些风险点。

请只读代码，不要编辑文件。

输出格式：  
\- 相关文件列表  
\- [数据流](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E6%B5%81&zhida_source=entity)说明  
\- 可复用点  
\- 风险点  
\- 建议下一步  
\`\`\`

这个任务就很适合 subagent。

它边界清楚。

只读。

输出可验证。

不会和主 Agent 争抢文件。

相比之下，这样的任务就不适合：

\`\`\`  
帮我把成员导入功能做完。  
\`\`\`

太大、太模糊、上下文太多、责任不清。

\## 十一、不要按人类岗位拆，要按上下文边界拆

很多人喜欢按人类岗位拆 Agent：

planner。

developer。

tester。

reviewer。

security。

release。

这可以作为粗略分类，但不能机械套用。

真正应该按上下文边界拆。

如果 tester 需要读 developer 刚写的所有细节，那它可能不应该太早并行。

如果 reviewer 只需要 diff、spec、测试结果，那它可以独立。

如果 security 只检查权限和敏感信息，它可以独立。

如果 developer 和 tester 会同时改测试文件，就要小心冲突。

按岗位拆，看起来像团队协作。

按上下文边界拆，才像[工程系统](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E5%B7%A5%E7%A8%8B%E7%B3%BB%E7%BB%9F&zhida_source=entity)。

\## 十二、多 Agent 最怕“[并行幻觉](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E5%B9%B6%E8%A1%8C%E5%B9%BB%E8%A7%89&zhida_source=entity)”

多 Agent 很容易让人觉得事情在加速。

你看到几个窗口同时跑，感觉[吞吐量](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E5%90%9E%E5%90%90%E9%87%8F&zhida_source=entity)很高。

但最后可能出现：每个 subagent 都做了一些东西，主 Agent 花很久合并，发现方向不一致，测试也不通过。

这叫并行幻觉。

真正的并行，要满足三个条件：

任务独立。

接口清楚。

结果可验证。

不满足这三个条件，并行只是把混乱提前扩散。

所以，复杂任务不要急着并行。

先串行建立共识，再[并行处理](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E5%B9%B6%E8%A1%8C%E5%A4%84%E7%90%86&zhida_source=entity)独立部分。

\## 十三、subagent 和 skill 的关系

Skill 是工作方法。

Subagent 是执行隔离。

这两者不要混。

比如 review skill 定义了怎么 review：先看 spec，再看 diff，再看测试，再看风险。

这个 skill 可以在主 Agent 里执行，也可以放到 read-only review subagent 里执行。

如果 review 过程会读大量文件，适合 subagent。

如果 review 只是当前 diff 很小，主 Agent 直接做就够了。

所以，不是每个 skill 都要变成 subagent。

Skill 解决“怎么做”。

Subagent 解决“在哪个上下文里做”。

\## 十四、subagent 和 hook 的关系

Hook 是强制门禁。

Subagent 是[智能执行](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E6%99%BA%E8%83%BD%E6%89%A7%E8%A1%8C&zhida_source=entity)。

不要用 subagent 代替 hook。

比如检查 secret，不应该只派一个 security subagent 看看。

应该有 secret scan。

比如禁止删除测试，不应该只让 reviewer subagent 注意。

应该在 CI 或 hook 里检测。

Subagent 可以解释风险、给建议、补分析。

Hook 负责强制拦截。

高风险事项要[程序化](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=%E7%A8%8B%E5%BA%8F%E5%8C%96&zhida_source=entity)，不能只靠 subagent 自觉。

\## 十五、一个实用策略：先单 Agent，后 subagent

团队刚开始做 AI Coding，不建议一上来多 Agent。

更稳的路径是：

第一阶段，单 Agent + 明确任务 + 测试 gate。

先把任务写清楚，让一个 Agent 能稳定完成。

第二阶段，引入只读 subagent。

比如 code search、PR review、安全检查。这类风险低。

第三阶段，引入并行探索。

让多个 subagent 分别调研不同模块，但不写代码。

第四阶段，引入边界清楚的并行实现。

前提是文件边界清晰、接口契约明确、测试能覆盖。

第五阶段，做更完整的 agent team。

这时才考虑 planner、worker、tester、reviewer 的协同。

很多团队跳过前面阶段，直接做第五阶段，所以效果不稳定。

\## 十六、最后

Subagent 是很有价值的能力。

但它不是让 Agent 模拟人类团队越多越好。

它真正的价值是：在合适的时候，把噪声、搜索、验证、审查这些工作隔离出去，让主上下文保持清晰。

如果任务边界清楚，subagent 很好用。

如果任务高度耦合，subagent 会增加成本。

如果上下文传递不清楚，subagent 会重复探索。

如果结果不可验证，subagent 会制造新的不确定性。

所以，多 Agent 协作的关键不是“拆几个 Agent”，而是“哪些工作值得隔离，哪些工作必须共享上下文”。

这也是 [AI Engineering](https://zhida.zhihu.com/search?content_id=280708879&content_type=Article&match_order=1&q=AI+Engineering&zhida_source=entity) 和简单玩工具的区别。

简单玩工具，会觉得多开几个 Agent 就是先进。

真正工程化，会先算上下文成本、合并成本和验证成本。

Subagent 用得好，是加速器。

Subagent 用不好，是噪声放大器。

团队要追求的不是 Agent 数量，而是任务边界、上下文传递和验证闭环。