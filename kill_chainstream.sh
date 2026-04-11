#!/bin/bash

# 终止ChainStream相关进程的脚本
# 包括Python主进程和Java Agent进程

echo "=== ChainStream 进程清理脚本 ==="

# 1. 终止Java Agent进程
echo "1. 查找并终止Java Agent进程..."
JAVA_AGENT_PIDS=$(ps aux | grep "com.chainstream.agent.DebugHelloAgent" | grep -v grep | awk '{print $2}')

if [ ! -z "$JAVA_AGENT_PIDS" ]; then
    echo "找到Java Agent进程: $JAVA_AGENT_PIDS"
    for pid in $JAVA_AGENT_PIDS; do
        echo "终止Java Agent进程 $pid"
        kill -TERM $pid 2>/dev/null
    done
    sleep 2
    
    # 检查是否还有Java Agent进程
    REMAINING_JAVA=$(ps aux | grep "com.chainstream.agent.DebugHelloAgent" | grep -v grep | awk '{print $2}')
    if [ ! -z "$REMAINING_JAVA" ]; then
        echo "强制终止剩余的Java Agent进程..."
        for pid in $REMAINING_JAVA; do
            kill -9 $pid 2>/dev/null
        done
    fi
else
    echo "未找到Java Agent进程"
fi

# 2. 终止Python主进程
echo "2. 查找并终止Python主进程..."
PYTHON_PIDS=$(ps aux | grep "chainstream.runtime.start" | grep -v grep | awk '{print $2}')

if [ ! -z "$PYTHON_PIDS" ]; then
    echo "找到Python主进程: $PYTHON_PIDS"
    for pid in $PYTHON_PIDS; do
        echo "终止Python主进程 $pid"
        kill -TERM $pid 2>/dev/null
    done
    sleep 2
    
    # 检查是否还有Python主进程
    REMAINING_PYTHON=$(ps aux | grep "chainstream.runtime.start" | grep -v grep | awk '{print $2}')
    if [ ! -z "$REMAINING_PYTHON" ]; then
        echo "强制终止剩余的Python主进程..."
        for pid in $REMAINING_PYTHON; do
            kill -9 $pid 2>/dev/null
        done
    fi
else
    echo "未找到Python主进程"
fi

# 3. 终止所有Java进程（备用方案）
echo "3. 检查是否还有其他Java进程..."
ALL_JAVA_PIDS=$(ps aux | grep java | grep -v grep | awk '{print $2}')

if [ ! -z "$ALL_JAVA_PIDS" ]; then
    echo "发现其他Java进程: $ALL_JAVA_PIDS"
    echo "终止所有Java进程..."
    for pid in $ALL_JAVA_PIDS; do
        kill -TERM $pid 2>/dev/null
    done
    sleep 2
    
    # 强制终止剩余的Java进程
    REMAINING_ALL_JAVA=$(ps aux | grep java | grep -v grep | awk '{print $2}')
    if [ ! -z "$REMAINING_ALL_JAVA" ]; then
        for pid in $REMAINING_ALL_JAVA; do
            kill -9 $pid 2>/dev/null
        done
    fi
else
    echo "没有其他Java进程"
fi

echo "=== 清理完成 ==="
echo "当前Java进程状态:"
ps aux | grep java | grep -v grep || echo "没有Java进程运行"

echo "当前Python进程状态:"
ps aux | grep chainstream | grep -v grep || echo "没有ChainStream Python进程运行"
