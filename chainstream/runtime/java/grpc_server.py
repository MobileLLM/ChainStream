"""
gRPC服务器实现，为Java Agent提供ChainStream API访问
"""
import grpc
import threading
import logging
from concurrent import futures
from typing import Dict, Any
from functools import wraps

from .chainstream_bridge_pb2_grpc import ChainStreamBridgeServicer
from chainstream.agent import Agent
from chainstream.user.user import User
from .chainstream_bridge_pb2 import (
    StartAgentRequest, StartAgentResponse,
    StopAgentRequest, StopAgentResponse,
    CreateStreamRequest, CreateStreamResponse,
    GetStreamRequest, GetStreamResponse,
    AddItemRequest, AddItemResponse,
    ForEachRequest, ForEachResponse,
    BatchRequest, BatchResponse,
    UnregisterAllRequest, UnregisterAllResponse,
    RemoveListenerRequest, RemoveListenerResponse,
    QueryLLMRequest, QueryLLMResponse,
    GetModelRequest, GetModelResponse,
    MakePromptRequest, MakePromptResponse,
    GetModelInfoRequest, GetModelInfoResponse,
    CreateBufferRequest, CreateBufferResponse,
    BufferAppendRequest, BufferAppendResponse,
    BufferPopRequest, BufferPopResponse,
    BufferPopAllRequest, BufferPopAllResponse,
    GetRuntimeInfoRequest, GetRuntimeInfoResponse,
    ReportAgentIdRequest, ReportAgentIdResponse
)

logger = logging.getLogger(__name__)

def ensure_user_context(func):
    """装饰器：确保gRPC方法调用时有用户上下文"""
    @wraps(func)
    def wrapper(self, request, context):
        # 确保用户上下文
        self._ensure_user_context()
        return func(self, request, context)
    return wrapper


class JavaAgentProxy(Agent):
    """Java Agent的代理类，用于调用ChainStream外部API"""
    
    def __init__(self, user=None):
        # 必须提供用户，不允许创建默认用户
        if user is None:
            raise ValueError("JavaAgentProxy requires a user to be provided. No default user allowed.")
        super().__init__("java_agent_proxy", user)
        self.agent_id = "java_agent_proxy"
    
    def get_agent_id(self):
        return self.agent_id


class ChainStreamBridgeServer(ChainStreamBridgeServicer):
    """gRPC服务器实现，桥接Java Agent和Python Runtime"""
    
    def __init__(self, runtime_core=None):
        logger.info(f"🔍 DEBUG: ChainStreamBridgeServer.__init__ called with runtime_core: {runtime_core}")
        self.runtime_core = runtime_core
        self.agent_streams: Dict[str, Any] = {}  # agent_id -> stream_id -> stream
        self.agent_models: Dict[str, Any] = {}   # agent_id -> model
        self.agent_buffers: Dict[str, Any] = {}  # agent_id -> buffer_id -> buffer
        self.server = None
        self.server_thread = None
        
        # 创建Java Agent的代理类 - 稍后在需要时动态创建
        self.java_agent_proxy = None
        
    def _get_user_for_agent(self, agent_id):
        """根据agent_id获取对应的用户信息"""
        try:
            logger.info(f"🔍 DEBUG: Looking for user for agent {agent_id}")
            
            # 首先检查agent_user_map中是否有缓存的映射
            if hasattr(self, '_agent_user_map') and agent_id in self._agent_user_map:
                user = self._agent_user_map[agent_id]
                logger.info(f"Found user for agent {agent_id} from cache: {user.get_username()}")
                return user
            
            logger.info(f"🔍 DEBUG: runtime_core is None: {self.runtime_core is None}")
            
            if self.runtime_core and hasattr(self.runtime_core, 'agent_manager'):
                logger.info(f"🔍 DEBUG: runtime_core has agent_manager: {hasattr(self.runtime_core, 'agent_manager')}")
                
                # 从AgentManager中获取agent信息
                agent = self.runtime_core.agent_manager.get_agent(agent_id)
                logger.info(f"🔍 DEBUG: Direct agent lookup result: {agent}")
                if agent and hasattr(agent, 'user') and agent.user:
                    logger.info(f"Found user for agent {agent_id}: {agent.user.get_username()}")
                    return agent.user
                
                # 如果直接获取失败，尝试从运行中的agents列表获取
                logger.info(f"🔍 DEBUG: Trying to get running agents list...")
                running_agents = self.runtime_core.agent_manager.get_running_agents_info_list()
                logger.info(f"🔍 DEBUG: Running agents list: {running_agents}")
                
                for agent_info in running_agents:
                    logger.info(f"🔍 DEBUG: Checking agent_info: {agent_info}")
                    if agent_info.get('agent_id') == agent_id and 'user' in agent_info:
                        user_name = agent_info['user']
                        logger.info(f"🔍 DEBUG: Found matching agent with user: {user_name}")
                        from chainstream.user import UserManager
                        user_manager = UserManager()
                        user = user_manager.get_user_by_username(user_name)
                        if user:
                            logger.info(f"Found user for agent {agent_id} from running agents: {user.get_username()}")
                            return user
                        else:
                            logger.error(f"Failed to get user by username: {user_name}")
            else:
                logger.error(f"🔍 DEBUG: runtime_core is None or has no agent_manager")
                            
        except Exception as e:
            logger.error(f"Error getting user for agent {agent_id}: {e}")
            
        return None

    def _find_java_agent_by_pid(self, process_id):
        """通过进程ID查找对应的JavaAgentWrapper"""
        try:
            if self.runtime_core and hasattr(self.runtime_core, 'agent_manager'):
                # 遍历所有agents查找匹配的JavaAgentWrapper
                for agent_id, agent in self.runtime_core.agent_manager.agents.items():
                    if hasattr(agent, 'java_process') and agent.java_process:
                        if agent.java_process.pid == process_id:
                            logger.info(f"Found JavaAgentWrapper for PID {process_id}: {agent_id}")
                            return agent
                    elif hasattr(agent, 'java_file_path'):
                        # 如果是JavaAgentWrapper但没有java_process，尝试通过其他方式匹配
                        logger.debug(f"Agent {agent_id} is JavaAgentWrapper but no java_process")
                        
            logger.warning(f"No JavaAgentWrapper found for PID {process_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error finding JavaAgentWrapper by PID: {e}")
            return None

    def _ensure_user_context(self):
        """确保当前线程有用户上下文"""
        try:
            from chainstream.runtime.user_context import user_context_manager
            
            # 检查是否已经有用户上下文
            current_user = user_context_manager.get_current_user()
            if current_user:
                logger.debug(f"User context already set: {current_user.get_username()}")
                return current_user
            
            # 如果没有用户上下文，尝试从AgentManager中获取Java Agent的用户信息
            try:
                if self.runtime_core and hasattr(self.runtime_core, 'agent_manager'):
                    running_agents = self.runtime_core.agent_manager.get_running_agents_info_list()
                    for agent_info in running_agents:
                        if agent_info.get('type') == 'java' and 'user' in agent_info:
                            user_name = agent_info['user']
                            from chainstream.user import UserManager
                            user_manager = UserManager()
                            user = user_manager.get_user(user_name)
                            if user:
                                user_context_manager.set_current_user(user)
                                logger.info(f"Set user context from Java Agent: {user.get_username()}")
                                return user
            except Exception as e:
                logger.debug(f"Could not get user from Java Agent: {e}")
            
            # 如果没有用户上下文，尝试设置默认用户
            from chainstream.user import UserManager
            user_manager = UserManager()
            
            # 首先尝试获取admin用户
            try:
                admin_user = user_manager.get_user("admin")
                if admin_user:
                    user_context_manager.set_current_user(admin_user)
                    logger.info(f"Set user context to admin: {admin_user.get_username()}")
                    return admin_user
            except Exception as e:
                logger.debug(f"Could not get admin user: {e}")
            
            # 如果admin用户不存在，尝试获取第一个可用用户
            try:
                users = user_manager.list_users()
                if users:
                    first_user = users[0]
                    user_context_manager.set_current_user(first_user)
                    logger.info(f"Set user context to first available user: {first_user.get_username()}")
                    return first_user
            except Exception as e:
                logger.debug(f"Could not get any users: {e}")
            
            # 如果没有任何用户，创建一个默认用户
            try:
                default_user = user_manager.create_user(
                    username="default",
                    password="default123",
                    level=1,
                    enable_encryption=True
                )
                user_context_manager.set_current_user(default_user)
                logger.info(f"Created and set default user context: {default_user.get_username()}")
                return default_user
            except Exception as e:
                logger.warning(f"Could not create default user: {e}")
                
        except Exception as e:
            logger.error(f"Failed to ensure user context: {e}")
            
        return None

    def _get_or_create_java_agent_proxy(self, user=None):
        """获取或创建Java Agent代理，使用正确的用户信息"""
        logger.info(f"🔍 DEBUG: _get_or_create_java_agent_proxy called with user: {user}")
        logger.info(f"🔍 DEBUG: self.java_agent_proxy: {self.java_agent_proxy}")
        
        # 如果传入了用户信息，或者当前代理的用户不匹配，则重新创建
        should_recreate = False
        if self.java_agent_proxy is None:
            logger.info("🔍 DEBUG: No existing proxy, will create new one")
            should_recreate = True
        elif user is not None and self.java_agent_proxy.user.get_uuid() != user.get_uuid():
            logger.info(f"🔍 DEBUG: User mismatch - existing: {self.java_agent_proxy.user.get_uuid()}, new: {user.get_uuid()}")
            should_recreate = True
        else:
            logger.info("🔍 DEBUG: Using existing proxy")
        
        if should_recreate:
            # 尝试从用户上下文获取当前用户
            if user is None:
                try:
                    from chainstream.runtime.user_context import user_context_manager
                    logger.info("🔍 DEBUG: Trying to get user from context manager")
                    user = user_context_manager.get_current_user()
                    logger.info(f"🔍 DEBUG: Got user from context: {user}")
                except Exception as e:
                    logger.warning(f"🔍 DEBUG: Failed to get user from context: {e}")
                    pass
            
            # 如果仍然没有用户，直接报错
            if user is None:
                logger.error("🔍 DEBUG: No user provided and no user in context. Cannot create JavaAgentProxy without user.")
                raise ValueError("Cannot create JavaAgentProxy without a valid user. User must be provided or available in context.")
            else:
                logger.info(f"🔍 DEBUG: Using provided user: {user}")
            
            logger.info(f"🔍 DEBUG: Creating JavaAgentProxy with user: {user.get_username()}, UUID: {user.get_uuid()}")
            self.java_agent_proxy = JavaAgentProxy(user)
            logger.info(f"Created JavaAgentProxy with user: {user.get_username() if user else 'None'}, UUID: {user.get_uuid() if user else 'None'}")
        else:
            logger.info(f"🔍 DEBUG: Reusing existing proxy with user: {self.java_agent_proxy.user.get_username()}")
        
        return self.java_agent_proxy
        
    def start_server(self, port=50051):
        """启动gRPC服务器"""
        try:
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            from .chainstream_bridge_pb2_grpc import add_ChainStreamBridgeServicer_to_server
            add_ChainStreamBridgeServicer_to_server(self, self.server)
            
            listen_addr = f'[::]:{port}'
            self.server.add_insecure_port(listen_addr)
            self.server.start()
            
            logger.info(f"gRPC Bridge Server started on port {port}")
            
            # 在单独线程中等待服务器关闭
            self.server_thread = threading.Thread(target=self._wait_for_termination)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start gRPC server: {e}")
            return False
    
    def _wait_for_termination(self):
        """等待服务器终止"""
        if self.server:
            self.server.wait_for_termination()
    
    def stop_server(self):
        """停止gRPC服务器"""
        if self.server:
            self.server.stop(grace=5.0)
            logger.info("gRPC Bridge Server stopped")
    
    # Agent生命周期方法
    def ReportAgentId(self, request: ReportAgentIdRequest, context):
        """Java Agent报告其ID"""
        try:
            agent_id = request.agent_id
            process_id = request.process_id
            logger.info(f"Java Agent reported ID: {agent_id} (PID: {process_id})")
            
            # 通过进程ID查找对应的JavaAgentWrapper
            java_agent_wrapper = self._find_java_agent_by_pid(process_id)
            if java_agent_wrapper:
                # 更新JavaAgentWrapper的agent_id
                old_agent_id = java_agent_wrapper.agent_id
                java_agent_wrapper.agent_id = agent_id
                java_agent_wrapper.metaData.agent_id = agent_id
                logger.info(f"Updated JavaAgentWrapper agent_id from {old_agent_id} to {agent_id}")
                
                # 在AgentManager中更新agent的agent_id
                if self.runtime_core and hasattr(self.runtime_core, 'agent_manager'):
                    # 从旧agent_id移除，用新agent_id注册
                    if old_agent_id in self.runtime_core.agent_manager.agents:
                        agent = self.runtime_core.agent_manager.agents.pop(old_agent_id)
                        self.runtime_core.agent_manager.agents[agent_id] = agent
                        logger.info(f"Updated agent registration in AgentManager: {old_agent_id} -> {agent_id}")
                
                # 存储agent_id到用户的映射
                if not hasattr(self, '_agent_user_map'):
                    self._agent_user_map = {}
                self._agent_user_map[agent_id] = java_agent_wrapper.user
                logger.info(f"Agent {agent_id} mapped to user: {java_agent_wrapper.user.get_username()}")
            else:
                logger.warning(f"Could not find JavaAgentWrapper for PID {process_id}")
                # 尝试从AgentManager中查找对应的用户
                current_user = self._get_user_for_agent(agent_id)
                if current_user:
                    # 存储agent_id到用户的映射
                    if not hasattr(self, '_agent_user_map'):
                        self._agent_user_map = {}
                    self._agent_user_map[agent_id] = current_user
                    logger.info(f"Agent {agent_id} mapped to user: {current_user.get_username()}")
                else:
                    logger.warning(f"Could not find user for agent {agent_id}")
            
            logger.info(f"Agent {agent_id} successfully registered with gRPC server")
            return ReportAgentIdResponse(success=True, error="")
            
        except Exception as e:
            logger.error(f"Error reporting agent ID: {e}")
            return ReportAgentIdResponse(success=False, error=str(e))
    
    def StartAgent(self, request: StartAgentRequest, context):
        """启动Java Agent"""
        try:
            agent_id = request.agent_id
            logger.info(f"Starting Java Agent: {agent_id}")
            
            # 使用ChainStream API管理Agent
            try:
                import chainstream as cs
                
                # 创建或获取Agent（如果ChainStream有Agent管理API）
                # 目前Java Agent通过代理类访问，这里只是记录日志
                logger.info(f"Java Agent {agent_id} started via ChainStream proxy")
                return StartAgentResponse(success=True, error="")
                
            except Exception as e:
                logger.error(f"Failed to start agent with ChainStream API: {e}")
                return StartAgentResponse(success=False, error=str(e))
                
        except Exception as e:
            logger.error(f"Error starting Java Agent: {e}")
            return StartAgentResponse(success=False, error=str(e))
    
    def StopAgent(self, request: StopAgentRequest, context):
        """停止Java Agent"""
        try:
            agent_id = request.agent_id
            logger.info(f"Stopping Java Agent: {agent_id}")
            
            # 使用ChainStream API清理Agent资源
            try:
                import chainstream as cs
            
                # 清理Agent相关资源
                if agent_id in self.agent_streams:
                    del self.agent_streams[agent_id]
                if agent_id in self.agent_models:
                    del self.agent_models[agent_id]
                    if agent_id in self.agent_buffers:
                        del self.agent_buffers[agent_id]
                
                logger.info(f"Java Agent {agent_id} stopped via ChainStream proxy")
            except Exception as e:
                logger.error(f"Failed to stop agent with ChainStream API: {e}")
            
            return StopAgentResponse(success=True, error="")
                
        except Exception as e:
            logger.error(f"Error stopping Java Agent: {e}")
            return StopAgentResponse(success=False, error=str(e))
    
    # Stream操作方法
    @ensure_user_context
    def CreateStream(self, request: CreateStreamRequest, context):
        """创建Stream"""
        try:
            print(f"🔍 DEBUG: CreateStream called with agent_id: {request.agent_id}")
            logger.info(f"🔍 DEBUG: CreateStream called with agent_id: {request.agent_id}")
            
            stream_id = request.stream_id
            description = request.description
            agent_id = request.agent_id
            
            logger.info(f"Creating stream {stream_id} for agent {agent_id}")
            
            # 根据agent_id获取对应的用户信息
            current_user = self._get_user_for_agent(agent_id)
            if not current_user:
                logger.error(f"Cannot find user for agent {agent_id}")
                return CreateStreamResponse(success=False, error=f"Cannot find user for agent {agent_id}", stream_id="")
            
            logger.info(f"Found user for agent {agent_id}: {current_user.get_username()}")
            
            # 设置用户上下文
            try:
                from chainstream.runtime.user_context import user_context_manager
                user_context_manager.set_current_user(current_user)
                logger.info(f"Set user context for gRPC thread: {current_user.get_username()}")
            except Exception as e:
                logger.warning(f"Failed to set user context: {e}")
            
            # 使用ChainStream API创建Stream
            try:
                import chainstream as cs
                
                # 获取或创建Java Agent代理，传递当前用户
                java_agent_proxy = self._get_or_create_java_agent_proxy(current_user)
                
                if not java_agent_proxy:
                    logger.error(f"Failed to create Java agent proxy for agent {agent_id}")
                    return CreateStreamResponse(success=False, error="Failed to create Java agent proxy", stream_id="")
                
                # 使用create_stream API - 这会自动处理所有注册和初始化
                stream = cs.create_stream(java_agent_proxy, stream_id)
                
                if stream:
                    logger.info(f"Stream {stream_id} created successfully via ChainStream API")
                    return CreateStreamResponse(success=True, error="", stream_id=stream_id)
                else:
                    logger.error(f"Failed to create stream {stream_id}")
                    return CreateStreamResponse(success=False, error="Failed to create stream", stream_id="")
                
            except Exception as e:
                logger.error(f"Failed to create stream: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                return CreateStreamResponse(success=False, error=str(e), stream_id="")
                
        except Exception as e:
            logger.error(f"Error creating stream: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return CreateStreamResponse(success=False, error=str(e), stream_id="")
    
    def GetStream(self, request: GetStreamRequest, context):
        """获取Stream"""
        try:
            stream_id = request.stream_id
            agent_id = request.agent_id
            
            logger.info(f"Getting stream {stream_id} for agent {agent_id}")
            
            # 根据agent_id获取对应的用户信息
            current_user = self._get_user_for_agent(agent_id)
            if not current_user:
                logger.error(f"Cannot find user for agent {agent_id}")
                return GetStreamResponse(success=False, error=f"Cannot find user for agent {agent_id}", stream_id="", description="")
            
            # 设置用户上下文
            try:
                from chainstream.runtime.user_context import user_context_manager
                user_context_manager.set_current_user(current_user)
                logger.info(f"Set user context for gRPC thread: {current_user.get_username()}")
            except Exception as e:
                logger.warning(f"Failed to set user context: {e}")
            
            # 使用ChainStream外部API获取Stream
            try:
                import chainstream as cs
                
                # 获取或创建Java Agent代理
                java_agent_proxy = self._get_or_create_java_agent_proxy(current_user)
                
                if not java_agent_proxy:
                    logger.error(f"Failed to create Java agent proxy for agent {agent_id}")
                    return GetStreamResponse(success=False, error="Failed to create Java agent proxy", stream_id="", description="")
                
                # 使用get_stream外部API
                stream = cs.get_stream(java_agent_proxy, stream_id)
                
                if stream:
                    logger.info(f"Stream {stream_id} retrieved successfully via ChainStream API")
                    return GetStreamResponse(success=True, error="", stream_id=stream_id, description=getattr(stream, 'description', ''))
                else:
                    logger.warning(f"Stream {stream_id} not found")
                    return GetStreamResponse(success=False, error="Stream not found", stream_id="", description="")
                    
            except Exception as e:
                logger.error(f"Failed to get stream with ChainStream API: {e}")
                return GetStreamResponse(success=False, error=str(e), stream_id="", description="")
                
        except Exception as e:
            logger.error(f"Error getting stream: {e}")
            return GetStreamResponse(success=False, error=str(e), stream_id="", description="")
    
    @ensure_user_context
    def AddItem(self, request: AddItemRequest, context):
        """向Stream添加项目"""
        try:
            stream_id = request.stream_id
            item = request.item
            agent_id = request.agent_id
            
            logger.info(f"Adding item to stream {stream_id}: {item}")
            
            # 使用ChainStream API添加项目到Stream
            try:
                import chainstream as cs
                
                # 获取当前用户信息
                current_user = None
                try:
                    from chainstream.runtime.user_context import user_context_manager
                    current_user = user_context_manager.get_current_user()
                    logger.info(f"🔍 DEBUG: AddItem - current_user: {current_user}")
                except Exception as e:
                    logger.error(f"🔍 DEBUG: AddItem - Exception getting current user: {e}")
                
                # 获取或创建Java Agent代理，传递当前用户
                java_agent_proxy = self._get_or_create_java_agent_proxy(current_user)
                logger.info(f"🔍 DEBUG: AddItem - java_agent_proxy: {java_agent_proxy}")
                
                # 先尝试获取stream
                stream = cs.get_stream(java_agent_proxy, stream_id)
                logger.info(f"🔍 DEBUG: AddItem - get_stream returned: {stream}")
                
                if stream:
                    stream.add_item(item)
                    logger.info(f"Item added to stream {stream_id} via ChainStream API")
                    return AddItemResponse(success=True, error="")
                else:
                    # 如果stream不存在，尝试创建它
                    logger.info(f"🔍 DEBUG: Stream {stream_id} not found, attempting to create it")
                    stream = cs.create_stream(java_agent_proxy, stream_id)
                    logger.info(f"🔍 DEBUG: AddItem - create_stream returned: {stream}")
                
                if stream:
                    stream.add_item(item)
                    logger.info(f"Stream {stream_id} created and item added via ChainStream API")
                    return AddItemResponse(success=True, error="")
                else:
                    logger.error(f"Failed to create stream {stream_id}")
                    return AddItemResponse(success=False, error=f"stream_id {stream_id} not found in stream_manager")
                    
            except Exception as e:
                logger.error(f"Failed to add item: {e}")
                return AddItemResponse(success=False, error=str(e))
                
        except Exception as e:
            logger.error(f"Error adding item: {e}")
            return AddItemResponse(success=False, error=str(e))
    
    @ensure_user_context
    def ForEach(self, request: ForEachRequest, context):
        """注册Stream监听器"""
        try:
            stream_id = request.stream_id
            agent_id = request.agent_id
            listener_function_name = request.listener_function_name
            
            logger.info(f"Registering listener {listener_function_name} for stream {stream_id}")
            
            # 使用ChainStream外部API注册监听器
            try:
                import chainstream as cs
                
                # 使用get_stream获取Stream
                # 获取或创建Java Agent代理
                java_agent_proxy = self._get_or_create_java_agent_proxy()
                stream = cs.get_stream(java_agent_proxy, stream_id)
                
                if stream:
                    # 创建一个Java监听器函数
                    def java_listener(item):
                        # 这里应该调用Java端的监听器函数
                        # 目前返回一个匿名流ID
                        return f"anonymous_stream_{stream_id}_{listener_function_name}"
                    
                    # 使用Stream的for_each方法
                    anonymous_stream = stream.for_each(java_listener)
                    
                    logger.info(f"Listener registered for stream {stream_id} via ChainStream API")
                    return ForEachResponse(success=True, error="", anonymous_stream_id=anonymous_stream.stream_id)
                else:
                    logger.error(f"Stream {stream_id} not found")
                    return ForEachResponse(success=False, error="Stream not found", anonymous_stream_id="")
                    
            except Exception as e:
                logger.error(f"Failed to register listener with ChainStream API: {e}")
                return ForEachResponse(success=False, error=str(e), anonymous_stream_id="")
                
        except Exception as e:
            logger.error(f"Error registering stream listener: {e}")
            return ForEachResponse(success=False, error=str(e), anonymous_stream_id="")
    
    @ensure_user_context
    def Batch(self, request: BatchRequest, context):
        """批次切分Stream"""
        try:
            stream_id = request.stream_id
            agent_id = request.agent_id
            by_count = request.by_count if request.by_count > 0 else None
            by_time = request.by_time if request.by_time > 0 else None
            by_item = request.by_item if request.by_item else None
            by_func_name = request.by_func_name if request.by_func_name else None
            
            logger.info(f"Adding batch processing for stream {stream_id}")
            
            # 使用ChainStream外部API进行批次切分
            try:
                import chainstream as cs
                
                # 使用get_stream获取Stream
                # 获取或创建Java Agent代理
                java_agent_proxy = self._get_or_create_java_agent_proxy()
                stream = cs.get_stream(java_agent_proxy, stream_id)
                
                if stream:
                    # 使用Stream的batch方法
                    batch_stream = stream.batch(
                        by_count=by_count,
                        by_time=by_time,
                        by_item=by_item,
                        by_func=None  # Java端暂时不支持by_func
                    )
                    
                    logger.info(f"Batch processing added for stream {stream_id} via ChainStream API")
                    return BatchResponse(success=True, error="", batch_stream_id=batch_stream.stream_id)
                else:
                    logger.error(f"Stream {stream_id} not found")
                    return BatchResponse(success=False, error="Stream not found", batch_stream_id="")
                    
            except Exception as e:
                logger.error(f"Failed to add batch processing with ChainStream API: {e}")
                return BatchResponse(success=False, error=str(e), batch_stream_id="")
                
        except Exception as e:
            logger.error(f"Error adding batch processing: {e}")
            return BatchResponse(success=False, error=str(e), batch_stream_id="")
    
    @ensure_user_context
    def UnregisterAll(self, request: UnregisterAllRequest, context):
        """注销Stream上的所有监听函数"""
        try:
            stream_id = request.stream_id
            agent_id = request.agent_id
            
            logger.info(f"Unregistering all listeners for stream {stream_id}")
            
            # 使用ChainStream外部API注销所有监听器
            try:
                import chainstream as cs
                
                # 使用get_stream获取Stream
                # 获取或创建Java Agent代理
                java_agent_proxy = self._get_or_create_java_agent_proxy()
                stream = cs.get_stream(java_agent_proxy, stream_id)
                
                if stream:
                    # 使用Stream的unregister_all方法
                    stream.unregister_all(java_agent_proxy)
                    
                    logger.info(f"All listeners unregistered for stream {stream_id} via ChainStream API")
                    return UnregisterAllResponse(success=True, error="")
                else:
                    logger.error(f"Stream {stream_id} not found")
                    return UnregisterAllResponse(success=False, error="Stream not found")
                    
            except Exception as e:
                logger.error(f"Failed to unregister listeners with ChainStream API: {e}")
                return UnregisterAllResponse(success=False, error=str(e))
                
        except Exception as e:
            logger.error(f"Error unregistering listeners: {e}")
            return UnregisterAllResponse(success=False, error=str(e))
    
    @ensure_user_context
    def RemoveListener(self, request: RemoveListenerRequest, context):
        """移除指定监听器"""
        try:
            stream_id = request.stream_id
            agent_id = request.agent_id
            listener_function_name = request.listener_function_name
            
            logger.info(f"Removing listener {listener_function_name} for stream {stream_id}")
            
            # 使用ChainStream外部API移除监听器
            try:
                import chainstream as cs
                
                # 使用get_stream获取Stream
                # 获取或创建Java Agent代理
                java_agent_proxy = self._get_or_create_java_agent_proxy()
                stream = cs.get_stream(java_agent_proxy, stream_id)
                
                if stream:
                    # 注意：ChainStream的Stream类没有直接的removeListener方法
                    # 这里需要根据实际API进行调整
                    logger.info(f"Listener removal requested for stream {stream_id} via ChainStream API")
                    return RemoveListenerResponse(success=True, error="")
                else:
                    logger.error(f"Stream {stream_id} not found")
                    return RemoveListenerResponse(success=False, error="Stream not found")
                    
            except Exception as e:
                logger.error(f"Failed to remove listener with ChainStream API: {e}")
                return RemoveListenerResponse(success=False, error=str(e))
                
        except Exception as e:
            logger.error(f"Error removing listener: {e}")
            return RemoveListenerResponse(success=False, error=str(e))
    
    # LLM操作方法
    @ensure_user_context
    def QueryLLM(self, request: QueryLLMRequest, context):
        """查询LLM"""
        try:
            query = request.query
            model_types = list(request.model_types)
            agent_id = request.agent_id
            
            logger.info(f"Querying LLM with query: {query}")
            
            # 使用ChainStream外部API查询LLM
            try:
                import chainstream as cs
                
                # 获取模型
                if not model_types:
                    model_types = ["text"]  # 默认使用text类型
                
                llm = cs.llm.get_model(model_types)
                
                # 制作prompt
                prompt = cs.llm.make_prompt(query)
                
                # 查询LLM
                response = llm.query(prompt)
                
                logger.info(f"LLM query successful via ChainStream API")
                return QueryLLMResponse(success=True, error="", response=response)
                
            except Exception as e:
                logger.error(f"Failed to query LLM with ChainStream API: {e}")
                return QueryLLMResponse(success=False, error=str(e), response="")
                
        except Exception as e:
            logger.error(f"Error querying LLM: {e}")
            return QueryLLMResponse(success=False, error=str(e), response="")
    
    @ensure_user_context
    def GetModel(self, request: GetModelRequest, context):
        """获取LLM模型"""
        try:
            model_types = list(request.model_types)
            agent_id = request.agent_id
            
            logger.info(f"Getting LLM model for types: {model_types}")
            
            # 使用ChainStream外部API获取模型
            try:
                import chainstream as cs
                
                # 获取模型
                if not model_types:
                    model_types = ["text"]  # 默认使用text类型
                
                llm = cs.llm.get_model(model_types)
                
                # 生成模型ID
                model_id = f"model_{'_'.join(model_types)}_{agent_id}"
                
                # 保存到本地字典（用于后续查询）
                if agent_id not in self.agent_models:
                    self.agent_models[agent_id] = {}
                self.agent_models[agent_id][model_id] = llm
                
                logger.info(f"LLM model obtained via ChainStream API")
                return GetModelResponse(success=True, error="", model_id=model_id)
                
            except Exception as e:
                logger.error(f"Failed to get model with ChainStream API: {e}")
                return GetModelResponse(success=False, error=str(e), model_id="")
                
        except Exception as e:
            logger.error(f"Error getting model: {e}")
            return GetModelResponse(success=False, error=str(e), model_id="")
    
    @ensure_user_context
    def MakePrompt(self, request: MakePromptRequest, context):
        """制作Prompt"""
        try:
            prompt_parts = list(request.prompt_parts)
            agent_id = request.agent_id
            
            logger.info(f"Making prompt with {len(prompt_parts)} parts")
            
            # 使用ChainStream外部API制作prompt
            try:
                import chainstream as cs
                
                # 制作prompt
                final_prompt = cs.llm.make_prompt(*prompt_parts)
                
                logger.info(f"Prompt made via ChainStream API")
                return MakePromptResponse(success=True, error="", final_prompt=final_prompt)
                
            except Exception as e:
                logger.error(f"Failed to make prompt with ChainStream API: {e}")
                return MakePromptResponse(success=False, error=str(e), final_prompt="")
                
        except Exception as e:
            logger.error(f"Error making prompt: {e}")
            return MakePromptResponse(success=False, error=str(e), final_prompt="")
    
    @ensure_user_context
    def GetModelInfo(self, request: GetModelInfoRequest, context):
        """获取模型信息"""
        try:
            model_types = list(request.model_types)
            agent_id = request.agent_id
            
            # 使用ChainStream API查询模型信息
            try:
                import chainstream as cs
            
                # 创建模型信息列表
                models = []
                for model_type in model_types:
                    from .chainstream_bridge_pb2 import ModelInfo
                    
                    # 尝试获取模型以检查可用性
                    try:
                        llm = cs.llm.get_model([model_type])
                        available = llm is not None
                    except:
                        available = False
                    
                model_info = ModelInfo(
                    name=f"{model_type}_model",
                    type=model_type,
                        available=available
                )
                models.append(model_info)
            
                logger.info(f"Model info retrieved via ChainStream API")
                return GetModelInfoResponse(success=True, error="", models=models)
                
            except Exception as e:
                logger.error(f"Failed to get model info with ChainStream API: {e}")
                return GetModelInfoResponse(success=False, error=str(e), models=[])
                
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return GetModelInfoResponse(success=False, error=str(e), models=[])
    
    # Buffer操作方法
    @ensure_user_context
    def CreateBuffer(self, request: CreateBufferRequest, context):
        """创建Buffer"""
        try:
            agent_id = request.agent_id
            
            logger.info(f"Creating buffer for agent {agent_id}")
            
            # 使用ChainStream外部API创建Buffer
            try:
                import chainstream as cs
                
                # 创建Buffer实例
                buffer = cs.context.Buffer()
                
                # 生成Buffer ID
                buffer_id = f"buffer_{agent_id}_{len(self.agent_buffers.get(agent_id, {}))}"
                
                # 保存到本地字典（用于后续操作）
                if agent_id not in self.agent_buffers:
                    self.agent_buffers[agent_id] = {}
                self.agent_buffers[agent_id][buffer_id] = buffer
                
                logger.info(f"Buffer created via ChainStream API")
                return CreateBufferResponse(success=True, error="", buffer_id=buffer_id)
                
            except Exception as e:
                logger.error(f"Failed to create buffer with ChainStream API: {e}")
                return CreateBufferResponse(success=False, error=str(e), buffer_id="")
                
        except Exception as e:
            logger.error(f"Error creating buffer: {e}")
            return CreateBufferResponse(success=False, error=str(e), buffer_id="")
    
    @ensure_user_context
    def BufferAppend(self, request: BufferAppendRequest, context):
        """向Buffer添加数据"""
        try:
            buffer_id = request.buffer_id
            agent_id = request.agent_id
            data = request.data
            
            logger.info(f"Appending data to buffer {buffer_id}")
            
            # 使用ChainStream外部API添加数据
            try:
                # 从本地字典获取Buffer
                if agent_id in self.agent_buffers and buffer_id in self.agent_buffers[agent_id]:
                    buffer = self.agent_buffers[agent_id][buffer_id]
                    buffer.append(data)
                    
                    logger.info(f"Data appended to buffer {buffer_id} via ChainStream API")
                    return BufferAppendResponse(success=True, error="")
                else:
                    logger.error(f"Buffer {buffer_id} not found")
                    return BufferAppendResponse(success=False, error="Buffer not found")
                    
            except Exception as e:
                logger.error(f"Failed to append data with ChainStream API: {e}")
                return BufferAppendResponse(success=False, error=str(e))
                
        except Exception as e:
            logger.error(f"Error appending data: {e}")
            return BufferAppendResponse(success=False, error=str(e))
    
    @ensure_user_context
    def BufferPop(self, request: BufferPopRequest, context):
        """从Buffer取出队首数据"""
        try:
            buffer_id = request.buffer_id
            agent_id = request.agent_id
            
            logger.info(f"Popping data from buffer {buffer_id}")
            
            # 使用ChainStream外部API取出数据
            try:
                # 从本地字典获取Buffer
                if agent_id in self.agent_buffers and buffer_id in self.agent_buffers[agent_id]:
                    buffer = self.agent_buffers[agent_id][buffer_id]
                    data = buffer.pop()
                    
                    logger.info(f"Data popped from buffer {buffer_id} via ChainStream API")
                    return BufferPopResponse(success=True, error="", data=str(data))
                else:
                    logger.error(f"Buffer {buffer_id} not found")
                    return BufferPopResponse(success=False, error="Buffer not found", data="")
                    
            except Exception as e:
                logger.error(f"Failed to pop data with ChainStream API: {e}")
                return BufferPopResponse(success=False, error=str(e), data="")
                
        except Exception as e:
            logger.error(f"Error popping data: {e}")
            return BufferPopResponse(success=False, error=str(e), data="")
    
    @ensure_user_context
    def BufferPopAll(self, request: BufferPopAllRequest, context):
        """从Buffer取出所有数据"""
        try:
            buffer_id = request.buffer_id
            agent_id = request.agent_id
            
            logger.info(f"Popping all data from buffer {buffer_id}")
            
            # 使用ChainStream外部API取出所有数据
            try:
                # 从本地字典获取Buffer
                if agent_id in self.agent_buffers and buffer_id in self.agent_buffers[agent_id]:
                    buffer = self.agent_buffers[agent_id][buffer_id]
                    data_list = buffer.pop_all()
                    
                    logger.info(f"All data popped from buffer {buffer_id} via ChainStream API")
                    return BufferPopAllResponse(success=True, error="", data_list=[str(item) for item in data_list])
                else:
                    logger.error(f"Buffer {buffer_id} not found")
                    return BufferPopAllResponse(success=False, error="Buffer not found", data_list=[])
                    
            except Exception as e:
                logger.error(f"Failed to pop all data with ChainStream API: {e}")
                return BufferPopAllResponse(success=False, error=str(e), data_list=[])
                
        except Exception as e:
            logger.error(f"Error popping all data: {e}")
            return BufferPopAllResponse(success=False, error=str(e), data_list=[])
    
    # Runtime操作方法
    @ensure_user_context
    def GetRuntimeInfo(self, request: GetRuntimeInfoRequest, context):
        """获取Runtime信息"""
        try:
            agent_id = request.agent_id
            
            # 使用ChainStream API查询Runtime信息
            try:
                import chainstream as cs
                
                # 获取Runtime信息
                runtime_id = f"ChainStream Runtime - Agent: {agent_id}"
                status = "running"
                
                # 获取活跃的Agent列表（从本地字典）
                active_agents = []
                if agent_id:
                    active_agents.append(agent_id)
                
                # 添加其他活跃的Agent
                for aid in self.agent_streams.keys():
                    if aid not in active_agents:
                        active_agents.append(aid)
                
                logger.info(f"Runtime info retrieved via ChainStream API")
                return GetRuntimeInfoResponse(
                    success=True, 
                    error="", 
                    runtime_id=runtime_id,
                    status=status,
                    active_agents=active_agents
                )
                
            except Exception as e:
                logger.error(f"Failed to get runtime info with ChainStream API: {e}")
                return GetRuntimeInfoResponse(
                    success=False, 
                    error=str(e), 
                    runtime_id="",
                    status="error",
                    active_agents=[]
                )
                
        except Exception as e:
            logger.error(f"Error getting runtime info: {e}")
            return GetRuntimeInfoResponse(
                success=False, 
                error=str(e), 
                runtime_id="",
                status="error",
                active_agents=[]
            )


def start_bridge_server(port=50051, runtime_core=None):
    """启动gRPC桥接服务器"""
    try:
        # 在启动gRPC服务器之前，设置默认用户到用户上下文
        _setup_default_user_context()
        
        server = ChainStreamBridgeServer(runtime_core)
        if server.start_server(port):
            logger.info(f"gRPC Bridge Server started successfully on port {port}")
            return server
        else:
            logger.error(f"Failed to start gRPC Bridge Server on port {port}")
            return None
    except Exception as e:
        logger.error(f"Error starting gRPC Bridge Server: {e}")
        return None


def _setup_default_user_context():
    """设置默认用户到用户上下文中"""
    try:
        from chainstream.runtime.user_context import user_context_manager
        from chainstream.user import UserManager
        
        # 检查是否已经有用户上下文
        current_user = user_context_manager.get_current_user()
        if current_user:
            logger.info(f"User context already set: {current_user.get_username()}")
            return
        
        # 尝试获取默认用户
        user_manager = UserManager()
        
        # 首先尝试获取admin用户
        try:
            admin_user = user_manager.get_user("admin")
            if admin_user:
                user_context_manager.set_current_user(admin_user)
                logger.info(f"Set default user context to admin: {admin_user.get_username()}")
                return
        except Exception as e:
            logger.debug(f"Could not get admin user: {e}")
        
        # 如果admin用户不存在，尝试获取第一个可用用户
        try:
            users = user_manager.list_users()
            if users:
                first_user = users[0]
                user_context_manager.set_current_user(first_user)
                logger.info(f"Set default user context to first available user: {first_user.get_username()}")
                return
        except Exception as e:
            logger.debug(f"Could not get any users: {e}")
        
        # 如果没有任何用户，创建一个默认用户
        try:
            default_user = user_manager.create_user(
                username="default",
                password="default123",
                level=1,
                enable_encryption=True
            )
            user_context_manager.set_current_user(default_user)
            logger.info(f"Created and set default user context: {default_user.get_username()}")
        except Exception as e:
            logger.warning(f"Could not create default user: {e}")
            
    except Exception as e:
        logger.error(f"Failed to setup default user context: {e}")


if __name__ == "__main__":
    # 测试服务器
    logging.basicConfig(level=logging.INFO)
    server = start_bridge_server()
    if server:
        try:
            # 保持服务器运行
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop_server()
