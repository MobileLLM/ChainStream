from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
import random
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class EmailTask6(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_emails",
            "description": "A series of emails",
            "fields": {
                "Subject": "The subject of the email, string",
                "Content": "The content of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "emails_emotion",
                "description": "A series of emails with the analysis of the emotion chosen from ['positive', "
                               "'negative', 'neutral', 'other'] based on the contents",
                "fields": {
                    "Subject": "The subject of the email, string",
                    "emotion": "The emotion analysed from the email chosen from ['positive', 'negative', 'neutral', "
                               "'other'], string"}
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
        self.output_stream = cs.get_stream(self,"emails_emotion")
        self.llm = get_model("Text")
    def start(self):
        def process_email(email):
            email_content = email["Content"]
            email_subject = email["Subject"]           
            prompt = "Classify the following email contents into one of the categories: positive, negative, neutral, other.Choose one and explain"
            response = self.llm.query(cs.llm.make_prompt(prompt,email_content))
            self.output_stream.add_item({
            "Subject": email_subject,
            "emotion": response
            })
        self.input_stream.for_each(process_email)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')
        self.output_email_stream = cs.stream.create_stream(self, 'emails_emotion')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['emails_emotion'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        email_dict = {'all_emails': []}
        for message in self.email_data:
            self.input_email_stream.add_item(message)
            email_dict['all_emails'].append(message)
        return email_dict
