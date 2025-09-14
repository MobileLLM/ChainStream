#!/usr/bin/env python3
"""
gRPC通信调试工具
用于调试Java Agent与Python Runtime的gRPC通信问题
"""

import grpc
import logging
import time
import threading
from concurrent import futures
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入gRPC相关模块
from chainstream.runtime.java import chainstream_bridge_pb2
from chainstream.runtime.java import chainstream_bridge_pb2_grpc

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('grpc_debug.log')
    ]
)

logger = logging.getLogger(__name__)

class DebugGrpcServer(chainstream_bridge_pb2_grpc.ChainStreamBridgeServicer):
    """调试用gRPC服务器，记录所有请求和响应"""
    
    def __init__(self):
        self.request_count = 0
        self.requests_log = []
        
    def _log_request(self, method_name, request, response):
        """记录请求和响应"""
        self.request_count += 1
        log_entry = {
            'id': self.request_count,
            'method': method_name,
            'request': str(request),
            'response': str(response),
            'timestamp': time.time()
        }
        self.requests_log.append(log_entry)
        
        logger.info(f"=== gRPC Request #{self.request_count} ===")
        logger.info(f"Method: {method_name}")
        logger.info(f"Request: {request}")
        logger.info(f"Response: {response}")
        logger.info("=" * 50)
    
    def StartAgent(self, request, context):
        logger.info("🔵 StartAgent called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.StartAgentResponse(
            success=True,
            error="",
            message=f"Debug: Agent {request.agent_id} started"
        )
        
        self._log_request("StartAgent", request, response)
        return response
    
    def StopAgent(self, request, context):
        logger.info("🔴 StopAgent called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.StopAgentResponse(
            success=True,
            error="",
            message=f"Debug: Agent {request.agent_id} stopped"
        )
        
        self._log_request("StopAgent", request, response)
        return response
    
    def CreateStream(self, request, context):
        logger.info("🟢 CreateStream called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.CreateStreamResponse(
            success=True,
            error="",
            stream_id=request.stream_id
        )
        
        self._log_request("CreateStream", request, response)
        return response
    
    def GetStream(self, request, context):
        logger.info("🟡 GetStream called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.GetStreamResponse(
            success=True,
            error="",
            stream_id=request.stream_id,
            description="Debug stream"
        )
        
        self._log_request("GetStream", request, response)
        return response
    
    def AddItem(self, request, context):
        logger.info("🟣 AddItem called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.AddItemResponse(
            success=True,
            error=""
        )
        
        self._log_request("AddItem", request, response)
        return response
    
    def RegisterStreamListener(self, request, context):
        logger.info("🟠 RegisterStreamListener called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.RegisterStreamListenerResponse(
            success=True,
            error=""
        )
        
        self._log_request("RegisterStreamListener", request, response)
        return response
    
    def QueryLLM(self, request, context):
        logger.info("🔵 QueryLLM called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.QueryLLMResponse(
            success=True,
            error="",
            response=f"Debug LLM response for: {request.query}"
        )
        
        self._log_request("QueryLLM", request, response)
        return response
    
    def GetModelInfo(self, request, context):
        logger.info("🟡 GetModelInfo called")
        logger.info(f"Request: {request}")
        
        model_info = chainstream_bridge_pb2.ModelInfo(
            name="debug_model",
            type="text",
            available=True
        )
        
        response = chainstream_bridge_pb2.GetModelInfoResponse(
            success=True,
            error="",
            models=[model_info]
        )
        
        self._log_request("GetModelInfo", request, response)
        return response
    
    def GetRuntimeInfo(self, request, context):
        logger.info("🟢 GetRuntimeInfo called")
        logger.info(f"Request: {request}")
        
        response = chainstream_bridge_pb2.GetRuntimeInfoResponse(
            success=True,
            error="",
            runtime_id="debug_runtime",
            status="running",
            active_agents=["debug_agent"]
        )
        
        self._log_request("GetRuntimeInfo", request, response)
        return response

def start_debug_server(port=50051):
    """启动调试gRPC服务器"""
    logger.info(f"🚀 Starting debug gRPC server on port {port}")
    
    # 创建gRPC服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # 添加调试服务
    debug_servicer = DebugGrpcServer()
    chainstream_bridge_pb2_grpc.add_ChainStreamBridgeServicer_to_server(debug_servicer, server)
    
    # 启动服务器
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    server.start()
    
    logger.info(f"✅ Debug gRPC server started on {listen_addr}")
    logger.info("📝 All requests will be logged to grpc_debug.log")
    
    try:
        # 保持服务器运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down debug gRPC server...")
        server.stop(0)
        logger.info("📊 Request summary:")
        logger.info(f"Total requests processed: {debug_servicer.request_count}")
        for log_entry in debug_servicer.requests_log:
            logger.info(f"  {log_entry['id']}: {log_entry['method']}")

def test_grpc_client():
    """测试gRPC客户端连接"""
    logger.info("🧪 Testing gRPC client connection...")
    
    try:
        # 创建gRPC通道
        channel = grpc.insecure_channel('localhost:50051')
        stub = chainstream_bridge_pb2_grpc.ChainStreamBridgeStub(channel)
        
        # 测试GetRuntimeInfo
        logger.info("Testing GetRuntimeInfo...")
        request = chainstream_bridge_pb2.GetRuntimeInfoRequest()
        response = stub.GetRuntimeInfo(request)
        logger.info(f"Response: {response}")
        
        # 测试StartAgent
        logger.info("Testing StartAgent...")
        request = chainstream_bridge_pb2.StartAgentRequest(agent_id="test_agent")
        response = stub.StartAgent(request)
        logger.info(f"Response: {response}")
        
        # 测试CreateStream
        logger.info("Testing CreateStream...")
        request = chainstream_bridge_pb2.CreateStreamRequest(
            stream_id="test_stream",
            description="Test stream"
        )
        response = stub.CreateStream(request)
        logger.info(f"Response: {response}")
        
        # 测试AddItem
        logger.info("Testing AddItem...")
        request = chainstream_bridge_pb2.AddItemRequest(
            stream_id="test_stream",
            item="test_item"
        )
        response = stub.AddItem(request)
        logger.info(f"Response: {response}")
        
        logger.info("✅ All gRPC tests passed!")
        
    except Exception as e:
        logger.error(f"❌ gRPC test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="gRPC Communication Debug Tool")
    parser.add_argument("--mode", choices=["server", "client", "both"], default="server",
                       help="Run mode: server, client, or both")
    parser.add_argument("--port", type=int, default=50051, help="gRPC server port")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        start_debug_server(args.port)
    elif args.mode == "client":
        test_grpc_client()
    elif args.mode == "both":
        # 启动服务器线程
        server_thread = threading.Thread(target=start_debug_server, args=(args.port,))
        server_thread.daemon = True
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 运行客户端测试
        test_grpc_client()
        
        # 保持主线程运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
