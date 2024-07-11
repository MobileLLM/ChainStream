from ..task_config_base import SingleAgentTaskConfigBase
import os
import json
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData

random.seed(6666)


class MessageTimeConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_sms',"
            "and process the value corresponding to the 'text' and 'time' keys in the SMS dictionary: "
            "Combine each SMS message text with its time information and output the combined message and time to the stream 'cs_sms'."
        )

        self.sms_data = SMSData().get_random_message()
        self.agent_example = '''
        import chainstream as cs
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_message_agent")
                self.input_stream = cs.get_stream("all_sms")
                self.output_stream = cs.get_stream("cs_sms")
        
            def start(self):
                def process_sms(sms):
                    sms_time = sms["time"]
                    sms_text = sms["text"]
                    self.output_stream.add_item(sms_text+" : "+sms_time)
                self.input_stream.for_each(self, process_sms)
        
            def stop(self):
                self.input_stream.unregister_all(self)
        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream('all_sms')
        self.output_sms_stream = cs.stream.create_stream('cs_sms')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sms_stream.for_each(self, record_output)

    def start_task(self, runtime):
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)


if __name__ == '__main__':
    config = MessageTimeConfig()
