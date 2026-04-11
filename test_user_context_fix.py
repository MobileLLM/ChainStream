#!/usr/bin/env python3
"""
测试用户上下文修复
"""
import sys
import os
import time
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chainstream.runtime import cs_server_core
from chainstream.user import UserManager

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_user_context_fix():
    """测试用户上下文修复"""
    try:
        logger.info("🚀 Starting user context fix test...")
        
        # 使用全局的ChainStream核心
        core = cs_server_core
        
        # 获取用户管理器
        user_manager = UserManager()
        admin_user = user_manager.get_user_by_username("admin")
        
        if not admin_user:
            logger.error("❌ Admin user not found")
            return False
        
        logger.info(f"✅ Found admin user: {admin_user.get_username()}")
        
        # 启动Java Agent
        java_file_path = "/Users/liou/project/llm/ChainStream/AgentStore/system_agents/utils/DebugHelloAgent.java"
        
        logger.info(f"🚀 Starting Java agent: {java_file_path}")
        success = core.start_agent_by_path(java_file_path, admin_user)
        
        if success:
            logger.info("✅ Java agent started successfully")
            
            # 等待一段时间让agent完全启动
            time.sleep(3)
            
            # 检查agent是否在运行
            running_agents = core.agent_manager.get_running_agents_info_list(admin_user)
            logger.info(f"📊 Running agents: {len(running_agents)}")
            
            for agent in running_agents:
                logger.info(f"  - {agent['agent_id']} ({agent['type']}) - {agent['status']}")
            
            # 检查streams
            streams = core.stream_manager.get_stream_info_by_user(admin_user)
            logger.info(f"📊 Streams: {len(streams)}")
            
            for stream in streams:
                logger.info(f"  - {stream['stream_id']} - {stream['status']}")
            
            return True
        else:
            logger.error("❌ Failed to start Java agent")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_user_context_fix()
    if success:
        logger.info("🎉 Test completed successfully!")
    else:
        logger.error("💥 Test failed!")
        sys.exit(1)