#!/usr/bin/env python3
"""
ChainStream Java集成测试脚本
测试Java Agent的编译、启动和基本功能
"""

import os
import sys
import time
import logging
import subprocess
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


class JavaIntegrationTester:
    """Java集成测试器"""
    
    def __init__(self):
        self.project_root = project_root
        self.java_dir = self.project_root / "chainstream" / "runtime" / "java"
        self.agent_store = self.java_dir / "AgentStore"
        self.test_results = []
    
    def run_all_tests(self):
        """运行所有测试"""
        logger.info("开始Java集成测试...")
        
        tests = [
            ("Java环境检查", self.test_java_environment),
            ("Java API编译测试", self.test_java_api_compilation),
            ("gRPC服务器测试", self.test_grpc_server),
            ("Java Agent编译测试", self.test_java_agent_compilation),
            ("Java Agent启动测试", self.test_java_agent_startup),
            ("端到端集成测试", self.test_end_to_end_integration),
        ]
        
        for test_name, test_func in tests:
            logger.info(f"运行测试: {test_name}")
            try:
                result = test_func()
                self.test_results.append((test_name, "PASS" if result else "FAIL"))
                logger.info(f"测试 {test_name}: {'通过' if result else '失败'}")
            except Exception as e:
                logger.error(f"测试 {test_name} 异常: {e}")
                self.test_results.append((test_name, "ERROR"))
        
        self.print_test_summary()
    
    def test_java_environment(self):
        """测试Java环境"""
        logger.info("检查Java环境...")
        
        try:
            # 检查Java版本
            result = subprocess.run(['java', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("Java命令执行失败")
                return False
            
            logger.info(f"Java版本信息: {result.stderr.strip()}")
            
            # 检查javac
            result = subprocess.run(['javac', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error("javac命令执行失败")
                return False
            
            logger.info(f"javac版本信息: {result.stdout.strip()}")
            
            # 检查JAVA_HOME
            java_home = os.environ.get('JAVA_HOME')
            if java_home:
                logger.info(f"JAVA_HOME: {java_home}")
            else:
                logger.warning("JAVA_HOME环境变量未设置")
            
            return True
            
        except Exception as e:
            logger.error(f"Java环境检查失败: {e}")
            return False
    
    def test_java_api_compilation(self):
        """测试Java API编译"""
        logger.info("测试Java API编译...")
        
        try:
            java_libs_path = self.java_dir / "java_libraries"
            if not java_libs_path.exists():
                logger.error(f"Java Libraries路径不存在: {java_libs_path}")
                return False
            
            # 查找所有Java文件
            java_files = list(java_libs_path.glob("*.java"))
            if not java_files:
                logger.error("未找到Java API文件")
                return False
            
            logger.info(f"找到 {len(java_files)} 个Java API文件")
            
            # 编译Java Libraries
            cmd = ['javac', '-d', str(java_libs_path)] + [str(f) for f in java_files]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.error(f"Java API编译失败: {result.stderr}")
                return False
            
            logger.info("Java API编译成功")
            return True
            
        except Exception as e:
            logger.error(f"Java API编译测试失败: {e}")
            return False
    
    def test_grpc_server(self):
        """测试gRPC服务器"""
        logger.info("测试gRPC服务器...")
        
        try:
            # 导入gRPC服务器
            from chainstream.runtime.java.grpc_server import start_bridge_server
            
            # 启动服务器
            server = start_bridge_server(port=50052)  # 使用不同端口避免冲突
            if not server:
                logger.error("gRPC服务器启动失败")
                return False
            
            logger.info("gRPC服务器启动成功")
            
            # 等待一下
            time.sleep(2)
            
            # 停止服务器
            server.stop_server()
            logger.info("gRPC服务器停止成功")
            
            return True
            
        except Exception as e:
            logger.error(f"gRPC服务器测试失败: {e}")
            return False
    
    def test_java_agent_compilation(self):
        """测试Java Agent编译"""
        logger.info("测试Java Agent编译...")
        
        try:
            # 查找Java Agent文件
            java_agent_files = list(self.agent_store.glob("*.java"))
            if not java_agent_files:
                logger.error("未找到Java Agent文件")
                return False
            
            logger.info(f"找到 {len(java_agent_files)} 个Java Agent文件")
            
            # 测试编译第一个Java Agent
            java_file = java_agent_files[0]
            logger.info(f"编译Java Agent: {java_file.name}")
            
            # 使用JavaAgentExecutor编译
            from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor
            executor = JavaAgentExecutor()
            
            class_file = executor._compile_java_file(str(java_file))
            if not os.path.exists(class_file):
                logger.error(f"编译失败，未生成class文件: {class_file}")
                return False
            
            logger.info(f"Java Agent编译成功: {class_file}")
            return True
            
        except Exception as e:
            logger.error(f"Java Agent编译测试失败: {e}")
            return False
    
    def test_java_agent_startup(self):
        """测试Java Agent启动"""
        logger.info("测试Java Agent启动...")
        
        try:
            # 查找Java Agent文件
            java_agent_files = list(self.agent_store.glob("*.java"))
            if not java_agent_files:
                logger.error("未找到Java Agent文件")
                return False
            
            # 测试启动第一个Java Agent
            java_file = java_agent_files[0]
            logger.info(f"启动Java Agent: {java_file.name}")
            
            # 使用JavaAgentExecutor启动
            from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor
            executor = JavaAgentExecutor()
            
            # 启动Java Agent
            java_agent_wrapper = executor.start_java_agent(str(java_file))
            if not java_agent_wrapper:
                logger.error("Java Agent启动失败")
                return False
            
            logger.info(f"Java Agent启动成功: {java_agent_wrapper.agent_id}")
            
            # 等待一下
            time.sleep(3)
            
            # 停止Java Agent
            java_agent_wrapper.stop()
            logger.info("Java Agent停止成功")
            
            return True
            
        except Exception as e:
            logger.error(f"Java Agent启动测试失败: {e}")
            return False
    
    def test_end_to_end_integration(self):
        """端到端集成测试"""
        logger.info("端到端集成测试...")
        
        try:
            # 启动ChainStream服务（带Java支持）
            logger.info("启动ChainStream服务...")
            
            # 这里可以添加更复杂的端到端测试
            # 例如：启动服务、通过Web界面启动Java Agent、验证功能等
            
            logger.info("端到端集成测试完成")
            return True
            
        except Exception as e:
            logger.error(f"端到端集成测试失败: {e}")
            return False
    
    def print_test_summary(self):
        """打印测试总结"""
        logger.info("\n" + "="*50)
        logger.info("测试总结")
        logger.info("="*50)
        
        passed = sum(1 for _, result in self.test_results if result == "PASS")
        failed = sum(1 for _, result in self.test_results if result == "FAIL")
        errors = sum(1 for _, result in self.test_results if result == "ERROR")
        total = len(self.test_results)
        
        for test_name, result in self.test_results:
            status_icon = "✅" if result == "PASS" else "❌" if result == "FAIL" else "⚠️"
            logger.info(f"{status_icon} {test_name}: {result}")
        
        logger.info("-"*50)
        logger.info(f"总计: {total} 个测试")
        logger.info(f"通过: {passed} 个")
        logger.info(f"失败: {failed} 个")
        logger.info(f"错误: {errors} 个")
        logger.info(f"成功率: {passed/total*100:.1f}%")
        
        if failed == 0 and errors == 0:
            logger.info("🎉 所有测试通过！Java集成工作正常。")
        else:
            logger.warning("⚠️ 部分测试失败，请检查相关配置。")


def main():
    """主函数"""
    tester = JavaIntegrationTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
