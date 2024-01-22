from chainstream.interfaces import AgentInterface
from chainstream.runtime import cs_server


class Agent(AgentInterface):
    def __init__(self, agent_id) -> None:
        super().__init__()
        self.agent_id = agent_id
        cs_server.register_agent(agent=self)

    def start(self):
        pass

    def stop(self):
        pass

    def query(self, query):
        pass

