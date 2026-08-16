---
id: "2654556842"
title: "Tailwind CSS 是否属于旁门左道？"
author: "Angry Bugs"
type: zhihu-answer
source: "https://www.zhihu.com/question/550275961/answer/2654556842"
created: "2022-08-31 23:31"
updated: "2022-09-01 16:29"
collected: "2022-08-31 23:31"
downloaded: "2026-08-16"
---
tailwind 补全了组件化的最后一块拼图。tailwind 不是旁门左道，而是另一种思维方式。

在 React 出现之前，传统 html+css+js 的模式是纵向切分的，讲究的是表现和结构分离，也就是 html 是骨，css 是皮，js 是肌肉。没有皮和肌肉，骨架只是看起来丑一点，但是没有骨架，皮和肌肉是完全撑不起来的。业界最佳实践也是 html 中绝不可混有 js 和 css，否则就是过分耦合。

```html
<style>
.link {
   color: red;
}
</style>

<h1><a class="link">Hello</a></h1>
<p>Welcome to my blog, <a class="link">Click here</a> to subscribe</p>
```

这样做看起来很好，有什么问题呢？在我看来至少有二：

1.  html 和 js/css 调试困难，写着几百行 html，然后去对应几百行的 css 文件里找到对应的 class 改改样式，或者去 js 中翻对应的 event listener。相信经历过的人都知道有多痛苦。**不断切换上下文是程序员效率低下之源。**
2.  再者，html 和 css 之间需要用 class 连结起来，为了复用代码，又需要在 html 中复用 class，同一个 class 可能被不同类型的组件使用着，结果就是组件样式耦合在了一起，修改样式的时候牵一发而动全身，被缚住了手脚。当然，有一些改良的措施，比如 less/sass 等等，但都是裱糊匠，而不是从头设计。

总之，这种模式下：**复用样式需要复用 html class。**

React 的思路恰恰相反，从纵向切分变成了横向切分。前端不再区分 html 和 js，而是按照功能划分成组件，每个组件中 js 和 html 融合在了一起，极大地方便了调试，程序员的注意力可以集中在当前组件，而不用在 html 和 js 之间跳来跳去。

那么剩下的 css 呢？如果依然写传统的 css 文件，和 React 按照组件切分的模式是格格不入的。相当于在两种模式之间跳来跳去，切分好好的组件，还得去一个大的 css 文件中找 class 更改样式，那不是又倒回去了吗？或者人工划分，一个 js 对应一个 css 文件，总感觉还差那么点意思……

tailwind 恰好补上了这块拼图。样式也成为了组件的一部分，**复用样式就是复用组件：**

```js
function Link({children}) {
  return <a className="text-red-500">{children}</a>
}

function Page() {
  return (<>
    <h1><Link>Hello</Link></h1>
    <p>Welcome to my blog, <Link>Click here</Link> to subscribe</p>
  </>)
}
```

当然，你可能会说 CSS-in-JS 也可以做到在组件里写样式啊，干嘛要用 tailwind？我觉得亲自写一写应该就不会有这个问题了。比如对我来说，用 css 在组件里写 flex 布局很懵，tailwind 的话，很顺畅就写出来了，几乎不用思考。看起来 tailwind 只是一个 css 的宏或者缩写而已，但是这个改进是巨大的。类比一下来说，瓦特也没发明蒸汽机，只是改进了蒸汽机，但是造成的差异是翻天覆地的。

最后，tailwind 只是原子化 css 的一个尝试，还有更多其他的库。比如 windi css，就不用把所有属性都写在 class 里：

```html
<button
  bg="blue-400 hover:blue-500 dark:blue-500 dark:hover:blue-600"
  text="sm white"
  font="mono light"
  p="y-2 x-4"
  border="2 rounded blue-200"
>
  Button
</button>
```