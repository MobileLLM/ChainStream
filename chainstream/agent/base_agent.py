from chainstream.interfaces import AgentInterface
from chainstream.runtime import cs_server_core
import logging
from .agent_recorder import AgentRecorder


class AgentMeta:
    def __init__(self, *args, **kwargs) -> None:
        self.agent_id = kwargs.get("agent_id")
        self.description = kwargs.get("description") if kwargs.get("description") else ""
        self.type = kwargs.get("type") if kwargs.get("type") else "base"

        # TODO: 增加权限、优先级、分组等属性
        # self.permissions = []
        # self.priority = 0
        # self.group = ""


class Agent(AgentInterface):
    def __init__(self, agent_id) -> None:
        super().__init__()
        self.agent_id = agent_id
        self.metaData = AgentMeta(agent_id=agent_id)
        cs_server_core.register_agent(agent=self)
        self.logger = logging.getLogger(self.agent_id)
        self.recorder = AgentRecorder(agentMetaData=self.metaData)

    def start(self):
        pass

    def stop(self):
        pass

    def query(self, query):
        pass
