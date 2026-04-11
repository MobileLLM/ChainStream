#!/bin/bash

# ChainStream Java Runtime 依赖安装脚本

echo "=== ChainStream Java Runtime 依赖安装 ==="

# 检查Java环境
echo "检查Java环境..."
if ! command -v java &> /dev/null; then
    echo "错误: 未找到Java。请安装JDK 11或更高版本。"
    exit 1
fi

if ! command -v javac &> /dev/null; then
    echo "错误: 未找到javac编译器。请安装JDK 11或更高版本。"
    exit 1
fi

echo "Java版本:"
java -version
echo ""

# 检查Maven
echo "检查Maven..."
if ! command -v mvn &> /dev/null; then
    echo "Maven未安装，正在安装..."
    
    # 检测操作系统
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            echo "使用Homebrew安装Maven..."
            brew install maven
        else
            echo "错误: 请先安装Homebrew，然后运行: brew install maven"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "使用apt安装Maven..."
            sudo apt-get update
            sudo apt-get install -y maven
        elif command -v yum &> /dev/null; then
            echo "使用yum安装Maven..."
            sudo yum install -y maven
        else
            echo "错误: 无法自动安装Maven。请手动安装Maven。"
            exit 1
        fi
    else
        echo "错误: 不支持的操作系统。请手动安装Maven。"
        exit 1
    fi
fi

echo "Maven版本:"
mvn -version
echo ""

# 检查Gradle（可选）
echo "检查Gradle..."
if ! command -v gradle &> /dev/null; then
    echo "Gradle未安装，但Maven已足够。如需使用Gradle，请手动安装。"
else
    echo "Gradle版本:"
    gradle -version
fi
echo ""

# 安装Python gRPC依赖
echo "安装Python gRPC依赖..."
if command -v pip &> /dev/null; then
    pip install grpcio grpcio-tools
    echo "Python gRPC依赖安装完成"
else
    echo "警告: 未找到pip，请手动安装Python gRPC依赖: pip install grpcio grpcio-tools"
fi
echo ""

echo "=== 依赖安装完成 ==="
echo ""
echo "下一步："
echo "1. 运行 'mvn clean compile' 编译项目"
echo "2. 运行 'mvn exec:java -Dexec.mainClass=\"com.chainstream.agent.SimpleAgent\"' 运行示例Agent"
echo "3. 或者使用Gradle: 'gradle runAgent'"
