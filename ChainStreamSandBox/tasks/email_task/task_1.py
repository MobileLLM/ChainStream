from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask1(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap

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
#         self.agent_example = '''
# import chainstream
# from chainstream.agent import Agent
# from chainstream.stream import get_stream, create_stream
# from chainstream.context import Buffer
# from chainstream.llm import get_model, make_prompt
#
# class EmailSummaryAgent(Agent):
#     def __init__(self, agent_id: str="email_summary_agent"):
#         super().__init__(agent_id)
#         self.email_stream = get_stream(self, "all_email")
#         self.summary_stream = get_stream(self, "summary_by_sender")
#         self.llm = get_model(["text"])
#
#     def start(self) -> None:
#         def filter_advertisements(email):
#             print("filter_advertisements", email)
#             if "advertisement" not in email['Content'].lower():
#                 print("not an advertisement", email)
#                 return email
#
#         def summarize_emails(email_batch):
#             print("summarize_emails", email_batch)
#             buffer = Buffer()
#             for email in email_batch['item_list']:
#                 buffer.append({'sender': email['sender'], 'content': email['Content']})
#
#             prompt = make_prompt(buffer, "Provide a summary for each sender's emails.")
#             summary = self.llm.query(prompt)
#
#             self.summary_stream.add_item({'sender': email['sender'], 'summary': summary})
#
#         self.email_stream.for_each(filter_advertisements)\
#                           .batch(by_count=5)\
#                           .for_each(summarize_emails)
#
#     def stop(self) -> None:
#         self.email_stream.unregister_all(self)
#         '''
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
            # print("adding message", message)
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages





