#!/bin/bash

# 终止所有Java子进程的脚本
# 使用方法: ./kill_java_processes.sh

echo "正在查找Java进程..."

# 查找所有Java进程（排除grep本身）
JAVA_PIDS=$(ps aux | grep java | grep -v grep | awk '{print $2}')

if [ -z "$JAVA_PIDS" ]; then
    echo "没有找到运行中的Java进程"
    exit 0
fi

echo "找到以下Java进程:"
ps aux | grep java | grep -v grep

echo ""
echo "正在终止Java进程..."

# 首先尝试优雅终止 (SIGTERM)
for pid in $JAVA_PIDS; do
    echo "发送SIGTERM信号到进程 $pid"
    kill -TERM $pid 2>/dev/null
done

# 等待3秒让进程优雅关闭
sleep 3

# 检查是否还有Java进程
REMAINING_PIDS=$(ps aux | grep java | grep -v grep | awk '{print $2}')

if [ ! -z "$REMAINING_PIDS" ]; then
    echo "仍有Java进程未关闭，强制终止..."
    for pid in $REMAINING_PIDS; do
        echo "强制终止进程 $pid"
        kill -9 $pid 2>/dev/null
    done
    
    # 再次检查
    sleep 1
    FINAL_CHECK=$(ps aux | grep java | grep -v grep | awk '{print $2}')
    if [ -z "$FINAL_CHECK" ]; then
        echo "所有Java进程已成功终止"
    else
        echo "警告：仍有Java进程无法终止:"
        ps aux | grep java | grep -v grep
    fi
else
    echo "所有Java进程已成功终止"
fi

echo "Java进程清理完成"
