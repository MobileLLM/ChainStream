# ChainStream Java Agent 使用指南

## 概述

ChainStream现在支持Java Agent的开发！Java Agent可以像Python Agent一样被ChainStream系统管理，享受相同的监控和管理功能。

## 快速开始

### 1. 创建Java Agent

在`AgentStore`目录下创建Java文件，例如`MyJavaAgent.java`：

```java
public class MyJavaAgent extends Agent {
    private Stream outputStream;
    private LLM llm;
    
    public MyJavaAgent() {
        super("my_java_agent");
    }
    
    @Override
    public void start() {
        System.out.println("MyJavaAgent starting...");
        
        // 创建输出流
        outputStream = createStream("output_stream", "My Java agent output");
        
        // 获取LLM模型
        llm = getModel("text");
        
        // 处理逻辑
        String result = llm.query("Hello from Java Agent!");
        outputStream.addItem(result);
        
        // 设置Stream监听器
        outputStream.forEach(item -> {
            System.out.println("Processing item: " + item);
        });
        
        System.out.println("MyJavaAgent started successfully!");
    }
    
    @Override
    public void stop() {
        System.out.println("MyJavaAgent stopping...");
        System.out.println("MyJavaAgent stopped");
    }
    
    public static void main(String[] args) {
        MyJavaAgent agent = new MyJavaAgent();
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

### 2. 启动ChainStream服务

```bash
# 设置Java环境（如果需要）
export JAVA_HOME=/path/to/java
export PATH=$JAVA_HOME/bin:$PATH

# 启动ChainStream服务
python start.py
```

### 3. 通过Web界面管理

1. 打开浏览器访问 `http://localhost:6677`
2. 在Agent管理页面中，你会看到Java Agent文件
3. 点击启动按钮启动Java Agent
4. 在监控页面中查看Java Agent的运行状态

## Java API

### Agent基类

```java
public abstract class Agent {
    protected String agentId;
    protected Runtime runtime;
    
    public Agent(String agentId);
    public abstract void start();
    public abstract void stop();
    protected Stream getStream(String streamId);
    protected Stream createStream(String streamId, String description);
    protected LLM getModel(String... types);
}
```

### Stream类

```java
public class Stream {
    public Stream forEach(StreamListener listener);
    public void addItem(Object item);
    
    @FunctionalInterface
    public interface StreamListener {
        void onItem(Object item);
    }
}
```

### LLM类

```java
public class LLM {
    public String query(String prompt);
    public String getModelInfo();
}
```

## 系统要求

- **Java环境**: JDK 8+ (支持Lambda表达式)
- **Python环境**: Python 3.8+
- **系统依赖**: 现有ChainStream依赖

## 注意事项

1. **文件命名**: Java Agent文件名应该与类名一致
2. **Agent ID**: 从文件名自动提取，例如`MyJavaAgent.java` → `myjava`
3. **编译**: Java文件会在启动时自动编译
4. **类路径**: Java Libraries会自动包含在类路径中
5. **进程管理**: Java Agent作为独立进程运行，通过包装器与Python Runtime通信

## 示例

查看`AgentStore/SimpleJavaAgent.java`了解完整的示例实现。

## 故障排除

### Java编译错误
- 检查Java语法是否正确
- 确保类名与文件名一致
- 检查Java环境是否正确安装

### 启动失败
- 检查JAVA_HOME环境变量
- 查看日志输出获取详细错误信息
- 确保Java Libraries编译成功

### 运行时错误
- 检查Java Agent的start()方法实现
- 查看Java进程的输出日志
- 确保Stream和LLM操作正确

## 技术架构

```
Java Agent文件 → AgentManager → JavaAgentExecutor → JVM进程 → JavaAgentWrapper → Python Runtime
```

Java Agent通过以下组件集成到ChainStream系统：

1. **AgentManager**: 扩展支持Java文件扫描和加载
2. **JavaAgentExecutor**: 处理Java编译和进程启动
3. **JavaAgentWrapper**: 将Java Agent包装成Python Agent对象
4. **Java Libraries**: 提供ChainStream API的Java实现

这种设计确保了Java Agent与Python Agent的无缝集成，享受相同的管理和监控功能。
