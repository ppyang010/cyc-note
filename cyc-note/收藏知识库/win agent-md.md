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