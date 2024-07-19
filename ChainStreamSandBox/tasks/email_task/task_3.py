from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask3(SingleAgentTaskConfigBase):
    def __init__(self, email_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "summary_by_receiver",
                "description": "A list of summaries of work-related emails for each email receiver",
                "fields": {
                    "receiver": "name xxx, string",
                    "summaries": "sum xxx, string"
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
        # self.email_output = cs.create_stream(self, {
        #     "stream_id": "summary_by_receiver",
        #     "description": "A list of summaries of work-related emails for each email receiver",
        #     "fields": {
        #         "receiver": "name xxx, string",
        #         "summaries": "sum xxx, string"
        #     }
        # })

        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_work(email):
            prompt = "is this email work-related? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            print("filter_work", res)
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

            print("group_by_receiver", list(receiver_group.values()))
            return list(receiver_group.values())

        def sum_by_receiver(receiver_email):
            receiver = receiver_email[0]['receiver']
            prompt = "Summarize all these emails here"
            print("sum_by_receiver: query", [x['Content'] for x in receiver_email], prompt)
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in receiver_email], prompt))
            print("sum_by_receiver", res)
            self.email_output.add_item({
                "receiver": receiver,
                "summaries": res
            })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(group_by_receiver).for_each(sum_by_receiver)
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'summary_by_receiver')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        received_messages = []
        for message in self.email_data:
            message['receiver'] = message['To']
            received_messages.append(message)
            self.input_email_stream.add_item(message)
        return received_messages





