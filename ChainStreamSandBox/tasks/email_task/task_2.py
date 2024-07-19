from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from datetime import datetime

random.seed(6666)

class EmailTask2(SingleAgentTaskConfigBase):
    def __init__(self, email_number=30, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "emo_from_work",
                "description": "A list of summaries of the purpose of the emails for each work-related email during these several months",
                "fields": {
                    "work_emails": "content xxx, string",
                    "purpose": "emo xxx, string"
                }
            }
        ])

        self.email_data = EmailData().get_emails(email_number)
        self.agent_example = '''
import chainstream as cs
class AgentExampleForEmailTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_2"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "emo_from_work")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_work(email):
            prompt = "is this email work-related? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            # print("filter_work", res, email)
            if res.lower() == 'y':
                return email

        def filter_date(email_list):
            # print("email_list", email_list)
            filtered_emails = []
            for email in email_list['item_list']:
                # print("email", email)
                if isinstance(email, dict):  
                    email_date_str = email.get('Date')
                    # print("email data str", email_date_str)
                    if email_date_str:
                        date_parts = email_date_str.split()
                        if len(date_parts) > 2:
                            month = date_parts[2]
                            print(month)
                            if month in ['Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']:
                                filtered_emails.append(email)
                        else:
                            print(f"Skipping email due to invalid date format: {email_date_str}")
                else:
                    print(f"Skipping email due to invalid data type: {type(email)}")
            # print("filter_date", filtered_emails)
            return {"email_list":filtered_emails}

            
        def sum_by_content(emails):
            content = [email['Content'] for email in emails['email_list']]
            print(content)
            prompt = "Analyze the purposes of these emails"
            # print("sum_by_content: query", content, prompt)
            res = self.llm.query(cs.llm.make_prompt(content, prompt))
            # print("sum_by_content", res)
            self.email_output.add_item({
                "work_emails": content,
                "purpose": res
            })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(filter_date).for_each(sum_by_content)
'''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'emo_from_work')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.email_data:
            sent_messages.append(message)
            self.input_email_stream.add_item(message)
        return sent_messages
