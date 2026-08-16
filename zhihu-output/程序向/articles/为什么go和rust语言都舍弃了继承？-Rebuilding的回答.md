---
id: "2746836518"
title: "为什么go和rust语言都舍弃了继承？"
author: "Rebuilding"
type: zhihu-answer
source: "https://www.zhihu.com/question/511958588/answer/2746836518"
created: "2022-11-06 16:45"
updated: "2023-04-06 17:21"
collected: "2022-11-06 16:45"
downloaded: "2026-08-16"
---
去看看《设计模式》黑书你就知道，大量的设计模型都是因为继承那蹩脚的表达能力，特别是这本书的第二章和第三章，这两章作为本书的重点，实际上都是在尝试在子类中去做组合，既然最终都是为了组合，为何不干脆抛弃继承？Go即是如此。