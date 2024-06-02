if __name__ == "__main__":
    from tasks import ALL_TASKS

    WorkSmsTaskConfig = ALL_TASKS['WorkSmsTask']

    agent_file = '''
import chainstream as cs

class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_message_agent")
        self.input_stream = cs.get_stream("all_sms")
        self.output_stream = cs.get_stream("cs_sms")

    def start(self):
        def process_sms(sms):
            sms_language = sms["language"]
            sms_text = sms["text"]
            self.output_stream.add_item(sms_text+" : "+sms_language)
        self.input_stream.register_listener(self, process_sms)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(WorkSmsTaskConfig(), agent_file)
    oj.start_test_agent()