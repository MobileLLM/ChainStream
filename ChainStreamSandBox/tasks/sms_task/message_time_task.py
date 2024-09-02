from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class MessageTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_sms",
            "description": "A stream of messages information",
            "fields": {
                "text": "The content of the message, string",
                "time": "The time of the message with the format of '%Y.%m.%d %H:%M:%S', datetime"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sms_in_December",
                "description": "A stream of the message texts in January (the month with the '12' format)",
                "fields": {
                    "text": "The content of the message in January (the month with the '12' format), string",
                    "time": "The time of the message with the format of '%Y.%m.%d %H:%M:%S', datetime"
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
        self.output_stream = cs.create_stream(self,"sms_in_December")
        self.llm = cs.llm.get_model("Text")
    def start(self):
        def process_sms(sms):
            sms_time = sms["time"]
            sms_text = sms["text"]
            date_parts = sms_time.split(' ')
            date = date_parts[0]
            year, month, day = date.split('.')
            if month == '12':
                self.output_stream.add_item({
                    "text": sms_text,
                    "sms_time": sms_time
                })
        self.input_stream.for_each(process_sms)
        
        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')
        self.output_sms_stream = cs.stream.create_stream(self, 'sms_in_December')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sms_in_December'].append(data)

        self.output_sms_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')

    def init_output_stream(self, runtime):
        self.output_sms_stream = cs.stream.get_stream(self, 'sms_in_December')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sms_in_December'].append(data)

        self.output_sms_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        message_data = [
            {
                "id": "42638",
                "text": "What happened on 12th December?",
                "language": "en",
                "time": "2012.12.12 10:15:45"
            },
            {
                "id": "42640",
                "text": "What occurred in May 2013?",
                "language": "en",
                "time": "2013.05.15 14:55:00"
            },
            {
                "id": "42641",
                "text": "Details about March 20th incident?",
                "language": "en",
                "time": "2012.03.20 16:45:10"
            },
            {
                "id": "42642",
                "text": "What happened in July 2014?",
                "language": "en",
                "time": "2014.07.25 11:30:00"
            },
            {
                "id": "42639",
                "text": "Why was the event on December 5th canceled?",
                "language": "en",
                "time": "2012.12.05 09:22:30"
            }
        ]
        self.sms_data.extend(message_data)
        message_dict = {'all_sms': []}
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)
            message_dict['all_sms'].append(message)
        return message_dict
