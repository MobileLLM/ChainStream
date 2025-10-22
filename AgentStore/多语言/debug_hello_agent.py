import chainstream as cs
import threading
import time
from datetime import datetime


class DebugHelloAgentPY(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='debug_hello_agent_py'):
        super().__init__(agent_id)
        self.hello_thread = None
        self.enabled = False
        self.stream = cs.stream.create_stream(self, "debug_hello_stream_py")

    def start(self):
        self.enabled = True
        self.hello_thread = threading.Thread(target=self.hello)
        self.hello_thread.start()

    def hello(self):
        while self.enabled:
            print(f'Hello, world! {datetime.now()}')
            self.stream.add_item({'message': 'Hello, world!'})
            # print(self.stream.get_record_data())
            time.sleep(3)

    def stop(self):
        self.enabled = False


if __name__ == '__main__':
    default_sensors_agent = DebugHelloAgentPY()
    default_sensors_agent.start()
