---
Title: "Claude内部爆火的Skill，开源了！！"
Url: "https://zhuanlan.zhihu.com/p/2078065284620070962"
Author: "小林coding​​计算机网络等 2 个话题下的优秀答主"
Origin: "知乎专栏"
Description: "大家好，我是小林。 这几天，我刷到 Anthropic 工程师 Thariq 发了一条推文，说他们公司内部最近有不少人在用一个叫 ELI5 的 Skill。 ELI5 是「Explain Like I’m 5」的缩写。你可以理解成，不管这个话题有多复杂…"
Tags:
  - "claude"
  - "Skill"
  - "anthropic"
Created: "2026-09-03 08:19:36"
Cover: "https://pica.zhimg.com/v2-af02884c40ba7466613735a8bca0af69_720w.jpg?source=172ae18b"
---

[收录于 · AI大模型实用手册](https://www.zhihu.com/column/c_1987478430338537192)

10 人赞同了该文章

大家好，我是小林。

这几天，我刷到 Anthropic 工程师 Thariq 发了一条推文，说他们公司内部最近有不少人在用一个叫 [ELI5](https://zhida.zhihu.com/search?content_id=282617714&content_type=Article&match_order=1&q=ELI5&zhida_source=entity) 的 Skill。

![](https://picx.zhimg.com/v2-3c313bc8d4166cd8d6974f36b55517d3_1440w.jpg)

ELI5 是「Explain Like I’m 5」的缩写。你可以理解成，不管这个话题有多复杂，都先把我当成一个完全不了解的人来讲。

它的用法很直接。在 [Claude](https://zhida.zhihu.com/search?content_id=282617714&content_type=Article&match_order=1&q=Claude&zhida_source=entity) Code 里输入 `/eli5`，后面跟上你想了解的东西。

```
/eli5 Agent 是什么？怎么工作的？
```

AI 会生成一个 HTML 页面，用大图配上很少的文字，把 Agent 的工作方式画给你看。

![动图封面](https://picx.zhimg.com/v2-f8a6eb357bd1554002cff47c17d705e3_b.jpg)

看起来有点像技术版的儿童绘本。

以后碰到一个陌生话题，不想一上来就啃大段资料，可以先丢给 ELI5，让它帮你把大概脉络画出来。

我当时就挺好奇，这么好用的 Skill，里面到底塞了多少提示词，才能让 AI 稳定做出这种页面？

结果点开 [GitHub](https://zhida.zhihu.com/search?content_id=282617714&content_type=Article&match_order=1&q=GitHub&zhida_source=entity) 一看，整个 Skill 的核心只有一句提示词。

![](https://pic2.zhimg.com/v2-6ed671caccb8c66030f3a940d75f6205_1440w.jpg)

我还以为页面没加载完整，顺手刷新了几次。

还是只有这一句。

## ────这个 Skill 到底写了什么？────

ELI5 的 `SKILL.md` 只有 321 字节，去掉开头的名字和触发说明，正文只有下面这句话。

```
Explain like I'm someone who knows nothing about this topic,
using a HTML artifact with big pictures and few words.

Topic: $ARGUMENTS
```

翻译过来很简单， **把我当成一个对这个主题完全不了解的人，用大图和少量文字，做成一个 HTML 页面讲给我看**。

![](https://pica.zhimg.com/v2-035921e4f02bd70ca441d304393c75dc_1440w.jpg)

整个 Skill 的工作全交给这一句话。页面该分成几块、画什么图、用什么颜色，Claude 自己判断。

这也是我觉得它有意思的地方。ELI5 没有教 AI 怎么写网页，模型本来就会。这句提示词只定了三个要求，默认你从零开始，内容要可视化，文字尽量少。

就这么一句提示词，AI 的回答就从大段文字变成了大图少字的网页。

## ────怎么安装和使用 ELI5？────

如果你想把 ELI5 装到 Claude Code 里，先添加 Anthropic 的社区插件市场，再安装这个 Skill。

```
claude plugin marketplace add anthropics/claude-plugins-community
claude plugin install eli5@claude-community
```

不过，ELI5 并不是 Claude Code 专属。它本质上就是一份 `SKILL.md`，所以也是可以安装到 Codex、WorkBuddy 等 Agent 里的。

安装的方式也很简单，直接丢个这个提示词就搞定了。

```
https://github.com/anthropics/claude-plugins-community/blob/main/eli5/skills/eli5/SKILL.md 帮我装这个 skill
```
![](https://pic2.zhimg.com/v2-05979db82a7cd924935c4c2ab34f6847_1440w.jpg)

装好之后，不管你用 Claude Code、Codex 还是 WorkBuddy，调用方式都一样。

你想学习一个陌生的知识，直接这样问题就可以：

```
/eli5 DNS是怎么工作的？
```

你还可以拿它理解陌生项目、技术取舍和事故原因，帮助你快速熟悉一个项目。

```
/eli5 这个项目是怎么工作的

/eli5 为什么要做这个技术取舍

/eli5 是什么导致了这次事故
```

## ────实测 ELI5 的效果────

最近 [DeepSeek V4 Flash](https://zhida.zhihu.com/search?content_id=282617714&content_type=Article&match_order=1&q=DeepSeek+V4+Flash&zhida_source=entity) 和 Pro 正式版出来后，很多人都在讨论它们比预览版强了多少。讨论里经常出现一个词，「后训练」。

后训练到底是什么？

如果直接搜资料，大概率又是一堆术语。我把这个问题丢给 ELI5，让它用最简单的方法教我。

![](https://pic1.zhimg.com/v2-f301cef26d4040b38697d3c15f7d243e_1440w.jpg)

它直接做了一个可以交互的图文网页。

![动图封面](https://picx.zhimg.com/v2-880e8944a5d83650ab29b67e874ee9b5_b.jpg)

我觉得它讲得挺顺。大模型完成预训练之后，还要针对回答、推理这些能力做专项练习，这个过程就是后训练。

那同一个模型，为什么练完之后会变强？

它用了一个很好懂的说法，「知道」不等于「会做」。

![](https://pica.zhimg.com/v2-8f839744359cf5392de4d65aabf657d6_1440w.jpg)

光解释还不够，网页里还做了一套互动演示，让你一步步看模型是怎么练出来的。

![动图封面](https://pic3.zhimg.com/v2-042ce68427cf87f93dfa4a1190d413ae_b.jpg)

我又试了一下，不用 ELI5，直接问 AI 同样的问题。

![动图封面](https://picx.zhimg.com/v2-2e57bfa344d721dd6b0d665c3b2a7549_b.jpg)

结果又回到了熟悉的长篇文字，信息全堆在一起，读起来确实更累。

放在一起看，ELI5 的优势就很直观了。它会先用图把关系讲清楚，再带着你一点点往下理解。

对了，很多林友跟我吐槽，Agent 开发里全是新名词，刚弄懂一个，又冒出来三个，学起来真的很累。

这种时候，ELI5 就挺好用。

比如你想知道「RAG 是怎么工作的」，直接把问题丢给它。

![](https://pic3.zhimg.com/v2-af62d330bbd1515882b4e26ee7940dfc_1440w.jpg)

最后出来的是这样的，讲解很清楚。

![动图封面](https://pic3.zhimg.com/v2-6ea622fadccdb5a43256359d1d3b45e4_b.jpg)

如果你在准备面试，碰到「如何提升 RAG 的召回率」，也可以让它做成网页，帮你把几种方法放在一起梳理。

![动图封面](https://picx.zhimg.com/v2-838c535b0909043608432c93b18e0dfb_b.jpg)

还有最近 AI 编程里经常提到的 `Harness`，看名字就有点让人摸不着头脑。交给 ELI5，它也能用图把这个概念讲明白。

![动图封面](https://pic3.zhimg.com/v2-dfcbfce016b07da235ef72a5b3888244_b.jpg)

这些新名词原来要在不同资料里来回查，现在可以先让 ELI5 画一张图，把大概脉络弄懂，再去看更详细的资料。

对了，我还顺手拿它试了一个真实项目。

我打开了我们的《 [智能 OnCall Agent 项目](https://mp.weixin.qq.com/s?__biz=MzUxODAzNDg4NQ==&mid=2247558967&idx=2&sn=690c765db6450c34eb9485a05b68874c&scene=21#wechat_redirect)》的源码，让 ELI5 解释这个项目是怎么工作的。

![](https://pic3.zhimg.com/v2-ec187e718b3329a0305c788adb9079e2_1440w.jpg)

它先把项目的三种工作模式列了出来。

![动图封面](https://pic4.zhimg.com/v2-b84027cc76e0ab7af062ab339631860f_b.jpg)

接着，我又问了它第二个问题，「这个项目用了哪些技术栈？」前端、后端、Agent、存储和容器，它都罗列得很清楚。

![动图封面](https://pica.zhimg.com/v2-f72a91bb7ca90a74454749d6ea4a5250_b.jpg)

如果你经常要学新知识，或者突然接手一个陌生项目，ELI5 最有用的地方，就是先帮你跨过第一道门槛。

至少不会一上来就被满屏术语劝退。

## ────写在最后────

看到 ELI5 的提示词这么短，我马上想到之前分享过的另一个 Skill， `grill-me`。

你把一个还没想清楚的方案交给 AI，它会追着你往下问，一次只问一个问题，还会给出它的推荐答案。代码库里能找到的信息，它就自己去查。

听着像一套挺复杂的流程，对吧？

结果 grill-me skill的核心提示词也只有下面几句话。

```
Interview me relentlessly about every aspect of this plan
until we reach a shared understanding. Walk down each branch
of the design tree, resolving dependencies between decisions
one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each
question before continuing. Asking multiple questions at once
is bewildering.

If a question can be answered by exploring the codebase,
explore the codebase instead.
```

翻译成中文，大概是这样。

```
毫不留情地追问我这个方案的每一个细节，直到我们达成共同理解。沿着设计树的每一条分支往下走，逐个解决各项决定之间的依赖关系。每次提问时，也给出你推荐的答案。

一次只问一个问题，等我回答后再继续。一次抛出多个问题会让人不知所措。

如果某个问题能通过查看代码库找到答案，那就自己查看代码库，不要再问我。
```

核心提示词就这几句话。

它没写先做什么、再做什么，只给 AI 定了一个目标，把方案问清楚。然后补了两条规矩，一次只问一个，能自己查的就自己查。

![](https://pic1.zhimg.com/v2-a7256cc3da4149d86e532d0eecf4caa0_1440w.jpg)

ELI5 也是这个思路。

把复杂问题讲明白，这是目标。具体画什么图、用什么比喻、从哪里开始讲，交给模型自己判断。

我觉得这两个 Skill 有意思的地方就在这里。它们没有把 AI 限在一套固定流程里，只给了一个方向和几条关键规则。

模型越强，自己能补出来的细节越多，同一个 Skill 用起来也会越顺。

有一种大道至简的感觉了。

还没有人送礼物，鼓励一下作者吧

[所属专栏 · 2026-09-01 17:44 更新](https://zhuanlan.zhihu.com/c_1987478430338537192)

![](https://picx.zhimg.com/v2-c5be1695771c4f9b442b5bde56e5e8e0_720w.jpg?source=172ae18b)

AI大模型实用手册

![](https://pic1.zhimg.com/v2-98f2e73c0d32161569ee7beb5b58ad55_l.jpg?source=172ae18b)

小林coding

AI编程开发等 2 个话题下的优秀答主

78 篇内容 · 7289 赞同

最热内容 ·

万字长文图解 Claude Code 剖析源码：架构设计、Agent工作模式、System Prompt、记忆系统、上下文窗口管理等

发布于 2026-09-01 10:24・广东

[claude](https://www.zhihu.com/topic/27244636)

[Skill](https://www.zhihu.com/topic/23777133)

[anthropic](https://www.zhihu.com/topic/27829820)