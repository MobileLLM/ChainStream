import collections
import importlib
import importlib.util
from pathlib import Path
import os
import inspect
import logging
import json
from .user_context import user_context_manager

logger = logging.getLogger(__name__)


class AgentAnalyzer:
    def __init__(self):
        self.local_scanned_agents = collections.OrderedDict()
        self.agents = collections.OrderedDict()
        self.agents_metaData = collections.OrderedDict()
        self.path_to_agentId = {}

    def get_path_to_agentId(self):
        return self.path_to_agentId

    def get_running_agents_info_list(self, user=None):
        """
        Get list of running agents, filtered by user level permissions
        
        Args:
            user: User object to filter agents by. If None, returns all agents.
        
        Returns:
            List of agent metadata dictionaries filtered by user level
        """
        logger.info(f"🔍 get_running_agents_info_list called with user: {user.get_username() if user else 'None'}")
        logger.info(f"📊 Total agents in manager: {len(self.agents)}")
        
        if user is None:
            # Return all agents
            agents_info = []
            for agent in self.agents.values():
                agent_meta = agent.get_meta_data()
                # 检查Agent是否真的在运行
                if hasattr(agent, 'is_running'):
                    is_running = agent.is_running()
                    logger.info(f"📊 Agent {agent.agent_id} running status: {is_running}")
                    if is_running:
                        agents_info.append(agent_meta)
                        logger.info(f"✅ Added running agent: {agent.agent_id}")
                    else:
                        logger.warning(f"⚠️ Agent {agent.agent_id} is not running, excluding from list")
                else:
                    logger.warning(f"⚠️ Agent {agent.agent_id} doesn't have is_running method, including anyway")
                    agents_info.append(agent_meta)
            
            logger.info(f"📊 Returning {len(agents_info)} running agents")
        else:
            # Filter by user level permissions
            agents_info = []
            user_level = user.get_level()
            user_uuid = user.get_uuid()
            logger.info(f"🔍 Filtering by user level: {user_level}, UUID: {user_uuid}")
            
            for agent in self.agents.values():
                logger.info(f"🔍 Checking agent: {agent.agent_id}")
                
                if agent.user is None:
                    # Legacy agents without user assignment - only show to high level users
                    if user_level >= 10:  # Admin level
                        if hasattr(agent, 'is_running') and agent.is_running():
                            agents_info.append(agent.get_meta_data())
                            logger.info(f"✅ Added legacy running agent: {agent.agent_id}")
                        else:
                            logger.warning(f"⚠️ Legacy agent {agent.agent_id} is not running")
                else:
                    agent_user_level = agent.user.get_level()
                    agent_user_uuid = agent.user.get_uuid()
                    logger.info(f"👤 Agent user level: {agent_user_level}, UUID: {agent_user_uuid}")
                    
                    # High level users can see their own agents and lower level users' agents
                    # Same level users can only see their own agents
                    if (user_level > agent_user_level) or (user_level == agent_user_level and user_uuid == agent_user_uuid):
                        if hasattr(agent, 'is_running') and agent.is_running():
                            agents_info.append(agent.get_meta_data())
                            logger.info(f"✅ Added running agent: {agent.agent_id}")
                        else:
                            logger.warning(f"⚠️ Agent {agent.agent_id} is not running")
        
        logger.info(f"📊 Final result: {len(agents_info)} running agents")
        return agents_info

    def get_running_agents_name_list(self):
        return list(self.agents.keys())

    def get_agent_node(self):
        return self.agents.keys()

    def get_agent_file_path_to_agent_id(self):
        return self.path_to_agentId


class FunctionManager:
    def __init__(self, agent_id):
        self.functions = {}


class AgentManager(AgentAnalyzer):
    def __init__(self):
        super().__init__()
        self.predefined_agents_path = Path(os.path.dirname(__file__)).parent.parent / 'AgentStore'

    def register_agent(self, agent, user):
        logger.debug(f"register_agent called with agent: {agent}, user: {user}")
        logger.debug(f"agent.user before: {agent.user}")
        # 确保agent的user信息正确设置
        if agent.user is None and user is not None:
            agent.user = user
            agent.metaData.user = user
            logger.debug(f"Set agent.user to: {user}")
        else:
            logger.debug(f"Not setting user - agent.user: {agent.user}, user: {user}")
        
        logger.debug(f"agent.user after registration: {agent.user}")
        self.agents[agent.agent_id] = agent
        self.agents_metaData[agent.agent_id] = agent.metaData
        self.path_to_agentId[agent.metaData.agent_file_path] = agent.agent_id
        agent.set_agent_store_base_path(self.predefined_agents_path)

    def unregister_agent(self, agent, user):
        self.agents.pop(agent.agent_id)

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def get_agent_by_path(self, path):
        if path in self.path_to_agentId:
            return self.get_agent(self.path_to_agentId[path])
        return None

    def get_agents_by_user(self, user):
        """Get all agents owned by a specific user"""
        return [
            agent for agent in self.agents.values() 
            if agent.user and agent.user.get_uuid() == user.get_uuid()
        ]

    def get_agent_count_by_user(self, user):
        """Get count of agents owned by a specific user"""
        return len(self.get_agents_by_user(user))

    def can_user_access_agent(self, user, agent_id):
        """Check if user can access a specific agent"""
        agent = self.get_agent(agent_id)
        if agent is None:
            return False
        
        # If agent has no user assigned, allow access (legacy agents)
        if agent.user is None:
            return True
        
        # Check if user owns the agent
        return agent.user.get_uuid() == user.get_uuid()

    def scan_predefined_agents(self):
        agent_list = []
        for root, dirs, files in os.walk(self.predefined_agents_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.java'):
                    agent_list.append(os.path.join(root, file))
        return agent_list

    def scan_predefined_agents_tree(self):
        agent_list = []
        for root, dirs, files in os.walk(self.predefined_agents_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.java'):
                    # agent_list.append(os.path.join(root, file))
                    agent_list.append(os.path.relpath(os.path.join(root, file), start=self.predefined_agents_path))
        agent_list = self._path_to_json(agent_list)
        return agent_list

    def shutdown(self):
        try:
            try:
                for agent in self.agents.values():
                    try:
                        agent.stop()
                    except Exception as e:
                        logger.error(f'failed to stop agent {agent.agent_id}: {e}')
                    finally:
                        self.agents[agent.agent_id] = None
            except Exception as e:
                logger.error(f'failed to stop all agents: {e}')
            self.agents = collections.OrderedDict()
        except Exception as e:
            logger.error(f'failed to shutdown agent manager: {e}')

        return True

    def _path_to_json(self, paths):
        json_data = {}

        for path in paths:
            path = path.replace('\\', '/')
            directories = path.split('/')
            current_dict = json_data

            for i, directory in enumerate(directories):
                if directory != '':
                    if directory not in current_dict:
                        if i == len(directories) - 1:
                            current_dict[directory] = str(self.predefined_agents_path / path)
                        else:
                            current_dict[directory] = {}
                    current_dict = current_dict[directory]

        def process_dict(node):
            tmp_list = []
            for key, value in node.items():
                if isinstance(value, dict):
                    # if isinstance(value[0], str):
                    #     tmp_list.append({
                    #         "label": key,
                    #         "is_running": self.get_agent_by_path(value[0]) is not None,
                    #     })
                    # else:
                    tmp_list.append({
                        "label": key,
                        "disabled": True,
                        "children": process_dict(value)
                    })
                else:
                    node[key] = {"name": value}
                    tmp_list.append({
                        "label": key,
                        "is_running": self.get_agent_by_path(str(value)) is not None,
                    })
            return tmp_list

        list_data = process_dict(json_data)

        return list_data

    def start_agent_by_id(self, agent_id, user):
        agents_list = self.scan_predefined_agents()
        target_agent_path = None
        for agent_path in agents_list:
            agent_path = agent_path.replace('\\', '/')
            if agent_path.split('/')[-1] == agent_id:
                target_agent_path = agent_path
                break
        if target_agent_path is None:
            return False
        res = self.start_agent_by_path(target_agent_path, user)
        if res:
            return True
        return False

    def stop_agent_by_id(self, agent_id, user):
        agent_id = agent_id.split('.')[0]
        agent = self.get_agent(agent_id)
        if agent is None:
            return False  # Agent not found
        agent.stop()
        self.remove_agent_by_id(agent_id, user)
        return True

    def remove_agent_by_id(self, agent_id, user):
        self.agents.pop(agent_id)
        return True

    def start_agent_by_path(self, path, user):
        logger.debug(f"start_agent_by_path called with path: {path}, user: {user}")
        # If no user is provided, try to get it from the user context
        if user is None:
            user = user_context_manager.get_current_user()
            logger.debug(f"Retrieved user from context: {user}")
            if user is None:
                logger.warning("No user provided and no user context available")
                # For backward compatibility, we'll continue without user
                # but log a warning
        
        if not path.startswith('/'):
            path = str(self.predefined_agents_path / path)
        
        # 检查文件是否存在
        if not os.path.exists(path):
            raise Exception(f'agent not found: {path}')
        
        # 根据文件扩展名选择处理方式
        if path.endswith('.py'):
            return self._start_python_agent(path, user)
        elif path.endswith('.java'):
            return self._start_java_agent(path, user)
        else:
            raise Exception(f'unsupported agent file type: {path}')
    
    def _start_python_agent(self, path, user):
        """启动Python Agent（原有逻辑）"""
        module_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        from chainstream.agent import Agent
        agent_list = []
        for name, obj in module.__dict__.items():
            if inspect.isclass(obj) and issubclass(obj, Agent) and obj.is_agent:
                print(name, obj)
                agent_list.append((name, obj))
        success_count = 0
        for name, obj in agent_list:
            try:
                # Create agent instance with user information
                # Try to get agent_id from the class, fallback to name if not available
                agent_id = getattr(obj, 'agent_id', name)
                
                # Check if the agent's __init__ method accepts user parameter
                init_signature = inspect.signature(obj.__init__)
                init_params = list(init_signature.parameters.keys())
                
                # Prepare arguments for agent instantiation
                agent_args = {'agent_id': agent_id}
                if 'user' in init_params:
                    agent_args['user'] = user
                    logger.debug(f'Agent {name} accepts user parameter, passing user: {user}')
                else:
                    logger.debug(f'Agent {name} does not accept user parameter, skipping user')
                
                new_agent = obj(**agent_args)
                # Call start method (may return None, True, or False)
                start_result = new_agent.start()
                
                # Register the agent with the manager regardless of start() return value
                # The agent is considered successfully started if it was created without exception
                logger.info(f'agent {name} started successfully (start() returned: {start_result})')
                success_count += 1
                
            except Exception as e:
                logger.error(f'failed to start agent {name}: {e}')

        logger.info(f'Started {success_count} out of {len(agent_list)} agents')
        return success_count > 0
    
    def _start_java_agent(self, path, user):
        """启动Java Agent"""
        try:
            logger.info(f"🚀 Starting Java agent from file: {path}")
            logger.info(f"👤 User: {user.get_username() if user else 'None'}")
            
            # 导入Java Agent执行器
            from chainstream.runtime.java.java_agent_executor import JavaAgentExecutor
            
            # 创建Java Agent执行器
            java_executor = JavaAgentExecutor()
            
            # 启动Java Agent
            logger.info("📦 Creating Java agent wrapper...")
            # 获取RuntimeCore实例
            from chainstream.runtime.runtime_core import RuntimeCore
            runtime_core = None
            # 尝试从当前对象获取runtime_core
            if hasattr(self, '_runtime_core'):
                runtime_core = self._runtime_core
            else:
                # 如果没有，尝试从全局获取
                try:
                    from chainstream.runtime import cs_server_core
                    runtime_core = cs_server_core
                except:
                    pass
            
            java_agent_wrapper = java_executor.start_java_agent(path, user, runtime_core)
            
            # 注册到AgentManager
            logger.info("📝 Registering Java agent to AgentManager...")
            self.register_agent(java_agent_wrapper, user)
            
            # 检查Agent是否真的在运行
            logger.info("🔍 Checking if Java agent is actually running...")
            if hasattr(java_agent_wrapper, 'is_running'):
                is_running = java_agent_wrapper.is_running()
                logger.info(f"📊 Java agent running status: {is_running}")
            else:
                logger.warning("⚠️ Java agent wrapper doesn't have is_running method")
            
            logger.info(f"✅ Java agent started successfully: {java_agent_wrapper.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to start Java agent: {e}")
            import traceback
            logger.error(f"❌ Full traceback: {traceback.format_exc()}")
            return False


if __name__ == '__main__':
    print(Path(os.path.dirname(__file__)).parent.parent / 'agents')
