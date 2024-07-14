from tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from datetime import datetime

random.seed(6666)

class EmailTask2(SingleAgentTaskConfigBase):
    def __init__(self, paper_number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_paper_stream = None
        self.input_paper_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "emo_from_work",
                "description": "A list of email emotion analysis for each work-related email during this month",
                "fields": {
                    "work_emails": "content xxx, string",
                    "emotion": "emo xxx, string"
                }
            }
        ])

        self.paper_data = EmailData().get_emails(paper_number)
        self.agent_example = '''
import chainstream as cs
from datetime import datetime

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
            print("filter_work", res)
            if res.lower() == 'y':
                return list(email)

        def filter_date(email_list):
            filtered_emails = []
            for email in email_list:
                email_date_str = email.get('Date')
                if email_date_str:
                    try:
                        email_date = datetime.strptime(email_date_str, '%a, %d %b %Y %H:%M:%S %z (%Z)')
                        if email_date.strftime('%b') in ['Jun', 'Jul']:
                            filtered_emails.append(email)
                    except ValueError as e:
                        print(f"Skipping email due to date parsing error: {email_date_str}, error: {e}")
            return filtered_emails

        def sum_by_content(emails):
            content = [email['Content'] for email in emails]
            prompt = "Analyze the emotion of these email contents"
            print("sum_by_content: query", content, prompt)
            res = self.llm.query(cs.llm.make_prompt(content, prompt))
            print("sum_by_content", res)
            self.email_output.add_item({
                "work_emails": content,
                "emotion": res
            })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(filter_date).for_each(sum_by_content)
'''

    def init_environment(self, runtime):
        self.input_paper_stream = cs.stream.create_stream(self, 'all_email')
        self.output_paper_stream = cs.stream.create_stream(self, 'emo_from_work')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_paper_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.paper_data:
            sent_messages.append(message)
            self.input_paper_stream.add_item(message)
        return sent_messages
