---
id: "1916774397"
title: "如何评价 mimalloc？"
author: "李杭帆"
type: zhihu-answer
source: "https://www.zhihu.com/question/330717205/answer/1916774397"
created: "2021-06-01 12:07"
updated: "2021-06-01 12:07"
collected: "2021-06-01 12:07"
downloaded: "2026-08-16"
---
微软的宣传水平实在是烂。

![](images/641_001.png)

这 mimalloc 可是好东西啊。除了性能好以外，构建，使用都很方便。启用 override 特性后，在 Windows 平台只要加载上 mimalloc-override.dll（包括但不限于 LoadLibrary，给导入表加条目，通过别的 DLL 加载），就能可靠地覆写链接 Universal C Runtime（UCRT）应用的 malloc，基本上无需重新编译原程序。

一般会选 jemalloc 的，不一定是看中它的性能。jemalloc 毕竟有这么多奇奇怪怪的选项和功能。jemalloc 的缺点有：

-   Windows 平台上性能差。
-   第五版 bug 修复前，不支持动态加载。一大类用到应用程序 VM/脚本引擎的软件都长期用不了。（后添加 --disable-initial-exec-tls 构建选项。）
-   虽然有比较多的调优空间，但调起来麻烦，很难发挥最佳性能。

相比之下，mimalloc 就很贴心。CMake 构建，轻轻松松。默认配置就很优化了。Windows 和 Unix-like 平台上性能都很好。mimalloc 也有弱项：

-   0.5 MiB ~ 十数 MiB 的分配在 Linux 平台对比 jemalloc 不占优势。这是 IO buffer 可能用到的尺寸。

*tcmalloc 放弃跨平台，既没有吸引人的特性，性能上也不是最佳的。除了 Google 广告做得好，粉丝多，可真就没什么了，不提也罢。（你们可以猜猜 Chromium 的 tcmalloc 实质上多久没更新了。）*

吐槽一下常见的语言自带 malloc。

glibc 的 malloc 的问题在于：

-   系统负载高时，资源若在线程间迁移，free 的性能很差。（对应用程序 VM/脚本引擎中的非系统线程亲和的托管线程/轻量线程/绿色线程很不友好。）
-   内存消耗多。（倾向于增长，而不是搜索可用区间。碎片化较严重。）

严格说来，Linux 的进程在系统层面上没有「堆」这一概念的。很多代码假设通过 malloc 共用一个堆，这有时会是个坑点。

UCRT 的 malloc（其实就是 Windows API HeapAlloc 包装了一层）的缺点：

-   进程默认堆上内存承担较多功能，分配速度慢。（和理想状态下 glibc 的 malloc 比，速度只有六成左右。）

除了比较节约内存，其他方面真的乏善可陈。

mimalloc 可以说改善了上面的这些问题。当然，它算是后起之秀，吸取了前人的教训。说不上有多创新，但细节上做得比较好。Codebase 规模小（现在增长到 8k LoC 了），也很容易迁移到新平台。现在可以说是大流行。没用过的话，一定要试试。

*未来甚至有可能复兴一波 non-compacting GC。*

## 示例

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using UltimateOrb.Unmanaged;

namespace ThisAssembly {

    public unsafe static class Program {

        public static void Main() {

            Thread.CurrentThread.Priority = ThreadPriority.Highest;
            Console.Out.WriteLine($@"{nameof(DefaultAlloctorImpl.UseMiMalloc)}: {DefaultAlloctorImpl.UseMiMalloc}");
            Console.Out.WriteLine($@"{nameof(DefaultAlloctorImpl.UseJeMalloc)}: {DefaultAlloctorImpl.UseJeMalloc}");
            Console.Out.WriteLine();

            // Thread.BeginThreadAffinity();
            try {
                var sw = new Stopwatch();
                sw.Restart();
                DoWork();
                sw.Stop();
                Console.Out.WriteLine($@"Elapsed time: {sw.Elapsed}");
                Console.Out.WriteLine();
                sw.Restart();
                DoWork();
                sw.Stop();
                Console.Out.WriteLine($@"Elapsed time: {sw.Elapsed}");
                Console.Out.WriteLine();
            } finally {
                // Thread.EndThreadAffinity();
            }
            Console.Out.WriteLine("Done.");
            return;
        }

        static readonly Ptr<char> sabcde = (char*)Marshal.StringToHGlobalUni("abcde");
        static readonly Ptr<char> sabc = (char*)Marshal.StringToHGlobalUni("abc");
        static readonly Ptr<char> s4444 = (char*)Marshal.StringToHGlobalUni("4444");
        static readonly Ptr<char> s7777777 = (char*)Marshal.StringToHGlobalUni("7777777");
        static readonly Ptr<char> s999999999 = (char*)Marshal.StringToHGlobalUni("999999999");
        static readonly Ptr<char> s22 = (char*)Marshal.StringToHGlobalUni("22");
        static readonly Ptr<char> s1 = (char*)Marshal.StringToHGlobalUni("1");
        static readonly Ptr<char> s333 = (char*)Marshal.StringToHGlobalUni("333");
        static readonly HashSet<Ptr<char>> stringPool = new() {
            sabcde,
            sabc,
            s4444,
            s7777777,
            s999999999,
            s22,
            s1,
            s333
        };

        private static void DoWork() {
            GC.Collect();
            if (GC.TryStartNoGCRegion(1 * 1024 * 1024, true)) {
                try {
                    var ws = Environment.WorkingSet;
                    var tcb = GC.GetGCMemoryInfo().TotalCommittedBytes;

                    for (var i = 0; 2000000 > i; ++i) {
                        static void DestructValue(ref Ptr<char> begin) {
                            if (stringPool.Contains(begin)) {
                                return;
                            }
                            Alloctor.DefaultFree((nint)begin.Value);
                            begin = null;
                        }
                        AvlTree.Tree<long, Ptr<char>>.DestructValue = &DestructValue;

                        AvlTree.Tree<long, Ptr<char>> tree = default;

                        static int Compare(in long first, in long second) {
                            return first.CompareTo(second);
                        }
                        tree.Compare = &Compare;

                        tree.Insert(9, sabcde);
                        tree.Insert(4, s4444);
                        tree.Insert(3, sabc);
                        tree.Insert(7, s7777777);
                        tree.Insert(9, s999999999);
                        tree.Remove(3);
                        tree.Insert(2, s22);
                        tree.Insert(1, s1);
                        tree.Insert(3, s333);

                        static Ptr<char> ToStringCStyle(long value) {
                            var size = 65;
                            var buffer = (Ptr<char>)Alloctor.DefaultAlloc((uint)size * sizeof(char)).ToPointer();
                            if (value.TryFormat(new Span<char>(buffer, size), out var c)) {
                                if (c < size) {
                                    buffer[c] = '\0';
                                }
                                return buffer;
                            }
                            throw new FormatException();
                        }
                        tree.Insert(-42, ToStringCStyle(i));
                        // tree.Insert(-42, (char*)Marshal.StringToHGlobalUni($"{i}"));

                        if (i % 900000 == 11) {
                            static void Print(in long key, in Ptr<char> value) {
                                var t = new ReadOnlySpan<char>(value, int.MaxValue);
                                var n = t.IndexOf('\0');
                                t = t[..n];
                                Console.Out.WriteLine(t);
                            }
                            tree.Foreach(&Print);
                            Console.Out.WriteLine();
                        }
                        tree.Clear();
                    }

                    Console.Out.WriteLine("Managed memory total committed bytes delta: ");
                    Console.Out.WriteLine($@"    {GC.GetGCMemoryInfo().TotalCommittedBytes - tcb}");
                    Console.Out.WriteLine("Process working set bytes delta: ");
                    Console.Out.WriteLine($@"    {Environment.WorkingSet - ws}");
                } finally {
                    GC.EndNoGCRegion();
                }
            }
        }
    }
}
```

Allocator

```csharp
    unsafe static class DefaultAlloctorImpl {

        internal static readonly bool PlatformIsWindows = Environment.OSVersion.Platform == PlatformID.Win32NT;
        internal static readonly bool PlatformIsUnix = Environment.OSVersion.Platform == PlatformID.Unix;
        internal static readonly bool UseMiMalloc = /*false && */Internal.MiMalloc.IsImported;
        internal static readonly bool UseJeMalloc = !UseMiMalloc && Internal.JeMalloc.IsImported;

        public static readonly delegate* managed<nuint, IntPtr> Alloc = GetAlloc();

        static delegate*<nuint, IntPtr> GetAlloc() {
            return UseMiMalloc ? &MiMallocAlloctor.Alloc : UseJeMalloc ? &JeMallocAlloctor.Alloc : PlatformIsWindows ? &WindowsHeapAlloctor.Alloc : PlatformIsUnix ? &LibCAlloctor.Alloc : &MarshalHGlobalAlloctor.Alloc;
        }

        public static readonly delegate* managed<IntPtr, void> Free = GetFree();

        static delegate*<IntPtr, void> GetFree() {
            return UseMiMalloc ? &MiMallocAlloctor.Free : UseJeMalloc ? &JeMallocAlloctor.Free : PlatformIsWindows ? &WindowsHeapAlloctor.Free : PlatformIsUnix ? &LibCAlloctor.Free : &MarshalHGlobalAlloctor.Free;
        }
    }
```

输出

```text
UseMiMalloc: True
UseJeMalloc: False

11
1
22
333
4444
7777777
999999999

900011
1
22
333
4444
7777777
999999999

1800011
1
22
333
4444
7777777
999999999

Managed memory total committed bytes delta:
    0
Process working set bytes delta:
    757760
Elapsed time: 00:00:00.7539620

11
1
22
333
4444
7777777
999999999

900011
1
22
333
4444
7777777
999999999

1800011
1
22
333
4444
7777777
999999999

Managed memory total committed bytes delta:
    0
Process working set bytes delta:
    139264
Elapsed time: 00:00:00.7067218

Done.
```

同硬件。Windows 大概要 0.71 秒。Linux 上大概要 0.72 秒。

而 jemalloc 在 Windows 大概要 1.16 秒。Linux 上大概要 0.76 秒。

HeapAlloc（Windows） 大概要 1.44 秒。glibc（Linux） 大概要 0.77 秒。

其中，最节约内存的是 HeapAlloc。最浪费内存的是 glibc。

mimalloc 在 Linux 平台一般略优于 jemalloc，在 Windows 平台**完胜**。

## 结论

如果 malloc 仅作为动态内存分配的解决方案，不需要进程堆的概念（老旧的 COM 应用可能有错误的假设），内存也不是特别紧张的情况，在 Windows 上请务必用 mimalloc 把 UCRT 的 malloc 换掉。Windows 上只推荐 mimalloc。Linux 上，在有精力调优的情况下，数据库/网络等有机会大量反复申请/释放较大的 IO buffer 的库/应用可考虑用 jemalloc，一般情况也是建议用 mimalloc。