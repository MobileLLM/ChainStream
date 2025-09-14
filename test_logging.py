#!/usr/bin/env python3
"""
测试日志配置
"""

import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置详细的日志配置
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置日志
)

logger = logging.getLogger(__name__)

def test_logging():
    """测试日志输出"""
    logger.debug("🔍 DEBUG message")
    logger.info("ℹ️ INFO message")
    logger.warning("⚠️ WARNING message")
    logger.error("❌ ERROR message")
    
    # 测试agent_manager的日志
    from chainstream.runtime.agent_manager import AgentManager
    agent_manager = AgentManager()
    
    # 直接调用logger来测试
    import chainstream.runtime.agent_manager as am
    am.logger.info("🔍 Test message from agent_manager")
    am.logger.debug("🔍 DEBUG message from agent_manager")
    am.logger.warning("⚠️ WARNING message from agent_manager")

if __name__ == "__main__":
    test_logging()
