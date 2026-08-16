---
id: "613313196"
title: "Chromium浏览器的定制开发"
author: "stevevista"
type: zhihu-article
source: "https://zhuanlan.zhihu.com/p/613313196"
created: "2023-03-12 12:11"
updated: "2023-03-12 12:11"
collected: "2023-03-12 12:11"
downloaded: "2026-08-16"
---
## chromium代码膨大但不复杂

近期需要做一个基于浏览器的功能，也就是在浏览器里额外增加一些功能，浏览器本身的功能尽量保留。想着浏览器本身代码庞大，不想去碰，尝试取巧用electron去实现，这样连c++代码都不用去碰了。但开发了一部分后，总是有些小细节无法实现，于是只有去electron和chromium代码库找线索，结果发现我原来的想法是错的，错在两点：

1.  electron 并不是完全基于我们理解中的chromium浏览器，浏览器本身的一些特性（src/chrome目录下），并不包含在编译里。
2.  chromium 结构非常清晰，可读性，可修改性都很强，编译环境也是自封闭的，编译几乎不会碰到幺蛾子。

当然，说不复杂是相对的，但我要扩充的功能几乎不会触及v8, blink，其他的模块，只要抓住大的架构，要修改哪里也是很清楚的。

在此，我对定制过程中的一些问题做一些记录，但不提供具体的细节，以本文里的关键字搜索代码，结合代码也很容易理解，这得益于chromium代码本身的可读性。

本文介绍如何为 Chromium 浏览器添加或修改一些功能，但不涉及如何删除一些功能。删除功能听起来似乎比添加要简单，其实删除更困难一些，首先，Chromium代码虽然整体上模块划分清晰，但目前内部还是有很多相互耦合的，这些耦合也许从编译上并体现不出来，因为模块间可能是以 IPC方式相互联系的，并不是编译耦合。另外，代码的很多宏控制并不十分精确。很多时候，你觉得成功删除了一些模块，运行起来好像也没问题，但是要完整进行测试是非常庞大的工作，你不知道哪些情况下会有问题。

得益于Chromium代码的良好工程架构，添加功能则要轻松得多。

## Chromium 代码的获取和编译

具体的编译方式参考官方文档，以Windows 为例

[Chromium Docs - Checking out and Building Chromium for Windows (googlesource.com)](https://link.zhihu.com/?target=https%3A//chromium.googlesource.com/chromium/src/%2B/main/docs/windows_build_instructions.md)

本文不再赘述，但建议编译器用clang （已经在third\_party里了）, 不要用MSVC，这样可能遇到编译问题的概率更小。

## Chromium的概念和模块结构

Chromium的架构本文不赘述，可以参考官方文档 \[src/docs\] 和网络上的分析文章，最重要的是了解进程架构，这对理解代码结构非常关键。

代码目录里，简要的说，content 目录提供最主要的浏览器接口，而 chrome则是在 content 接口之上的 Chrome浏览器定制，我们实现一个定制浏览器，应该是删掉 chrome目录，而实现一个和 chrome 类似的模块，electron 就是这么做的。

但本文里我们不这么做，chrome代码里不是简单的封装，大量的浏览器功能实际是在chrome里实现的，比如，chrome://host 相关的页面。

chromium有main进程和renderer进程，大多数情况下，这两个进程的代码也是分开的，一个进程中的代码，意味着在另一个进程里也有对应的部分，这两部分通过ipc联系，接口形式可能是 idl，json 等定义的。

## 非侵入式修改

我们希望修改是非侵入式的，这样更利于代码合并。升级合并是必然的，不管你用的哪个标签的代码，我敢保证，里面肯定有Bug, 某些Bug 可能在后面又修复了，你可能会希望合并这些修复。

但要完全非侵入几乎不可能，那就要借助 patch 等工具来管理定制代码，但还是尽量减少对chromium的修改。

## 定制代码的组织

我们尽量将我们的定制代码组织在一起，包括代码，资源，脚本等，如，我们在 chromium/src目录下新建一个目录 customize。

Chromium采用 GN 构建系统，我们在 customize 目录新建一个 BUILD.gn, 这样，我们在chromium里添加进我们的customize构建依赖会比较清晰，比如

```text
deps += [“//customize”]
```

在customize目录里，要怎么编译，则比较自由，我们几乎可以加入任何需要构建的东西，比如 webpack, nodejs

### 编译参数

Chromium的编译参数是比较多的，再加上我们定制的参数，管理起来也是比较麻烦的，所以我们在 customize目录里加入编译配置，比如

```text
customize/build/args/release.gn
customize/build/args/debug.gn
customize/build/args/other_config.gn
```

命令行我们则可以简单输入

gn gen out/release\_110\_x64 --args="import(\\"//customize/build/args/release.gn\\") target\_cpu=\\"x64\\""

## webui 定制

我们定制的功能可能是需要有界面的，在Chromium里，当然是以Web的形式呈现，就像你打开 chrome://settings 看到的页面

如何开发 Webui, 在 \[src/docs\] 里有几篇文档都有介绍

```text
src\docs\webui_in_components.md
src\docs\webui_in_chrome.md
```

但要注意，这些文档可能落后于代码，有些API可能已经变更或废弃，如果碰到问题，建议参考 chrome里的 webui实现。\[chrome/browser/ui/webui\]。

另外，以chromium里的webui实现为线索，探索chromium的架构也是很好的路径，比如 src/chrom/browser/ui/webui/settings 和 src/chrom/browser/resources/settings, 是 chrome://settings 的实现。

## 修改 Chromium 的命令行参数

Chromium的很多功能是可以通过命令行参数控制的，比如，取消sandbox, 命令行参数增加 –no-sandbox

在Chromium的代码里，有很多点可以修改 command line，比如，在 ChromeMain(…) 函数里，这是一个比较早的时机，在这个函数里你会发现很多 SetUpCommandLine 的调用，这是很多模块在这个时机点进行 command line 检查或修改，我们也可以在这里添加我们的修改，为了结构清晰，我们实现一个函数

```cpp
customize:: SetUpCommandLine(base::CommandLine*) {
  cmd_line->AppendSwitch(sandbox::policy::switches::kNoSandbox)
}
```

在 ChromeMain函数里加上我们的 customize:: SetUpCommandLine(cmd\_line);

```text
void ChromeMain(...) {
  ...
  customize:: SetUpCommandLine(cmd_line);
}
```

以 –no-sandbox为例，我们可能希望更精细的控制，而不是所有的功能取消sandbox，那么我们应该将修改时机点放到其他地方。

Chromium是多进程架构，在新的进程启动前，都有机会修改 command line, 比如 renderer 进程， gpu 进程，plugin进程，不同类型的进程的启动入口不同，比如 PPAPI进程的入口在函数 PpapiPluginProcessHost::Init

## 添加设置项

如果我们希望定制功能里添加一些设置项， 就如我们在Chrome的设置页面看到的一样，设置项在Chromium里是统一接口管理的，各模块通过接口注册自己的设置项，我们的定制模块当然也一样

我们在customize模块里实现 customize:: RegisterProfilePrefs(user\_prefs::PrefRegistrySyncable\* registry)

然后在 chrome\\browser\\prefs\\[http://browser\_prefs.cc](https://link.zhihu.com/?target=http%3A//browser_prefs.cc)

RegisterProfilePrefs() 里添加上我们的调用

```cpp
 customize:: RegisterProfilePrefs(registry);
```

如果需要使设置项变成响应式，则要用到类 PrefChangeRegistrar ，来注册参数变化的回调

```cpp
PrefChangeRegistrar pref_change_registrar；
pref_change_registrar.Init(prefs_service);
pref_change_registrar.Add(“key”, callback);
```

## 资源打包

对于我们定制模块所需的资源，不要像 webui 文档里指导的那样放在 components 或 chrome 脚本里，这样管理起来比较混乱，不利于代码合并，而是要在 customize目录里建独立脚本。

  

## 哪些功能不建议定制

建议定制的功能要兼容规范

比如假设我们要实现一个更强功能的播放器，不建议添加一个新的 HTMLElement 类，比如 <my-video>

而是对<video> 的功能进行兼容扩充，比如增加编码类型支持，增强Control Bar等

## Native Plugin的问题

随着对Flash的不再支持，Chromium 已经开始取消对所有第三方 Native Plugins的支持，本来这是一个比较轻松的非侵入式功能扩充的方式。

但是Chromium内部ppapi支持还是在的，只是不再允许通过命令行注册，我们可以在函数 ChromeContentClient::AddPlugins(...) 里手动注册所需的Plugins。很多时候，把定制功能实现在Plugin里是更容易和安全的。

## extension api

Chromium 的Extension API 还是比较方便和安全调用的，避免写 c++代码，但是这些 API默认 是没有曝露到一般Web UI里的，需要在 下面文件里配置，这样才有可能在你的定制webui里调用到

```text
src\chrome\common\extensions\api\_api_features.json 
src\extensions\common\api\_api_features.json
```