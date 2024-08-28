from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class EmailTask4(SingleAgentTaskConfigBase):
    def __init__(self, email_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Interpersonal_relationship,
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "Content": "the content of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_email_reply",
                "description": "A series of replied emails, excluding advertisements, with emails filtered for "
                               "advertisements first, followed by packaging every two emails into a batch, "
                               "and then listing the replies",
                "fields": {
                    "Content": "the content of the email, string",
                    "Auto_reply": "Reply of the email, string = Received!"
                }
            }
        ])

        self.email_data = EmailData().get_emails(email_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForEmailTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_4"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "auto_email_reply")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_advertisements(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            if res.lower() == 'n':
                return email

        def auto_reply(email_list):
            email_list = email_list['item_list']
            for email in email_list:
                content = email.get('Content')
                if content:
                    self.email_output.add_item({
                        "Content": content,
                        "Auto_reply": "Received!"
                    })

        self.email_input.for_each(filter_advertisements).batch(by_count=2).for_each(auto_reply)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'auto_email_reply')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_email_reply'].append(data)

        self.output_email_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'auto_email_reply')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_email_reply'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_emails = {"all_email": []}
        for email in self.email_data:
            sent_emails['all_email'].append(email)
            self.input_email_stream.add_item(email)
        return sent_emails
