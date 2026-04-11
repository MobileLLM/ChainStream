# Java Listener 回调机制设计文档

## 问题描述

当前系统中，Java Agent通过gRPC向Python Runtime注册Stream Listener时，只传递了listener的名称，没有实际的执行能力。需要实现真正的Java函数回调机制。

## 架构设计

### 方案选择

经过分析，采用 **Java端启动HTTP/Socket服务** 的方案：

1. **Java Agent启动时**：在一个独立线程中启动简单的HTTP服务器（如使用Sun HttpServer）
2. **注册Listener时**：将HTTP服务的地址和端口通过gRPC传递给Python
3. **调用Listener时**：Python通过HTTP POST请求调用Java的listener
4. **返回结果**：Java通过HTTP响应返回处理结果

### 为什么不使用其他方案

- **gRPC双向流**：需要重新设计proto，改动较大
- **stdin/stdout**：不适合双向异步通信
- **共享内存/文件**：跨平台兼容性问题
- **新的gRPC Server**：需要动态端口分配，复杂度高
- **HTTP服务器**：✅ 简单、可靠、跨平台

## 实现步骤

### 1. Proto扩展（已完成）

```protobuf
message ForEachRequest {
    string stream_id = 1;
    string agent_id = 2;
    string listener_function_name = 3;
    string listener_id = 4;
    string callback_address = 5;  // 新增：Java HTTP服务地址
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

### 2. Java端实现

#### 2.1 HTTP Listener服务器

```java
public class ListenerHttpServer {
    private HttpServer server;
    private Map<String, StreamListener> listenerRegistry;
    private int port;
    
    public ListenerHttpServer(int port) throws IOException {
        this.port = port;
        this.listenerRegistry = new ConcurrentHashMap<>();
        this.server = HttpServer.create(new InetSocketAddress(port), 0);
        this.server.createContext("/invoke", this::handleInvoke);
        this.server.setExecutor(Executors.newFixedThreadPool(4));
    }
    
    public void start() {
        server.start();
        logger.info("Listener HTTP Server started on port: " + port);
    }
    
    public void registerListener(String listenerId, StreamListener listener) {
        listenerRegistry.put(listenerId, listener);
    }
    
    private void handleInvoke(HttpExchange exchange) throws IOException {
        if (!"POST".equals(exchange.getRequestMethod())) {
            exchange.sendResponseHeaders(405, 0);
            exchange.close();
            return;
        }
        
        try {
            // 读取请求体
            String requestBody = new String(exchange.getRequestBody().readAllBytes());
            JSONObject request = new JSONObject(requestBody);
            
            String listenerId = request.getString("listener_id");
            String itemData = request.getString("item_data");
            
            // 查找listener
            StreamListener listener = listenerRegistry.get(listenerId);
            if (listener == null) {
                sendError(exchange, "Listener not found: " + listenerId);
                return;
            }
            
            // 执行listener
            listener.onItem(itemData);
            
            // 返回结果（目前listener是void，所以没有返回值）
            JSONObject response = new JSONObject();
            response.put("success", true);
            response.put("has_result", false);
            
            sendResponse(exchange, response.toString());
            
        } catch (Exception e) {
            logger.error("Error handling invoke request", e);
            sendError(exchange, e.getMessage());
        }
    }
    
    private void sendResponse(HttpExchange exchange, String response) throws IOException {
        byte[] bytes = response.getBytes("UTF-8");
        exchange.sendResponseHeaders(200, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }
    
    private void sendError(HttpExchange exchange, String error) throws IOException {
        JSONObject response = new JSONObject();
        response.put("success", false);
        response.put("error", error);
        sendResponse(exchange, response.toString());
    }
}
```

#### 2.2 Agent基类修改

```java
public abstract class Agent {
    protected String agentId;
    protected ChainStreamGrpcClient grpcClient;
    protected ListenerHttpServer listenerServer;
    private int listenerPort;
    
    public Agent(String agentId) {
        this.agentId = agentId != null ? agentId : 
            System.getProperty("chainstream.agent.id", generateAgentId());
        
        // 初始化gRPC客户端
        this.grpcClient = new ChainStreamGrpcClient("localhost", 50051);
        
        // 启动HTTP服务器用于listener回调
        this.listenerPort = findAvailablePort();
        try {
            this.listenerServer = new ListenerHttpServer(listenerPort);
            this.listenerServer.start();
        } catch (IOException e) {
            logger.error("Failed to start listener server", e);
        }
        
        // 向Python报告agent ID和listener服务地址
        reportAgentId();
    }
    
    private int findAvailablePort() {
        try (ServerSocket socket = new ServerSocket(0)) {
            return socket.getLocalPort();
        } catch (IOException e) {
            return 8000 + new Random().nextInt(1000);
        }
    }
    
    protected String getListenerCallbackAddress() {
        return "http://localhost:" + listenerPort;
    }
}
```

#### 2.3 Stream.forEach修改

```java
public Stream forEach(StreamListener listener) {
    // 生成唯一的listener ID
    String listenerId = UUID.randomUUID().toString();
    String listenerName = listener.getClass().getSimpleName();
    
    // 注册到本地服务器
    listenerServer.registerListener(listenerId, listener);
    
    // 调用gRPC注册，传递回调地址
    ChainstreamBridge.ForEachResponse response = grpcClient.forEach(
        streamId, agentId, listenerName, listenerId, 
        agent.getListenerCallbackAddress()
    );
    
    if (response.getSuccess()) {
        logger.info("Stream listener registered: " + listenerId);
        return new Stream(response.getAnonymousStreamId(), agentId, grpcClient);
    } else {
        logger.warning("Failed to register listener: " + response.getError());
        return this;
    }
}
```

### 3. Python端实现（已部分完成）

#### 3.1 JavaListenerFunction修改

```python
class JavaListenerFunction:
    def __init__(self, agent, listener_id, listener_name, callback_address):
        self.agent = agent
        self.listener_id = listener_id
        self.listener_name = listener_name
        self.callback_address = callback_address  # HTTP地址
        self.func_id = f"java_listener_{listener_id}"
        self.is_java_listener = True
        self._output_stream = None
        
    def __call__(self, item):
        try:
            # 序列化item
            if isinstance(item, str):
                item_json = item
            elif isinstance(item, dict):
                item_json = json.dumps(item)
            else:
                item_json = str(item)
            
            # 通过HTTP调用Java listener
            import requests
            response = requests.post(
                f"{self.callback_address}/invoke",
                json={
                    "listener_id": self.listener_id,
                    "item_data": item_json
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    if result.get('has_result') and result.get('result_data'):
                        # 有返回值，添加到输出流
                        if self._output_stream:
                            self._output_stream.add_item(result['result_data'])
                        return result['result_data']
                else:
                    logger.error(f"Java listener error: {result.get('error')}")
            else:
                logger.error(f"HTTP error {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error invoking Java listener: {e}")
        
        return None
```

#### 3.2 gRPC Server ForEach修改

```python
def ForEach(self, request: ForEachRequest, context):
    listener_id = request.listener_id
    callback_address = request.callback_address  # HTTP地址
    
    # 创建Java Listener包装器
    java_listener = JavaListenerFunction(
        agent=java_agent_proxy,
        listener_id=listener_id,
        listener_name=request.listener_function_name,
        callback_address=callback_address
    )
    
    # 注册到stream
    anonymous_stream = stream.for_each(java_listener)
    
    return ForEachResponse(
        success=True, 
        error="", 
        anonymous_stream_id=anonymous_stream.stream_id
    )
```

## 优势

1. **简单可靠**：HTTP是成熟的协议
2. **无需修改现有gRPC架构**：只是增量添加
3. **易于调试**：可以用curl测试
4. **跨语言兼容**：HTTP是通用协议

## 待完成工作

1. ✅ Proto定义扩展
2. ✅ JavaListenerFunction Python实现
3. ✅ grpc_server.py ForEach修改
4. ⏳ Java HTTP服务器实现
5. ⏳ Java Agent基类集成
6. ⏳ 端到端测试

## 下一步

建议用户决定：
1. 是否采用此HTTP方案
2. 是否需要我继续完成Java端代码
3. 是否有其他架构偏好


