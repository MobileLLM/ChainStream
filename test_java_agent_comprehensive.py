#!/usr/bin/env python3
"""
Java Agent 综合测试脚本
测试Java Agent的启动、运行状态检测、停止等功能
"""

import os
import sys
import time
import logging
import signal
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_java_agent_comprehensive():
    """综合测试Java Agent功能"""
    
    logger.info("🚀 Starting comprehensive Java Agent test...")
    
    try:
        # 导入必要的模块
        from chainstream.runtime.agent_manager import AgentManager
        from chainstream.user import User
        
        logger.info("✅ Successfully imported modules")
        
        # 创建用户
        user = User("test_user", "test@example.com", 5)
        logger.info("👤 Created user: test_user")
        
        # 创建AgentManager
        agent_manager = AgentManager()
        logger.info("📦 Created AgentManager")
        
        # 查找Java Agent文件
        java_agent_path = "/Users/liou/project/llm/ChainStream/AgentStore/system_agents/utils/SimpleTestAgent.java"
        if not os.path.exists(java_agent_path):
            logger.error(f"❌ Java agent file not found: {java_agent_path}")
            return False
        
        logger.info(f"📁 Found Java agent file: {java_agent_path}")
        
        # 测试1: 启动Java Agent
        logger.info("🧪 Test 1: Starting Java Agent...")
        result = agent_manager.start_agent_by_path(java_agent_path, user)
        logger.info(f"📊 Start result: {result}")
        
        if not result:
            logger.error("❌ Failed to start Java Agent")
            return False
        
        # 等待一下让Agent完全启动
        time.sleep(2)
        
        # 测试2: 检查运行状态
        logger.info("🧪 Test 2: Checking running status...")
        running_agents = agent_manager.get_running_agents_info_list(user)
        logger.info(f"📊 Found {len(running_agents)} running agents")
        
        for agent_info in running_agents:
            logger.info(f"📋 Agent info: {agent_info}")
            agent_id = agent_info['agent_id']
            
            # 检查单个Agent状态
            agent = agent_manager.get_agent_by_id(agent_id)
            if agent:
                is_running = agent.is_running()
                logger.info(f"📊 Agent {agent_id} running status: {is_running}")
                
                if hasattr(agent, 'java_process') and agent.java_process:
                    poll_result = agent.java_process.poll()
                    logger.info(f"📊 Java process poll result: {poll_result}")
                    logger.info(f"📊 Java process PID: {agent.java_process.pid}")
        
        # 测试3: 等待Agent完成工作
        logger.info("🧪 Test 3: Waiting for Agent to complete work...")
        time.sleep(8)  # 等待SimpleTestAgent完成5次处理
        
        # 测试4: 检查Agent是否自然结束
        logger.info("🧪 Test 4: Checking if Agent completed naturally...")
        running_agents_after = agent_manager.get_running_agents_info_list(user)
        logger.info(f"📊 Found {len(running_agents_after)} running agents after completion")
        
        # 测试5: 测试停止功能（如果Agent还在运行）
        if running_agents_after:
            logger.info("🧪 Test 5: Testing stop functionality...")
            for agent_info in running_agents_after:
                agent_id = agent_info['agent_id']
                agent = agent_manager.get_agent_by_id(agent_id)
                if agent:
                    logger.info(f"🛑 Stopping agent: {agent_id}")
                    agent.stop()
                    time.sleep(1)
                    
                    is_running_after_stop = agent.is_running()
                    logger.info(f"📊 Agent {agent_id} running status after stop: {is_running_after_stop}")
        
        # 最终检查
        final_running_agents = agent_manager.get_running_agents_info_list(user)
        logger.info(f"📊 Final running agents count: {len(final_running_agents)}")
        
        logger.info("🎉 Comprehensive test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with exception: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return False

def test_java_agent_with_long_running():
    """测试长时间运行的Java Agent"""
    
    logger.info("🚀 Starting long-running Java Agent test...")
    
    try:
        from chainstream.runtime.agent_manager import AgentManager
        from chainstream.user import User
        
        # 创建一个长时间运行的Java Agent
        long_running_agent_code = '''
package com.chainstream.agent;

public class LongRunningTestAgent {
    private String agentId;
    private boolean running;
    private Thread workerThread;
    
    public LongRunningTestAgent() {
        this.agentId = "long_running_test_agent";
        this.running = false;
    }
    
    public void start() {
        System.out.println("=== LongRunningTestAgent Started ===");
        System.out.println("Agent ID: " + agentId);
        
        this.running = true;
        this.workerThread = new Thread(this::work);
        this.workerThread.start();
    }
    
    private void work() {
        int count = 0;
        while (this.running) {
            count++;
            System.out.println("Working... count: " + count);
            
            try {
                Thread.sleep(2000); // 2秒间隔
            } catch (InterruptedException e) {
                System.out.println("Agent interrupted");
                break;
            }
        }
        System.out.println("=== LongRunningTestAgent Stopped ===");
    }
    
    public void stop() {
        System.out.println("Stopping LongRunningTestAgent...");
        this.running = false;
        if (this.workerThread != null) {
            this.workerThread.interrupt();
        }
    }
    
    public boolean isRunning() {
        return running;
    }
    
    public String getAgentId() {
        return agentId;
    }
    
    public static void main(String[] args) {
        LongRunningTestAgent agent = new LongRunningTestAgent();
        agent.start();
        
        // 保持运行直到被中断
        try {
            Thread.sleep(Long.MAX_VALUE);
        } catch (InterruptedException e) {
            agent.stop();
        }
    }
}
'''
        
        # 写入临时Java文件
        temp_java_path = "/Users/liou/project/llm/ChainStream/AgentStore/system_agents/utils/LongRunningTestAgent.java"
        with open(temp_java_path, 'w') as f:
            f.write(long_running_agent_code)
        
        logger.info(f"📝 Created temporary Java file: {temp_java_path}")
        
        # 创建用户和AgentManager
        user = User("test_user", "test@example.com", 5)
        agent_manager = AgentManager()
        
        # 启动长时间运行的Agent
        logger.info("🚀 Starting long-running Java Agent...")
        result = agent_manager.start_agent_by_path(temp_java_path, user)
        logger.info(f"📊 Start result: {result}")
        
        if not result:
            logger.error("❌ Failed to start long-running Java Agent")
            return False
        
        # 等待一段时间
        logger.info("⏳ Waiting for 10 seconds...")
        time.sleep(10)
        
        # 检查运行状态
        running_agents = agent_manager.get_running_agents_info_list(user)
        logger.info(f"📊 Found {len(running_agents)} running agents")
        
        # 停止Agent
        if running_agents:
            agent_info = running_agents[0]
            agent_id = agent_info['agent_id']
            agent = agent_manager.get_agent_by_id(agent_id)
            
            if agent:
                logger.info(f"🛑 Stopping long-running agent: {agent_id}")
                agent.stop()
                time.sleep(2)
                
                is_running = agent.is_running()
                logger.info(f"📊 Agent running status after stop: {is_running}")
        
        # 清理临时文件
        if os.path.exists(temp_java_path):
            os.remove(temp_java_path)
            logger.info("🧹 Cleaned up temporary file")
        
        logger.info("🎉 Long-running test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Long-running test failed: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Java Agent Comprehensive Test Suite")
    print("=" * 60)
    
    # 运行基本测试
    print("\n1. Running basic comprehensive test...")
    success1 = test_java_agent_comprehensive()
    
    print("\n2. Running long-running agent test...")
    success2 = test_java_agent_with_long_running()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Basic Test: {'✅ PASSED' if success1 else '❌ FAILED'}")
    print(f"Long-running Test: {'✅ PASSED' if success2 else '❌ FAILED'}")
    print(f"Overall: {'✅ ALL TESTS PASSED' if success1 and success2 else '❌ SOME TESTS FAILED'}")
    print("=" * 60)
