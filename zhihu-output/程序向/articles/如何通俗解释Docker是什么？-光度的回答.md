---
id: "2488146755"
title: "如何通俗解释Docker是什么？"
author: "光度"
type: zhihu-answer
source: "https://www.zhihu.com/question/28300645/answer/2488146755"
created: "2022-05-16 17:09"
updated: "2023-09-21 14:11"
collected: "2022-05-16 17:09"
downloaded: "2026-08-16"
---
这个问题是15年提出的，扫了下至今（2022.05）的所有回答都在解释docker**是什么**与**怎么用**，那我这个回答就来补充上**docker大体上是怎么实现的**，用100行C/C++把思路捋一下。懒得看文字的可以直接戳代码：

[GitHub - Kirhhoff/mini-docker: illustrate what docker really is in 100 line C/C++](https://link.zhihu.com/?target=https%3A//github.com/Kirhhoff/mini-docker)

* * *

首先声明，我这个回答只是一份搬运，实现完全参考2018年的GOTO Conference：

[Containers From Scratch • Liz Rice • GOTO 2018](https://link.zhihu.com/?target=https%3A//www.youtube.com/watch%3Fapp%3Ddesktop%26v%3D8fi7uSYlOdc%26feature%3Dyoutu.be)

这个视频仅以数十行Go实现了一个UTS、pid、filesystem隔离的“迷你docker”，并能限制资源的使用。关于cgroup的部分我个人不是很感兴趣，所以转述为C/C++的时候只实现了前半部分。

好，如果你能够接受：

-   英文字幕/无字幕
-   Go描述的实现
-   视频而非文字

**我建议你直接去看原视频，不要听我转述**

如果你：

-   嫌英文麻烦
-   对Go反感，但能看懂C/C++
-   懒得看视频

那继续

* * *

### 一点关于**docker是什么、相比其他VM区别、有什么用**的介绍，不感兴趣的跳过即可

最常听到的说法，“docker是一种轻量级、进程级VM”，但这种描述并不能完全解答疑惑，用专业术语去解释专业术语也像没说：所谓的“轻量级、进程级VM”又tm是什么？

如果对普通的VM是怎样也没什么概念，那“docker是一种xx的VM”就更没有意义了，因为根本没有参考的标准。

比如linux的kvm[^1]，他能够借助硬件的帮助以相对（软件方法）较低的开销实现同指令集（x86）上的全虚拟化。翻译成人话，就是你可以在x86\_linux（host OS）上起一个新的x86\_linux（guest OS）虚拟机，完全与host独立的操作系统，而且这个操作系统本身不知道虚拟化的存在。当guest OS来到某些执行边界需要host OS介入时，会发生异常trap到host OS里，有kvm处理，再恢复guest OS执行。这个“会发生异常trap到host OS里”就需要硬件的支持，比如Intel VT或者AMD-V；而“同指令集”（在这里就是x86了）是说，你不能借助kvm来实现在x86上跑一个arm\_linux的操作系统，只能虚拟出x86\_linux。

再比如qemu-system[^2]的虚拟化，好吧这其实是emulation，就可以做到cross-architecture的VM，你可以在x86上面随便跑mips或者risc-v的独立OS，但这是软件实现的，具体来说是动态二进制翻译（DBT[^3], Dynamic Binary Translation），所以跟kvm这种性能完全没法比，不过如果你是在x86上虚拟x86，qemu也可以借助kvm来加速。

### 那么docker与上面这些相比如何？

首先docker并不会运行一个独立的操作系统，而只是给进程提供了一种假象，使进程运行得就好像在一个独立的操作系统上。这也是为什么docker被称为进程级、轻量级的VM：他根本不需要另起一个操作系统。

问题来了，没有独立的操作系统，那还能起到VM的作用吗？

这个问题可以反过来想：真的有必要隔离出一个完整的操作系统吗？

并不。很多时候其实我们只是想减轻运维的负担：为程序提供一个统一的“运行环境”。这所谓的“运行环境”，具体来说是系统库、运行时、第三方库等等的文件。如果我们仅仅想保持文件环境的一致，只需要提供一份独立的磁盘镜像即可，并不需要替换操作系统。

当然，一个程序也不只是看到文件，他还看到当前所有进程、网络端口使用等等的一系列系统信息，我们要同时能够隔离这些系统信息，保证每个进程都看到、以为自己是独立运行的。

所有这些，其实都不至于非得另起一个操作系统，因为内核本身就提供一些基础设施（namespace、cgroup等）来达到这一效果，这也是docker得以实现的基础。

**【打个广告】对docker不熟悉可以考虑跟下深蓝学院的docker课，比较务实，注重理论和实践，课程内容也比较实用：**

[Docker 容器技术基础入门- 深蓝学院- 专注人工智能与自动驾驶的学习平台](https://link.zhihu.com/?target=https%3A//www.shenlanxueyuan.com/page/234)

* * *

## 从一个“复读机”开始

我们从实现一个“复读机”开始，也即把我们传递给它的命令直接执行，而不提供任何的隔离功能，这个程序的名字就叫`mocker`吧（笑。

借助`execv`一族的函数，这一点可以很容易实现：把命令中的参数丢给`execv`函数即可。我们模仿`docker run` 来实现一个`mocker run` （略去头文件与一些声明）：

```cpp
int main(int argc, char **argv) {

    if (argc < 3) {
        cerr << "Too few arguments" << endl;
        exit(-1);
    }

    if (!strcmp(argv[1], "run")) {
        run(argc - 2, &argv[2]);
    }
}

static void run(int argc, char **argv) {
    cout << "Running " << cmd(argc, argv) << endl;    

    execvp(argv[0], argv); 
}

static string cmd(int argc, char **argv) {
    string cmd = "";
    for (int i = 0; i < argc; i++) {
        cmd.append(argv[i] + string(" "));
    }
    return cmd;
}
```

可以简单运行个`ls`：

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ ./mocker run ls -l
Running ls -l
total 28
-rw-rw-r-- 1 user user    46 May 13 15:04 Makefile
-rw-rw-r-- 1 user user   767 May 13 15:18 main.cc
-rwxrwxr-x 1 user user 18856 May 13 15:18 mocker
```

可以运行个`bash`，对比父子进程的pid：

```bash
user@linux:~/mini-docker$ ps
  PID TTY          TIME CMD
  513 pts/0    00:00:00 bash
 1302 pts/0    00:00:00 ps
user@linux:~/mini-docker$ ./mocker run /bin/bash
Running /bin/bash
user@linux:~/mini-docker$ ps
  PID TTY          TIME CMD
  513 pts/0    00:00:00 bash
 1303 pts/0    00:00:00 bash
 1309 pts/0    00:00:00 ps
user@linux:~/mini-docker$ exit
exit
user@linux:~/mini-docker$ ps
  PID TTY          TIME CMD
  513 pts/0    00:00:00 bash
 1310 pts/0    00:00:00 ps
```

为了不让`bash`覆盖掉`mocker`父进程，我们修改`run`，多加一个`fork`，将`execv`放到子进程中：

```cpp
static void run(int argc, char **argv) {
    cout << "Running " << cmd(argc, argv) << endl;

    pid_t child_pid = fork();

    if (child_pid < 0) {
        cerr << "Fail to fork" << endl;
        return;
    }

    if (child_pid) {
        if(waitpid(child_pid, NULL, 0) < 0) {
            cerr << "Fail to wait for child" << endl;
        } else {
            cout << "Child terminated" << endl;
        }
    } else {
        run_child(argc, argv);
    }
}

static void run_child(int argc, char **argv) {
    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

得到的输出与先前是类似的：

```bash
user@linux:~/mini-docker$ ps
  PID TTY          TIME CMD
  513 pts/0    00:00:00 bash
 1740 pts/0    00:00:00 ps
user@linux:~/mini-docker$ ./mocker run /bin/bash
Running /bin/bash
user@linux:~/mini-docker$ ps
  PID TTY          TIME CMD
  513 pts/0    00:00:00 bash
 1741 pts/0    00:00:00 mocker
 1742 pts/0    00:00:00 bash
 1748 pts/0    00:00:00 ps
user@linux:~/mini-docker$ exit
exit
Child terminated
```

不过在这里我们会看到子进程的`ps` 相较之前多显示了一个`mocker`进程，这是因为我们把`bash`的执行放到了`fork`后的子进程中，而父进程的`mocker`也就得以保留下来，等待子进程的退出，借助`ps`可以看到进程关系：

```bash
user@linux:~/Documents/mini-docker$ ps axjf | grep pts
   2452    2463    2463    2463 pts/0       5646 Ss    1000   0:00  |   \_ bash
   2463    4436    4436    2463 pts/0       5646 S     1000   0:00  |       \_ ./mocker run /bin/bash
   4436    4437    4437    2463 pts/0       5646 S     1000   0:00  |           \_ /bin/bash
   4437    5646    5646    2463 pts/0       5646 R+    1000   0:00  |               \_ ps axjf
   4437    5647    5646    2463 pts/0       5646 S+    1000   0:00  |               \_ grep --color=auto pts
```

## UTS namespace

接下来，我们实现对UTS的隔离。这里的所谓UTS起到的作用是，显示主机名（hostname）。比如我们可以在host中看到自己的hostname：

```bash
user@linux:~$ hostname
linux
```

同样，在我们的container中也可以看到hostname：

```bash
user@linux:~/mini-docker$ ./mocker run /bin/bash
Running /bin/bash
user@linux:~/mini-docker$ hostname
linux
user@linux:~/mini-docker$ exit
exit
Child terminated
```

如果我们在container中修改了hostname，那么在host中我们也会察觉到这一修改：

```bash
user@linux:~/mini-docker$ hostname
linux
user@linux:~/mini-docker$ ./mocker run /bin/bash
Running /bin/bash
user@linux:~/mini-docker$ sudo hostname container
user@linux:~/mini-docker$ hostname
container
user@linux:~/mini-docker$ exit
exit
Child terminated
user@linux:~/mini-docker$ hostname
container
user@linux:~/mini-docker$ ./mocker run /bin/bash
Running /bin/bash
user@container:~/mini-docker$ 
```

hostname的改动不会立马在`@` 后展现出来，但当我们再起一个子进程`bash` 时，hostname就已被替换为先前container修改的值了。

我们当然不希望container中的行为影响到host，那接下来我们借助namespace技术隔离UTS。从代码的角度我们只要对子进程部分略微改动：

```cpp
static void run_child(int argc, char **argv) {
    int flags = CLONE_NEWUTS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

我们稍后再解释这是在做什么，先看看这点改动是否奏效：

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ hostname
linux
user@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Running /bin/bash
root@linux:/home/user/mini-docker# hostname container
root@linux:/home/user/mini-docker# hostname
container
root@linux:/home/user/mini-docker# exit
exit
Child terminated
user@linux:~/mini-docker$ hostname
linux
```

child对hostname的修改，没有影响到host，我们实现了对UTS的隔离（用特权级是出于`unshare`调用的要求）。为了方便区分子进程的hostname，也为了让这个程序看起来正式一些，我们在启动container（也就是我们的这个子进程）的时候自动修改hostname，使之在终端上展现出来：

```cpp
const char *child_hostname = "container";

static void run_child(int argc, char **argv) {
    int flags = CLONE_NEWUTS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (sethostname(child_hostname, strlen(child_hostname)) < 0) {
        cerr << "Fail to change hostname" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

看起来还真像那么回事，对吧？

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ hostname
linux
user@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Running /bin/bash
root@container:/home/user/mini-docker# hostname
container
root@container:/home/user/mini-docker# exit
exit
Child terminated
user@linux:~/mini-docker$ hostname
linux
```

### Linux kernel namespace

现在我们回过头来看看这个`unshare`，这所谓的namespace是干嘛的。

类比于C++的namespace，内核中的namespace技术也是为了限制“你能看到什么”。namespace也有不同的类别[^4]，从mount到pid再到网络等等，uts也是其中之一。不同的namespace类别负责限制进程在“某一方面”都能看到什么。根据不同的需求，这个“某一方面”可以是主机名（比如上面我们隔离的hostname），也可以是挂载或者pid等等。

最直观也是最早引入内核的是mount namespace[^5]，用于实现挂载方面的隔离。把不同进程放在不同的mount namespace中，这样一来你在一个mount namespace中进行的挂载操作，其他mount namespace中的进程看不到，以此实现挂载方面的隔离。

系统启动时，会创建一个global initial mount namespace，所有进程都在其中[^5]。当某个进程主动要求创建一个新的mount namespace时，它和它的子进程就都会放到这个新的mount namespace中，实现隔离，同时可以想象到，这些不同的mount namespace之间也会像进程的父子层级关系一样，形成自己的层级关系并由kernel负责维护。

具体到实现上，每个mount namespace都会由一个`mnt_namespace`[^6]kernel object负责维护，当我们在进行诸如`open`等涉及pathname resolution的syscall时，会经过当前进程对应的`mnt_namepace` “翻译”，得到这个进程最终看到的pathname对应的`inode`。当发生`unshare`[^7]时，根据传入的flag，不同的namespace（mount、pid、uts等等）实例被创建/拷贝，并修改当前进程的指向，实现不同namespace间对system resource view的隔离。

类似mount，UTS namespace则是隔离了不同进程的hostname view，这样一来我们修改了container的UTS namespace中的主机名时，host进程namespace中的主机名就不会受到影响了。

## PID namespace

接下来我们试着隔离pid namespace。

上面我们在container中执行`ps`时可以看到container的pid是从host侧pid增长得来的。比如我们可以在程序中打印：

```cpp
static void run(int argc, char **argv) {
    cout << "Parent running " << cmd(argc, argv) << " as " << getpid() << endl;    

    pid_t child_pid = fork();

    ...
}

static void run_child(int argc, char **argv) {
    cout << "Child running " << cmd(argc, argv) << " as " << getpid() << endl;    

    int flags = CLONE_NEWUTS;

    ...
}
```

运行结果：

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Parent running /bin/bash as 10929
Child running /bin/bash as 10930
root@container:/home/user/mini-docker# 
```

然而我们希望container获得一个全新的pid空间，如此一来我们的container的pid应该是1。为了实现这一点，我们仍借助`unshare`创建一个新的PID namespace：

```cpp
static void run(int argc, char **argv) {
    cout << "Parent running " << cmd(argc, argv) << " as " << getpid() << endl;    

    if (unshare(CLONE_NEWPID) < 0) {
        cerr << "Fail to unshare PID namespace" << endl;
        exit(-1);
    }

    pid_t child_pid = fork();

    if (child_pid < 0) {ptx
        cerr << "Fail to fork child" << endl;
        return;
    }

    if (child_pid) {
        if(waitpid(child_pid, NULL, 0) < 0) {
            cerr << "Fail to wait for child" << endl;
        }
    } else {        
        run_child(argc, argv);
    }
}
```

这时候再次运行我们就可以看到，container真的以pid 1运行了：

```text
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Parent running /bin/bash as 11713
Child running /bin/bash as 1
root@container:/home/ptx/mini-docker# 
```

于是你尝试`ps`，却发现咦，涛声依旧了，妈的咋又不灵了，pid咋又回去了？

```bash
root@container:/home/user/mini-docker# ps
    PID TTY          TIME CMD
  11712 pts/0    00:00:00 sudo
  11713 pts/0    00:00:00 mocker
  11714 pts/0    00:00:00 bash
  11764 pts/0    00:00:00 ps
```

别急，这是正常的，这涉及到`ps`是怎么打印进程信息的。`ps`是通过读取 `/proc`目录下的pseudo filesystem来获取当前进程信息的[^8]，虽然我们将container放到了一个新的PID namespace中，但在读取`/proc`目录时得到的信息仍然与host进程是相同的，而这一信息仍然是基于原先的PID namespace维护的，所以我们`ps`看到的pid就又回去了。不过这并不耽误我们的pid在自己进程的视角中是1，因为`getpid`并不依赖于`/proc` 中的信息。不管怎么说，我们仍然是成功地隔离了pid view的，只是不那么明显罢了。

另外或许你会发现我们调用`unshare`创建PID namespace是在父进程中进行的，而不像之前UTS那样在子进程中调用。这其实是kernel实现方面的问题，创建PID namespace的进程本身不会被放入新的PID namespace中[^9]，而是他的子进程们才会进入新的PID namespace，而`fork`等函数创建的第一个子进程会以pid 1作为这个PID namespace的intial process，接收orphaned进程等等[^10]。

## Filesystem isolation

对container来说filesystem的隔离算是非常重要的一部分，所谓的依赖环境正是通过不同的磁盘镜像来实现的。不过在谈这个问题之前，我必须要澄清一点，就是**不同的mount namespace本身不能提供filesystem的隔离**。

咦，刚不是才说mount namespace能提供不同的mount view吗，怎么又不能了？

也许这个比喻不太恰当，但mount isolation与filesystem isolation间的区别就好比数学家关心一个方程解是否存在，解是否唯一，但工程人员关心这个方程的解是几。

mount isolation关心一个mount point被挂载在一个mount namespace中时，会不会也出现在其他mount namespace中（share、private等等），而filesystem isolation关心的是这个mount point里的内容挂载到哪里去了，里面装的是什么内容。

光说或许很难理解，不妨通过一个例子来看。假如我很巧，手边正好有一个ubuntu filesystem的拷贝在`~`目录下：

```bash
user@linux:~$ ls ubuntu-fs/
bin    dev  lib32   lost+found  opt   run   srv       tmp            var
boot   etc  lib64   media       proc  sbin  swapfile  ubuntu-fs.tar
cdrom  lib  libx32  mnt         root  snap  sys       usr
```

当然，这其中的`/proc`、`/sys`等pseudo filesystem都是空的，因为我们只拷贝了真正的磁盘文件。

我们可以对子进程代码做简单的修改，将container对整个filesystem的view限制在这个目录下：

```cpp
static void run_child(int argc, char **argv) {
    cout << "Child running " << cmd(argc, argv) << " as " << getpid() << endl;    

    int flags = CLONE_NEWUTS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (chroot("../ubuntu-fs") < 0) {
        cerr << "Fail to chroot" << endl;
        exit(-1);
    }

    if (chdir("/") < 0) {
        cerr << "Fail to chdir to /" << endl;
        exit(-1);
    }

    if (sethostname(child_hostname, strlen(child_hostname)) < 0) {
        cerr << "Fail to change hostname" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

在这部分中我们只做了两处修改：`chroot`和`chdir`。其中非常核心的就是这个`chroot`，它的功能是修改**当前进程及后续子进程**眼中的根目录，让后续的**absolute path**文件访问全都从这个新的根目录开始[^11]，而我们这里就把它改到了我们的文件系统镜像；紧跟着`chroot`我们用`chdir`将目录切换到新设置的`/`，看起来更像一回事了：

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
ptx@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Parent running /bin/bash  as 14418
Child running /bin/bash  as 1
root@container:/# ls
bin  boot  cdrom  dev  etc  lib  lib32  lib64  libx32  lost+found  media  mnt  opt  proc  root  run  sbin  snap  srv  swapfile  sys  tmp  ubuntu-fs.tar  usr  var
```

但要强调的是，chroot并不是一个面向安全的函数，而只是为了**view** isolation，你可以很轻易地通过相对目录访问trick[^12]来逃出这个根目录。

原先的`ubuntu-fs`目录中有一个`ubuntu-fs.tar`文件， 在这里我们也又在container的根目录里看到它了，如此一来我们也实现了对文件系统的隔离：

## /proc

虽然做到了filesystem isolation，我们仍然未解决`/proc`目录的问题，这时我们运行`ps`干脆就开始报错了：

```text
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
user@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Parent running /bin/bash  as 17636
Child running /bin/bash  as 1
root@container:/# ps
Error, do this: mount -t proc proc /proc
```

这是因为我们将根目录切换到`ubuntu-fs`后，后续的`proc`访问也全都是基于这个basepath了，而很明显，`ubuntu-fs`下的`/proc`里是什么都没有的。

不过这可以通过一个简单的挂载来解决：

```cpp
static void run_child(int argc, char **argv) {
    cout << "Child running " << cmd(argc, argv) << " as " << getpid() << endl;    

    int flags = CLONE_NEWUTS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (chroot("../ubuntu-fs") < 0) {
        cerr << "Fail to chroot" << endl;
        exit(-1);
    }

    if (chdir("/") < 0) {
        cerr << "Fail to chdir to /" << endl;
        exit(-1);
    }

    if (mount("proc", "proc", "proc", 0, NULL) < 0) {
        cerr << "Fail to mount /proc" << endl;
        exit(-1);
    } 

    if (sethostname(child_hostname, strlen(child_hostname)) < 0) {
        cerr << "Fail to change hostname" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

运行发现说哎这就好啦，就不报错啦，就能显示啦，甚至还体现出来pid隔离啦：

```bash
user@linux:~/mini-docker$ make
g++ main.cc -o mocker
ptx@linux:~/mini-docker$ sudo ./mocker run /bin/bash
Parent running /bin/bash  as 18685
Child running /bin/bash  as 1
root@container:/# ps
    PID TTY          TIME CMD
      1 ?        00:00:00 bash
      8 ?        00:00:00 ps
root@container:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0  12916  4220 ?        S    23:18   0:00 /bin/bash
root           9  0.0  0.0  14568  3452 ?        R+   23:18   0:00 ps aux
```

还可以在container中查看挂载过的`/proc`

```bash
root@container:/# cat /proc/mounts 
proc /proc proc rw,relatime 0 0
```

但别急着高兴，如果你这时候回到host查看所有挂载过的`proc`文件系统会发现：

```bash
user@linux:~/mini-docker$ cat /proc/mounts | grep ^proc
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
proc /home/user/ubuntu-fs/proc proc rw,relatime 0 0
```

这个挂载点也出现在了host中。也即，虽然我们让container获得一致的pid isolation view，但没能将这个mount point本身的存在从host中隔离出来。

我们退出container，`umount`掉container挂载的`/proc`，来看看最后的mount namespace问题。

```bash
root@container:/# exit
exit
user@linux:~/mini-docker$ sudo umount ../ubuntu-fs/proc 
```

## Mount namespace

相比于其他部分，mount的问题一些，比较直观的体现是，你没法通过简单地加一个flag实现预期中的mount point isolation，也就是说：

```cpp
static void run_child(int argc, char **argv) {
    cout << "Child running " << cmd(argc, argv) << " as " << getpid() << endl;    

    int flags = CLONE_NEWUTS | CLONE_NEWNS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (chroot("../ubuntu-fs") < 0) {
        cerr << "Fail to chroot" << endl;
        exit(-1);
    }

    if (chdir("/") < 0) {
        cerr << "Fail to chdir to /" << endl;
        exit(-1);
    }

    if (mount("proc", "proc", "proc", 0, NULL) < 0) {
        cerr << "Fail to mount /proc" << endl;
        exit(-1);
    } 

    if (sethostname(child_hostname, strlen(child_hostname)) < 0) {
        cerr << "Fail to change hostname" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

类比`CLONE_NEWUTS`、`CLONE_NEWPID`仅通过给`unshare`加一个`CLONE_NEWNS`是没办法实现对mount point的isolation的（可以运行试一试），需要重新设置根目录mount point的propagation type（对“为什么需要这几行”不是三言两语就能解释清的，我把这个放在末尾，有兴趣的话可以去看看，但这里就不展开了）：

```cpp
static void run_child(int argc, char **argv) {
    cout << "Child running " << cmd(argc, argv) << " as " << getpid() << endl;    

    int flags = CLONE_NEWUTS | CLONE_NEWNS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (mount(NULL, "/", NULL, MS_SLAVE | MS_REC, NULL) < 0) {
        cerr << "Fail to mount /" << endl;
        exit(-1);
    } 

    if (chroot("../ubuntu-fs") < 0) {
        cerr << "Fail to chroot" << endl;
        exit(-1);
    }

    if (chdir("/") < 0) {
        cerr << "Fail to chdir to /" << endl;
        exit(-1);
    }

    if (mount("proc", "proc", "proc", 0, NULL) < 0) {
        cerr << "Fail to mount /proc" << endl;
        exit(-1);
    } 

    if (sethostname(child_hostname, strlen(child_hostname)) < 0) {
        cerr << "Fail to change hostname" << endl;
        exit(-1);
    }

    if (execvp(argv[0], argv)) {
        cerr << "Fail to exec" << endl;
    }
}
```

如此一来我们运行container的时候挂载`/proc`就不会propagate到host view，container的`/proc`mount point visibility被限制在了container的mount namespace中。不过我们仍然可以在container运行着的时候在host中看到这个mount namespace的存在：

```bash
user@linux:~/mini-docker$ ps axjf | grep /bin/bash
   2420   21908   21907    2420 pts/0      21907 S+    1000   0:00  |       \_ grep --color=auto /bin/bash
   4031    4136    4136    4136 pts/1      21777 Ss    1000   0:00  |       |   \_ /usr/bin/bash
   4136   21775   21775    4136 pts/1      21777 S        0   0:00  |       |       \_ sudo ./mocker run /bin/bash
  21775   21776   21775    4136 pts/1      21777 S        0   0:00  |       |           \_ ./mocker run /bin/bash
  21776   21777   21777    4136 pts/1      21777 S+       0   0:00  |       |               \_ /bin/bash
user@linux:~/mini-docker$ sudo lsns -t mnt | grep 21777
4026533509 mnt       1 21777 root             /bin/bash
```

## 一些想法

这次搬运的原视频是我在20年看到的，当时就感觉是非常好的资源，即便你对namespace、cgroup所知甚少（在当时我甚至是不知道有这两项技术存在的），也能大致理解她在说什么。用到的Go也是很简单的语法，只要对C系的语言有所了解应该就能看懂。

最近也是出于研究需要重新回忆这方面的内容，闲暇之余在知乎搜了一圈发现到现在也没人提到过这个资源，实在是太可惜了。

在知乎总能看到有人分享很好的资源，这次我也来贡献点力量，希望对于想更进一步了解容器技术的人，这篇回答能多少解决他们的一些疑惑～

* * *

## 附：关于remount root mount point的讨论

### Mount namespace propagation & shared subtree

这部分的讨论主要是参考了lwn上的这篇文章：

[https://lwn.net/Articles/689856](https://link.zhihu.com/?target=https%3A//lwn.net/Articles/689856)

在一开始提到mount namespace的时候，我们说他隔离了不同mount namespace间mount point可见性的隔离。然而在一开始kernel实现了这个feature的时候，人们发现这样会导致一些易用性的问题，主要是因为mount namespace提供的隔离有点强过头了。

最直观的一个例子是，如果我们clone一个新的mount namepsace而不chroot，完全隔离会导致我们在原先的mount namespace下挂载一个新的设备时，新的mount namespace完全看不到这个设备，结果就是我们不得不手动在所有需要的mount namespace中手动挂载一次。也就是说，我们在希望不同mount namespace隔离的同时也希望它们之间能够实现部分mount point的共享。

出于上面这些考虑，后续的内核实现了shared subtree feature，借助这个feature来实现自动的mount/unmount事件传播。具体来说，每个mount point会带有一个propagation type，它决定**这个mount point下的直接mount point**（也即“mount point下的mount point创建/删除是否propagate不归我管”）创建/删除如何propagate到其他mount points。

propagation type分为四类，分别是：

-   `MS_SHARED`：在当前mount point下的创建或删除新的mount point会propagate到“peer group”中所有其他mount point。也就是说，在这些其他mount point下也可以看到心创建或删除的mount point。这里的“peer group”是怎么来的先按下不表。
-   `MS_PRIVATE`：与`MS_SHARED`完全相反，任何在当前mount point下创建/删除的mount point都不会对其他mount point可见
-   `MS_SLAVE`：这个mount point是某个“peer group”（称为master）的slave，类似于单向的share，master中的改动会propagate到slave中，反之则是不可见的。

`MS_UNBINDABLE`：这一个不可以被bind的private mount point，也即除了具备`MS_PRIVATE`外，它不能被当作其他bind mount的source mount point[^13]

> 这里值得一提的是，propagation type作用的对象是mount point而非mount namespace，共享的对象也是mount point非mount namespace。因为可能存在一个mount point X，在相同mount namespace下有一个bind mount point Y被bind到了X上，另一个mount namespace下有另一个bind mount point Z也被bind到了X上，那么此时它们各自下的mount point创建/删除propagation只跟它们的propagation type有关，而与是不是在相同的mount namespace无关。  
> 然而如果我们希望通过`/proc/mounts`或者`findmnt`查看所有的mount point以及对应的propagation type，就只能看到当前进程所属的mount namespace下的mount point了。比如`sudo findmnt -o TARGET,PROPAGATION`，我们当然不可能看到其他mount namespace的`/`挂载到哪里以及是什么type。如果真的希望这么做，也只能找到一个属于目标mount namespace的pid，去它的`/proc`下查看

那么peer group是怎么产生的呢？有两种途径：

-   bind mount到一个MS\_SHARED的mount point，这样新的mount point就和原先的mount point在一个peer group中了
-   发生mount namespace clone时，按照以下规则确定新的mount namespace中各个mount point的propagation type[^14]：

> A cloned namespace contains all the mounts as that of the parent namespace.  
> Let's say 'A' and 'B' are the corresponding mounts in the parent and the child namespace.  
>   
> If 'A' is shared, then 'B' is also shared and 'A' and 'B' propagate to each other.  
>   
> If 'A' is a slave mount of 'Z', then 'B' is also the slave mount of 'Z'.  
>   
> If 'A' is a private mount, then 'B' is a private mount too.  
>   
> If 'A' is unbindable mount, then 'B' is a unbindable mount too.

也即原先`MS_SHARED`的mount point在clone后的mount point也自动进入它的peer group。

### 默认行为

说了这么多，听起来很啰嗦，但为了理解我们到底要解决什么问题，这些background是必要的。

我们回过头来考虑一个问题：当创建（而非clone或者bind）一个新的mount point的时候，它的默认propagation type是什么？

在linux中是按照如下规则来确定的：

-   如果这个mount point不是root，且它的parent mount point的propagation type是`MS_SHARED`，那么它也是`MS_SHARED`的
-   否则一律`MS_PRIVATE`

很明显按照这个规则，在最开始挂载root的时候它的propagation type会是`MS_PRIVATE`，而且如果我们不显式地声明，那么后续的创建所有mount point都会是`MS_PRIVATE`。

而我们刚才也说了，像诸如设备的挂载，我们其实反而希望它们能够自动propagate到不同的其他mount namespace所clone出来的对应mount point，从这个角度来看`MS_SHARED`反而是一个更好的default type。

考虑到上面的种种原因，`systemd`会将系统中初始mount namespace的mount point全部设置为`MS_SHARED`，因此在实际的linux发行版中，默认的propagation type其实是`MS_SHARED`。

不过对于像`unshare`[^15]这样的工具（是command line tool的`unshare`而不是我们上面调用的库函数的那个`unshare`），它的本意就是将新的进程放在一个完全隔离的mount namespace中执行，因此在启动一个新的mount namespace中，它会重新将所有mount point全部设置为`MS_PRIVATE`，就类似于clone完mount namespace后立即：

```bash
mount --make-rprivate /
```

递归地将根目录下的所有mount point重置为`MS_PRIVATE`。

* * *

回到我们的那一处代码中的修改来：

```cpp
    int flags = CLONE_NEWUTS | CLONE_NEWNS;

    if (unshare(flags) < 0) {
        cerr << "Fail to unshare in child" << endl;
        exit(-1);
    }

    if (mount(NULL, "/", NULL, MS_SLAVE | MS_REC, NULL) < 0) {
        cerr << "Fail to mount /" << endl;
        exit(-1);
    } 
```

在这里我们必须要弄清`mount`之前发生了什么。我们clone了一个mount namespace，而先前mount namespace中mount point的propagation type可以在host中看到：

```bash
user@linux:~$ sudo findmnt -o TARGET,PROPAGATION
TARGET                                PROPAGATION
/                                     shared
├─/sys                                shared
│ ├─/sys/kernel/security              shared
...
 └─/sys/kernel/config                shared
├─/proc                               shared
│ └─/proc/sys/fs/binfmt_misc          shared
│   └─/proc/sys/fs/binfmt_misc        shared
├─/dev                                shared
│ ├─/dev/pts                          shared
│ ├─/dev/shm                          shared
│ ├─/dev/hugepages                    shared
│ └─/dev/mqueue                       shared
...
```

因此当我们clone了namespace后，root mount point会是`MS_SHARED`状态，此时我们`chroot`并挂载`/proc`时，由于新mount namespace的root mount point与host mount namespace在相同peer group中，我们在root mount point下发生的immediate mount会反映到host namespace中，结果就是我们在host中也观测到了一个新的proc mount point。值得注意的是，我们虽然将container的根目录给`chroot`到了ubuntu-fs下，却不会影响`ubuntu-fs/proc`是root mount point的immediate child mount point这个事实。因为root mount point和根目录并不是一回事（类似mount point hierarchy vs. directory hierarchy），`chroot`只是改变了container视角中的根目录位置，却没有改变`ubuntu-fs`不是一个mount point的事实，也因此root mount point的propagation type会左右container中`/proc`在peer group中的可见性（怎么感觉车轱辘话在来回说。。

为了让`/proc`的挂载对其他mount point（这里也即其他mount namespace）不可见，我们用类似`unshare`command line tool的做法：

```bash
mount --make-rslave /
```

将根目录下的所有mount point递归地设置为`MS_SLAVE`（`MS_PRIVATE`也可，`MS_LAVE`可以让host的mount操作对container单向可见），于是我们传递给`mount`的flag就是`MS_SLAVE`和`MS_REC`。

[^1]: KVM https://www.linux-kvm.org/
[^2]: qemu system emulation https://www.qemu.org/docs/master/system/
[^3]: Dynamic binary translation https://en.wikipedia.org/wiki/Binary_translation#Dynamic_binary_translation
[^4]: namespaces(7) — Linux manual page https://man7.org/linux/man-pages/man7/namespaces.7.html
[^5]: Mount namespaces and shared subtrees https://lwn.net/Articles/689856/
[^6]: [6] https://elixir.bootlin.com/linux/v5.15.31/source/fs/mount.h#L8
[^7]: unshare(2) — Linux manual page https://man7.org/linux/man-pages/man2/unshare.2.html
[^8]: ps(1) — Linux manual page https://man7.org/linux/man-pages/man1/ps.1.html#NOTES
[^9]: [9] https://man7.org/linux/man-pages/man2/unshare.2.html#DESCRIPTION
[^10]: [10] https://man7.org/linux/man-pages/man7/pid_namespaces.7.html#DESCRIPTION
[^11]: chroot(2) — Linux manual page https://man7.org/linux/man-pages/man2/chroot.2.html
[^12]: [12] https://man7.org/linux/man-pages/man2/chroot.2.html#DESCRIPTION
[^13]: What is a bind mount? https://unix.stackexchange.com/questions/198590/what-is-a-bind-mount
[^14]: Shared Subtrees https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt
[^15]: unshare(1) — Linux manual page https://man7.org/linux/man-pages/man1/unshare.1.html