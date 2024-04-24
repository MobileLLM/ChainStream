import chainstream as cs
from time import sleep

class TestAndroidLogAction(cs.agent.Agent):
    def __init__(self):
        super().__init__("TestAndroidLogAction")
        self.log_action = cs.stream.get_stream("log_to_android")

    def start(self):
        for i in range(10):
            self.log_action.add_item(f"Test log action: {i}")
            sleep(3)
