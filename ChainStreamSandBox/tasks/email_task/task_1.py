from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None
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
                "description": "A list of email summaries for each email sender, excluding ads",
                "fields": {
                    "sender": "the name of the sender, string",
                    "summary": "the summary of the email for each email sender,excluding ads, string"
                }
            }
        ])

        self.paper_data = EmailData().get_emails(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForEmailTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "summary_by_sender")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_ads(email):
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
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in sender_email], prompt))
            self.email_output.add_item({
                "sender": sender,
                "summary": res
            })

        self.email_input.for_each(filter_ads).batch(by_count=2).for_each(group_by_sender).for_each(sum_by_sender)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_email')
        self.output_paper_stream = cs.stream.create_stream(self, 'summary_by_sender')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            message['sender'] = message['From']
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





