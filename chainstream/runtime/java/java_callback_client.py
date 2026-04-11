"""
Java Callback gRPC Client
Python端用于调用Java Agent的gRPC Server，实现listener回调
"""
import grpc
import logging
from typing import Optional
from .chainstream_bridge_pb2_grpc import JavaAgentCallbackStub
from .chainstream_bridge_pb2 import InvokeListenerRequest

logger = logging.getLogger(__name__)


class JavaCallbackClient:
    """
    Java Agent回调客户端
    用于Python调用Java Agent的listener函数
    """
    
    def __init__(self, callback_address: str):
        """
        初始化Java回调客户端
        
        Args:
            callback_address: Java gRPC Server地址，格式：host:port
        """
        self.callback_address = callback_address
        self.channel = None
        self.stub = None
        self._connect()
        
    def _connect(self):
        """建立到Java gRPC Server的连接"""
        try:
            self.channel = grpc.insecure_channel(self.callback_address)
            # 导入生成的gRPC代码
            from .chainstream_bridge_pb2_grpc import JavaAgentCallbackStub
            self.stub = JavaAgentCallbackStub(self.channel)
            logger.info(f"Connected to Java Agent callback server at {self.callback_address}")
        except Exception as e:
            logger.error(f"Failed to connect to Java callback server at {self.callback_address}: {e}")
            raise
    
    def invoke_listener(self, agent_id: str, listener_id: str, item_data: str) -> dict:
        """
        调用Java端的listener
        
        Args:
            agent_id: Agent ID
            listener_id: Listener ID
            item_data: 要处理的数据（JSON字符串）
            
        Returns:
            dict: {
                'success': bool,
                'error': str,
                'result_data': str,
                'has_result': bool
            }
        """
        try:
            from .chainstream_bridge_pb2 import InvokeListenerRequest
            
            request = InvokeListenerRequest(
                agent_id=agent_id,
                listener_id=listener_id,
                item_data=item_data
            )
            
            logger.debug(f"Invoking Java listener {listener_id} with data: {item_data[:100]}...")
            
            response = self.stub.InvokeListener(request, timeout=30)
            
            result = {
                'success': response.success,
                'error': response.error if hasattr(response, 'error') else '',
                'result_data': response.result_data if hasattr(response, 'result_data') else '',
                'has_result': response.has_result if hasattr(response, 'has_result') else False
            }
            
            if result['success']:
                logger.debug(f"Java listener {listener_id} invoked successfully")
            else:
                logger.error(f"Java listener {listener_id} failed: {result['error']}")
            
            return result
            
        except grpc.RpcError as e:
            logger.error(f"gRPC error invoking Java listener {listener_id}: {e}")
            return {
                'success': False,
                'error': f"gRPC error: {e.code()} - {e.details()}",
                'result_data': '',
                'has_result': False
            }
        except Exception as e:
            logger.error(f"Error invoking Java listener {listener_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'result_data': '',
                'has_result': False
            }
    
    def close(self):
        """关闭连接"""
        if self.channel:
            self.channel.close()
            logger.info(f"Closed connection to Java callback server at {self.callback_address}")
    
    def __del__(self):
        """析构函数，确保连接被关闭"""
        self.close()

