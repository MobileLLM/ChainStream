#!/usr/bin/env python3
"""
简单Java Agent测试脚本
测试不依赖gRPC的Java Agent编译和启动
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


def test_simple_java_compilation():
    """测试简单Java Agent编译"""
    logger.info("测试简单Java Agent编译...")
    
    try:
        # 查找Java Agent文件
        java_dir = project_root / "chainstream" / "runtime" / "java"
        agent_store = java_dir / "AgentStore"
        
        java_files = list(agent_store.glob("*.java"))
        if not java_files:
            logger.error("未找到Java Agent文件")
            return False
        
        logger.info(f"找到 {len(java_files)} 个Java Agent文件")
        
        # 测试编译第一个Java Agent
        java_file = java_files[0]
        logger.info(f"编译Java Agent: {java_file.name}")
        
        # 获取输出目录
        output_dir = java_file.parent
        
        # 编译命令
        cmd = ['javac', '-d', str(output_dir), str(java_file)]
        logger.info(f"编译命令: {' '.join(cmd)}")
        
        # 执行编译
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            logger.error(f"Java编译失败: {result.stderr}")
            return False
        
        logger.info("Java编译成功")
        
        # 检查class文件是否生成
        class_file = output_dir / (java_file.stem + '.class')
        if class_file.exists():
            logger.info(f"Class文件生成成功: {class_file}")
            return True
        else:
            logger.error(f"Class文件未生成: {class_file}")
            return False
            
    except Exception as e:
        logger.error(f"Java编译测试失败: {e}")
        return False


def test_simple_java_execution():
    """测试简单Java Agent执行"""
    logger.info("测试简单Java Agent执行...")
    
    try:
        # 查找Java Agent文件
        java_dir = project_root / "chainstream" / "runtime" / "java"
        agent_store = java_dir / "AgentStore"
        
        java_files = list(agent_store.glob("*.java"))
        if not java_files:
            logger.error("未找到Java Agent文件")
            return False
        
        # 测试执行第一个Java Agent
        java_file = java_files[0]
        class_name = java_file.stem
        
        logger.info(f"执行Java Agent: {class_name}")
        
        # 获取输出目录
        output_dir = java_file.parent
        
        # 执行命令
        cmd = ['java', '-cp', str(output_dir), class_name]
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        # 启动Java进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(output_dir)
        )
        
        logger.info(f"Java进程启动成功，PID: {process.pid}")
        
        # 等待一段时间
        time.sleep(3)
        
        # 检查进程是否还在运行
        if process.poll() is None:
            logger.info("Java进程正在运行")
            
            # 终止进程
            process.terminate()
            process.wait(timeout=5)
            logger.info("Java进程已终止")
            return True
        else:
            # 进程已结束，读取输出
            stdout, stderr = process.communicate()
            logger.info(f"Java进程输出: {stdout}")
            if stderr:
                logger.warning(f"Java进程错误: {stderr}")
            return True
            
    except Exception as e:
        logger.error(f"Java执行测试失败: {e}")
        return False


def test_java_environment():
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
        
        return True
        
    except Exception as e:
        logger.error(f"Java环境检查失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("开始简单Java Agent测试...")
    
    tests = [
        ("Java环境检查", test_java_environment),
        ("简单Java编译测试", test_simple_java_compilation),
        ("简单Java执行测试", test_simple_java_execution),
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
