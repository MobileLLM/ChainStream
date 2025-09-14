# ChainStream Java API 完整文档

## 概述

本文档描述了ChainStream Java Runtime的完整API，这些API通过gRPC与Python Runtime通信，实现了完整的ChainStream功能。

## 核心类

### 1. Agent (com.chainstream.runtime.Agent)

所有Java Agent的基类，需要继承此类。

#### 构造函数
```java
public Agent(String agentId)
```

#### 抽象方法
```java
public abstract void start()    // 启动Agent
public abstract void stop()     // 停止Agent
```

#### 受保护方法
```java
// Stream操作
protected Stream getStream(String streamId)
protected Stream createStream(String streamId, String description)

// LLM操作
protected LLM getModel(String... types)
protected String makePrompt(String... promptParts)

// Buffer操作
protected Buffer createBuffer()

// Agent生命周期
protected boolean startAgent()
protected boolean stopAgent()
```

### 2. Stream (com.chainstream.runtime.Stream)

数据流处理类，提供流式数据处理功能。

#### 构造函数
```java
public Stream(String streamId, String agentId, ChainStreamGrpcClient grpcClient)
```

#### 主要方法
```java
// 挂载监听函数
public Stream forEach(StreamListener listener)

// 批次切分
public Stream batch(Integer byCount, Integer byTime, String byItem, String byFuncName)
public Stream batchByCount(int count)      // 按数量切分
public Stream batchByTime(int seconds)     // 按时间切分
public Stream batchByItem(String item)     // 按键值切分
public Stream batchByFunc(String funcName) // 按函数切分

// 注销监听器
public void unregisterAll()

// 添加数据
public void addItem(Object item)

// 获取Stream ID
public String getStreamId()
```

#### 监听器接口
```java
@FunctionalInterface
public interface StreamListener {
    void onItem(Object item);
}
```

### 3. LLM (com.chainstream.runtime.LLM)

大语言模型类，提供LLM查询功能。

#### 构造函数
```java
public LLM(String modelId, String agentId, ChainStreamGrpcClient grpcClient)
```

#### 主要方法
```java
// 查询LLM
public String query(String prompt)

// 获取模型ID
public String getModelId()
```

### 4. Buffer (com.chainstream.runtime.Buffer)

数据容器类，提供队列式数据存储功能。

#### 构造函数
```java
public Buffer(String bufferId, String agentId, ChainStreamGrpcClient grpcClient)
```

#### 主要方法
```java
// 添加数据
public void append(Object data)

// 取出队首数据
public String pop()

// 取出所有数据
public List<String> popAll()

// 获取Buffer ID
public String getBufferId()
```

### 5. Runtime (com.chainstream.runtime.Runtime)

Runtime单例类，提供全局访问点。

#### 获取实例
```java
public static Runtime getInstance()
```

#### 主要方法
```java
// 设置Agent ID
public void setAgentId(String agentId)

// Stream操作
public Stream getStream(String streamId)
public Stream createStream(String streamId, String description)

// LLM操作
public LLM getModel(String... types)
public String makePrompt(String... promptParts)

// Buffer操作
public Buffer createBuffer()

// Runtime信息
public String getRuntimeInfo()

// Agent生命周期
public boolean startAgent()
public boolean stopAgent()

// 关闭Runtime
public void shutdown()
```

## gRPC API

### ChainStreamGrpcClient

gRPC客户端类，负责与Python Runtime通信。

#### 主要方法

**Agent生命周期**
```java
public StartAgentResponse startAgent(String agentId)
public StopAgentResponse stopAgent(String agentId)
```

**Stream操作**
```java
public CreateStreamResponse createStream(String streamId, String description, String agentId)
public GetStreamResponse getStream(String streamId, String agentId)
public AddItemResponse addItem(String streamId, String item, String agentId)
public ForEachResponse forEach(String streamId, String agentId, String listenerFunctionName)
public BatchResponse batch(String streamId, String agentId, Integer byCount, Integer byTime, String byItem, String byFuncName)
public UnregisterAllResponse unregisterAll(String streamId, String agentId)
```

**LLM操作**
```java
public QueryLLMResponse queryLLM(String prompt, String modelType, String agentId)
public GetModelResponse getModel(String agentId, String... modelTypes)
public MakePromptResponse makePrompt(String agentId, String... promptParts)
public GetModelInfoResponse getModelInfo(String modelType)
```

**Buffer操作**
```java
public CreateBufferResponse createBuffer(String agentId)
public BufferAppendResponse bufferAppend(String bufferId, String agentId, String data)
public BufferPopResponse bufferPop(String bufferId, String agentId)
public BufferPopAllResponse bufferPopAll(String bufferId, String agentId)
```

**Runtime信息**
```java
public GetRuntimeInfoResponse getRuntimeInfo(String agentId)
```

## 使用示例

### 简单Agent示例

```java
public class SimpleAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    
    public SimpleAgent() {
        super("simple_agent");
    }
    
    @Override
    public void start() {
        // 创建输出流
        outputStream = createStream("output_stream", "Simple agent output");
        
        // 获取LLM模型
        llm = getModel("text");
        
        // 简单的处理逻辑
        String result = llm.query("Hello from Java Agent!");
        outputStream.addItem(result);
    }
    
    @Override
    public void stop() {
        // 清理资源
    }
}
```

### 完整Agent示例

```java
public class CompleteAgent extends Agent {
    private Stream inputStream;
    private Stream outputStream;
    private LLM llm;
    private Buffer buffer;
    
    public CompleteAgent() {
        super("complete_agent");
    }
    
    @Override
    public void start() {
        // 创建Stream
        inputStream = createStream("input_stream", "Input data stream");
        outputStream = createStream("output_stream", "Output data stream");
        
        // 获取LLM模型
        llm = getModel("text", "image", "audio");
        
        // 创建Buffer
        buffer = createBuffer();
        
        // 设置监听器
        inputStream.forEach(item -> {
            // 处理数据
            buffer.append(item);
            String processed = processData(item.toString());
            outputStream.addItem(processed);
        });
        
        // 批次处理
        Stream batchStream = inputStream.batchByCount(5);
        batchStream.forEach(batch -> {
            // 处理批次数据
        });
    }
    
    @Override
    public void stop() {
        // 注销监听器
        inputStream.unregisterAll();
        outputStream.unregisterAll();
    }
    
    private String processData(String data) {
        String prompt = makePrompt("Process: ", data);
        return llm.query(prompt);
    }
}
```

## 与Python API的对应关系

| Java API | Python API | 说明 |
|----------|------------|------|
| `getStream(streamId)` | `chainstream.get_stream(agent, stream_id)` | 获取Stream |
| `createStream(streamId, description)` | `chainstream.create_stream(agent, stream_id)` | 创建Stream |
| `forEach(listener)` | `stream.for_each(listener_func)` | 挂载监听函数 |
| `batchByCount(count)` | `stream.batch(by_count=count)` | 按数量批次切分 |
| `batchByTime(seconds)` | `stream.batch(by_time=seconds)` | 按时间批次切分 |
| `batchByItem(item)` | `stream.batch(by_item=item)` | 按键值批次切分 |
| `batchByFunc(funcName)` | `stream.batch(by_func=func)` | 按函数批次切分 |
| `unregisterAll()` | `stream.unregister_all(agent)` | 注销所有监听器 |
| `addItem(item)` | `stream.add_item(item)` | 添加数据 |
| `getModel(types)` | `chainstream.llm.get_model(types)` | 获取LLM模型 |
| `makePrompt(parts)` | `chainstream.llm.make_prompt(parts)` | 制作Prompt |
| `query(prompt)` | `llm.query(prompt)` | 查询LLM |
| `createBuffer()` | `chainstream.context.Buffer()` | 创建Buffer |
| `append(data)` | `buffer.append(data)` | 添加数据 |
| `pop()` | `buffer.pop()` | 取出队首数据 |
| `popAll()` | `buffer.pop_all()` | 取出所有数据 |

## 注意事项

1. **Agent ID**: 所有操作都需要Agent ID，确保在创建Agent时设置正确的ID。

2. **gRPC连接**: 默认连接到localhost:50051，确保Python Runtime的gRPC服务器正在运行。

3. **错误处理**: 所有gRPC调用都包含错误处理，检查返回值的success字段。

4. **资源清理**: 在stop()方法中正确清理资源，包括注销监听器和清空Buffer。

5. **线程安全**: Runtime是单例模式，但Stream、LLM、Buffer实例不是线程安全的。

6. **数据类型**: 所有数据都以字符串形式传输，复杂对象需要序列化。

## 编译和运行

### 编译
```bash
mvn compile
```

### 运行示例
```bash
# 运行简单Agent
java -cp target/classes com.chainstream.examples.SimpleAgent

# 运行完整Agent
java -cp target/classes com.chainstream.examples.CompleteAgent
```

### 依赖
- JDK 8+
- gRPC Java库
- Protocol Buffers Java库

## 总结

ChainStream Java API提供了与Python API完全对等的功能，通过gRPC实现了Java Agent与Python Runtime的无缝集成。所有API都经过精心设计，保持了与Python版本的一致性，同时充分利用了Java的面向对象特性。
