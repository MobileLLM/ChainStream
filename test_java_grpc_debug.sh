#!/bin/bash

# Java gRPC调试测试脚本
# 用于测试Java Agent与Python Runtime的gRPC通信

set -e

echo "🚀 Java gRPC Debug Test Script"
echo "================================"

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAVA_DIR="$PROJECT_ROOT/chainstream/runtime/java"
JAVA_BRIDGE_DIR="$PROJECT_ROOT/chainstream/runtime/java"

echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"
echo -e "${BLUE}📁 Java directory: $JAVA_DIR${NC}"

# 检查Java环境
echo -e "${YELLOW}🔍 Checking Java environment...${NC}"
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java not found. Please install Java 11 or higher.${NC}"
    exit 1
fi

if ! command -v javac &> /dev/null; then
    echo -e "${RED}❌ javac not found. Please install Java Development Kit.${NC}"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | head -n 1 | cut -d'"' -f2 | cut -d'.' -f1)
echo -e "${GREEN}✅ Java version: $JAVA_VERSION${NC}"

# 检查Maven
echo -e "${YELLOW}🔍 Checking Maven...${NC}"
if ! command -v mvn &> /dev/null; then
    echo -e "${RED}❌ Maven not found. Please install Maven.${NC}"
    exit 1
fi

MAVEN_VERSION=$(mvn -version | head -n 1 | cut -d' ' -f3)
echo -e "${GREEN}✅ Maven version: $MAVEN_VERSION${NC}"

# 生成gRPC代码
echo -e "${YELLOW}🔧 Generating gRPC code...${NC}"
cd "$JAVA_BRIDGE_DIR"
if [ -f "generate_grpc_code.py" ]; then
    python3 generate_grpc_code.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ gRPC Python code generated successfully${NC}"
    else
        echo -e "${RED}❌ Failed to generate gRPC Python code${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ generate_grpc_code.py not found${NC}"
    exit 1
fi

# 编译Java代码
echo -e "${YELLOW}🔧 Compiling Java code...${NC}"
cd "$JAVA_DIR"
if [ -f "pom.xml" ]; then
    mvn clean compile
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Java code compiled successfully${NC}"
    else
        echo -e "${RED}❌ Failed to compile Java code${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ pom.xml not found${NC}"
    exit 1
fi

# 启动Python调试服务器
echo -e "${YELLOW}🚀 Starting Python debug gRPC server...${NC}"
cd "$PROJECT_ROOT"
python3 debug_grpc_communication.py --mode server --port 50051 &
SERVER_PID=$!

# 等待服务器启动
echo -e "${YELLOW}⏳ Waiting for server to start...${NC}"
sleep 3

# 检查服务器是否启动成功
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}❌ Failed to start gRPC server${NC}"
    exit 1
fi

echo -e "${GREEN}✅ gRPC server started (PID: $SERVER_PID)${NC}"

# 运行Java调试Agent
echo -e "${YELLOW}🧪 Running Java DebugAgent...${NC}"
cd "$JAVA_DIR"
mvn exec:java -Dexec.mainClass="com.chainstream.agent.DebugAgent" -Dexec.args="test_debug_agent"

# 检查Java Agent执行结果
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Java DebugAgent executed successfully${NC}"
else
    echo -e "${RED}❌ Java DebugAgent execution failed${NC}"
fi

# 停止服务器
echo -e "${YELLOW}🛑 Stopping gRPC server...${NC}"
kill $SERVER_PID 2>/dev/null || true
wait $SERVER_PID 2>/dev/null || true

echo -e "${GREEN}✅ gRPC server stopped${NC}"

# 显示日志文件
echo -e "${YELLOW}📋 Log files:${NC}"
if [ -f "$PROJECT_ROOT/grpc_debug.log" ]; then
    echo -e "${BLUE}📄 gRPC debug log: $PROJECT_ROOT/grpc_debug.log${NC}"
    echo -e "${YELLOW}Last 20 lines of gRPC debug log:${NC}"
    tail -20 "$PROJECT_ROOT/grpc_debug.log"
fi

echo -e "${GREEN}🎉 Java gRPC debug test completed!${NC}"
echo -e "${BLUE}💡 Check the log files for detailed debugging information.${NC}"
