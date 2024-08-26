from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class EmailTask3(SingleAgentTaskConfigBase):
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
                "receiver": "the name of the email receiver, string",
                "Content": "the content of the email, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_by_receiver",
                "description": "A list of email summaries for each email receiver, with advertisements filtered out "
                               "first, followed by packaging every two emails into a batch, then grouping by receiver, "
                               "and finally summarizing",
                "fields": {
                    "receiver": "the name of the email receiver, string",
                    "summary": "the summary of the email for each email receiver, string"
                }
            }
        ])

        self.email_data = EmailData().get_emails(email_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForEmailTask3(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_3"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "summary_by_receiver")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_work(email):
            prompt = "is this email work-related? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            if res.lower() == 'y':
                return email

        def group_by_receiver(email_list):
            email_list = email_list['item_list']
            receiver_group = {}
            for email in email_list:
                if email['receiver'] not in receiver_group:
                    receiver_group[email['receiver']] = [email]
                else:
                    receiver_group[email['receiver']].append(email)
            return list(receiver_group.values())

        def sum_by_receiver(receiver_email):
            receiver = receiver_email[0]['receiver']
            prompt = "Summarize all these emails here"
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in receiver_email], prompt))
            self.email_output.add_item({
                "receiver": receiver,
                "summary": res
            })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(group_by_receiver).for_each(sum_by_receiver)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'summary_by_receiver')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['summary_by_receiver'].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        received_emails = {"all_email": []}
        for email in self.email_data:
            email['receiver'] = email['To']
            received_emails['all_email'].append(email)
            self.input_email_stream.add_item(email)
        return received_emails





