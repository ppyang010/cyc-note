[不用框架，手搓 AI Agent：(一) 先让它跑起来给 AI Agent 去个魅！核心公式：大模型（大脑）+ Harn - 掘金](https://juejin.cn/post/7661531893103935539) 

 > 🚀 **插播一条**：欢迎来到 **[不用框架，手搓 AI Agent](https://juejin.cn/column/7661531339729829926 "https://juejin.cn/column/7661531339729829926")** 👈 专栏！这是咱们的第一站。

> 别被 Agent 这个词绕晕了，它的核心其实就两部分。
> 
> 我们平时使用的 **Cursor、Trae、Claude Code、Codex**，本质上都属于 AI Agent。 很多人第一次接触 Agent，会觉得它特别神秘，好像背后藏着一套非常复杂、深不可测的技术。 但如果给 AI Agent“去个魅”，它其实可以简化成一个非常直观的公式：
> 
> **AI Agent = 大模型（大脑）+ Harness（缰绳）**
> 
> 大模型负责思考，Harness 负责让它真正把事情做好。

### `先来“放个毒”，看看经过本系列的打磨，我们最终会亲手搞出一个怎样的“完全体”`

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/7d60aab406204deaac6090027f939d77~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=J9p2elvdH4a9WKl6yYum9BNTKTY%3D)

如上图所示，它将拥有类似claudecode的终端交互、能感知你当前的工作目录，还能自主决定如何帮你完成研发任务。

**是不是感觉很酷？**

但这些能力并不是模型天生就有的。模型本身只负责理解需求、思考下一步；至于如何进入你的工作目录、调用终端、读写文件、执行命令，并在失败后继续尝试，靠的是另一套运行机制。

这套机制，就是 Harness。

Harness 到底是什么？
--------------

Harness 直译过来是“马具”或者“缰绳”。

放在 AI 工程里，这个比喻其实非常形象。

*   **大模型就像一匹能力很强的马**：动力十足、创意丰富，但有时候也比较“冲动”。如果没有约束，它写代码时可能会乱用依赖、执行危险命令，甚至产生幻觉，然后一本正经地胡说八道。
*   **Harness 就像套在马身上的缰绳**：它负责约束和引导大模型，把模型的想法转化成一个个可执行的工程步骤，确保它既能跑起来，也不至于跑偏。

### 举个最简单的例子。

当你对 Claude Code 或 Codex 说：帮我修复这个项目里的登录 Bug。

背后的大模型并不能凭空读取你的代码，也不能直接修改文件。

真正让它拥有这些能力的，是 Harness 为它提供的：

*   读取文件
*   搜索代码
*   修改代码
*   执行命令
*   检查运行结果
*   限制危险操作
*   在失败后继续调整方案

所以，只有大模型还不够。

没有 Harness 的大模型，更像是一个会聊天、会出主意的“大脑”；接上 Harness 之后，它才能真正读代码、改文件、执行命令，成为一个可以帮我们完成任务的 AI Agent。

大模型决定它能不能想明白，Harness 决定它能不能把事情做好。

而这个系列要做的事情，就是和你一起从零开始，亲手打磨出这样一套 Harness“缰绳”系统。

今天的目标：先让它跑起来
------------

罗马不是一天建成的。我们把复杂的高级能力先放一边，任何一个强大的 AI Agent，都有一个极其朴素的起点。

**本系列的第一篇，我们就来亲手敲下它的第一行核心代码，调通这条最基础的“一问一答”最短链路：** 

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/c61cad7b6f4148619a3d337ef6ee63d9~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=J%2FI9HTqKTMVJXKIfztnZgiXPRWc%3D)

我们今天第一步要实现的“最小可用版本”跑起来长这样：

```bash
$ npm run start -- -prompt "用一句话解释什么是 TypeScript"

AI：TypeScript 是 JavaScript 的超集，为 JavaScript 添加了静态类型能力。

```

> 注意：它现在还只是“会聊天的命令行助手”，还不会读文件、改代码。但这正是后面实现 AI 编程 Agent 的地基。
> 
> 🚀 **本节配套源码：[powercode](https://link.juejin.cn/?target=https%3A%2F%2Fgithub.com%2FTeernage%2Fpowercode "https://github.com/Teernage/powercode")** 👈点它
> 
> 如果中途遇到问题，可以对照源码排查。后续章节的代码也会持续更新，如果这个项目对你有帮助，欢迎点个 Star ⭐

* * *

一、准备环境
------

*   **Node.js21 或 更高版本**
*   **npm**
*   **一个 OpenAI 兼容的 API Key**：这是通向各大模型的“万能通行证”。无论你用 DeepSeek、GLM 还是 Kimi，它们都遵循这套行业通用协议。拿到它，就等于拿到了所有主流模型的“入场券”。

先检查 Node.js 版本：

```bash
node -v

```

如果版本低于 `v21`，建议先升级。

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/649c0772b7fc44c290ba6673e16e3fec~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=aicRU1zR%2BsWqI%2FK1M46DlrIO7%2Fo%3D)

二、新建一个独立项目
----------

新建一个文件夹powercode

```bash
mkdir powercode
cd powercode
npm init -y

```

安装依赖：

```bash
npm install openai 
npm install -D typescript @types/node

```

现在项目目录大致是：

```bash
powercode/
├── node_modules/
├── package.json
└── package-lock.json

```

* * *

三、配置 TypeScript
---------------

新建 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*.ts"]
}

```

然后修改 `package.json`，将它调整为：

```json
{
  "name": "powercode",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsc",
    "start": "node dist/main.js"
  },
  "dependencies": {
    "openai": "^6.0.0"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.0.0"
  }
}

```

**划重点**：注意这里添加了 `"type": "module"`，这是为了让我们能在 Node.js 中直接使用现代的 `import` 语法，而不是老式的 `require`。

四、配置你的大模型
---------

在项目根目录新建 `provider.json`：

```json
{
  "protocol": "openai",
  "baseURL": "https://api.deepseek.com",
  "apiKey": "替换成你的 API Key",
  "model": "deepseek-v4-flash"
}

```

如果你使用别的兼容 OpenAI 接口的服务，**`protocol` 保持不变，你只需要改下面这三个字段**：

*   `baseURL`：接口地址
*   `apiKey`：你的密钥
*   `model`：模型名称

> ⚠️ **警告**：`provider.json` 包含私人密钥，**绝对不要**提交到 Git！

所以我们在根目录新建 `.gitignore` 文件：

新建 `.gitignore`：

```gitignore
node_modules
dist
provider.json

```

> 💡 **科普小知识**
> 
> 你可能会好奇：市面上有几百种大模型，难道我们要学几百种调用方法吗？ 其实不用。目前业界的 API 调用基本上被两大“普通话”统一了：**OpenAI 协议** 和 **Claude 协议**。尤其是 OpenAI 协议，国内的绝大多数主流模型（比如 DeepSeek、glm、通义千问、Kimi、豆包等）都完美兼容了它。
> 
> 所以，**只要你学会了 OpenAI 的接入方式，稍微改一下 `baseURL` 和 `apiKey`，就能无缝切换到几乎任何国产模型**。这就是为什么我们在配置里只写这三个字段的原因。

* * *

五、先写一个读取配置的模块
-------------

在powercode下创建src源码目录：

新建 `powercode/src/config.ts`：

```ts
import { readFile } from "node:fs/promises";


 * 提供商配置接口
 * 定义与 AI 提供商通信所需的配置参数
 */
export interface ProviderConfig {
  baseURL: string;   
  apiKey: string;   
  model: string;    
}


 * 加载并验证提供商配置
 *
 * @returns Promise<ProviderConfig> 完整的提供商配置对象
 * @throws 当 provider.json 缺失或必需字段不完整时抛出错误
 * @example
 * ```ts
 * const config = await loadConfig();
 * // 使用配置初始化 AI 客户端
 * ```  
 */
export async function loadConfig(): Promise<ProviderConfig> {
  const content = await readFile("provider.json", "utf8");
  const config = JSON.parse(content) as Partial<ProviderConfig>;

  if (!config.baseURL || !config.apiKey || !config.model) {
    throw new Error(
      "provider.json 配置不完整，需要提供 baseURL、apiKey 和 model。",
    );
  }

  return {
    baseURL: config.baseURL,
    apiKey: config.apiKey,
    model: config.model,
  };
}

```

它告诉 TypeScript：配置对象必须包含这三个字符串字段。

**说白了，这就相当于你给 AI 拨打电话必需的“三件套”：** 

*   `baseURL` 是区号；
*   `apiKey` 是你的专属通讯证；
*   `model` 是你要找的哪位接线员。

准备好这三样，下一步我们就能真正向大模型发请求、让它干活了。

* * *

六、封装一次大模型请求
-----------

新建 `src/chat.ts`：

```ts
import OpenAI from "openai";
import type { ProviderConfig } from "./config.js";

export class ChatClient {
  private readonly client: OpenAI; 

  
   * 初始化 ChatClient 实例
   *
   * @param config 提供商配置对象
   */
  constructor(private readonly config: ProviderConfig) {
    this.client = new OpenAI({
      apiKey: config.apiKey,
      baseURL: config.baseURL,
    });
  }
  
  
   * 向 AI 模型发送问题并获取回答
   *
   * @param prompt 用户的问题或指令
   * @returns 模型回答的内容
   */
  async ask(prompt: string): Promise<string> {
    const response = await this.client.chat.completions.create({
      model: this.config.model,
      messages: [
        {
          role: "system",
          content: "你是power-code,一个由驾驭工程驱动的骨灰级研发助手,请使用中文回答。",
        },
        {
          role: "user",
          content: prompt,
        },
      ],
    });

    return response.choices[0]?.message.content ?? "模型没有返回内容。";
  }
}

```

先用大白话解释这段代码。

`OpenAI` 是官方 SDK 提供的客户端。即使你接入的不是 OpenAI，只要接入的模型服务兼容 OpenAI 的接口格式，通常也能这样调用

```ts
this.client = new OpenAI({
  apiKey: config.apiKey,
  baseURL: config.baseURL,
});

```

真正发请求的核心是：

```ts
this.client.chat.completions.create(...)

```

我们把对话内容放进 `messages` 数组：

```json
messages: [
  {
    role: "system",
    content: "你是power-code,一个由驾驭工程驱动的骨灰级研发助手，请使用中文回答。",
  },
  {
    role: "user",
    content: prompt,
  },
]

```

其中：

*   `system`：给 AI 定规则，例如让它用中文、保持某种身份。
*   `user`：用户真正提出的问题。
*   `assistant`：AI 历史回答的位置，后续实现多轮对话时会用到。

目前我们只有一问一答，所以只需要 `system` 和 `user`。

* * *

七、写命令行入口
--------

新建 `src/main.ts`：

```ts
import { ChatClient } from "./chat.js";
import { loadConfig } from "./config.js";


 * 从命令行参数中提取用户问题
 *
 * @param args 命令行参数数组
 * @returns 用户的问题或指令
 * @throws 当 -prompt 参数缺失或后面为空时抛出错误
 */
function getPrompt(args: string[]): string {
  const promptIndex = args.indexOf("-prompt");

  if (promptIndex === -1) {
    throw new Error('请通过 -prompt 传入问题，例如：-prompt "你好"');
  }

  const prompt = args[promptIndex + 1];

  if (!prompt) {
    throw new Error("-prompt 后面不能是空内容。");
  }

  return prompt;
}


 * 主函数，处理命令行参数并调用 ChatClient 发送问题
 */
async function main() {
  const prompt = getPrompt(process.argv.slice(2));
  const config = await loadConfig();
  const client = new ChatClient(config);

  console.log("AI 正在思考...\n");

  const answer = await client.ask(prompt);

  console.log(`AI：${answer}`);
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`启动失败：${message}`);
  process.exit(1);
});

```

这里的关键是 Node.js 提供的一个内置数组：`process.argv`。它会把我们在命令行敲下的每一段文字收集起来。

当我们执行这行命令时：

```ts
npm run start -- prompt "你好"

```

> 💡 **小提示**：中间的 `--` 是为了告诉 npm：“后面的参数请原封不动地传给我的代码，不要你自己处理掉。” 程序内部收到的完整的 `process.argv` 数组，其实长这样：

```ts
[
  "/usr/local/bin/node",       
  "/你的项目路径/dist/main.js", 
  "-prompt",                   
  "你好"                       
]

```

你看，前两项都是系统自带的路径信息，对我们没有任何用处。

所以，我们要用 `.slice(2)` 像切蛋糕一样，把前面那两项切掉，只保留从第 2 项开始的真实参数：

```ts
["-prompt", "你好"]

```

拿到这个干净的数组后，`getPrompt` 函数的工作就非常傻瓜化了：去数组里找 `-prompt` 在哪个位置，然后把紧跟在它后面的那句话（也就是 `"你好"`）提取出来，这就是用户真正要问 AI 的问题。

* * *

八、编译并运行
-------

一切准备就绪，现在我们要把 TS 代码转化为 Node.js 可执行的 JS 代码，并让 Agent 跑起来。

### 1\. 编译代码

执行构建指令，将 `src` 下的 TypeScript 代码编译至 `dist` 目录：

如果没有报错，项目中会多出一个 `dist` 目录：

```ts
powercode/
├── dist/
│   ├── chat.js
│   ├── config.js
│   └── main.js
└── src/
    ├── chat.ts
    ├── config.ts
    └── main.ts

```

### 2\. 让 Agent 跑起来

接下来，调用我们的系统，并传入你的第一个指令：

```bash
npm run start -- -prompt "用一句话解释什么是 TypeScript"

```

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/48ffe3559afd429b9dc8d336be2f9613~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=C7CPGogl3bLNwaL%2FFcL7QTy%2Bas8%3D)

恭喜，你已经写出了第一个命令行 AI 助手。

* * *

九、我们刚刚到底完成了什么？
--------------

把整件事画成一条数据流，就是：

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/f803f4d2309a42b39b964f72be0571d5~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=Wq3tQJOFnYQCOqqrvhR76ykfbls%3D)

目前的项目结构也非常简单：

```bash
powercode/
├── src/
│   ├── config.ts    
│   ├── chat.ts      
│   └── main.ts      
├── provider.json    
├── .gitignore
├── package.json
└── tsconfig.json

```

每个文件只有一个职责：

*   `config.ts` 不关心如何请求模型；
*   `chat.ts` 不关心命令行参数怎么解析；
*   `main.ts` 只负责把它们串起来。

这种拆分方式会在后面越来越重要。因为当我们加入读文件、修改代码、执行命令等能力后，项目不会轻易变成一团乱麻。

* * *

十一、这算 AI Agent 吗？
-----------------

严格来说，还不算。

现在的程序只有：

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/222ab2f845fd4ea2983559b3e0ab69f4~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=AFEi20yb8EqI5gNcDe0DVB10%2BVQ%3D)

而一个真正能帮我们完成编程任务的 Agent，至少还要具备：

![](https://p3-xtjj-sign.byteimg.com/tos-cn-i-73owjymdk6/d2c633938e2a44dd9e524af2ad71b7f7~tplv-73owjymdk6-jj-mark-v1:0:0:0:0:5o6Y6YeR5oqA5pyv56S-5Yy6IEAg5LiN5LiA5qC355qE5bCR5bm0Xw==:q75.awebp?rk3s=f64ab15b&x-expires=1785244938&x-signature=pL3p%2BCbkAdK75VS4nXtbxDV%2FXl8%3D)

这也是下一篇要解决的问题。

下一篇，我们会给这个助手发一个“工具箱”，让 AI 不只是回答问题，而是能够主动请求读取项目里的文件。到那一步，它才真正开始具备 Agent 的味道。