if __name__ == "__main__":
    from tasks import ALL_TASKS

    WorkSmsTaskConfig = ALL_TASKS['WorkSmsTask']

    agent_file = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_message_agent")
        self.input_stream = cs.get_stream("all_sms")
        self.output_stream = cs.get_stream("cs_sms")
        self.llm = get_model(["text"])
    def start(self):
        def process_sms(sms):
            sms_text = sms["text"]
            prompt = "Summarize the content of the following each SMS message in a sentence"
            prompt = [
                {
                    "role": "user",
                    "content": prompt+sms_text
                }
            ]
            response = self.llm.query(prompt)
            print(sms_text+" : "+response)
            self.output_stream.add_item(sms_text+" : "+response)
        self.input_stream.register_listener(self, process_sms)

    def stop(self):
        self.input_stream.unregister_listener(self)

    '''
    oj = OJ(WorkSmsTaskConfig(), agent_file)
    oj.start_test_agent()



