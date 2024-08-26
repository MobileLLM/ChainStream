from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldMessageTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_sms",
            "description": "A list of messages information",
            "fields": {
                "text": "The content of the message, string",
                "language": "The language of the message, string",
                "time": "The time of the message, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sms_summary",
                "description": "A list of the summary of the message reports",
                "fields": {
                    "content": "The content of the message, string",
                    "summary": "The summary of the message report, string"
                }
            }
        ])

        self.sms_data = SMSData().get_random_message()
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_message_agent")
        self.input_stream = cs.get_stream(self,"all_sms")
        self.output_stream = cs.get_stream(self,"sms_summary")
        self.llm = get_model("Text")
    def start(self):
        def process_sms(sms):
            sms_text = sms["text"]
            prompt = "Summarize the content of the following each SMS message in a sentence"
            response = self.llm.query(cs.llm.make_prompt(prompt,sms_text))
            self.output_stream.add_item({
                "content": sms_text,
                "summary": response
            })
        self.input_stream.for_each(process_sms)
        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')
        self.output_sms_stream = cs.stream.create_stream(self, 'sms_summary')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sms_summary'].append(data)

        self.output_sms_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        message_dict = {'all_sms': []}
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)
            message_dict['all_sms'].append(message)
        return message_dict

