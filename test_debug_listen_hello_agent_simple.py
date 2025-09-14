#!/usr/bin/env python3
"""
简单测试DebugListenHelloAgent
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

def test_debug_listen_hello_agent():
    """测试DebugListenHelloAgent"""
    try:
        logger.info("🚀 开始测试DebugListenHelloAgent")
        
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
        
        # 启动DebugListenHelloAgent
        logger.info("🏃 启动DebugListenHelloAgent")
        debug_listen_hello_agent_path = os.path.abspath("AgentStore/system_agents/utils/DebugListenHelloAgent.java")
        
        if not os.path.exists(debug_listen_hello_agent_path):
            logger.error(f"❌ DebugListenHelloAgent文件不存在: {debug_listen_hello_agent_path}")
            return False
        
        success = runtime_core.start_agent_by_path(debug_listen_hello_agent_path, user)
        if not success:
            logger.error("❌ 启动DebugListenHelloAgent失败")
            return False
        
        logger.info("✅ DebugListenHelloAgent启动成功")
        
        # 等待agent启动完成
        logger.info("⏳ 等待agent启动完成...")
        time.sleep(3)
        
        # 检查AgentManager中的agents
        logger.info("🔍 检查AgentManager中的agents")
        running_agents = runtime_core.agent_manager.get_running_agents_info_list()
        logger.info(f"📋 运行中的agents: {running_agents}")
        
        # 检查是否有Java Agent
        java_agents = [agent for agent in running_agents if agent.get('type') == 'java']
        if len(java_agents) == 0:
            logger.error("❌ 没有找到Java Agent")
            return False
        
        logger.info(f"✅ 找到 {len(java_agents)} 个Java Agent")
        
        # 等待一段时间让agent运行
        logger.info("⏳ 等待agent运行...")
        time.sleep(5)
        
        logger.info("🎉 测试完成！")
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}")
        import traceback
        logger.error(f"❌ 详细错误: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_debug_listen_hello_agent()
    if success:
        print("✅ 测试成功")
        sys.exit(0)
    else:
        print("❌ 测试失败")
        sys.exit(1)
