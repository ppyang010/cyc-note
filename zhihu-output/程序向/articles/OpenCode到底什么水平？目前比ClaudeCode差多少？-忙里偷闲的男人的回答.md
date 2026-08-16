---
id: "2010518852354712904"
title: "OpenCode到底什么水平？目前比ClaudeCode差多少？"
author: "忙里偷闲的男人"
type: zhihu-answer
source: "https://www.zhihu.com/question/1996214081452009106/answer/2010518852354712904"
created: "2026-02-27 00:57"
updated: "2026-02-27 00:57"
collected: "2026-02-27 00:57"
downloaded: "2026-08-16"
---
opencode 必须的导入 oh-my-opencode 和引入 claude code 技能，主代理最好设成 glm-5 或 deepseek-reasoner，死命 ulw 或 raph 循环。glm-5 时常写代码会很久，可以用 kimi-2.5 或 deepseek 代替，个人体验 glm-5 大多时候可以一遍过，kimi-2.5 需要多一两轮提示，deepseek-reasoner 有时会过度思考🤔 但简单的 debug 和代码修改足以应付，我没试过 minimax 不好评价。最重要的是要慢慢梳理自己的工作流程把它们转成子代理、技能或命令。文件内容不要写太长，并且需要强调多思考及迭代查错验证。