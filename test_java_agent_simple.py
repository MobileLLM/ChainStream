#!/usr/bin/env python3
"""
简单的Java Agent启动测试
"""

import os
import sys
import logging
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置详细的日志配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)

logger = logging.getLogger(__name__)

def test_java_agent_simple():
    """简单测试Java Agent启动"""
    
    logger.info("🚀 Starting simple Java Agent test...")
    
    try:
        # 导入必要的模块
        from chainstream.runtime.agent_manager import AgentManager
        from chainstream.user import User
        
        logger.info("✅ Successfully imported modules")
        
        # 创建用户
        user = User("test_user", "test@example.com", 5)
        logger.info(f"👤 Created user: {user.get_username()}")
        
        # 创建AgentManager
        agent_manager = AgentManager()
        logger.info("📦 Created AgentManager")
        
        # 查找Java Agent文件
        java_agent_path = "/Users/liou/project/llm/ChainStream/AgentStore/system_agents/utils/SimpleTestAgent.java"
        if not os.path.exists(java_agent_path):
            logger.error(f"❌ Java agent file not found: {java_agent_path}")
            return False
        
        logger.info(f"📁 Found Java agent file: {java_agent_path}")
        
        # 直接调用start_agent_by_path
        logger.info("🚀 Calling start_agent_by_path...")
        result = agent_manager.start_agent_by_path(java_agent_path, user)
        
        logger.info(f"📊 Start result: {result}")
        
        # 等待一段时间
        logger.info("⏳ Waiting 5 seconds...")
        time.sleep(5)
        
        # 检查运行中的Agent
        logger.info("🔍 Checking running agents...")
        running_agents = agent_manager.get_running_agents_info_list(user)
        logger.info(f"📊 Found {len(running_agents)} running agents")
        
        for agent_info in running_agents:
            logger.info(f"📋 Agent info: {agent_info}")
        
        # 检查Agent是否真的在运行
        logger.info("🔍 Checking individual agent status...")
        for agent_id, agent in agent_manager.agents.items():
            logger.info(f"🔍 Checking agent: {agent_id}")
            if hasattr(agent, 'is_running'):
                is_running = agent.is_running()
                logger.info(f"📊 Agent {agent_id} running status: {is_running}")
                
                if hasattr(agent, 'java_process') and agent.java_process:
                    poll_result = agent.java_process.poll()
                    logger.info(f"📊 Java process poll result: {poll_result}")
                    logger.info(f"📊 Java process PID: {agent.java_process.pid}")
            else:
                logger.warning(f"⚠️ Agent {agent_id} doesn't have is_running method")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed with exception: {e}")
        import traceback
        logger.error(f"❌ Full traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_java_agent_simple()
    if success:
        logger.info("🎉 Test completed successfully")
    else:
        logger.error("❌ Test failed")
        sys.exit(1)
