---
id: "24218651"
title: "HTTPS 要比 HTTP 多用多少服务器资源？"
author: "陈硕"
type: zhihu-answer
source: "https://www.zhihu.com/question/21518760/answer/24218651"
created: "2014-04-08 07:26"
updated: "2014-07-26 06:58"
collected: "2014-04-08 07:26"
downloaded: "2026-08-16"
---
开启 SSL 会增加内存、CPU、网络带宽的开销，后二者跟你使用的 cipher suite 密切相关，其中参数很多，很难一概而论。开启 SSL 的前提是你的 cert 和 key 必须放在 TCP endpoint，你是否信得过那台设备？

SSL 开销来自于两部分，handshake 和 bulk encryption。对于性能，前者我们关注 handshakes/s，后者关注 MiB/s。

先说比较简单的 bulk encryption，首先由于 padding 和 MAC，消息会变长，增加一些网络带宽。其次，bulk encryption 和 MAC 会增加 CPU 使用，具体跟所使用的加密算法和 MAC 算法有关，如果用 AES，也跟 CPU 是否支持 AESNI 指令有关。如果用常见的 AES-256-CBC + SHA1 组合，单个 CPU core 就能轻松打满千兆网带宽。（AES128 vs. AES256 和 SHA1 vs. SHA256 还有细微差别，但透过千兆网就不一定能看出来了，不过 3DES 要慢得多。）另外，如果用 GCM 代替 CBC，会节约一些带宽（省了 MAC），但会增加 CPU 开销。测试 bulk encryption 的性能是比较容易的。

再说 handshake，这里边水比较深。开销主要取决于 key exchange 算法。这里暂且只考虑流行的 2048 bit RSA key，不考虑新潮的 ECDSA。

首先，你要决定是否采用

[forward secrecy](https://link.zhihu.com/?target=http%3A//en.wikipedia.org/wiki/Forward_secrecy)

，即如果有人录下你今天的 traffic，将来再搞到了你的 private key，他是否能追溯解密以往的消息。这决定了是 RSA key exchange 还是 ECDHE RSA key exchange。（这里就不考虑慢得多的 DHE key exchange 了。）

单从性能方面考虑，RSA key exchange 比 ECDHE RSA key exchange 快。大体上一秒钟能做几百上千次 handshake，比 TCP 三路握手慢很多。如果你用 ECDHE，注意选 secp256r1/secp224r1 等曲线，而不是更慢的 secp521r1。还有，对于 ECDHE，“每次 handshake 用新的 key （SSL\_OP\_SINGLE\_ECDH\_USE）”与“进程启动时产生一个 key 反复使用”也会有细微的性能差别。如果你要贴 benchmark 的对比结果，一定要把各个参数细节指明，否则没有参考意义。

ECDHE RSA key exchange 比 RSA key exchange 的总运算量大，但分配在服务端和客户端的比例不及后者悬殊。RSA key exchange 中，抛开 cert 验证，客户端耗CPU的操作是 RSA public key encrypt，而服务端需要做 RSA private key decrypt，后者要慢几倍。ECDHE RSA key exchange 中，客户端和服务端都要做 EC key generation 和 scalar multiplication，运算量相当，区别在于服务端还要做 RSA sign with private key，客户端只要 RSA verify with public key，总体来看，服务端的运算量略大。也就是说两种 key exchange 策略 handshake 产生的 CPU 负载在服务端和客户端的分配比例差别较大。

总之，你需要找一位安全顾问，不然一个轻微的配置失误也许就葬送了增强安全的全部努力。我不是专家，以上文字算是我的笔记吧。《Everything you need to know about cryptography in 1 hour》

[https://www.bsdcan.org/2010/schedule/attachments/135\_crypto1hr.pdf](https://link.zhihu.com/?target=https%3A//www.bsdcan.org/2010/schedule/attachments/135_crypto1hr.pdf)