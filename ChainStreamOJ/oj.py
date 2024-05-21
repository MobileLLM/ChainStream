from chainstream.runtime import RuntimeCore

class OJ:
    def __init__(self, task, agent_file):
        self.runtime = RuntimeCore()
        self.task = task
        self.agent_file = agent_file
    
    def start_test_agent(self):
        self.task.init_enviroment(self.runtime)

        self._start_agent()

        self.task.start_stream(self.runtime)

        self.task.evaluate_stream(self.runtime)

    def _start_agent():
        try:
            pass
        except Exception as e:
            print(e)
            print("Agent file not found")
            return
        