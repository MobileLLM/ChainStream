# Java gRPC通信调试指南

本指南提供了完整的Java Agent与Python Runtime gRPC通信调试方案。

## 🚀 快速开始

### 1. 环境检查
```bash
# 检查Java环境
java -version
javac -version

# 检查Maven
mvn -version

# 检查Python环境
python3 --version
```

### 2. 快速测试连接
```bash
# 启动Python gRPC服务器
python3 quick_grpc_test.py --mode server

# 在另一个终端测试连接
python3 quick_grpc_test.py --mode test
```

### 3. 完整调试测试
```bash
# 运行完整的Java gRPC调试测试
./test_java_grpc_debug.sh
```

## 🔧 调试工具

### 1. 调试gRPC服务器 (`debug_grpc_communication.py`)
- **功能**: 记录所有gRPC请求和响应
- **日志**: 输出到 `grpc_debug.log`
- **使用**:
  ```bash
  # 启动调试服务器
  python3 debug_grpc_communication.py --mode server
  
  # 测试客户端
  python3 debug_grpc_communication.py --mode client
  
  # 同时运行服务器和客户端
  python3 debug_grpc_communication.py --mode both
  ```

### 2. 快速测试工具 (`quick_grpc_test.py`)
- **功能**: 快速验证gRPC连接
- **使用**:
  ```bash
  # 启动简单服务器
  python3 quick_grpc_test.py --mode server
  
  # 测试连接
  python3 quick_grpc_test.py --mode test
  ```

### 3. Java调试Agent (`DebugAgent.java`)
- **功能**: 详细的Java端gRPC通信日志
- **位置**: `chainstream/runtime/java/src/main/java/com/chainstream/agent/DebugAgent.java`
- **使用**:
  ```bash
  cd chainstream/runtime/java
  mvn exec:java -Dexec.mainClass="com.chainstream.agent.DebugAgent"
  ```

## 🐛 常见问题排查

### 1. 连接问题
**症状**: Java客户端无法连接到Python服务器
**排查步骤**:
```bash
# 检查端口是否被占用
lsof -i :50051

# 检查防火墙设置
netstat -an | grep 50051

# 测试网络连接
telnet localhost 50051
```

### 2. gRPC代码生成问题
**症状**: 编译时找不到gRPC生成的类
**解决方案**:
```bash
# 重新生成gRPC代码
cd chainstream/runtime/java
python3 generate_grpc_code.py

# 重新编译Java代码
cd ../java
mvn clean compile
```

### 3. 协议不匹配问题
**症状**: gRPC调用失败，错误信息包含"UNIMPLEMENTED"
**排查步骤**:
1. 检查proto文件定义
2. 确认服务名称匹配
3. 验证方法签名一致

### 4. 日志级别问题
**症状**: 看不到详细的调试信息
**解决方案**:
```bash
# 设置Java日志级别
export JAVA_OPTS="-Djava.util.logging.config.file=logging.properties"

# 或在代码中设置
logger.setLevel(Level.ALL);
```

## 📊 调试信息收集

### 1. 收集Java日志
```bash
# 运行Java Agent并保存日志
mvn exec:java -Dexec.mainClass="com.chainstream.agent.DebugAgent" > java_debug.log 2>&1
```

### 2. 收集Python日志
```bash
# 运行Python调试服务器
python3 debug_grpc_communication.py --mode server > python_debug.log 2>&1
```

### 3. 网络抓包（可选）
```bash
# 使用tcpdump抓包
sudo tcpdump -i lo0 -w grpc_traffic.pcap port 50051

# 使用Wireshark分析
wireshark grpc_traffic.pcap
```

## 🔍 详细调试步骤

### 步骤1: 验证环境
```bash
# 1. 检查所有依赖
./test_java_grpc_debug.sh

# 2. 查看生成的gRPC代码
ls -la chainstream/runtime/java/*.py
ls -la chainstream/runtime/java/src/main/java/chainstream/
```

### 步骤2: 测试基础连接
```bash
# 1. 启动简单服务器
python3 quick_grpc_test.py --mode server &

# 2. 测试连接
python3 quick_grpc_test.py --mode test

# 3. 停止服务器
pkill -f quick_grpc_test.py
```

### 步骤3: 测试完整功能
```bash
# 1. 启动调试服务器
python3 debug_grpc_communication.py --mode server &

# 2. 运行Java调试Agent
cd chainstream/runtime/java
mvn exec:java -Dexec.mainClass="com.chainstream.agent.DebugAgent"

# 3. 查看日志
tail -f grpc_debug.log
```

### 步骤4: 分析结果
```bash
# 1. 检查gRPC日志
grep "ERROR\|FAILED\|Exception" grpc_debug.log

# 2. 检查Java日志
grep "❌\|ERROR\|Exception" java_debug.log

# 3. 统计请求数量
grep "gRPC Request" grpc_debug.log | wc -l
```

## 📋 调试检查清单

- [ ] Java环境正确安装 (Java 11+)
- [ ] Maven正确安装
- [ ] Python环境正确安装 (Python 3.7+)
- [ ] gRPC代码已生成
- [ ] Java代码编译成功
- [ ] 端口50051未被占用
- [ ] 防火墙允许本地连接
- [ ] 日志级别设置为DEBUG/ALL
- [ ] 所有依赖库已安装

## 🛠️ 高级调试技巧

### 1. 使用gRPC调试工具
```bash
# 安装grpcurl
brew install grpcurl

# 测试服务
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 chainstream.ChainStreamBridge/GetRuntimeInfo
```

### 2. 使用gRPC反射
在proto文件中添加反射支持:
```protobuf
import "google/protobuf/descriptor.proto";
```

### 3. 性能分析
```bash
# 使用JProfiler或VisualVM分析Java性能
# 使用cProfile分析Python性能
python3 -m cProfile debug_grpc_communication.py
```

## 📞 获取帮助

如果遇到问题，请提供以下信息：
1. 完整的错误日志
2. 环境信息 (Java版本、Python版本、操作系统)
3. 复现步骤
4. 相关的配置文件

## 🔗 相关文件

- `debug_grpc_communication.py` - 调试gRPC服务器
- `quick_grpc_test.py` - 快速连接测试
- `test_java_grpc_debug.sh` - 完整测试脚本
- `DebugAgent.java` - Java调试Agent
- `chainstream_bridge.proto` - gRPC协议定义
- `grpc_debug.log` - 调试日志文件


