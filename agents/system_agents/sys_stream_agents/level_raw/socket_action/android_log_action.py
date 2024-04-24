from agents.system_agents.sys_stream_agents.level_raw.socket_action.base_socket_action import BaseSocketActions
import chainstream as cs


class AndroidLogAction(cs.agent.Agent):
    is_agent = True

    def __init__(self, ip='192.168.43.41', port=6666):
        super().__init__(agent_id='android_log_action')
        self.base_action = BaseSocketActions(cmd='log', stream_name='log_to_android', ip=ip, port=port)

    def start(self):
        self.base_action.register_func(self)

    def stop(self):
        self.base_action.stop()


if __name__ == '__main__':
    import chainstream as cs

    a = AndroidLogAction()
    a.start()
    #
    # haha = cs.stream.get_stream("log_to_android")
    #
    # for i in range(10):
    #     print("main send item")
    #     haha.add_item("hello world")
    #     time.sleep(2)
