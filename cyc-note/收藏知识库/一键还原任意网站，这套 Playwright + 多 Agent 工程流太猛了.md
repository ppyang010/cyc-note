---
Title: "一键还原任意网站，这套 Playwright + 多 Agent 工程流太猛了"
Url: "https://juejin.cn/post/7661439504077176847?utm_source=gold_browser_extension"
Author: "我不是外星人"
Origin: "掘金"
Description: "一 前言 哈喽，大家好，我是 alien，今天我们来讲一个能够将精美网站一键复制的功能——ai-website-cloner-template 的使用和实现原理。 通过本篇文档你能收获到哪些内容？ A 一 前言\n\n哈喽，大家好，我是 alien，今天我们来讲一个能够将精美网站一键复制的功能——ai-website-cl"
Tags:
  - "前端"
  - "后端"
  - "AI编程中文技术社区"
  - "前端开发社区"
  - "前端技术交流"
  - "前端框架教程"
  - "JavaScript 学习资源"
  - "CSS 技巧与最佳实践"
  - "HTML5 最新动态"
  - "前端工程师职业发展"
  - "开源前端项目"
  - "前端技术趋势"
Created: "2026-10-15 15:20:57"
Cover: "https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1c0b7004c8e54ed5a0279f13d612287d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=dxeUFT4g90aI6wE5lrmjm1YxaLQ%3D"
---

## 一 前言

哈喽，大家好，我是 alien，今天我们来讲一个能够将精美网站一键复制的功能——ai-website-cloner-template 的使用和实现原理。

通过本篇文档你能收获到哪些内容？

- AI 自动逆向解析网页的新思路；
- playwright 使用介绍；
- ai-website-cloner-template 的介绍；

ai-website-cloner-template 的用法十分简单：

第一步：把 github 上的模板下载到本地：

```js
js 代码解读复制代码git clone https://github.com/JCodesMore/ai-website-cloner-template.git
```

第二步：运行 Claude Code，运行 /clone-website （这个本质上是模板工程维度的 skill）

![3dfdca83a7eb81576305b5fc2833fe5d.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1c0b7004c8e54ed5a0279f13d612287d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=dxeUFT4g90aI6wE5lrmjm1YxaLQ%3D)

废话不说，用掘金的网站为例子（ [juejin.cn），我们先来看一下实现的效果：](https://juejin.cn%EF%BC%89%EF%BC%8C%E6%88%91%E4%BB%AC%E5%85%88%E6%9D%A5%E7%9C%8B%E4%B8%80%E4%B8%8B%E5%AE%9E%E7%8E%B0%E7%9A%84%E6%95%88%E6%9E%9C%EF%BC%9A "https://juejin.cn%EF%BC%89%EF%BC%8C%E6%88%91%E4%BB%AC%E5%85%88%E6%9D%A5%E7%9C%8B%E4%B8%80%E4%B8%8B%E5%AE%9E%E7%8E%B0%E7%9A%84%E6%95%88%E6%9E%9C%EF%BC%9A")

pc 端效果对比（左：生成/右：原图）：

![bcf4f44235c451291204bf95bb67a957.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/1f292ef3a94b4a108c60571f6b1331d1~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=UcTStX5fNhu99cfQ%2Baga2u5Lc2M%3D)

移动端效果对比（左：生成/右：原图）：

![cd1b1a44d37879542b551e1cec909794.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/30f356b1c1c544939e0f1f7a7a39b603~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=Mx15af1s8hyTPvRGT8tlHNP%2B77M%3D)

多端兼容场景：

![2026-07-048.14.44-ezgif.com-video-to-gif-converter.gif](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0ec758a9dffc4ee3bb7e66db03d8bc89~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=18S0sGNwXaL21nteuqGQLrpH4fw%3D)

生成的代码整体效果评估下来：

- 整体 UI 还原还行，没有达到预期那么完美，还原度亲测能到 70%以上；
- 对于一些细节，移动端适配做的比较好；
- 生成的代码的质量，可维护性还可以；（这个本质上受到模型本身影响比较大）；

接下来我们来看一下 ai-website-cloner-template 内部是如何处理的。

## 二 核心实现

### 2.1 核心原理

![138c7c494a76e62e4047bcf0308ab52a.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/0a37fd2a27cb48b8a45cd9e608168e20~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=vNK8JJEggu1nrYB8uXn8Kzkd%2Bfo%3D)

ai-website-cloner-template 原理可以分为四个部分：

**Phase 1：摸底（Reconnaissance）**

拿到目标 URL 后，第一件事是搞清楚"它到底长啥样、怎么动"。

- **截图**：用 Playwright 启一个真浏览器，在三个标准视口（1440×900、768×1024、390×844）下分别截全页图和首屏图。为什么要三个视口？因为响应式断点不是猜的，是要验证的。
- **抓 design tokens**：在浏览器里跑 JS，遍历页面上所有 DOM 节点，调用 getComputedStyle() 把每个节点的字体、字号、颜色、背景、圆角、间距全部聚合去重。这不是抄 CSS 源码，而是读最终生效的计算值——能穿透 @apply、CSS 变量、媒体查询。
- **交互扫描**：静态截图只能看到"现在长啥样"，但 tab 切换会换内容，滚动可能改 header 样式，hover 可能让卡片变色。所以还要模拟滚动到不同位置、点击 tab、鼠标悬停，把每个交互态都抓一份。
- **产出**：一堆截图 + 一堆 JSON（tokens.json、assets.json、topology.json 等），全在 docs/research/ 和 docs/design-references/ 下。

我们来看一下：

![05b16ab2b73f8287c4b3a9cdf0498ce8.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c800affac85f4afaad18fa9f5a84e7a7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=hiUFtovDqSuO0MWfpuzwWHlNAgQ%3D)

![c2d06a90278674467aabd50efeaf39a3.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/9cbbe60ac8014647a1ef327e55c8f57d~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=eXvKt6kQeGdEORhIAtsHyzxggwU%3D)

![215ca30db1f8b3a7d8a605ac1caf930b.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c8bcd5f61ef94430a3a8a8f194423308~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=fG2SZlbiIBiraG9fQMXtHSQxrS8%3D)

**Phase 2：搭骨架（Foundation）**

摸完底，开始铺地基。这一步必须先做完，后续所有组件才能开工。

- **design tokens 落地**：把 Phase 1 抓出来的颜色、字号映射到 Tailwind v4 的 @theme 块和:root CSS 变量。这样后面写组件时，bg-primary、text-muted-foreground 这些 class 直接可用，不用每次查色值。
- **字体策略**：根据目标站的字体族决定怎么加载。如果目标站用 Google Fonts，直接走 next/font/google；如果像掘金这种纯系统字体（PingFang SC、Microsoft YaHei），就退回到 system font stack，省掉外网请求。
- **图标去重**：目标站页面里可能有三四十个 SVG 节点，但很多是重复的。用脚本去重后只剩十几个唯一的，把它们整理成 React 组件放到 icons.tsx。
- **资源下载**：把页面里的所有图片、logo、favicon 用脚本批量下载到 public/images/ 和 public/seo/，按用途分目录。下载不了的占位图，用基于 id 的 hash 渐变色块顶替（每个 id 颜色唯一，视觉上合理）。
- **产出**：globals.css 配好、icons.tsx 配好、public/images/ 配好。

**Phase 3：组件生成（Spec & Build）**

这是流水线最关键的阶段，也是最能体现"规约驱动"思想的地方。

- **写 spec 文件**：先不为每个 section 写代码，而是先写一份 markdown 格式的规约文档（\*.spec.md）。这份文档是 builder agent 的施工合同，里面写清楚：
	1. 目标组件长啥样（截图路径）
	2. 像素级别的样式（字号 17px、padding 12px 20px 0px、颜色 #252933，全是从 getComputedStyle 拿的真实值，不是"差不多"）
	3. 真实的内容数据（标题、作者、缩略图，全是从目标 DOM 抓的真实文本，不是 Lorem Ipsum）
	4. 交互模型（hover 会怎样、点击会怎样、有没有滚动驱动）
- **复杂度预算**：单份 spec 不能超过 150 行。掘金首页 12 个 section 就拆 12 份 spec，分别派给 12 个 builder agent 干。拆得越细，单个 agent 任务越聚焦，质量越高。
- **worktree 并发**：每个 builder agent 在独立的 git worktree 分支上工作，互不冲突。干完后由 orchestrator 逐个 merge 进 main，每次 merge 立刻跑一次 npm run check（lint + typecheck + build）。这就是 "Build Must Always Compile" 原则——main 分支永远保持可构建状态。
- **产出**：每个 section 一个 React 组件文件 + 它对应的 spec 文件。

![121af4ffe5e688769d4854a5fd094b78.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/8574b6c30956406daaa1c0c6631dc328~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=dCBtYPOPnFCrgKow2EB8cHYsliU%3D)

**Phase 4：拼装与 QA（Assembly & QA）**

所有组件都写完了，现在要拼成完整页面，并验证它跟目标站是否真的像。

- **拼装**：page.tsx 按 z-index 和断点把所有组件组合起来。比如 header 是 sticky top（z-index: 250），移动端的浮动下载按钮要 position: fixed（z-index: 100），不能挡住 header 但要能盖住 footer。
- **视觉 QA**：用脚本同时截三个视口下的"目标站"和"我们做的"，生成 target-*.png 和 clone-*.png，并排对比。优先级：
	1. 尺寸差异（最容易暴露——宽高、padding、gap）
	2. 颜色差异（肉眼最敏感——背景、文字、边框）
	3. 布局差异（flex 方向、grid 列数、sticky 是否失效）

在实现过程中，核心的逻辑就是要真实的获取浏览器里面的页面状态，Playwright 起到了核心作用。

### 2.2 Playwright 介绍

先看一下 Playwright 是什么？

> Playwright 是一个由 Microsoft 开源的、用于端到端测试和浏览器自动化的库。它让你用代码控制真实的浏览器（Chrome、Firefox、Safari），自动完成点击、填写、截图、读取页面内容等操作。

比如我们想在 Node 环境唤起浏览器，那么可以直接调用对应的 API:

```js
js 代码解读复制代码// 1. 启动浏览器
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true });
```

还可以创建一个独立的隐身窗口：

```js
js 代码解读复制代码// 2. 新建一个 context（独立隐身窗口）                                                                                                                 
const context = await browser.newContext();
```

操作浏览器，本质上我们可以借助这个能力去完成 e2e 等自动化测试验证：

```js
js 代码解读复制代码// 点击
await page.click('button#submit');  
// 导航跳转
await page.goto('https://example.com');
```

还可以截图用来获取效果：

```js
js 代码解读复制代码await page.screenshot({ path: 'screenshot.png' });
```

感兴趣的同学可以研究一下，这里是总结的一些 API 能力：

![1bbe988dbfe40bc21918c37a106a3d51.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7781ea6ef65c4bc087767683fc4157a1~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=0wbcJ%2FUlI%2BrYUyNaCn2KFueEVYY%3D)

## 三 具体实现思路

介绍完核心原理，我们挑一些重点场景，来看一下核心实现：

**多视口截图：**

```typescript
typescript 代码解读复制代码const viewports = [
  { name: "desktop-1440", width: 1440, height: 900 },
  { name: "tablet-768", width: 768, height: 1024 },
  { name: "mobile-390", width: 390, height: 844 },
];

for (const vp of viewports) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    locale: "zh-CN",
    userAgent: "Mozilla/5.0 ... Chrome/131.0.0.0 ...",
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
  await page.waitForTimeout(2500); // 等 hydration
  await page.screenshot({ path: \`${outDir}/${vp.name}-full.png\`, fullPage: true });
  await ctx.close();
}
```

跨三个标准视口各截一张 fullPage 图，注意 `waitUntil: "networkidle"` 后还要再等 2.5 秒 —— juejin 用了大量懒加载图片和 IntersectionObserver，networkidle 不等于"完全稳定"。

**样式还原：提取全局样式 tokens：**

`page.evaluate()` 跑一段 JS，遍历所有 DOM 节点调用 `getComputedStyle()`：

```typescript
typescript 代码解读复制代码const tokens = await page.evaluate(() => {
  const all = document.querySelectorAll("*");
  const fonts = new Set(), sizes = new Set(), colors = new Set();
  for (const el of all) {
    const s = getComputedStyle(el);
    fonts.add(s.fontFamily);
    sizes.add(s.fontSize);
    if (s.color !== "rgba(0, 0, 0, 0)") colors.add(s.color);
  }
  return { fonts: [...fonts], sizes: [...sizes].sort(), colors: [...colors] };
});
```

juejin 的真实 token 抓出来后是这个样子的：

```
text 代码解读复制代码主色蓝:  rgb(30, 128, 255)  →  #1e80ff
页面底:  rgb(242, 243, 245) →  #f2f3f5
卡片底:  rgb(255, 255, 255) →  #ffffff
正文:    rgb(37, 41, 51)    →  #252933
次要文字:  rgb(81, 87, 103)   →  #515767
三级文字:  rgb(134, 144, 156) →  #86909c
边框:    rgb(228, 230, 235) →  #e4e6eb
危险红:  rgb(246, 66, 66)   →  #f64242
字体族:  PingFang SC, Microsoft YaHei, Helvetica Neue
```

**强制性交互扫描：**

这一步是 **整个 skill 的精华**。静态截图只能看见"现在长什么样"，但站点是"活"的：tab 切换会换内容、滚动会让 header 变样式、hover 会让卡片换底色。

以 juejin 为例做一遍完整 sweep：

```typescript
typescript 代码解读复制代码// 滚动 sweep：截不同 scrollY 下的 header 样式
for (const y of [0, 300, 600, 900, 1200, 1500, 1800, 2094]) {
  await page.evaluate((sy) => window.scrollTo({ top: sy, behavior: "instant" }), y);
  await page.waitForTimeout(400);
  const data = await page.evaluate(() => {
    const header = document.querySelector("header");
    return {
      scrollY: window.scrollY,
      headerBg: header ? getComputedStyle(header).backgroundColor : null,
      headerShadow: header ? getComputedStyle(header).boxShadow : null,
    };
  });
  scrollSnapshots.push(data);
}

// 点击 sweep：点"最新" tab 看内容是否变化
const tabClick = await page.evaluate(() => {
  const target = [...document.querySelectorAll("a, button, div, span")].find(
    (el) => el.textContent?.trim() === "最新" && el.children.length === 0
  );
  if (!target) return { ok: false };
  target.click();
  return { ok: true };
});
await page.waitForTimeout(1500);
const latestContent = await page.evaluate(() => {
  return document.querySelectorAll(".entry").length; // 真实数据：1 张卡
});
```

实测发现 juejin 的"最新" tab 切换后 **文章数从 16 降到 1**，说明这不是纯 UI 切换，是真实重新拉数据。克隆时用 `useState` 切两份静态 mock，但生产部署需要后端 API 配合。

**页面拓扑映射：**

把所有 section 列出来，标注交互模型：

```
text 代码解读复制代码1. Header       — 静态 (无 scroll 变化)
2. LeftSidebar  — 点击 (导航)
3. ArticleList  — 点击 (tab 切换)
4. ArticleCard  — hover (subtle bg)
5. CtaBanner    — 静态
6. RightRail    — 静态 (刷新按钮 mock)
7. Footer       — 静态
8. MobileAppPill — 静态 (position: fixed)
```

这一步的产出是 `PAGE_TOPOLOGY.md`，作为后续 spec 文件的索引。

![d2413f24dfb89d57ada3b56c89939dbe.png](https://p9-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/bcd98b88b1c742368747a058a9a0b6d1~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5oiR5LiN5piv5aSW5pif5Lq6:q75.awebp?rk3s=f64ab15b&x-expires=1792272189&x-signature=ET2O8s%2BliQDgOw%2BpubaMQ7TF5Qo%3D)

如上就是 Phase 1 部分，后面两个部分会对样式，资源，以及生成组件的规范 spec 进行系统化处理，这里就不过多介绍了。我们看一下 Phase 4 部分是如何做视觉 Diff 的。

QA 脚本遍历三个视口分别截 target 和 clone：

```typescript
typescript 代码解读复制代码for (const vp of viewports) {
  const ourCtx = await browser.newContext({ viewport: vp });
  const ourPage = await ourCtx.newPage();
  await ourPage.goto("http://localhost:3010/", { waitUntil: "networkidle" });
  await ourPage.screenshot({ path: \`clone-${vp.name}-full.png\`, fullPage: true });

  const targetCtx = await browser.newContext({ viewport: vp });
  const targetPage = await targetCtx.newPage();
  await targetPage.goto("https://juejin.cn/", { waitUntil: "networkidle" });
  await targetPage.screenshot({ path: \`target-${vp.name}-full.png\`, fullPage: true });
}
```

对比找差异的优先级：

1. **尺寸差异**：宽高、padding、gap（最容易暴露）
2. **颜色差异**：背景、文字、边框（肉眼最敏感）
3. **布局差异**：flex 方向、grid 列数、sticky 失效

juejin 实战中 mobile 一次性暴露了 3 个差异（tag wrap、author truncate、button-in-anchor），desktop/tablet 一次通过。

## 四 总结

ai-website-cloner-template 的真正价值，不在于"能复制网站"——这本身就是 DevTools 的本职工作。它把一次看似简单的"截图+抄代码"，重构成了一条 **可复用、可验证、可并发的工程流水线**：先 Reconnaissance 抓计算值、再 Foundation 搭骨架、再用 Spec & Build 的规约驱动多 Agent 并行生成、最后 Assembly & QA 做多视口视觉回归。 **先写 spec、再写代码** 这个顺序的颠倒，是从"AI 玩具"迈向"AI 工程"的分水岭。

建议大家 clone 一份到本地，挑一个欣赏的站点跑一遍，亲身感受"规约驱动 + 多 Agent 并行"的真实体感。 **先动手的人，先看到未来**。感谢阅读，我们下篇见。希望的朋友可以点赞 + 收藏，支持更新 AI 场景的“奇思妙想”。