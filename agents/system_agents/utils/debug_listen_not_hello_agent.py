import chainstream as cs


class DebugListenHelloAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='debug_listen_hello_agent'):
        super().__init__(agent_id)
        self.stream = cs.stream.get_stream("debug_not_hello_stream")

    def start(self):
        def handle_new_hello(data):
            print("Received hello message:", data)

        self.stream.register_listener(self, handle_new_hello)


    def stop(self):
        self.stream.remove_listener(self)


if __name__ == '__main__':
    default_sensors_agent = DebugListenHelloAgent()
    default_sensors_agent.start()
