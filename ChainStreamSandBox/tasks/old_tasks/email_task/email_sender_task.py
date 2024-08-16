from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
import random
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
random.seed(6666)


class OldEmailTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_emails",
            "description": "A list of emails",
            "fields": {
                "From": "The sender of the email,string",
                "Subject": "The subject of the email,string",
                "Content": "The content of the email,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "emails_sender",
                "description": "A list of emails with the extraction of the sender",
                "fields": {
                    "subject": "The subject of the email,string",
                    "sender": "The sender of the email,string"}
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
        self.output_stream = cs.get_stream(self,"emails_sender")
        self.llm = get_model("Text")
    def start(self):
        def process_email(email):
            email_sender = email["From"]
            email_subject = email["Subject"]           
            self.output_stream.add_item({
            "subject":email_subject,
            "sender":email_sender
            })
        self.input_stream.for_each(process_email)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_emails')
        self.output_email_stream = cs.stream.create_stream(self, 'emails_sender')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime):
        email_list = []
        for message in self.email_data:
            self.input_email_stream.add_item(message)
            email_list.append(message)
        return email_list
