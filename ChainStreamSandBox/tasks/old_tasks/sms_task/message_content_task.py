from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData
from AgentGenerator.io_model import StreamListDescription
random.seed(6666)


class OldMessageTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_news",
            "description": "A list of news information",
            "fields": {
                "text": "The content of the news,string",
                "language": "The language of the news,string",
                "time": "The time of the news,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sms_content",
                "description": "A list of the content of the news based on the text",
                "fields": {
                    "content": "The content of the news,string"
                }
            }
        ])

        self.sms_data = SMSData().get_random_message()
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_message_agent")
        self.input_stream = cs.get_stream(self,"all_sms")
        self.output_stream = cs.get_stream(self,"sms_content")

    def start(self):
        def process_sms(sms):
            sms_text = sms["text"]
            self.output_stream.add_item({
                "content":sms_text
            })
        self.input_stream.for_each(process_sms)

        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')
        self.output_sms_stream = cs.stream.create_stream(self, 'sms_content')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sms_stream.for_each(record_output)

    def start_task(self, runtime):
        message_list = []
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)
            message_list.append(message)
        return message_list


