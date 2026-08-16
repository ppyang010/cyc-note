---
id: "3559406542"
title: "Java NIO到底是个什么东西?"
author: "sea"
type: zhihu-answer
source: "https://www.zhihu.com/question/624841657/answer/3559406542"
created: "2024-07-12 10:38"
updated: "2024-07-12 10:38"
collected: "2024-07-12 10:38"
downloaded: "2026-08-16"
---
对于 TCP 或 UDP 的服务器，如何实现并发处理客户端。

最直观的想法就是为每个到来的请求，创建一个单独的线程来处理，但是这种方式未免太浪费资源了，那可以使用线程池来管理线程，这样可以节约资源。以 TCP 服务器举例。

首先需要定义一个需要提交到线程池中的任务。

  

public class TCPRunnable implements Runnable {

private Socket mSocket;

  

public TCPRunnable(Socket socket) {

mSocket = socket;

}

  

@Override

public void run() {

try {

System.out.println("Handling client: " + mSocket.getRemoteSocketAddress());

InputStream in = mSocket.getInputStream();

OutputStream out = mSocket.getOutputStream();

BufferedReader br = new BufferedReader(new InputStreamReader(in));

String line;

System.out.println("Client said: ");

while ((line = br.readLine()) != null) {

System.out.println(line);

}

out.write("Welcome!".getBytes());

} catch (IOException e) {

e.printStackTrace();

} finally {

try {

if (mSocket != null) {

mSocket.close();

}

} catch (IOException e) {

e.printStackTrace();

}

}

}

}

在构造函数中，需要传入一个 Socket 实例，当任务提交到线程池后，Socket 的读写操作就在异步线程中执行。

现在可以改进下服务器端，只需要在获取 Socket 实例后提交任务即可

  

public class TCPServer1 {

public static void main(String\[\] args) {

ExecutorService mThreadPool = Executors.newCachedThreadPool();

ServerSocket serverSocket = null;

try {

serverSocket = new ServerSocket(8890);

while (true) {

Socket socket = serverSocket.accept();

mThreadPool.execute(new TCPRunnable(socket));

}

} catch (IOException e) {

e.printStackTrace();

} finally {

try {

if (serverSocket != null) {

serverSocket.close();

}

} catch (IOException e) {

e.printStackTrace();

}

}

}

}

使用线程池好像很完美，但是现在再思考一个总是，假如客户端希望与服务器保持一个长连接，那么很显然线程池也限制了客户端并发访问的数量，因为核心线程就那么几个。 那么可不可以增大线程池中的核心线程数量呢？ 可以是可以，但是要增大多少呢？面对数以百万计的客户端，你选择不了！而且增大线程数量，只会带来更大的线程开销，包括线程调度以及上下文切换。 同时，我们还要面对一个总是，那就是多线程临界资源的访问，我们需要同步或者加锁，这些隐藏的开销是开发者无法控制的。

Java NIO 的到来解决了这些问题，并且可以让服务器同时处理上千个客户端，而且还可以保持良好的性能。那么本文就探讨下 NIO 到底强在哪里。

Channel

NIO 使用信道 (Channel) 来发送和接收数据，而不使用传统的流 (InputStream/OutputStream)。

Channel 实例代表了打开一个实体的连接，这些实体包括硬件设备，文件，网络套接字等等。 Channel 有个特色，在 Channel 上的操作，例如读写，都是线程安全的。

SelectableChannel

SelectableChannel 是一个抽象类，它实现了 Channel 接口，这个类比较特殊。

首先 SelectableChannel 可以是阻塞或者非阻塞模式。如果是阻塞模式，在这个信道上的任何 I/O 操作都是阻塞的直到 I/O 完成。 而如果是非阻塞模式，任何在这个信道上的 I/O 都不会阻塞，但是传输的字节数可能比原本请求的字节数要少，甚至一个也没有。

其次呢 SelectableChannel 可以被 Selector 用来多路复用，不过首先需要调用 selectableChannel.configureBlocking(false) 调整为非阻塞模式(nonblocking mode)，这一点很重要。然后进行注册

  

SelectionKey register(Selector sel, int ops)

SelectionKey register(Selector sel, int ops, Object att)

  

第一个参数代表要注册的 Selector 实例。关于 Selector 后面再讲。

第二个参数代表本通道感兴趣的操作，这些都定义在 SelectionKey 类中，如下

  

public static final int OP\_READ = 1 << 0;

public static final int OP\_WRITE = 1 << 2;

public static final int OP\_CONNECT = 1 << 3;

public static final int OP\_ACCEPT = 1 << 4;

对于 SocketChannel ，它感兴趣的操作只有 OP\_READ, OP\_WIRTE 和 OP\_CONNECT，然而它并不包括 OP\_ACCEPT。 而 ServerSocketChannel可以对这四个操作都感兴趣。为何？因为只有 ServerSocketChannel 有 accpet() 方法。

  

SocketChannel 和 ServerSocketChannel 都是 SelectableChannel 的子类。

  

第三个参数 Object att 是注册时的附件，也就是可以在注册的时候带点什么东西过去。

register() 方法会返回一个 SelectionKey 实例。SelectionKey 相当于一个 Java Bean，其实就是 register() 的三个参数的容器，它可以返回和设置这些参数

  

Selector selector();

int interestOps();

Object attachment()

  

SocketChannel

SocketChannel 代表套接字通道(socket channel)。

SocketChannel 实例是通过它的静态的方法 open() 创建的

  

public static SocketChannel open() throws IOException {

return SelectorProvider.provider().openSocketChannel();

}

  

public static SocketChannel open(SocketAddress remote)

throws IOException

{

// 1. ceate socket channel

SocketChannel sc = open();

try {

// 2. connect channel's socket, blocking until connected or error

sc.connect(remote);

} catch (Throwable x) {

try {

sc.close();

} catch (Throwable suppressed) {

x.addSuppressed(suppressed);

}

throw x;

}

assert sc.isConnected();

return sc;

}

open() 方法仅仅是创建一个 SocketChannel 对象，而 open(SocketAddress remote) 就更进一步，它还调用了 connect(addr) 来连接服务器。

SocketChannel 是 SelectableChannel 的子类，还记得前面 SelectableChannel 的特性吗？如果不配置阻塞模式，那么 SocketChannel 对象默认就是阻塞模式，那么 open(SocketAddress remote) 方法其实就是阻塞式打开服务器连接。而且在 SocketChannel 上任何 I/O 操作都是阻塞式的。

那么既然 SelectableChannel 可以在非阻塞模式下的任何 I/O 操作都不阻塞，那么我们可以先调用无参的 open() 方法，然后再配置为非阻塞模式，再进行连接，而这个连接就是非阻塞式连接，伪代码如下

  

// 创建 SocketChannel 实例

SocketChannel sc = [SocketChannel.open](https://link.zhihu.com/?target=http%3A//SocketChannel.open)();

// 调整为非阻塞模式

sr.configureBlocking(false);

// 连接服务器

sr.connect(remoteAddr);

此时的 connect() 方法是非阻塞式的，我们可以通过 isConnectionPending() 方法来查询是否还在连接中，如果还在连接中我们可以做点其它事，而不用像创建 Socket 一样一起阻塞走到连接建立，在这里我们可以看到使用 NIO 的好处了。

如果 isConnectionPending() 返回了 false，那就代表已经建立连接了，但是我们还要调用 finishConnect() 来完成连接，这点需要注意。

用 SocketChannel 实现客户端

  

public class NonBlockingTCPClient {

public static void main(String\[\] args) {

byte\[\] data = "hello".getBytes();

SocketChannel channel = null;

try {

// 1. open a socket channel

channel = [SocketChannel.open](https://link.zhihu.com/?target=http%3A//SocketChannel.open)();

// adjust to be nonblocking

channel.configureBlocking(false);

// 2. init connection to server and repeatedly poll with complete

// connect() and finishConnect() are nonblocking operation, both return immediately

if (!channel.connect(new InetSocketAddress(InetAddress.getLocalHost(), 8899))) {

while (!channel.finishConnect()) {

System.out.print(".");

}

}

  

System.out.println("Connected to server...");

  

ByteBuffer writeBuffer = ByteBuffer.wrap(data);

ByteBuffer readBuffer = ByteBuffer.allocate(data.length);

int totalBytesReceived = 0;

int bytesReceived;

// 3. read and write bytes

while (totalBytesReceived < data.length) {

if (writeBuffer.hasRemaining()) {

channel.write(writeBuffer);

}

if ((bytesReceived = [channel.read](https://link.zhihu.com/?target=http%3A//channel.read)(readBuffer)) == -1) {

throw new SocketException("Connection closed prematurely");

}

totalBytesReceived += bytesReceived;

System.out.print(".");

}

System.out.println("Server said: " + new String(readBuffer.array()));

} catch (IOException e) {

e.printStackTrace();

} finally {

// 4 .close socket channel

try {

if (channel != null) {

channel.close();

}

} catch (IOException e) {

e.printStackTrace();

}

}

}

}

第一步，创建 SocketChannel 实例，并配置为非阻塞模式，只有在非阻塞模式下，任何在 SocketChannel 实例上的 I/O 操作才是非阻塞的。这样我们的客户端就是一个非阻塞式客户端，也就可以提升客户端性能。

第二步，用 connect() 方法连接服务器，同时用 while 循环不断检测并完全连接。 其实我们可以不用这样盲等，这里只是为了演示连接的过程。 当你在需要马上进行 I/O 操作前，必须要用 finishConnect() 完成连接过程。

第三步，用 ByteBuffer 读写字节，这里我们为何和一个 while 循环不断地读写呢？ 还记得前面讲 SelectableChannel 非阻塞时的特性吗？ 如果一个 SelectableChannel 为非阻塞模式，它的 I/O 操作读写的字节数可能比实际的要少，甚至没有。 所以我们这里用循环不断的读写，保证读写完成。

  

官方对 SocketChannel.write() 有一段话是这样说的: A socket channel in non-blocking mode, for example, cannot write any more bytes than are free in the socket's output buffer.

  

ServerSocketChannel

ServerSocketChannel 类代表服务器端套接字通道(server-socket channel)。

ServerSocketChannel 和 SocktChannel 一样，需要通过静态方法 open() 来创建一个实例，创建后，还需要通过 bind() 方法来绑定到本地的 IP 地址和端口

代码解读复制代码ServerSocketChannel bind(SocketAddress local)

ServerSocketChannel bind(SocketAddress local, int limitQueue)

  

参数 SocketAddress local 代表本地 IP 地址和端口号，参数 int limitQueue 限制了连接的数量。

Selector

Selector 是 SelectableChannel 的多路复用器，可以用一个 Selector 管理多个 SelectableChannel。例如，可以用 Selector 在一个线程中管理多个 ServerSocketChannel，那么我们就可以在单线程中同时监听多个端口的请求，这简直是美不可言。 从这里我们也可以看出使用 NIO 的好处。

创建 Selector 实例

Selector 实例也需要通过静态方法 open() 创建。

注册 SelectableChannel

前面说过，我们需要调用 SelectableChannel 的 register() 来向 Selector 注册，它会返回一个 SelctionKey 来代表这次注册。

选择通道

前面说过，可以通过 Selector 管理多个 SelectableChannel，它的 select() 方法可以监测哪些信道已经准备好进行 I/O 操作了，返回值代表了这些 I/O 的数量。

  

int select()

int select(long timeout)

int selectNow()

  

当调用 select() 方法后，它会把代表已经准备好 I/O 操作的信道的 SelectionKey 保存在一个集合中，可以通过 selectedKeys() 返回。

代码解读复制代码Set<SelectionKey> selectedKeys()

  

select() 的三个方法，从命名就可以看出这几个方法的不同之处，第一个方法是阻塞式调用，第三个方法设置了一个超时时间，第三个方法是立即返回。

wakeUp()

如果调用 selcet() 方法会导致线程阻塞，甚至无限阻塞，wakeUp() 方法是唤醒那些调用 select() 方法而处于阻塞状态的线程。

使用 Selector 和 ServerSocketChannel 实现服务器

  

  

package com.ckt.sockettest;

  

  

import java.io.IOException;

import java.net.InetSocketAddress;

import java.nio.ByteBuffer;

import java.nio.channels.SelectionKey;

import java.nio.channels.Selector;

import java.nio.channels.ServerSocketChannel;

import java.nio.channels.SocketChannel;

import java.util.Iterator;

import java.util.Set;

  

public class TCPChannelServer {

public static void main(String\[\] args) {

Selector selector = null;

try {

// 1. open a selector

selector = [Selector.open](https://link.zhihu.com/?target=http%3A//Selector.open)();

// 2. listen for server socket channel

ServerSocketChannel ssc = [ServerSocketChannel.open](https://link.zhihu.com/?target=http%3A//ServerSocketChannel.open)();

// must to be nonblocking mode before register

ssc.configureBlocking(false);

// bind server socket channel to port 8899

ssc.bind(new InetSocketAddress(8899));

// 3. register it with selector

ssc.register(selector, SelectionKey.OP\_ACCEPT);

  

while (true) { // run forever

// 4. select ready SelectionKey for I/O operation

if ([selector.select](https://link.zhihu.com/?target=http%3A//selector.select)(3000) == 0) {

continue;

}

// 5. get selected keys

Set<SelectionKey> selectionKeys = selector.selectedKeys();

Iterator<SelectionKey> iterator = selectionKeys.iterator();

// 6. handle selected key's interest operations

while (iterator.hasNext()) {

SelectionKey key = [iterator.next](https://link.zhihu.com/?target=http%3A//iterator.next)();

  

if (key.isAcceptable()) {

ServerSocketChannel serverSocketChannel = (ServerSocketChannel) [key.channel](https://link.zhihu.com/?target=http%3A//key.channel)();

// get socket channel from server socket channel

SocketChannel clientChannel = serverSocketChannel.accept();

// must to be nonblocking before register with selector

clientChannel.configureBlocking(false);

// register socket channel to selector with OP\_READ

clientChannel.register(key.selector(), SelectionKey.OP\_READ);

}

  

if (key.isReadable()) {

// read bytes from socket channel to byte buffer

SocketChannel clientChannel = (SocketChannel) [key.channel](https://link.zhihu.com/?target=http%3A//key.channel)();

ByteBuffer readBuffer = ByteBuffer.allocate(10);

int readBytes = [clientChannel.read](https://link.zhihu.com/?target=http%3A//clientChannel.read)(readBuffer);

if (readBytes == -1) {

System.out.println("closed.......");

clientChannel.close();

} else if (readBytes > 0) {

String s = new String(readBuffer.array());

System.out.println("Client said: " + s);

if (s.trim().equals("Hello")) {

// attachment is content used to write

key.interestOps(SelectionKey.OP\_WRITE);

key.attach("Welcome!!!");

}

}

}

  

if (key.isValid() && key.isWritable()) {

SocketChannel clientChannel = (SocketChannel) [key.channel](https://link.zhihu.com/?target=http%3A//key.channel)();

// get content from attachment

String content = (String) key.attachment();

// write content to socket channel

clientChannel.write(ByteBuffer.wrap(content.getBytes()));

key.interestOps(SelectionKey.OP\_READ);

}

  

// remove handled key from selected keys

iterator.remove();

}

}

} catch (IOException e) {

e.printStackTrace();

} finally {

// close selector

if (selector != null) {

try {

selector.close();

} catch (IOException e) {

e.printStackTrace();

}

}

}

}

}

第一步，创建 Selector 实例。

第二步，创建 ServerSocketChannel 实例，配置为非阻塞模式，绑定本地端口。

第三步，把 ServerSocketChannel实例 注册到 Selector 实例中。

第四步，选择一些准备好 I/O 操作的信道，这里设置了3秒超时时间，也就是阻塞3秒。

第五步，获取选中的 SelectionKey 的集合。

第六步，处理 SelectionKey 的感兴趣的操作。注册到 selector 中的 serverSocketChannel 只能是 isAcceptable() ，因此通过它的 accept() 方法，我们可以获取到客户端的请求 SocketChannel 实例，然后再把这个 socketChannel 注册到 selector 中，设置为可读的操作。那么下次遍历 selectionKeys 的时候，就可以处理那么可读的操作。