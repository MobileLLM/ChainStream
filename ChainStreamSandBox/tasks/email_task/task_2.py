from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTask2(SingleAgentTaskConfigBase):
    def __init__(self, email_number=30):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "the name of the email sender, string",
                "Content": "the content of the email, string",
                "Date": "RFC 822 datetime format, string"

            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "purpose_of_work_email",
                "description": "A list of purposes for each work-related email during June to December(every two "
                               "emails are packaged as a batch after filtering the work-related topic)",
                "fields": {
                    "work_emails": "the content of the work-related email, string",
                    "purpose": "the purpose of the work-related email sent by the sender, string"
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
        self.email_output = cs.get_stream(self, "purpose_of_work_email")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_work(email):
            prompt = "is this email work-related? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            if res.lower() == 'y':
                return email

        def filter_date(email_list):
            filtered_emails = []
            for email in email_list['item_list']:
                if isinstance(email, dict):  
                    email_date_str = email.get('Date')
                    if email_date_str:
                        date_parts = email_date_str.split()
                        if len(date_parts) > 2:
                            month = date_parts[2]
                            if month in ['Jun', 'Jul','Aug','Sep','Oct','Nov','Dec']:
                                filtered_emails.append(email)
            return {"email_list":filtered_emails}

            
        def sum_by_content(emails):
            content = [email['Content'] for email in emails['email_list']]
            prompt = "Analyze the purposes of these emails"
            res = self.llm.query(cs.llm.make_prompt(content, prompt))
            self.email_output.add_item({
                "work_emails": content,
                "purpose": res
            })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(filter_date).for_each(sum_by_content)
'''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'purpose_of_work_email')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_emails = []
        for email in self.email_data:
            sent_emails.append(email)
            self.input_email_stream.add_item(email)
        return sent_emails
