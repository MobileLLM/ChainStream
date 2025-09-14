#!/usr/bin/env python3
"""
调试日志配置问题
"""

import logging
import sys

def test_logging_before_import():
    """在导入ChainStream之前测试日志"""
    print("=== 测试导入ChainStream之前的日志配置 ===")
    
    # 设置日志配置
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
    
    logger = logging.getLogger('test_before')
    logger.debug('🔍 DEBUG before import')
    logger.info('ℹ️ INFO before import')
    logger.warning('⚠️ WARNING before import')
    logger.error('❌ ERROR before import')
    
    print(f"Root logger level: {logging.getLogger().level}")
    print(f"Root logger handlers: {logging.getLogger().handlers}")

def test_logging_after_import():
    """在导入ChainStream之后测试日志"""
    print("\n=== 测试导入ChainStream之后的日志配置 ===")
    
    # 重新设置日志配置
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
    
    logger = logging.getLogger('test_after')
    logger.debug('🔍 DEBUG after import')
    logger.info('ℹ️ INFO after import')
    logger.warning('⚠️ WARNING after import')
    logger.error('❌ ERROR after import')
    
    print(f"Root logger level: {logging.getLogger().level}")
    print(f"Root logger handlers: {logging.getLogger().handlers}")

def test_specific_loggers():
    """测试特定的logger"""
    print("\n=== 测试特定logger ===")
    
    # 测试agent_manager的logger
    am_logger = logging.getLogger('chainstream.runtime.agent_manager')
    am_logger.setLevel(logging.DEBUG)
    am_logger.debug('🔍 AgentManager DEBUG')
    am_logger.info('ℹ️ AgentManager INFO')
    am_logger.warning('⚠️ AgentManager WARNING')
    
    # 测试java_agent_executor的logger
    jae_logger = logging.getLogger('chainstream.runtime.java.java_agent_executor')
    jae_logger.setLevel(logging.DEBUG)
    jae_logger.debug('🔍 JavaAgentExecutor DEBUG')
    jae_logger.info('ℹ️ JavaAgentExecutor INFO')
    jae_logger.warning('⚠️ JavaAgentExecutor WARNING')

if __name__ == "__main__":
    # 测试导入前的日志
    test_logging_before_import()
    
    # 导入ChainStream
    print("\n=== 导入ChainStream ===")
    try:
        from chainstream.runtime import cs_server
        from chainstream.runtime.agent_manager import AgentManager
        print("✅ ChainStream导入成功")
    except Exception as e:
        print(f"❌ ChainStream导入失败: {e}")
        sys.exit(1)
    
    # 测试导入后的日志
    test_logging_after_import()
    
    # 测试特定logger
    test_specific_loggers()
    
    print("\n=== 测试完成 ===")
