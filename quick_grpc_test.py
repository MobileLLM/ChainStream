#!/usr/bin/env python3
"""
快速gRPC连接测试工具
用于快速验证Java和Python之间的gRPC通信
"""

import grpc
import sys
import os
import time
import logging

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入gRPC相关模块
from chainstream.runtime.java import chainstream_bridge_pb2
from chainstream.runtime.java import chainstream_bridge_pb2_grpc

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_grpc_connection(host="localhost", port=50051):
    """测试gRPC连接"""
    logger.info(f"🔍 Testing gRPC connection to {host}:{port}")
    
    try:
        # 创建gRPC通道
        channel = grpc.insecure_channel(f'{host}:{port}')
        
        # 测试连接
        grpc.channel_ready_future(channel).result(timeout=5)
        logger.info("✅ gRPC channel connected successfully")
        
        # 创建stub
        stub = chainstream_bridge_pb2_grpc.ChainStreamBridgeStub(channel)
        
        # 测试GetRuntimeInfo
        logger.info("🧪 Testing GetRuntimeInfo...")
        request = chainstream_bridge_pb2.GetRuntimeInfoRequest()
        response = stub.GetRuntimeInfo(request)
        logger.info(f"✅ GetRuntimeInfo response: {response}")
        
        # 测试StartAgent
        logger.info("🧪 Testing StartAgent...")
        request = chainstream_bridge_pb2.StartAgentRequest(agent_id="test_agent")
        response = stub.StartAgent(request)
        logger.info(f"✅ StartAgent response: {response}")
        
        # 测试CreateStream
        logger.info("🧪 Testing CreateStream...")
        request = chainstream_bridge_pb2.CreateStreamRequest(
            stream_id="test_stream",
            description="Test stream description"
        )
        response = stub.CreateStream(request)
        logger.info(f"✅ CreateStream response: {response}")
        
        # 测试AddItem
        logger.info("🧪 Testing AddItem...")
        request = chainstream_bridge_pb2.AddItemRequest(
            stream_id="test_stream",
            item="test_item_data"
        )
        response = stub.AddItem(request)
        logger.info(f"✅ AddItem response: {response}")
        
        # 测试QueryLLM
        logger.info("🧪 Testing QueryLLM...")
        request = chainstream_bridge_pb2.QueryLLMRequest(
            query="Hello from Python test client!",
            model_types=["text"]
        )
        response = stub.QueryLLM(request)
        logger.info(f"✅ QueryLLM response: {response}")
        
        logger.info("🎉 All gRPC tests passed successfully!")
        return True
        
    except grpc.RpcError as e:
        logger.error(f"❌ gRPC RPC error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False
    finally:
        try:
            channel.close()
        except:
            pass

def start_simple_server(port=50051):
    """启动简单的gRPC服务器用于测试"""
    from concurrent import futures
    import threading
    
    logger.info(f"🚀 Starting simple gRPC server on port {port}")
    
    # 创建简单的服务器实现
    class SimpleServicer(chainstream_bridge_pb2_grpc.ChainStreamBridgeServicer):
        def __init__(self):
            self.streams = {}  # 存储stream信息
        
        def GetRuntimeInfo(self, request, context):
            logger.info("📥 GetRuntimeInfo called")
            return chainstream_bridge_pb2.GetRuntimeInfoResponse(
                success=True,
                error="",
                runtime_id="simple_test_runtime",
                status="running",
                active_agents=["test_agent"]
            )
        
        def StartAgent(self, request, context):
            logger.info(f"📥 StartAgent called: {request.agent_id}")
            return chainstream_bridge_pb2.StartAgentResponse(
                success=True,
                error="",
                agent_id=request.agent_id
                # message=f"Agent {request.agent_id} started"
            )
        
        def StopAgent(self, request, context):
            logger.info(f"📥 StopAgent called: {request.agent_id}")
            return chainstream_bridge_pb2.StopAgentResponse(
                success=True,
                error="",
                # message=f"Agent {request.agent_id} stopped"
                agent_id=request.agent_id
            )
        
        def CreateStream(self, request, context):
            logger.info(f"📥 CreateStream called: {request.stream_id}")
            # 存储stream信息
            self.streams[request.stream_id] = {
                'description': request.description,
                'items': []
            }
            return chainstream_bridge_pb2.CreateStreamResponse(
                success=True,
                error="",
                stream_id=request.stream_id
            )
        
        def GetStream(self, request, context):
            logger.info(f"📥 GetStream called: {request.stream_id}")
            if request.stream_id in self.streams:
                stream_info = self.streams[request.stream_id]
                return chainstream_bridge_pb2.GetStreamResponse(
                    success=True,
                    error="",
                    stream_id=request.stream_id,
                    description=stream_info['description']
                )
            else:
                return chainstream_bridge_pb2.GetStreamResponse(
                    success=False,
                    error=f"Stream {request.stream_id} not found",
                    stream_id="",
                    description=""
                )
        
        def AddItem(self, request, context):
            logger.info(f"📥 AddItem called: {request.stream_id} -> {request.item}")
            if request.stream_id in self.streams:
                self.streams[request.stream_id]['items'].append(request.item)
                return chainstream_bridge_pb2.AddItemResponse(
                    success=True,
                    error=""
                )
            else:
                return chainstream_bridge_pb2.AddItemResponse(
                    success=False,
                    error=f"Stream {request.stream_id} not found"
                )
        
        def RegisterStreamListener(self, request, context):
            logger.info(f"📥 RegisterStreamListener called: {request.stream_id}")
            return chainstream_bridge_pb2.RegisterStreamListenerResponse(
                success=True,
                error=""
            )
        
        def QueryLLM(self, request, context):
            logger.info(f"📥 QueryLLM called: {request.query}")
            return chainstream_bridge_pb2.QueryLLMResponse(
                success=True,
                error="",
                response=f"Echo: {request.query}"
            )
        
        def GetModelInfo(self, request, context):
            logger.info(f"📥 GetModelInfo called: {request.model_types}")
            # 创建模拟的模型信息
            models = []
            for model_type in request.model_types:
                models.append(chainstream_bridge_pb2.ModelInfo(
                    name=f"mock_{model_type}_model",
                    type=model_type,
                    available=True
                ))
            
            return chainstream_bridge_pb2.GetModelInfoResponse(
                success=True,
                error="",
                models=models
            )
    
    # 创建并启动服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = SimpleServicer()
    chainstream_bridge_pb2_grpc.add_ChainStreamBridgeServicer_to_server(servicer, server)
    
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    server.start()
    
    logger.info(f"✅ Simple gRPC server started on {listen_addr}")
    
    try:
        # 保持服务器运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down server...")
        server.stop(0)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick gRPC Test Tool")
    parser.add_argument("--mode", choices=["test", "server"], default="test",
                       help="Mode: test connection or start server")
    parser.add_argument("--host", default="localhost", help="gRPC server host")
    parser.add_argument("--port", type=int, default=50051, help="gRPC server port")
    
    args = parser.parse_args()
    
    if args.mode == "test":
        success = test_grpc_connection(args.host, args.port)
        sys.exit(0 if success else 1)
    elif args.mode == "server":
        start_simple_server(args.port)
