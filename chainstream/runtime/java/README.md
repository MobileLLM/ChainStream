# ChainStream Java Runtime

这是ChainStream的Java运行时环境，允许您使用Java编写Agent并与Python Runtime进行通信。

## 架构概述

```
Java Agent Code
       │
       ▼
Java Libraries (API Wrapper)
       │
       ▼
gRPC Client
       │
       ▼
gRPC Server (Python)
       │
       ▼
Python Runtime Core
```

## 快速开始

### 1. 安装依赖

运行安装脚本：

```bash
./install_dependencies.sh
```

或者手动安装：

```bash
# 安装Maven
brew install maven  # macOS
# 或
sudo apt-get install maven  # Ubuntu

# 安装Python gRPC依赖
pip install grpcio grpcio-tools
```

### 2. 编译项目

使用Maven：
```bash
mvn clean compile
```

或使用Gradle：
```bash
gradle build
```

### 3. 运行示例Agent

使用Maven：
```bash
mvn exec:java -Dexec.mainClass="com.chainstream.agent.SimpleAgent"
```

或使用Gradle：
```bash
gradle runAgent
```

## 项目结构

```
src/main/java/com/chainstream/
├── agent/
│   ├── Agent.java          # Agent基类
│   └── SimpleAgent.java    # 示例Agent
├── runtime/
│   ├── Runtime.java        # Runtime主类
│   ├── Stream.java         # Stream类
│   └── LLM.java           # LLM类
└── grpc/
    └── ChainStreamGrpcClient.java  # gRPC客户端
```

## 编写Java Agent

### 1. 继承Agent基类

```java
package com.chainstream.agent;

import com.chainstream.runtime.Stream;
import com.chainstream.runtime.LLM;

public class MyAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    
    public MyAgent() {
        super("my_agent");
    }
    
    @Override
    public void start() {
        // 创建输出流
        outputStream = createStream("output", "My agent output");
        
        // 获取LLM模型
        llm = getModel("text");
        
        // 处理逻辑
        String result = llm.query("Hello from my agent!");
        outputStream.addItem(result);
    }
    
    @Override
    public void stop() {
        // 清理资源
    }
    
    public static void main(String[] args) {
        MyAgent agent = new MyAgent();
        agent.start();
        
        // 保持运行
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            agent.stop();
        }
    }
}
```

### 2. 使用Stream

```java
// 创建Stream
Stream stream = createStream("my_stream", "Description");

// 添加监听器
stream.forEach(item -> {
    System.out.println("Received: " + item);
});

// 添加项目
stream.addItem("Hello World");
```

### 3. 使用LLM

```java
// 获取LLM模型
LLM llm = getModel("text");

// 查询LLM
String response = llm.query("What is the weather like?");
System.out.println("LLM Response: " + response);
```

## gRPC通信

Java Agent通过gRPC与Python Runtime通信：

- **Protocol Buffers**: 定义通信协议
- **gRPC Client**: Java端客户端
- **gRPC Server**: Python端服务器

### 支持的gRPC服务

- `StartAgent` / `StopAgent`: Agent生命周期管理
- `CreateStream` / `GetStream`: Stream操作
- `AddItem`: 向Stream添加数据
- `QueryLLM`: LLM查询
- `GetModelInfo`: 获取模型信息
- `GetRuntimeInfo`: 获取运行时信息

## 配置

### gRPC服务器地址

默认连接到 `localhost:50051`，可以通过修改 `ChainStreamGrpcClient` 构造函数来更改。

### 日志配置

使用Java标准日志框架，可以通过 `logging.properties` 文件配置日志级别。

## 故障排除

### 1. 编译错误

确保安装了正确的Java版本（JDK 11+）和Maven。

### 2. gRPC连接错误

确保Python gRPC服务器正在运行：
```bash
python grpc_server.py
```

### 3. 依赖问题

运行 `mvn dependency:resolve` 检查依赖是否正确下载。

## 开发指南

### 添加新的gRPC服务

1. 修改 `proto/chainstream_bridge.proto`
2. 重新生成Java代码：`mvn clean compile`
3. 在 `ChainStreamGrpcClient` 中添加新方法
4. 在相应的Runtime类中暴露新功能

### 调试

使用Java调试器：
```bash
mvn exec:java -Dexec.mainClass="com.chainstream.agent.SimpleAgent" -Dexec.args="-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=y,address=5005"
```

## 许可证

与ChainStream主项目相同的许可证。
