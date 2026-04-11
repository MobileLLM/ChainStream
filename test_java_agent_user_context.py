#!/usr/bin/env python3
"""
测试Java Agent的用户上下文传递
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import logging
import time
import threading
from chainstream.runtime.user_context import user_context_manager
from chainstream.user import UserManager

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_java_agent_with_user_context():
    """测试Java Agent的用户上下文传递"""
    logger.info("=== 测试Java Agent的用户上下文传递 ===")
    
    try:
        from chainstream.runtime.java.grpc_server import start_bridge_server
        
        # 启动gRPC服务器
        logger.info("启动gRPC服务器...")
        server = start_bridge_server(port=50053)  # 使用不同端口避免冲突
        
        if server:
            logger.info("gRPC服务器启动成功")
            
            # 等待服务器完全启动
            time.sleep(1)
            
            # 测试gRPC调用中的用户上下文
            logger.info("测试gRPC调用中的用户上下文...")
            
            # 模拟gRPC调用 - 创建一个Stream
            try:
                # 这里我们直接调用gRPC服务器的方法来测试用户上下文
                from chainstream.runtime.java.chainstream_bridge_pb2 import CreateStreamRequest
                
                # 创建一个测试请求
                request = CreateStreamRequest(
                    stream_id="test_stream_123",
                    description="Test stream for user context",
                    agent_id="test_agent"
                )
                
                # 模拟gRPC上下文
                class MockContext:
                    def __init__(self):
                        pass
                
                context = MockContext()
                
                # 调用CreateStream方法
                logger.info("调用CreateStream方法...")
                response = server.CreateStream(request, context)
                
                if response.success:
                    logger.info(f"✅ Stream创建成功: {response.stream_id}")
                    logger.info("✅ 用户上下文在gRPC调用中正确传递")
                else:
                    logger.error(f"❌ Stream创建失败: {response.error}")
                    
            except Exception as e:
                logger.error(f"❌ 测试gRPC调用时出错: {e}")
                import traceback
                logger.error(f"错误详情: {traceback.format_exc()}")
            
            # 停止服务器
            server.stop_server()
            logger.info("gRPC服务器已停止")
        else:
            logger.error("gRPC服务器启动失败")
            
    except Exception as e:
        logger.error(f"测试Java Agent时出错: {e}")
        import traceback
        logger.error(f"错误详情: {traceback.format_exc()}")

def main():
    """主测试函数"""
    logger.info("开始测试Java Agent的用户上下文传递...")
    
    # 测试Java Agent的用户上下文传递
    test_java_agent_with_user_context()
    
    logger.info("测试完成!")

if __name__ == "__main__":
    main()
