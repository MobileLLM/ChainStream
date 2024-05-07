from chainstream.interfaces import AgentInterface
from chainstream.runtime import cs_server_core
import logging
from .agent_recorder import AgentRecorder
import inspect
import datetime


class AgentMeta:
    def __init__(self, *args, **kwargs) -> None:
        self.agent_id = kwargs.get("agent_id")
        self.agent_file_path = kwargs.get("agent_file_path") if kwargs.get("agent_file_path") else ""
        self.description = kwargs.get("description") if kwargs.get("description") else ""
        self.type = kwargs.get("type") if kwargs.get("type") else "base"
        self.created_at = datetime.datetime.now()
        self.status = kwargs.get("status") if kwargs.get("status") else "running"

        # TODO: 增加权限、优先级、分组等属性
        # self.permissions = []
        # self.priority = 0
        # self.group = ""

    def __dict__(self):
        return {
            "agent_id": self.agent_id,
            "agent_file_path": self.agent_file_path,
            "description": self.description,
            "type": self.type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status
        }


class Agent(AgentInterface):
    def __init__(self, agent_id) -> None:
        super().__init__()
        self.agent_id = agent_id
        caller_frame = inspect.currentframe().f_back

        self.metaData = AgentMeta(agent_id=agent_id, agent_file_path=caller_frame.f_globals['__file__'])
        self.logger = logging.getLogger(self.agent_id)
        self.recorder = AgentRecorder(agentMetaData=self.metaData)
        cs_server_core.register_agent(agent=self)

    def start(self):
        pass

    def stop(self):
        pass

    def query(self, query):
        pass

    def get_meta_data(self):
        return self.metaData.__dict__()

    @staticmethod
    def get_doc():
        raise NotImplementedError("Please implement this method in your agent class")