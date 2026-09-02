来源：[(99+ 封私信 / 56 条消息) 首页 - 知乎](https://www.zhihu.com/)

## 摘录内容 
独立发现windows powershell （也就是5.1）默认编码不是utf-8，大模型总是要读两遍后，手动升级到了powershell （7.6）

真是娇气啊

附上当前的AGENT.md

```text
# 个人全局配置

## 关于我
- I am a hardware architecture engineer.
- My main work involves AI accelerators, SoC, RTL, Verilog, SystemC, and computer architecture.

## 回答偏好
- 回复使用中文
- 遇到有多种实现方案时，列出选项让我选择，而不是直接选一种
- 回答保持精简
- 写python代码时，关键模块或者函数都加上中文的docstring或者注释，以方便阅读

## 安全习惯
- 修改认证相关代码前主动提示我注意安全影响

## 默认的python解释器
使用miniconda环境中的python解释器，路径如下：
- D:\500software\miniconda\envs\mywork\python.exe

## 需要转换PDF到markdown文件时
优先使用 pymupdf4llm 

## 环境
- OS: Windows
- 终端请优先使用 PowerShell 7
- 如果有些时候外网连不上去，你可以先尝试使用镜像之类的，如果不行，也可以使用一个本地的代理端口：http://127.0.0.1:7890
```
## 想法



```text
## Windows Shell

- 在 Windows 环境中，所有 PowerShell 命令必须使用 PowerShell 7（`pwsh`）。
- 禁止使用旧版 Windows PowerShell（`powershell.exe`）。
- 首次执行命令前，使用以下命令确认版本：
  `pwsh -NoLogo -NoProfile -Command '$PSVersionTable | Select-Object PSVersion, PSEdition'`
- 验证结果必须满足：
  - `PSEdition` 为 `Core`
  - `PSVersion.Major` 大于或等于 `7`
- 当前 Shell 已经是 PowerShell 7 时，直接执行 PowerShell 命令，不要再次嵌套 `pwsh -Command`。
- 从其他 Shell 调用 PowerShell 时，使用：
  `pwsh -NoLogo -NoProfile -NonInteractive -Command "..."`
- 对包含变量、多行逻辑或复杂引号的命令，优先写入临时 `.ps1` 文件，再通过：
  `pwsh -NoLogo -NoProfile -NonInteractive -File <script.ps1>`
  执行，避免多层引号和变量提前展开。
- PowerShell 脚本使用 UTF-8 编码，不依赖 Windows PowerShell 5.1 专属行为。
```


2222
在本站别人那抄来的适用于 codex 的 [AGENTS.md](http://agents.md/) ，自己略微改了一下，其它 agent 改改也能用：  
  
```  
## Windows 约束  
**当前环境是 Windows 10 / pwsh7**  
- 默认禁止使用 Bash 语法，除非确定此 shell 处在 Linux 环境  
- 不要使用 Bash 引号/转义习惯，在 PowerShell 命令里，复杂正则优先用单引号包裹。  
- 如果正则本身同时包含单引号和双引号，优先拆成多个简单 rg 命令。  
- 执行多行 Python 禁止使用 Bash heredoc ；改用 PowerShell here-string | python -  
- pwsh 中，语句块表达式（如 `foreach`、`if`）不能直接作为管道输入。 需要先使用 `$()` / `@()` 包裹，或先赋值给变量。 普通命令输出可直接进入管道，无需额外包裹。  
- PowerShell 使用 `rg` 时，通配目录必须先用 `Get-ChildItem -Filter` 展开为真实路径，禁止直接把含 `*` 的搜索路径传给 `rg`。  
```




凑活用吧。安装 PowerShell7 和 RG 。 然后全局 [AGENTS.MD](http://agents.md/) 里加入以下内容  
  
```  
## Windows 与命令执行  
  
- Windows 环境使用当前 PowerShell 7 ；不得调用 `powershell.exe`（当前机器会降级到 Windows PowerShell 5.1 ）。除非任务明确要求，不嵌套调用 `pwsh.exe`、`cmd.exe`、Git Bash 、WSL 或其他 shell 。  
- 确需启动独立 PowerShell 7 进程时，使用 `pwsh.exe -NoLogo -NoProfile`，避免加载用户 profile 注入额外命令与配置。  
- 直接使用 PowerShell 语法；避免 Unix 命令及 `cat`、`find`、`where` 等含义不明确的别名或同名程序。  
- PowerShell 字符串和正则在无需变量展开时使用单引号；需要展开时使用双引号，相邻字符有歧义时写 `${name}`。双引号字符串内使用反引号而非反斜杠转义。  
- 多行文本使用 PowerShell here-string ，不使用 Bash heredoc （`<<EOF`）。  
- 将 `foreach`、`if` 等语句块的输出接入管道时，使用 `& { ... } | ...` 包裹，不直接在 `}` 后接 `|`。  
- 命令失败时先检查命令、路径、引号及退出码，不随意切换 shell 。  
  
## 检索  
  
- 文本检索优先使用 `rg`，文件枚举优先使用 `rg --files`，按文件名查找使用 `rg --files | rg`。  
- 不把含 `*` 的路径直接作为 `rg` 的 PATH 参数；文件类型筛选使用 `-g`，目录通配先用 `Get-ChildItem -Directory -Path` 展开为 `FullName` 后再传给 `rg`。  
- `rg` 不可用时，使用 PowerShell 的 `Get-ChildItem` 和 `Select-String`；如需安装工具，先征求用户同意。  
- `rg` 退出码 `1` 表示没有匹配结果，不视为执行错误。