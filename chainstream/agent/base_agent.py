from chainstream.interfaces import AgentInterface
from chainstream.runtime import cs_server_core
import logging


class Agent(AgentInterface):
    def __init__(self, agent_id) -> None:
        super().__init__()
        self.agent_id = agent_id
        cs_server_core.register_agent(agent=self)
        self.logger = logging.getLogger(self.agent_id)

    def start(self):
        pass

    def stop(self):
        pass

    def query(self, query):
        pass

