#!/usr/bin/env python3
"""
Java集成测试总结
"""
import sys
import os
import logging

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def test_java_environment():
    """测试Java环境"""
    logger.info("=== Java环境测试 ===")
    
    try:
        import subprocess
        
        # 检查Java版本
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Java环境正常")
            logger.info(f"Java版本: {result.stderr.split('\\n')[0]}")
        else:
            logger.error("❌ Java环境异常")
            return False
            
        # 检查javac版本
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Java编译器正常")
            logger.info(f"javac版本: {result.stderr}")
        else:
            logger.error("❌ Java编译器异常")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Java环境测试失败: {e}")
        return False

def test_maven_environment():
    """测试Maven环境"""
    logger.info("=== Maven环境测试 ===")
    
    try:
        import subprocess
        
        # 检查Maven版本
        result = subprocess.run(['mvn', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Maven环境正常")
            logger.info(f"Maven版本: {result.stdout.split('\\n')[0]}")
        else:
            logger.error("❌ Maven环境异常")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Maven环境测试失败: {e}")
        return False

def test_java_compilation():
    """测试Java编译"""
    logger.info("=== Java编译测试 ===")
    
    try:
        import subprocess
        
        # 测试简单Java文件编译
        java_file = "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/AgentStore/SimpleTestAgent.java"
        
        if not os.path.exists(java_file):
            logger.error(f"❌ Java文件不存在: {java_file}")
            return False
        
        # 编译Java文件
        result = subprocess.run(['javac', java_file], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ 简单Java文件编译成功")
        else:
            logger.error(f"❌ 简单Java文件编译失败: {result.stderr}")
            return False
        
        # 测试Maven编译
        java_project_root = "/Users/liou/project/llm/ChainStream/chainstream/runtime/java"
        result = subprocess.run(['mvn', 'compile'], cwd=java_project_root, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Maven编译成功")
        else:
            logger.error(f"❌ Maven编译失败: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Java编译测试失败: {e}")
        return False

def test_grpc_generation():
    """测试gRPC代码生成"""
    logger.info("=== gRPC代码生成测试 ===")
    
    try:
        # 检查生成的gRPC文件
        grpc_files = [
            "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/chainstream_bridge_pb2.py",
            "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/chainstream_bridge_pb2_grpc.py"
        ]
        
        for file_path in grpc_files:
            if os.path.exists(file_path):
                logger.info(f"✅ gRPC文件存在: {os.path.basename(file_path)}")
            else:
                logger.error(f"❌ gRPC文件不存在: {file_path}")
                return False
        
        # 测试导入gRPC模块
        try:
            sys.path.insert(0, "/Users/liou/project/llm/ChainStream/chainstream/runtime/java")
            import chainstream_bridge_pb2
            import chainstream_bridge_pb2_grpc
            logger.info("✅ gRPC模块导入成功")
        except Exception as e:
            logger.error(f"❌ gRPC模块导入失败: {e}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ gRPC代码生成测试失败: {e}")
        return False

def test_java_agent_executor():
    """测试Java Agent执行器"""
    logger.info("=== Java Agent执行器测试 ===")
    
    try:
        from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor
        
        # 创建执行器
        executor = JavaAgentExecutor()
        logger.info("✅ Java Agent执行器创建成功")
        
        # 测试简单Java Agent编译
        java_file = "/Users/liou/project/llm/ChainStream/chainstream/runtime/java/AgentStore/SimpleTestAgent.java"
        
        if os.path.exists(java_file):
            logger.info("✅ 简单Java Agent文件存在")
        else:
            logger.error("❌ 简单Java Agent文件不存在")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Java Agent执行器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    logger.info("=== ChainStream Java集成测试总结 ===")
    
    tests = [
        ("Java环境", test_java_environment),
        ("Maven环境", test_maven_environment),
        ("Java编译", test_java_compilation),
        ("gRPC代码生成", test_grpc_generation),
        ("Java Agent执行器", test_java_agent_executor)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\\n--- 测试: {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"测试 {test_name} 出现异常: {e}")
            results.append((test_name, False))
    
    # 总结
    logger.info("\\n=== 测试总结 ===")
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\\n总计: {total} 个测试，通过: {passed} 个")
    
    if passed == total:
        logger.info("🎉 所有测试通过！Java集成基本功能正常")
    else:
        logger.info("⚠️ 部分测试失败，需要进一步调试")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
