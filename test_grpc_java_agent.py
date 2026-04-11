#!/usr/bin/env python3
"""
测试gRPC Java Agent的脚本
"""
import sys
import os
import logging
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_grpc_java_agent():
    """测试gRPC Java Agent"""
    logger.info("开始测试gRPC Java Agent...")
    
    try:
        # 创建Java Agent执行器
        executor = JavaAgentExecutor()
        logger.info("Java Agent执行器创建成功")
        
        # Java Agent文件路径
        java_file_path = "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/AgentStore/GrpcTestAgent.java"
        
        if not os.path.exists(java_file_path):
            logger.error(f"Java文件不存在: {java_file_path}")
            return False
        
        logger.info(f"开始启动Java Agent: {java_file_path}")
        
        # 启动Java Agent
        java_agent_wrapper = executor.start_java_agent(java_file_path, user=None)
        
        if java_agent_wrapper:
            logger.info(f"Java Agent启动成功: {java_agent_wrapper.agent_id}")
            
            # 等待一段时间让Agent运行
            logger.info("等待Java Agent运行...")
            time.sleep(10)
            
            # 停止Agent
            logger.info("停止Java Agent...")
            java_agent_wrapper.stop()
            
            logger.info("gRPC Java Agent测试完成")
            return True
        else:
            logger.error("Java Agent启动失败")
            return False
            
    except Exception as e:
        logger.error(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_java_agent():
    """测试简单Java Agent（不依赖gRPC）"""
    logger.info("开始测试简单Java Agent...")
    
    try:
        # 创建Java Agent执行器
        executor = JavaAgentExecutor()
        logger.info("Java Agent执行器创建成功")
        
        # Java Agent文件路径
        java_file_path = "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/AgentStore/SimpleTestAgent.java"
        
        if not os.path.exists(java_file_path):
            logger.error(f"Java文件不存在: {java_file_path}")
            return False
        
        logger.info(f"开始启动简单Java Agent: {java_file_path}")
        
        # 启动Java Agent
        java_agent_wrapper = executor.start_java_agent(java_file_path, user=None)
        
        if java_agent_wrapper:
            logger.info(f"简单Java Agent启动成功: {java_agent_wrapper.agent_id}")
            
            # 等待一段时间让Agent运行
            logger.info("等待简单Java Agent运行...")
            time.sleep(5)
            
            # 停止Agent
            logger.info("停止简单Java Agent...")
            java_agent_wrapper.stop()
            
            logger.info("简单Java Agent测试完成")
            return True
        else:
            logger.error("简单Java Agent启动失败")
            return False
            
    except Exception as e:
        logger.error(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    logger.info("=== Java Agent集成测试 ===")
    
    # 测试简单Java Agent
    logger.info("\n1. 测试简单Java Agent（不依赖gRPC）")
    simple_success = test_simple_java_agent()
    
    # 测试gRPC Java Agent
    logger.info("\n2. 测试gRPC Java Agent（依赖gRPC）")
    grpc_success = test_grpc_java_agent()
    
    # 总结
    logger.info("\n=== 测试总结 ===")
    logger.info(f"简单Java Agent测试: {'✅ 通过' if simple_success else '❌ 失败'}")
    logger.info(f"gRPC Java Agent测试: {'✅ 通过' if grpc_success else '❌ 失败'}")
    
    if simple_success and grpc_success:
        logger.info("🎉 所有测试通过！")
    else:
        logger.info("⚠️ 部分测试失败")
