---
id: "2468261772"
title: "JAVA大军，开始把目光从spring cloud转向k8s甚至k8s+istio了么？"
author: "黄枣颖"
type: zhihu-answer
source: "https://www.zhihu.com/question/345497663/answer/2468261772"
created: "2022-05-03 12:20"
updated: "2022-05-03 12:20"
collected: "2022-05-03 12:20"
downloaded: "2026-08-16"
---
早在18年研究Spring Cloud的时候，我就意识到这个问题，果断从docker转向k8s，但依然保留spring cloud作为过渡的手段……

然而在调研Service Mesh落地方案等相关的案例，发现即便是背后有Google背书的ServiceMesh一个Istio，在落地的时候依然遇到不少阻碍，其中最主要的是Istio的分体式架构过于复杂，极大地限制落地条件，对于大型企业还好，对于中小企业本身不太复杂的业务，落地Istio简直就是本末倒置！

反观Istio的强力竞争对手Linkerd，很早就意识到分体式架构的弊端，从Linkerd2.0开始重新回归到单体架构，并使用无GC的编程语言Rust重构，很好地遏制SideCar容器喧宾夺主：资源消耗比业务容器还多的势头！

再加上Google后来出尔反尔，没有把Istio捐赠给CNCF，反而交给新成立100%控股的子公司！而Linkerd2.0已经成为CNCF的孵化项目！

我推荐中小企业都应该使用Linkerd，既节约成本，加速Service Mesh落地，又可以避免日后Google背刺

* * *

下面聊聊现有Service Mesh解决方案的局限性

其实我从18年末接触Service Mesh，直到19年末转向云原生开发，耕耘Service Mesh领域的时间不算长！因为在该领域并没有投入过多的资源和精力，不会因为投入过多深陷其中不能自拔只能继续忽悠别人加入Service Mesh来减少损失！

目前主流的Service Mesh方案都离不开SideCar容器，而随着业务需求的不断变化，SideCar容器也会随之变得越来越复杂，甚至到了资源占用消耗超过业务容器，喧宾夺主的地步！

这是Service Mesh解决方案商不愿意告诉你Service Mesh落地可能会带来的**不良后果**之一！

这也可以说是微服务架构不可避免的缺陷之一！

要解决问题，必须逐步过渡到Serverless架构

**Serverless = FaaS + BaaS**

其中**BaaS**的含义就是"Backend as a Service"，把后端服务当作是一种可以提供服务的资源！

后端服务既可以是传统的单体架构，也可以新兴的微服务架构！

要解决微服务的治理问题，你可以继续使用SideCar模式的Istio和Linkerd，但要解决SideCar容器膨胀的问题，你不得不引入**FaaS。**

**FaaS**的全称是Function as a Service，把函数当作是一种可以提供服务的资源。

也就是把SideCar容器的功能拆分一个一个的功能独立的函数，例如：日记收集、流量管控、身份鉴权等等，再接入FaaS引擎后，SideCar容器占用资源就可以大幅度减少！

目前已经有很多云服务厂商推出FaaS产品，例如aws的lambda，阿里云和腾讯云也有类似的产品

但使用以上产品很容易产生厂商锁定，而且使用场景也不是针对SideCar场景，所以我推荐使用WebAssembly作为FaaS的落地方案！

WebAssembly，简称wasm，是一种面向Web的汇编字节码标准！它在性能表现/资源消耗等方面，都远优于JavaScript，更有C/C++/Rust/Go/Swift/Kotlin/Ruby等主流编程语言的支持。由于wasm是开放标准，并且已经演进到2.0草案阶段，未来还有更多的特性支持以及更多编程语言加入wasm阵营！

业界普遍认为WASM未来成为公认的FaaS标准！

个人认为SideCar最佳解决方案，就是通过DaemonSet在每个节点上部署一个WASM调度器，开发人员将日志收集、流量管控或身份鉴权等功能编译为wasm格式，再由WASM调度器统一调度！

目前开源的wasm调度框架就有fermyon推出的spin

wasm实例的创建与销毁overhead和footprint，都远低于docker容器的创建和销毁，是sidecar容器的优秀替代品！

* * *

至于因为公司业务体量小等原因，还没有上了Istio或者linkerd船的企业，可以考虑一下cilium

cilium原本只是k8s的容器网络CNI解决方案之一，但由于cilium采用Linux最热门的新特性eBPF，cilium在性能效率和功能丰富层面上击败其他CNI解决方案，成为最受欢迎的CNI解决方案！

eBPF是目前Linux内核最受追捧的子系统，它的本质是Linux内核中的一个虚拟机！它的出现使得在linux内核中动态执行任意的代码变成了可能！进一步降低linux内核开发的难度：以驱动开发为例，由于linux是宏内核，驱动必须与内核一起加载，一旦新开发的驱动存在bug，就极有可能导致内核崩溃，造成无法挽救的损失！现在有eBPF之后，调试驱动程序就变得相对容易多了，由于eBPF本身是个虚拟机，在加上eBPF程序都必须经过一系列的检测确保程序不会出现问题后才能执行！

除了内核开发以外，eBPF的出现也推动SDN/NFV的发展，最近cilium也宣布进军Service Mesh领域，与Istio/Linkerd不同的是，cilium针对Service Mesh的解决方案并没有出现SideCar，而是通过eBPF钩子来实现流量管控、服务发现、负载均衡、链路追踪、灰度发布等常见的Service Mesh特性！

但eBPF目前而言，并不满足图灵完备的要求，例如不支持循环，过深递归调用，程序大小限制等等！

再者有些功能需求，例如日志收集、应用配置等，采用常规的技术栈完全可以满足需求，没必要采用eBPF来增加开发的难度，完全可以用wasm的方案来解决SideCar容器膨胀的问题。

综上所述，eBPF based cilium 和 wasm based Spin才是最理想的Service Mesh解决方案