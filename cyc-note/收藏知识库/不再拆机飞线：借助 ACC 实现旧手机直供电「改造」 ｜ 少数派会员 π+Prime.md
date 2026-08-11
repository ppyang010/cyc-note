去年4月，我在某视频的影响下，萌生了将家里的旧安卓手机利用起来的想法。后续虽然跑起来了，但因为设备需要长期充电，电池安全又成了一个让我困扰的难题。为了解决这个问题，我在《彻底告别电池焦虑：旧手机再利用 ...

去年 4 月，我在某视频的影响下，萌生了将家里的旧安卓手机利用起来的想法。后续虽然跑起来了，但因为设备需要长期充电，电池安全又成了一个让我困扰的难题。

为了解决这个问题，我在[《彻底告别电池焦虑：旧手机再利用的直供电改造》](https://sspai.com/post/98174)一文中，把手机电池整个移除，然后通过飞线的方式，让充电器直接给主板供电，实现所谓的「直供电」或「旁路供电」。

当时的改造确实一劳永逸地解决了电池鼓包的问题（毕竟电池都被移除了😂），但代价是主板裸露、走线外接，手机的物理结构也被彻底破坏了。以至于我每次在家里看到它的时候，都会担心这种粗暴的改造方式会不会带来新的安全隐患，也总忍不住在心里琢磨：

> 有没有一种不用拆机、也能达成同样直供电效果的方式？

于是，我开始在网上搜寻，几番搜索之后，我惊奇地发现我以前用过的一个工具 [Advanced Charging Controller](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2FVR-25%2Facc)（以下简称 ACC）就能满足我的「直供电」需求。

说来惭愧，之前我在使用 ACC 时，纯粹是照着网上的教程依葫芦画瓢，从没真正深入探究它的功能。而这一次，我决定沉下心来先搞懂它的原理，再完成对旧手机的直供电「改造」。

关于 ACC
------

多年的折腾经验教会我，想用好一个新工具，得先通读一遍「说明书」，尽量做到「知其所以然」，是避免弯路的最佳途径。

所幸，在该项目的 [GitHub 主页](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2FVR-25%2Facc)上作者对它的运作原理做了详细的说明，让我不必大费周章地去他处查找。通过阅读，我得以了解到 ACC 是通过读写系统底层的充电参数，来接管手机硬件原本的充电行为，进而实现对充电的精准控制。

简而言之，如果说原生系统的充电逻辑是「傻瓜式」——插上充电器就开始充电，充满了就停——那装上 ACC 就相当于给手机系统加装了一个「充电开关」。我们可以自由设置手机的充电过程（例如电量降到 40% 就启动充电，升到 60% 就自动停止等），甚至可以更进一步让电流绕过电池直接为主板供电。这也正是我想要实现的「直供电」模式。

安装 ACC 及相关工具
------------

在对 ACC 有了基本的了解之后，接下来就是将它安装到手机中，并配置好相关工具。其中第一步是获得手机系统的 root 权限。

受限于文章篇幅，且 root 的方式往往会因手机品牌、型号的差异而不同，所以这一步我建议参考极客湾的视频：《[玩机必看！带你入坑安卓刷机，小白也能看懂的 ROOT 基础指南来啦！](https://www.bilibili.com/video/BV1BY4y1H7Mc)》来进行操作。我也是参考着视频一步步操作之后，成功获得了手里这台小米 Note 3 的 root 权限，并顺利安装上了 Magisk（它是一个 root 后，能让手机安全安装各种功能模块的框架）。

Magisk 安装完成后就可以开始安装 ACC 模块了：

1.  进入项目的 [Releases](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2FVR-25%2Facc%2Freleases) 页面；
2.  下载最新的 `.zip` 文件；
3.  将文件传输到手机内；
4.  打开手机中的 Magisk，依次点击「模块」->「从本地安装」；
5.  找到已经传输到手机中的 `.zip` 文件，等待安装完成；
6.  重启手机。

![](https://cdnfile.sspai.com/2026/08/04/f2475eaf100313876bbe7677f86cb6bd.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

重启后 ACC 模块默认会随着 Magisk 的启动自动在后台运行。需要注意的是，由于它本身是一个纯后台服务，因此主屏幕上不会出现任何启动图标。如果你偏好图形化界面，可以考虑单独安装 [ACCA](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2FMatteCarra%2FAccA) 或 [ACC Settings](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2FCrazyBoyFeng%2FAccSettings) 这两个第三方客户端。不过由于二者均已停止维护，对新版 ACC 的兼容性较弱，因此强烈推荐直接使用命令行工具 Termux 来设置 ACC。

Termux 的安装过程与安装其它 APK 无异，同样在项目的 [Releases](https://sspai.com/link?target=https%3A%2F%2Fgithub.com%2Ftermux%2Ftermux-app%2Freleases) 页面下载对应型号的 `.apk` 包即可。

![](https://cdnfile.sspai.com/2026/08/04/acd61198ec79b21541f8f670580fc201.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

Termux 安装完成后就可以通过它来执行命令来设置 ACC 了。不过在此之前，建议先执行一次`pkg update && pkg upgrade -y`命令，确保软件源与依赖都是最新的（此步骤为可选操作，非必要）。

![](https://cdnfile.sspai.com/2026/08/04/0a07b3468556d47b074290d80a2528e3.jpg?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

如果过程中提示更新失败，大概率是因为国内网络直连受限，通常将软件源切换至国内镜像即可解决。具体操作如下：

*   执行：`termux-change-repo`，系统会打开一个交互选单，将光标停在 `Mirror groupRotate` 上，按回车；

![](https://cdnfile.sspai.com/2026/07/30/771456d3131c307f5ec0807bd9f4b095.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

*   选择 `Mirrors in chinese`，确认。之后 Termux 会自动将软件源切换为国内镜像；

![](https://cdnfile.sspai.com/2026/07/30/4cb419a71cf3a739a68a578cd6fea36d.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

*   再次执行：`pkg update && pkg upgrade -y`，一般即可顺利完成更新。

至此，准备工作全部完成。接下来就正式进入 ACC 模块的参数配置环节了。

配置 ACC
------

接着回到 Termux 终端，继续以下操作：

*   执行 `su`，获取 Root 权限；
*   执行 `acc -v`，查看当前 ACC 版本；

![](https://cdnfile.sspai.com/2026/07/30/ddfbb12e55078d839e70e9fe78109428.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

*   执行 `acc -u dev`，确保 ACC 版本为最新。

![](https://cdnfile.sspai.com/2026/07/30/7bfeeea98849afeae0be5e6a4ba4bd29.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

将手机插上充电线，确保手机是充电状态，在 Termux 中运行测试命令：

运行该命令后，ACC 会自动开始测试可以适配手机的充电开关（测试时间有点长，请耐心等待）。测试完成后，除了会在当前终端窗口中显示结果外，还会在 `sdcard/Download` 目录下自动生成一份 `.log` 文件。

![](https://cdnfile.sspai.com/2026/07/30/8b7eab80fcc7fa87b1d8d77a83791a4e.png?imageView2/2/w/1120/q/90/interlace/1/ignore-error/1/format/webp)

⚠️注意，为保证测试结果的可靠性，请尽可能使用原装充电头及数据线。

### 如何选择合适的充电开关

许多人可能会和我一样，初次看到测试结果的时候脑袋完全是发懵的：这么长的结果哪些是可用的？我该怎么选择？

其实这里我们任意选择一个测试结果最后两行显示如下的开关即可：

```null
Switch works ✅
battIdleMode=true
```

但若是你想更深入地了解这份测试报告背后的含义，就不得不了解一下`acc -t`这条命令背后的运作原理了：

Android 手机的充电控制本质上依赖一个基本逻辑：系统向充电控制器发送「开始充电」或「停止充电」的指令。但由于安卓生态的高度碎片化，不同的设备制造商（OEM）、不同的芯片组（SoC）、不同的 Android 版本的「充电控制」指令各不相同，所以并不存在一条能「通杀」所有机型的统一指令。

那怎么办呢？ACC 的解决方案是内置了一个作者从大量设备中收集而来的充电控制参数列表，而`acc -t`这个命令，就是用来逐一验证列表中开关是否有效的命令。测试过程与结果会完整记录在测试报告中，以下面我测试出的这段为例：

```null
6/33: battery/constant_charge_current_max 3300000 0
  off (0)        -6mA        Idle
  on (3300000)        -6mA        Idle
  on (3300000)        -866mA        Charging
  Switch works ✅
  battIdleMode=true
```

首行显示的是充电开关的参数说明：

*   6/33：它是当前测试的第 6 个开关，共 33 个；
*   battery/constant\_charge\_current\_max：是开关的路径或名称；
*   3300000 0：是开启和关闭这个开关的控制指令（数值）。

第二行是第一次的测试结果：

*   off (0)：充电开关成功关闭（执行关闭指令 0）；
*   \-6mA：此时进入电池的电流很小，接近无充电状态；
*   Idle：系统判定电池处于空闲或直供状态。

第三行是第二次的测试结果：

*   on (3300000)：充电开关成功开启（执行开启指令 3300000）；
*   \-6mA：此时电流仍未明显上升；
*   「Idle」系统依然判定电池是空闲状态；

在第四行中，ACC 再次尝试向系统发送开启充电开关的指令。此时，后两个结果出现了变化：

*   \-866mA：进入电池的电流显著增加；
*   Charging：系统确认电池已恢复充电状态。

基于这个变化，ACC 在第五行给出 `Switch works ✅` 的结论。并在第六行认为该开关支持 `battIdleMode=true`（即支持直供电/电池空闲模式）。

由于测试报告里可用的充电开关往往不止一个，例如在我的结果中，除了上面例子中的开关外，还有以下两个开关同样支持直供电：

```null
7/33: battery/constant_charge_current_max 3300000 10000
  off (10000)        -6mA        Idle
  on (3300000)        -897mA        Charging
  Switch works ✅
  battIdleMode=true
```

```null
17/33: main/constant_charge_current_max 3300000 0
  off (0)        -687mA        Charging
  off (0)        -5mA        Idle
  on (3300000)        -900mA        Charging
  Switch works ✅
  battIdleMode=true
```

通常来讲这三个开关我只需任选其一即可，但如果想在其中找到「最佳」的开关，就需要通过上述方法，观察测试结果中开关与电池的状态变化来做出选择了。

### 指定充电开关

了解了哪些充电开关是可用的后，下一步就是让 ACC 通过该开关来控制手机的充放电了，为此，需要先指定 ACC 使用的充电开关。例如我想使用`battery/constant_charge_current_max 3300000 0`这个开关，则需要在 Termux 中执行：

```null
acc -s s="battery/constant_charge_current_max 3300000 0 --"
```

如果想确认是否设置成功，可以输入 `acc -s` 查看当前设置，在列表中确认`charging_switch`项已正确显示为目标开关。

之后，就是「告诉」ACC 在怎样的条件下让系统启用和关闭充电，一般此处有两种设置思路。

#### 通过电量百分比控制

该思路的运作逻辑是充电到预设的百分比时停止充电，进入直供电模式；在电量低于预设的百分比时，退出直供电，恢复充电。

假如我想将充电上限设置为 50%，下限为 40%，需要输入的命令为：

如果想要确认自己是否设置成功，同样可以通过 `acc -s` 核对设置，关键参数应如下所示：