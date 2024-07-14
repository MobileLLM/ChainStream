from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask4(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply",
                "description": "Replied list of emails,excluding ads",
                "fields": {
                    "content": "xxx, string",
                    "tag": "Received, string"
                }
            }
        ])

        self.paper_data = EmailData().get_emails(paper_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForEmailTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_4"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "auto_reply")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_ads(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            print("filter_ads", res)
            if res.lower() == 'n':
                return email

        # def group_by_sender(email_list):
        #     email_list = email_list['item_list']
        #     sender_group = {}
        #     for email in email_list:
        #         sender = email.get('sender')
        #         if sender:
        #             if sender not in sender_group:
        #                 sender_group[sender] = [email]
        #             else:
        #                 sender_group[sender].append(email)
        #     print("group_by_sender", list(sender_group.values()))
        #     return list(sender_group.values())

        def auto_reply(email):
            content = email.get('Content')
            if content:
                self.email_output.add_item({
                    "sender": content,
                    "tag": "Received!"
                })
            else:
                print(f"Email missing 'Content' field: {email}")

        self.email_input.for_each(filter_ads).batch(by_count=2).for_each(auto_reply)
        '''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_email')
        self.output_paper_stream = cs.stream.create_stream(self, 'auto_reply')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            # message['sender'] = message['From']
            # print("adding message", message)
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





