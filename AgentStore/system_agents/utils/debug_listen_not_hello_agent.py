import chainstream as cs


class DebugListenHelloAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='debug_listen_hello_agent'):
        super().__init__(agent_id)
        self.stream = cs.stream.get_stream(self, "debug_not_hello_stream")

    def start(self):
        def handle_new_hello(data):
            # print("Received hello message:", data)
            return data

        def handle_new_hello_2(data):
            # print("Received not hello message:", data)
            return data

        # self.stream.for_each(lambda data: data).for_each(handle_new_hello).for_each(handle_new_hello).batch(by_count=2).for_each(lambda data: print(data))
        self.stream.batch(by_count=2).for_each(lambda data: print(data))

    def stop(self):
        self.stream.remove_listener(self)


if __name__ == '__main__':
    default_sensors_agent = DebugListenHelloAgent()
    default_sensors_agent.start()
