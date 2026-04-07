# Java Listener 回调功能实现文档

## 📋 实现概述

本次实现了**方案A1: gRPC双Server模式**，使Python能够真正调用Java的listener函数，实现完整的双向通信。

---

## 🏗️ 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ChainStream 双向通信架构                          │
└─────────────────────────────────────────────────────────────────────┘

Python Runtime                           Java Agent
┌──────────────────┐                    ┌──────────────────┐
│  gRPC Server     │                    │  gRPC Client     │
│  (port 50051)    │◄───────────────────┤  (调用Python)     │
│                  │  1. CreateStream   │                  │
│  - CreateStream  │  2. ForEach注册     │  Agent.java      │
│  - GetStream     │  3. AddItem        │  ├─ callbackSrv  │
│  - ForEach       │                    │  └─ listeners    │
│  - AddItem       │                    │                  │
└──────────────────┘                    └──────────────────┘
         │                                       │
         │                                       │
         │  4. 当item到达时调用                   │
         ▼                                       ▼
┌──────────────────┐                    ┌──────────────────┐
│ JavaListener     │    gRPC回调         │ Callback Server  │
│ Function         ├────────────────────►│  (dynamic port)  │
│                  │ InvokeListener      │                  │
│  - agent_id      │                    │  - 管理listeners  │
│  - listener_id   │                    │  - 执行Java代码   │
│  - callback_addr │                    │  - 返回结果       │
└──────────────────┘                    └──────────────────┘

   Python gRPC Client                        Java gRPC Server
```

### 通信流程

1. **Java Agent启动**
   - Java Agent构造函数初始化`JavaAgentCallbackServer`
   - 服务器监听动态端口（自动分配）
   - 将callback地址设置到Runtime中

2. **注册Listener**
   - Java调用`stream.forEach(listener)`
   - Java生成唯一的`listener_id`
   - 将listener注册到本地callbackServer
   - 通过gRPC向Python发送ForEachRequest，包含：
     - stream_id
     - agent_id
     - listener_function_name
     - listener_id
     - **callback_address** (新增)

3. **Python端处理**
   - Python收到ForEachRequest
   - 创建`JavaListenerFunction`包装器
   - 包装器内部创建`JavaCallbackClient`连接到Java Server
   - 将包装器注册到Python的Stream

4. **回调执行**
   - 当Stream有新item时，Python调用`JavaListenerFunction`
   - `JavaListenerFunction`通过gRPC Client调用Java的`InvokeListener`
   - Java的`JavaAgentCallbackServer`收到请求
   - 根据`listener_id`查找并执行对应的Java listener
   - 返回结果给Python

---

## 📁 代码结构

### Proto定义

**文件**: `chainstream/runtime/java/proto/chainstream_bridge.proto`

```protobuf
// Python端作为Server
service ChainStreamBridge {
    rpc ForEach(ForEachRequest) returns (ForEachResponse);
    // ... 其他RPC
}

// Java端作为Server (新增)
service JavaAgentCallback {
    rpc InvokeListener(InvokeListenerRequest) returns (InvokeListenerResponse);
}

message ForEachRequest {
    string stream_id = 1;
    string agent_id = 2;
    string listener_function_name = 3;
    string listener_id = 4;
    string callback_address = 5;  // 新增字段
}

message InvokeListenerRequest {
    string agent_id = 1;
    string listener_id = 2;
    string item_data = 3;
}

message InvokeListenerResponse {
    bool success = 1;
    string error = 2;
    string result_data = 3;
    bool has_result = 4;
}
```

### Python端实现

#### 1. `java_callback_client.py` (新文件)
- **作用**: Python的gRPC客户端，用于调用Java Server
- **主要方法**:
  - `__init__(callback_address)`: 建立连接
  - `invoke_listener(agent_id, listener_id, item_data)`: 调用Java listener
  - `close()`: 关闭连接

#### 2. `java_listener_function.py` (更新)
- **作用**: Java listener的Python包装器
- **关键变更**:
  - 构造函数接受`callback_address`而非`grpc_client`
  - 内部创建`JavaCallbackClient`实例
  - `__call__`方法调用`_grpc_client.invoke_listener`
  - 支持`set_output_stream`用于链式调用

#### 3. `grpc_server.py` (更新)
- **ForEach方法变更**:
  - 从请求中提取`callback_address`
  - 验证callback_address是否存在
  - 创建`JavaListenerFunction`时传入callback_address
  - 简化了实现，不再需要查找JavaAgentWrapper

### Java端实现

#### 1. `JavaAgentCallbackServer.java` (新文件)
- **位置**: `com.chainstream.callback.JavaAgentCallbackServer`
- **作用**: Java端的gRPC服务器
- **主要功能**:
  - 自动分配可用端口
  - 管理listener注册表`Map<String, StreamListener>`
  - 实现`invokeListener` RPC方法
  - 根据`listener_id`查找并执行listener

```java
public class JavaAgentCallbackServer extends JavaAgentCallbackGrpc.JavaAgentCallbackImplBase {
    private final Map<String, Stream.StreamListener> listenerRegistry;
    
    @Override
    public void invokeListener(InvokeListenerRequest request, 
                               StreamObserver<InvokeListenerResponse> responseObserver) {
        // 1. 根据listener_id查找listener
        // 2. 调用listener.onItem(itemData)
        // 3. 返回结果
    }
}
```

#### 2. `Agent.java` (更新)
- **构造函数变更**:
  - 创建`JavaAgentCallbackServer`实例
  - 启动callback server
  - 将server引用和地址设置到Runtime

```java
public Agent() {
    // ... agent_id初始化
    
    // 初始化callback server
    this.callbackServer = new JavaAgentCallbackServer();
    this.callbackServer.start();
    this.runtime.setCallbackAddress(this.callbackServer.getAddress());
    this.runtime.setCallbackServer(this.callbackServer);
}
```

#### 3. `Runtime.java` (更新)
- **新增字段和方法**:
  - `callbackAddress`: 存储callback地址
  - `callbackServer`: 存储server引用
  - `setCallbackAddress()`, `getCallbackAddress()`
  - `setCallbackServer()`, `getCallbackServer()`

#### 4. `Stream.java` (更新)
- **forEach方法变更**:
  - 生成唯一的`listener_id`（包含时间戳）
  - 从Runtime获取`callback_address`和`callbackServer`
  - 将listener注册到callbackServer
  - 调用gRPC Client的forEach，传递所有参数

```java
public Stream forEach(StreamListener listener) {
    String listenerId = agentId + "_" + streamId + "_" + 
                        listenerFunctionName + "_" + System.currentTimeMillis();
    
    Runtime runtime = Runtime.getInstance();
    String callbackAddress = runtime.getCallbackAddress();
    
    JavaAgentCallbackServer callbackServer = runtime.getCallbackServer();
    callbackServer.registerListener(listenerId, listener);
    
    ForEachResponse response = grpcClient.forEach(
        streamId, agentId, listenerFunctionName, listenerId, callbackAddress
    );
    // ...
}
```

#### 5. `ChainStreamGrpcClient.java` (更新)
- **forEach方法签名变更**:
  - 新增`listenerId`和`callbackAddress`参数
  - 构建ForEachRequest时包含这两个字段

---

## ✅ 实现完成清单

- [x] 扩展proto定义，添加JavaAgentCallback服务
- [x] Python端：添加Java gRPC Client (`java_callback_client.py`)
- [x] Python端：更新JavaListenerFunction使用gRPC Client
- [x] Java端：实现JavaAgentCallback gRPC Server
- [x] Java端：Agent启动时初始化gRPC Server
- [x] Java端：更新forEach传递callback地址
- [x] 重新编译proto生成代码（Python + Java）
- [x] Maven编译成功

---

## 🧪 测试说明

### 测试文件
`test_java_listener_callback.py`

### 测试流程
1. 初始化Python Runtime
2. 启动Java Agent (`DebugListenHelloAgent`)
3. 等待Java Agent完全初始化（包括callback server）
4. 从Python向`debug_hello_stream`添加数据
5. 观察Java端是否收到回调并执行listener

### 预期结果
Java控制台应该输出：
```
Received before batch: Hello from Python Test 1
Received before batch: Hello from Python Test 2
Received before batch: Hello from Python Test 3
```

---

## 🔍 关键点说明

### 1. 端口管理
- Java的callback server使用动态端口（自动分配）
- 通过`ServerSocket(0)`实现
- 端口号通过callback_address传递给Python

### 2. Listener ID生成
- 格式：`{agent_id}_{stream_id}_{listener_name}_{timestamp}`
- 时间戳确保唯一性，支持同一listener多次注册

### 3. 数据序列化
- Python → Java: JSON字符串
- Java端收到的`item_data`是String类型
- Java listener需要自己解析数据

### 4. 返回值处理
- 当前`StreamListener.onItem`返回void
- 如果未来需要返回值，可以修改接口为`Object onItem(Object item)`
- Python端已经支持处理返回值（`has_result`和`result_data`字段）

### 5. 错误处理
- 网络错误：gRPC会抛出`StatusRuntimeException`
- Listener不存在：返回`success=false`的响应
- 所有错误都会记录日志

---

## 📊 性能考虑

1. **gRPC开销**: 每次listener调用需要一次网络往返
2. **适用场景**: 适合中低频率的回调（< 1000次/秒）
3. **优化方向**: 如果需要极高性能，考虑批量调用或共享内存

---

## 🚀 后续改进

1. **连接池**: 复用gRPC连接，避免重复创建
2. **异步调用**: 使用gRPC的异步API提高并发性能
3. **超时控制**: 添加可配置的调用超时
4. **重试机制**: 网络失败时自动重试
5. **监控指标**: 添加回调成功率、延迟等监控

---

## 📝 注意事项

1. **Proto版本一致性**: 确保Python和Java使用同一个proto文件
2. **端口冲突**: Callback server使用动态端口，避免冲突
3. **生命周期管理**: Agent停止时要正确关闭callback server
4. **线程安全**: listenerRegistry使用ConcurrentHashMap保证线程安全

---

## 🎉 总结

通过gRPC双Server模式，我们实现了：
- ✅ Python可以真正调用Java的listener函数
- ✅ 支持双向通信，架构清晰
- ✅ 性能足够好（适合大部分场景）
- ✅ 易于调试和维护
- ✅ 可扩展性强

这个实现为ChainStream的Java Agent提供了完整的Stream处理能力！



