from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class EmailTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
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
                "sender": "the name of the sender, string",
                "Content": "the content of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries for each email sender, with advertisements filtered out "
                               "first, followed by packaging every two emails into a batch, then grouping by sender, "
                               "and finally summarizing",
                "fields": {
                    "sender": "the name of the sender, string",
                    "summary": "the summary of the email for each email sender,excluding advertisements, string"
                }
            }
        ])

        self.email_data = EmailData().get_emails(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForEmailTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "summary_by_sender")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_advertisements(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            if res.lower() == 'n':
                return email

        def group_by_sender(email_list):
            email_list = email_list['item_list']
            sender_group = {}
            for email in email_list:
                if email['sender'] not in sender_group:
                    sender_group[email['sender']] = [email]
                else:
                    sender_group[email['sender']].append(email)
            return list(sender_group.values())

        def sum_by_sender(sender_email):
            sender = sender_email[0]['sender']
            prompt = "Summarize these all email here"
            for x in sender_email:
                res = self.llm.query(cs.llm.make_prompt(x['Content'], prompt))
                self.email_output.add_item({
                    "sender": sender,
                    "summary": res
                })

        self.email_input.for_each(filter_advertisements).batch(by_count=2).for_each(group_by_sender).for_each(sum_by_sender)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'summary_by_sender')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record["summary_by_sender"].append(data)

        self.output_email_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'summary_by_sender')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record["summary_by_sender"].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_emails = {"all_email": []}
        for email in self.email_data:
            email['sender'] = email['From']
            sent_emails['all_email'].append(email)
            self.input_email_stream.add_item(email)
        return sent_emails





