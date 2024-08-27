from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SMSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class MessageTask2(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_sms_stream = None
        self.input_sms_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_sms",
            "description": "A series of messages information",
            "fields": {
                "text": "The content of the message, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "sms_emotion",
                "description": "A series of the analysis of the emotion of the messages chosen from positive, "
                               "negative, neutral and other based on the text",
                "fields": {
                    "text": "The text content of the message, string",
                    "emotion": "The analysis of the emotion of the message, string"
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
        self.output_stream = cs.get_stream(self,"sms_emotion")
        self.llm = get_model("Text")
    def start(self):
        def process_sms(sms):
            sms_text = sms["text"]
            prompt = "Classify the following message contents into one of the categories: positive, negative, neutral, other.Choose one and explain"
            response = self.llm.query(cs.llm.make_prompt(prompt,sms_text))
            self.output_stream.add_item({
                "text": sms_text,
                "emotion": response
            })
        self.input_stream.for_each(process_sms)

        '''

    def init_environment(self, runtime):
        self.input_sms_stream = cs.stream.create_stream(self, 'all_sms')
        self.output_sms_stream = cs.stream.create_stream(self, 'sms_emotion')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['sms_emotion'].append(data)

        self.output_sms_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        message_dict = {'all_sms': []}
        for message in self.sms_data:
            self.input_sms_stream.add_item(message)
            message_dict['all_sms'].append(message)
        return message_dict
