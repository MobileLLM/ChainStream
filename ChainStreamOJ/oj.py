from chainstream.runtime import RuntimeCore

class OJ:
    def __init__(self, task_file, agent_file):
        self.runtime = RuntimeCore()
        self.task_file = task_file
        self.agent_file = agent_file
    
    def start_test_agent(self):
        pass

    def _init_task(self):
        self._read_task()
        