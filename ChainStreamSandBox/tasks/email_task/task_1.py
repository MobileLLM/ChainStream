from tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eot_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eot_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries for each email sender, excluding ads",
                "fields": {
                    "sender": "name xxx, string",
                    "summary": "sum xxx, string"
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
        # self.email_output = cs.create_stream(self, {
        #     "stream_id": "summary_by_sender",
        #     "description": "A list of email summaries for each email sender, excluding ads",
        #     "fields": {
        #         "sender": "name xxx, string",
        #         "summary": "sum xxx, string"
        #     }
        # })

        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_ads(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            print("filter_ads", res)
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
        
            print("group_by_sender", list(sender_group.values()))
            return list(sender_group.values())

        def sum_by_sender(sender_email):
            sender = sender_email[0]['sender']
            prompt = "Summarize these all email here"
            print("sum_by_sender: query", [x['Content'] for x in sender_email], prompt)
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in sender_email], prompt))
            print("sum_by_sender", res)
            self.email_output.add_item({
                "sender": sender,
                "sum": res
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

    def start_task(self, runtime):
        count = 0
        for message in self.paper_data:
            count += 1
            # if count % self.eos_gap == 0:
            #     print("adding EOS")
            #     self.input_paper_stream.add_item("EOS")
            message['sender'] = message['From']
            print("adding message", message)
            self.input_paper_stream.add_item(message)
        # self.input_paper_stream.add_item("EOS")





