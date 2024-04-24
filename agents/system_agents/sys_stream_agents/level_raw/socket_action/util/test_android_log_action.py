import chainstream as cs
from time import sleep
import threading
import datetime


class TestAndroidLogAction(cs.agent.Agent):
    is_agent = True

    def __init__(self):
        super().__init__("TestAndroidLogAction")
        self.log_action = cs.stream.get_stream("log_to_android")
        self.enable = False
        self.thread = None

    def start(self):
        self.enable = True
        self.thread = threading.Thread(target=self.send())
        self.thread.start()

    def send(self):
        while self.enable:
            # print(f"TestAndroidLogAction: {datetime.datetime.now()}")
            self.log_action.add_item(f"TestAndroidLogAction: {datetime.datetime.now()}")
            sleep(3)

    def stop(self):
        self.enable = False
