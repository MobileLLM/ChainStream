"""
Java Listener Function Wrapper
用于在Python端包装Java的listener函数，当被调用时通过gRPC回调Java端执行
"""
import logging
import json
import inspect
import threading

logger = logging.getLogger(__name__)

# 线程本地存储，用于跟踪当前正在执行的Java listener
_current_java_listener = threading.local()


def get_current_java_listener_context():
    """
    获取当前正在执行的Java listener上下文
    
    Returns:
        dict: {'func_id': str, 'agent': Agent, 'listener_name': str} 或 None
    """
    if hasattr(_current_java_listener, 'func_id') and _current_java_listener.func_id:
        return {
            'func_id': _current_java_listener.func_id,
            'agent': _current_java_listener.agent,
            'listener_name': _current_java_listener.listener_name
        }
    return None


class JavaListenerFunction:
    """
    Java Listener的Python包装器
    当这个函数被Stream调用时，会通过gRPC调用Java端的实际listener实现
    """
    
    def __init__(self, agent, listener_id, listener_name, callback_address, real_agent_id=None):
        """
        初始化Java Listener包装器
        
        Args:
            agent: Java agent的代理对象(通常是java_agent_proxy)
            listener_id: listener的唯一标识符
            listener_name: listener的函数名称
            callback_address: Java gRPC Server地址（host:port）
            real_agent_id: 真实的Java agent ID（用于上下文追踪）
        """
        self.agent = agent
        self.listener_id = listener_id
        self.listener_name = listener_name
        self.callback_address = callback_address
        self.real_agent_id = real_agent_id or (agent.agent_id if hasattr(agent, 'agent_id') else None)
        self.func_id = f"java_listener_{listener_id}"
        
        # 用于兼容AgentFunction的属性
        self.is_java_listener = True
        self._output_stream = None
        
        # 添加__qualname__属性以兼容base_stream.py的检查
        # 使用"<locals>"标记来表示这不是类方法，而是一个lambda/匿名函数风格的listener
        self.__qualname__ = f"<locals>.{listener_name}"
        
        # 添加__name__属性
        self.__name__ = listener_name
        
        # 添加__signature__属性以兼容inspect.signature检查
        # Java listener接受一个参数（data），返回void或result
        self.__signature__ = inspect.Signature([
            inspect.Parameter('data', inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ])
        
        # 创建gRPC客户端连接到Java Server
        self._grpc_client = None
        self._init_grpc_client()
        
        logger.info(f"Created JavaListenerFunction: {listener_name} (ID: {listener_id}, Address: {callback_address})")
    
    def _init_grpc_client(self):
        """初始化gRPC客户端"""
        try:
            from .java_callback_client import JavaCallbackClient
            self._grpc_client = JavaCallbackClient(self.callback_address)
            logger.debug(f"Initialized gRPC client for {self.listener_name}")
        except Exception as e:
            logger.error(f"Failed to initialize gRPC client for {self.listener_name}: {e}")
            self._grpc_client = None
    
    def __call__(self, item):
        """
        当listener被调用时，通过gRPC转发到Java端执行
        
        Args:
            item: 要处理的数据项
            
        Returns:
            Java listener的返回值（如果有）
        """
        if not self._grpc_client:
            logger.error(f"gRPC client not initialized for {self.listener_name}")
            return None
        
        # 设置Java listener执行上下文
        # 必须在调用Java之前就设置好上下文，因为Java可能立即进行内部addItem调用
        if self.real_agent_id:
            try:
                from chainstream.runtime.java.grpc_server import set_java_listener_context
                set_java_listener_context(self.real_agent_id, self.func_id, self.agent)
            except ImportError:
                pass
            
        try:
            # 序列化item为JSON字符串
            if isinstance(item, str):
                item_json = item
            elif isinstance(item, dict):
                item_json = json.dumps(item)
            else:
                item_json = str(item)
            
            logger.debug(f"Invoking Java listener {self.listener_name} with item: {item_json[:100]}...")
            
            # 通过gRPC调用Java端的listener
            response = self._grpc_client.invoke_listener(
                agent_id=self.agent.agent_id,
                listener_id=self.listener_id,
                item_data=item_json
            )
            
            if not response['success']:
                logger.error(f"Java listener {self.listener_name} failed: {response['error']}")
                # 失败情况下也不清理上下文，让系统自然清理
                return None
            
            # 处理返回值
            # 注意：不要在这里手动调用add_item！
            # AgentFunction会自动处理返回值的传播
            result = None
            if response['has_result'] and response['result_data']:
                result_data = response['result_data']
                
                # 首先尝试解析为JSON
                try:
                    result = json.loads(result_data)
                    # 如果解析成功，检查返回的类型
                    if isinstance(result, list):
                        logger.info(f"🔍 Java listener {self.listener_name} returned JSON list (type: {type(result)}, length: {len(result)}): {result}")
                    elif isinstance(result, dict):
                        logger.info(f"🔍 Java listener {self.listener_name} returned JSON dict (type: {type(result)}): {result}")
                    else:
                        logger.info(f"🔍 Java listener {self.listener_name} returned JSON (type: {type(result)}): {result}")
                except json.JSONDecodeError as e:
                    logger.debug(f"Java listener {self.listener_name} result_data is not valid JSON: {e}")
                    # 如果都不是，直接返回字符串
                    logger.debug(f"Java listener {self.listener_name} returned string: {result_data}")
                    result = result_data
            else:
                logger.debug(f"Java listener {self.listener_name} returned void")
                result = None
            
            # 注意：不要在这里清理上下文！
            # Java listener可能在返回后还会继续执行内部的addItem调用
            # 上下文应该由stream处理线程在完成所有listener处理后清理
            # 或者在下一个listener开始执行时清理
            
            return result
                
        except Exception as e:
            logger.error(f"Error invoking Java listener {self.listener_name}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # 异常情况下也不清理上下文，让系统自然清理
            return None
    
    def set_output_stream(self, output_stream):
        """设置输出流，用于将返回值添加到流中"""
        self._output_stream = output_stream
        logger.debug(f"Set output stream for Java listener {self.listener_name}: {output_stream.stream_id if output_stream else None}")
    
    def __str__(self):
        return f"JavaListenerFunction({self.listener_name}, {self.listener_id})"
    
    def __repr__(self):
        return self.__str__()

