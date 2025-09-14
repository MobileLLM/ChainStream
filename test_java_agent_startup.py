#!/usr/bin/env python3
"""
Java Agent启动测试脚本
专门测试Java Agent的启动和基本功能
"""

import os
import sys
import time
import logging
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


def test_java_agent_startup():
    """测试Java Agent启动"""
    logger.info("开始Java Agent启动测试...")
    
    try:
        # 导入必要的模块
        from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor
        from chainstream.runtime.agent_manager import AgentManager
        
        # 创建Java Agent执行器
        executor = JavaAgentExecutor()
        logger.info("Java Agent执行器创建成功")
        
        # 查找Java Agent文件
        java_dir = project_root / "chainstream" / "runtime" / "java"
        agent_store = java_dir / "AgentStore"
        
        if not agent_store.exists():
            logger.error(f"AgentStore目录不存在: {agent_store}")
            return False
        
        java_files = list(agent_store.glob("*.java"))
        if not java_files:
            logger.error("未找到Java Agent文件")
            return False
        
        logger.info(f"找到 {len(java_files)} 个Java Agent文件")
        
        # 测试启动第一个Java Agent
        java_file = java_files[0]
        logger.info(f"测试启动Java Agent: {java_file.name}")
        
        # 启动Java Agent
        java_agent_wrapper = executor.start_java_agent(str(java_file))
        if not java_agent_wrapper:
            logger.error("Java Agent启动失败")
            return False
        
        logger.info(f"Java Agent启动成功: {java_agent_wrapper.agent_id}")
        logger.info(f"Agent类型: {java_agent_wrapper.metaData.type}")
        logger.info(f"Agent状态: {java_agent_wrapper.get_status()}")
        
        # 等待一下让Agent运行
        logger.info("等待Agent运行...")
        time.sleep(5)
        
        # 检查Agent是否还在运行
        if java_agent_wrapper.is_running():
            logger.info("Java Agent正在运行")
        else:
            logger.warning("Java Agent已停止")
        
        # 停止Java Agent
        logger.info("停止Java Agent...")
        java_agent_wrapper.stop()
        
        # 等待停止完成
        time.sleep(2)
        
        if not java_agent_wrapper.is_running():
            logger.info("Java Agent已成功停止")
        else:
            logger.warning("Java Agent停止可能有问题")
        
        logger.info("Java Agent启动测试完成")
        return True
        
    except Exception as e:
        logger.error(f"Java Agent启动测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_manager_integration():
    """测试AgentManager集成"""
    logger.info("测试AgentManager集成...")
    
    try:
        from chainstream.runtime.agent_manager import AgentManager
        
        # 创建AgentManager
        agent_manager = AgentManager()
        logger.info("AgentManager创建成功")
        
        # 设置predefined_agents_path
        java_dir = project_root / "chainstream" / "runtime" / "java"
        agent_store = java_dir / "AgentStore"
        agent_manager.predefined_agents_path = agent_store
        
        # 扫描预定义Agent
        agent_list = agent_manager.scan_predefined_agents()
        logger.info(f"扫描到 {len(agent_list)} 个Agent文件")
        
        for agent_path in agent_list:
            logger.info(f"  - {agent_path}")
        
        # 测试通过路径启动Agent
        if agent_list:
            agent_path = agent_list[0]
            logger.info(f"测试通过路径启动Agent: {agent_path}")
            
            try:
                agent_manager.start_agent_by_path(agent_path, None)
                logger.info("Agent启动成功")
                
                # 等待一下
                time.sleep(3)
                
                # 获取运行中的Agent信息
                running_agents = agent_manager.get_running_agents_info_list()
                logger.info(f"运行中的Agent数量: {len(running_agents)}")
                
                for agent_info in running_agents:
                    logger.info(f"  - {agent_info.get('agent_id', 'unknown')}: {agent_info.get('status', 'unknown')}")
                
            except Exception as e:
                logger.error(f"通过路径启动Agent失败: {e}")
                return False
        
        logger.info("AgentManager集成测试完成")
        return True
        
    except Exception as e:
        logger.error(f"AgentManager集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    logger.info("开始Java Agent启动测试...")
    
    tests = [
        ("Java Agent启动测试", test_java_agent_startup),
        ("AgentManager集成测试", test_agent_manager_integration),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n运行测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, "PASS" if result else "FAIL"))
            logger.info(f"测试 {test_name}: {'通过' if result else '失败'}")
        except Exception as e:
            logger.error(f"测试 {test_name} 异常: {e}")
            results.append((test_name, "ERROR"))
    
    # 打印测试总结
    logger.info("\n" + "="*50)
    logger.info("测试总结")
    logger.info("="*50)
    
    for test_name, result in results:
        status_icon = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
        logger.info(f"{status_icon} {test_name}: {result}")
    
    passed = sum(1 for _, result in results if result == "PASS")
    total = len(results)
    logger.info(f"\n总计: {total} 个测试，通过: {passed} 个")
    
    if passed == total:
        logger.info("🎉 所有测试通过！")
    else:
        logger.warning("⚠️ 部分测试失败")


if __name__ == "__main__":
    main()
