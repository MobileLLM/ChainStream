from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
import random
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class OldEmailTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_emails",
            "description": "A list of emails",
            "fields": {
                "Subject": "The subject of the email, string",
                "Content": "The content of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "emails_summary",
                "description": "A list of emails with the summary based on the contents",
                "fields": {
                    "subject": "The subject of the email, string",
                    "summary": "The summary of the email, string"}
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
        self.output_stream = cs.get_stream(self,"emails_summary")
        self.llm = get_model("Text")
    def start(self):
        def process_email(email):
            email_content = email["Content"]
            email_subject = email["Subject"]    
            prompt = "Write a brief summary of the following email contents"
            response = self.llm.query(cs.llm.make_prompt(prompt,email_content))
            print(email_subject+" : "+response)
            self.output_stream.add_item({
            "subject": email_subject,
            "summary": response
            })
        self.input_stream.for_each(process_email)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')
        self.output_email_stream = cs.stream.create_stream(self, 'emails_summary')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['emails_summary'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        email_dict = {'all_emails': []}
        for message in self.email_data:
            self.input_email_stream.add_item(message)
            email_dict['all_emails'].append(message)
        return email_dict
