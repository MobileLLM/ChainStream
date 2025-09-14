#!/usr/bin/env python3
"""
测试agent_id同步功能
验证Java Agent启动后能够正确同步agent_id到Python端
"""

import sys
import os
import time
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_agent_id_sync():
    """测试agent_id同步功能"""
    try:
        logger.info("🚀 开始测试agent_id同步功能")
        
        # 导入ChainStream
        from chainstream.runtime.runtime_core import RuntimeCore
        from chainstream.user import UserManager
        
        # 创建RuntimeCore实例
        logger.info("📦 创建RuntimeCore实例")
        runtime_core = RuntimeCore()
        
        # 创建用户
        logger.info("👤 创建用户")
        user_manager = UserManager()
        user = user_manager.get_user_by_username("admin")
        if not user:
            user = user_manager.create_user("admin", "admin@example.com")
            logger.info(f"✅ 创建用户: {user.get_username()}")
        else:
            logger.info(f"✅ 找到用户: {user.get_username()}")
        
        # 启动Java Agent
        logger.info("🏃 启动Java Agent")
        java_agent_path = "AgentStore/system_agents/utils/DebugHelloAgent.java"
        
        # 转换为绝对路径
        java_agent_path = os.path.abspath(java_agent_path)
        
        if not os.path.exists(java_agent_path):
            logger.error(f"❌ Java Agent文件不存在: {java_agent_path}")
            return False
        
        success = runtime_core.start_agent_by_path(java_agent_path, user)
        if not success:
            logger.error("❌ 启动Java Agent失败")
            return False
        
        logger.info("✅ Java Agent启动成功")
        
        # 等待Java Agent报告agent_id
        logger.info("⏳ 等待Java Agent报告agent_id...")
        time.sleep(3)
        
        # 检查AgentManager中的agents
        logger.info("🔍 检查AgentManager中的agents")
        running_agents = runtime_core.agent_manager.get_running_agents_info_list()
        logger.info(f"📋 运行中的agents: {running_agents}")
        
        # 检查是否有Java Agent
        java_agents = [agent for agent in running_agents if agent.get('type') == 'java']
        if not java_agents:
            logger.error("❌ 没有找到Java Agent")
            return False
        
        logger.info(f"✅ 找到 {len(java_agents)} 个Java Agent")
        
        # 检查agent_id是否正确
        for agent_info in java_agents:
            agent_id = agent_info.get('agent_id')
            logger.info(f"🔍 Java Agent ID: {agent_id}")
            
            # 检查agent_id是否与文件名匹配
            expected_agent_id = "debughelloagent"  # 从DebugHelloAgent.java转换而来
            if agent_id == expected_agent_id:
                logger.info(f"✅ Agent ID匹配: {agent_id}")
            else:
                logger.warning(f"⚠️ Agent ID不匹配: 期望 {expected_agent_id}, 实际 {agent_id}")
        
        # 测试创建Stream
        logger.info("🧪 测试创建Stream")
        try:
            import chainstream as cs
            
            # 获取Java Agent
            java_agent = None
            for agent_id, agent in runtime_core.agent_manager.agents.items():
                if hasattr(agent, 'java_file_path'):
                    java_agent = agent
                    break
            
            if not java_agent:
                logger.error("❌ 没有找到Java Agent实例")
                return False
            
            logger.info(f"🔍 找到Java Agent: {java_agent.agent_id}")
            
            # 尝试创建Stream
            stream = cs.create_stream(java_agent, "test_stream")
            if stream:
                logger.info("✅ Stream创建成功")
            else:
                logger.error("❌ Stream创建失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 测试Stream创建时出错: {e}")
            import traceback
            logger.error(f"❌ 详细错误: {traceback.format_exc()}")
            return False
        
        logger.info("🎉 所有测试通过！")
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(f"❌ 详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_agent_id_sync()
    if success:
        print("✅ 测试成功")
        sys.exit(0)
    else:
        print("❌ 测试失败")
        sys.exit(1)
