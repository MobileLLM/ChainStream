from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class EmailTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_emails",
            "description": "A stream of emails",
            "fields": {
                "Date": "The date of the email with the format of '%a, %d %b %Y %H:%M:%S %z (%Z)', datetime",
                "Subject": "The subject of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "email_subject_in_Apr",
                "description": "A stream of emails in 'Apr' extracted from the field 'Date'",
                "fields": {
                    "Subject": "The subject of the email in 'Apr', string"
                }
            }
        ])
        self.email_data = EmailData().get_emails(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_email_agent")
        self.input_stream = cs.get_stream(self,"all_emails")
        self.output_stream = cs.create_stream(self,"email_subject_in_Apr")
        self.llm = get_model("Text")
    def start(self):
        def process_email(email):
            email_date = email["Date"]
            email_subject = email["Subject"]
            parts = email_date.split() 
            month = parts[2]
            if month == 'Apr':                  
                self.output_stream.add_item({
                "Subject": email_subject
                })
        self.input_stream.for_each(process_email)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')
        self.output_email_stream = cs.stream.create_stream(self, 'email_subject_in_Apr')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['email_subject_in_Apr'].append(data)

        self.output_email_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'email_subject_in_Apr')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['email_subject_in_Apr'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        email_dict = {'all_emails': []}
        for message in self.email_data:
            self.input_email_stream.add_item(message)
            email_dict['all_emails'].append(message)
        return email_dict
