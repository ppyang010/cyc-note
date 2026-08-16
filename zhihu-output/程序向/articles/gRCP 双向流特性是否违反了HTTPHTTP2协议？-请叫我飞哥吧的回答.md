---
id: "3488830123"
title: "gRCP 双向流特性是否违反了HTTP/HTTP2协议？"
author: "请叫我飞哥吧"
type: zhihu-answer
source: "https://www.zhihu.com/question/51048473/answer/3488830123"
created: "2024-05-06 10:19"
updated: "2024-05-06 10:19"
collected: "2024-05-06 10:19"
downloaded: "2026-08-16"
---
## 学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？

## 1、概述

gRPC的长连接实现基于HTTP/2协议，HTTP/2本身支持持久连接（persistent connections），允许在一个TCP连接上进行多个请求和响应的交换，从而避免了传统HTTP/1.x中为每个请求建立和关闭连接所带来的延迟和资源消耗。

在gRPC中，长连接的实现原理主要包括以下几个方面：

1.  **HTTP/2多路复用**：HTTP/2协议引入了多路复用技术，允许在一个TCP连接上并发处理多个请求和响应流，每个流都有唯一的标识符，这样就可以在一个连接上同时进行多次RPC调用。
2.  **流式传输**：gRPC定义了四种调用类型，其中两种（服务器流式和双向流式）涉及长连接的维持。在服务器流式RPC中，客户端发出一个请求后，服务器可以在单个连接上连续发送多个响应。在双向流式RPC中，客户端和服务器都可以发送多个请求和响应。
3.  **连接管理**：gRPC底层使用HTTP/2的特性来进行连接管理和心跳机制，确保连接的稳定性和可靠性。例如，服务端可以通过PING帧来检查连接是否存活，客户端也需要能够正确处理GOAWAY帧以便重新连接或恢复丢失的流。
4.  **Keepalive机制**：gRPC框架通常内置了keepalive探测功能，用来定期在空闲的长连接上发送ping帧以检测连接的有效性。当服务器或客户端长时间没有活动时，可以通过这种方式防止中间设备过早关闭连接。
5.  **错误重连**：在长连接中断的情况下，gRPC客户端通常会尝试自动重连至服务端，尤其是针对非临时性故障导致的连接断开。

  

## 2、代码示例

## 2.1、服务端

```java
syntax = "proto3";

package com.example.grpc;

service LongRunningConnection {
  rpc BidirectionalChat(stream ChatMessage) returns (stream ChatMessage) {}
}

message ChatMessage {
  string message = 1;
}
```

  

```java
// 导入必要的gRPC和自定义消息包
import io.grpc.stub.StreamObserver;
import com.example.grpc.LongRunningConnectionGrpc;
import com.example.grpc.ChatMessage;

// 定义服务端实现类
public class LongRunningConnectionService extends LongRunningConnectionGrpc.LongRunningConnectionImplBase {

    // 实现bidirectionalChat方法，这是我们在.proto文件中定义的双向流式RPC方法
    @Override
    public StreamObserver<ChatMessage> bidirectionalChat(StreamObserver<ChatMessage> responseObserver) {
        // 返回一个新的StreamObserver，每当客户端发送消息时，它将被调用
        return new StreamObserver<ChatMessage>() {
            // 当客户端发送一个ChatMessage时，此方法会被调用
            @Override
            public void onNext(ChatMessage request) {
                // 打印接收到的消息
                System.out.println("Received from client: " + request.getMessage());
                
                // 创建一个回复消息，并转发回客户端
                ChatMessage reply = ChatMessage.newBuilder().setMessage("Server replied: " + request.getMessage()).build();
                responseObserver.onNext(reply);
            }

            // 如果在处理过程中发生错误，此方法被调用
            @Override
            public void onError(Throwable t) {
                System.err.println("Error occurred: " + t.getMessage());
                // 将错误传播回客户端
                responseObserver.onError(t);
            }

            // 当客户端关闭连接或者调用了onCompleted时，此方法被调用
            @Override
            public void onCompleted() {
                System.out.println("Client closed the connection.");
                // 在关闭连接前发送一条结束消息
                ChatMessage endMessage = ChatMessage.newBuilder().setMessage("Session ended.").build();
                responseObserver.onNext(endMessage);
                // 通知服务端已经发送完所有的响应并关闭了连接
                responseObserver.onCompleted();
            }
        };
    }
}
```

  

## 2.2、客户端

```java
// 导入必要的gRPC和自定义消息包
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import com.example.grpc.LongRunningConnectionGrpc;
import com.example.grpc.ChatMessage;
import java.util.concurrent.TimeUnit;

// 定义客户端类
public class LongRunningConnectionClient {

    // 成员变量，管理连接到服务器的通道
    private final ManagedChannel channel;
    // 块状（同步）stub，用于简单的请求/响应模式
    private final LongRunningConnectionGrpc.LongRunningConnectionBlockingStub blockingStub;
    // 异步stub，用于流式RPC调用
    private final LongRunningConnectionGrpc.LongRunningConnectionStub asyncStub;

    // 构造函数，初始化通道和stub
    public LongRunningConnectionClient(String host, int port) {
        // 创建一个新的ManagedChannel指向服务器
        channel = ManagedChannelBuilder.forAddress(host, port)
            .usePlaintext()
            .build();
        blockingStub = LongRunningConnectionGrpc.newBlockingStub(channel);
        asyncStub = LongRunningConnectionGrpc.newStub(channel);
    }

    // 方法启动双向聊天会话
    public void startBidirectionalChat() {
        // 创建一个用于发送消息到服务器的StreamObserver
        StreamObserver<ChatMessage> requestObserver = asyncStub.bidirectionalChat(new StreamObserver<ChatMessage>() {
            // 当接收到服务器的响应时，此方法被调用
            @Override
            public void onNext(ChatMessage value) {
                System.out.println("Received from server: " + value.getMessage());
            }

            // 如果在接收过程中发生错误，此方法被调用
            @Override
            public void onError(Throwable t) {
                System.err.println("Error during chat: " + t.getMessage());
            }

            // 当服务器关闭连接或完成了所有的响应时，此方法被调用
            @Override
            public void onCompleted() {
                System.out.println("Chat session completed.");
            }
        });

        try {
            // 发送一系列消息到服务器
            for (int i = 0; i < 10; i++) {
                ChatMessage message = ChatMessage.newBuilder().setMessage("Client message " + i).build();
                requestObserver.onNext(message);
                Thread.sleep(1000); // 模拟延迟
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            // 完成消息发送后，关闭客户端的发送流
            requestObserver.onCompleted();
        }
    }

    // 关闭连接并等待一段时间直到通道完全关闭
    public void shutdown() throws InterruptedException {
        channel.shutdown().awaitTermination(5, TimeUnit.SECONDS);
    }

    // 主入口点，用于运行客户端
    public static void main(String[] args) throws InterruptedException {
        // 创建客户端实例并连接到服务器
        LongRunningConnectionClient client = new LongRunningConnectionClient("localhost", 50051);
        // 开始双向聊天会话
        client.startBidirectionalChat();
        // 关闭连接
        client.shutdown();
    }
}
```

  

## 3、为什么介绍这个知识点？

Nacos 1.0版本和2.0版本在长连接实现原理是不一样的，主要区别体现：

**1、连接方式**：

-   **Nacos 1.x**：早期版本的Nacos使用HTTP 1.1短连接模拟长连接的方式，通过每30秒发送一次心跳来维持连接，与服务端进行配置一致性校验。客户端和服务端之间并不是真正意义上的长连接，而是频繁地进行心跳交互来保持配置同步。
-   **Nacos 2.x**：升级到2.0版本之后，Nacos摒弃了原有HTTP短连接模拟长连接的机制，转而采用gRPC长连接模型。gRPC原生支持双向流和长连接，这意味着客户端和服务器之间的连接可以长期保持打开状态，更加高效地进行数据交换和实时推送。

**2、性能和稳定性**：

-   **Nacos 1.x**：由于1.x版本的心跳机制和短连接模拟长连接，可能会造成较高的网络开销和CPU消耗，特别是在大规模客户端连接情况下，可能导致服务器压力增大。
-   **Nacos 2.x**：Nacos 2.0通过gRPC长连接极大提升了性能和稳定性，能够支撑更多的客户端连接，同时在连接数较大时CPU消耗较低，且连接状态的维护更为可靠，增强了系统的整体承载能力和响应速度。

**3、事件通知和感知**：

-   **Nacos 1.x**：在连接断开时，可能需要等待心跳续约超时才能发现并移除实例。
-   **Nacos 2.x**：新版Nacos改进了连接管理，当长连接断开时可以更快地感知到，并迅速作出反应。

  

  

  

## 最后：若此文于您有所裨益，不妨收藏于夹，留待日后细细品读，亦可在评论区留下您的感悟，共同交流学习之道。