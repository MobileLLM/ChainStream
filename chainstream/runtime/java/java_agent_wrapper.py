"""
Java Agent Wrapper - 将Java Agent包装成Python Agent对象
"""
import os
import logging
import subprocess
import threading
from typing import Optional
from chainstream.agent.base_agent import Agent, AgentMeta
from .grpc_server import start_bridge_server


class JavaAgentWrapper(Agent):
    """Java Agent包装器，将Java Agent包装成Python Agent对象"""
    
    # 类级别的gRPC服务器实例
    _grpc_server = None
    _grpc_server_lock = threading.Lock()
    
    def __init__(self, java_process: subprocess.Popen, java_file_path: str, user=None, runtime_core=None):
        """
        初始化Java Agent包装器
        
        Args:
            java_process: Java进程对象
            java_file_path: Java文件路径
            user: 用户对象
            runtime_core: Runtime核心实例
        """
        # 从Java文件路径提取agent_id
        agent_id = self._extract_agent_id_from_path(java_file_path)
        
        # 调用父类构造函数
        super().__init__(agent_id=agent_id, user=user)
        
        self.java_process = java_process
        self.java_file_path = java_file_path
        self.runtime_core = runtime_core
        self.logger = logging.getLogger(f"{__name__}.JavaAgentWrapper.{agent_id}")
        
        # 设置Agent元数据
        self.metaData = AgentMeta(
            agent_id=agent_id,
            agent_file_path=java_file_path,
            description=f"Java Agent: {agent_id}",
            type="java",
            user=user
        )
        
        # 设置用户上下文
        if user:
            try:
                from chainstream.runtime.user_context import user_context_manager
                user_context_manager.set_current_user(user)
                self.logger.info(f"Set user context for Java Agent: {user.get_username()}")
            except Exception as e:
                self.logger.warning(f"Failed to set user context: {e}")
        
        # 确保gRPC服务器已启动
        self._ensure_grpc_server()
        
        self.logger.info(f"Java Agent wrapper created: {agent_id}")
    
    def _ensure_grpc_server(self):
        """确保gRPC服务器已启动"""
        with self._grpc_server_lock:
            if self._grpc_server is None:
                # 使用传入的 runtime_core 实例，如果没有则使用全局的
                runtime_core = self.runtime_core
                if runtime_core is None:
                    try:
                        from chainstream.runtime import cs_server_core
                        runtime_core = cs_server_core
                    except Exception as e:
                        logging.error(f"Failed to get runtime_core: {e}")
                        raise RuntimeError(f"Failed to get runtime_core: {e}")
                
                self._grpc_server = start_bridge_server(port=50051, runtime_core=runtime_core)
                if self._grpc_server:
                    logging.info("gRPC Bridge Server started for Java Agent communication")
                else:
                    logging.error("Failed to start gRPC Bridge Server")
    
    def _extract_agent_id_from_path(self, java_file_path: str) -> str:
        """从Java文件路径提取agent_id"""
        # 获取文件名（不包含扩展名）
        file_name = os.path.splitext(os.path.basename(java_file_path))[0]
        
        # 将文件名转换为合适的agent_id
        # 例如：DebugHelloAgent.java -> debug_hello_agent
        # 将驼峰命名转换为下划线命名
        import re
        # 在大写字母前插入下划线，然后转小写
        agent_id = re.sub(r'(?<!^)(?=[A-Z])', '_', file_name).lower()
        
        return agent_id
    
    def start(self) -> bool:
        """
        启动Java Agent
        
        Returns:
            bool: 启动是否成功
        """
        try:
            self.logger.info(f"🚀 Starting Java Agent: {self.agent_id}")
            self.logger.info(f"📊 Java process PID: {self.java_process.pid}")
            
            # 检查Java进程是否还在运行
            if self.java_process.poll() is not None:
                self.logger.error(f"❌ Java process already terminated with code: {self.java_process.returncode}")
                return False
            
            # 等待一小段时间让Java进程完全启动
            import time
            time.sleep(2)
            
            # 再次检查进程状态
            if self.java_process.poll() is not None:
                self.logger.error(f"❌ Java process terminated during startup with code: {self.java_process.returncode}")
                return False
            
            self.logger.info(f"✅ Java Agent {self.agent_id} started successfully and is running")
            return True
                
        except Exception as e:
            self.logger.error(f"❌ Error starting Java Agent: {e}")
            import traceback
            self.logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            return False
    
    def is_running(self) -> bool:
        """检查Java Agent是否还在运行"""
        if self.java_process is None:
            return False
        
        poll_result = self.java_process.poll()
        is_alive = poll_result is None
        
        if not is_alive:
            self.logger.warning(f"⚠️ Java Agent {self.agent_id} process terminated with code: {poll_result}")
        else:
            self.logger.debug(f"✅ Java Agent {self.agent_id} is still running")
            
        return is_alive
    
    def stop(self) -> None:
        """停止Java Agent"""
        try:
            self.logger.info(f"Stopping Java Agent: {self.agent_id}")
            
            if self.java_process and self.java_process.poll() is None:
                # 优雅地终止Java进程
                self.java_process.terminate()
                
                # 等待进程结束
                try:
                    self.java_process.wait(timeout=5)
                    self.logger.info(f"Java Agent {self.agent_id} stopped gracefully")
                except subprocess.TimeoutExpired:
                    # 强制杀死进程
                    self.java_process.kill()
                    self.java_process.wait()
                    self.logger.warning(f"Java Agent {self.agent_id} force killed")
            
        except Exception as e:
            self.logger.error(f"Error stopping Java Agent: {e}")
    
    
    def get_status(self) -> str:
        """获取Java Agent状态"""
        if not self.is_running():
            return "stopped"
        return "running"
    
    def get_meta_data(self):
        """获取Agent元数据"""
        meta = self.metaData.__dict__()
        meta['status'] = self.get_status()
        meta['type'] = 'java'
        return meta
