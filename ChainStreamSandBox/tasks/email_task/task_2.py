from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class EmailTask2(SingleAgentTaskConfigBase):
    def __init__(self, email_number=30):
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
                "Content": "the content of the email, string",
                "Date": "RFC 822 datetime format, string"

            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "purpose_of_work_email",
                "description": "A stream of purposes for each work-related email from June to December, with emails "
                               "filtered for work-related topics first, followed by packaging every two emails into a "
                               "batch, then filtering by date, and finally summarizing the purposes",
                "fields": {
                    "Content": "the content of the work-related email, string",
                    "purpose": "the purpose of the work-related email sent by the sender chosen from['Request for "
                               "Information', 'Meeting Scheduling', 'Project Update', 'Task Assignment', "
                               "'Feedback Request', 'Report Submission', 'Inquiry', 'Clarification', "
                               "'Approval Request', 'Status Update', 'Other'], string "
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
        self.email_output = cs.create_stream(self, "purpose_of_work_email")
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
            for email in emails['email_list']:
                content = email['Content']
                prompt = "Analyze the purposes of these emails chosen from ['Request for Information', 'Meeting Scheduling', 'Project Update', 'Task Assignment', 'Feedback Request', 'Report Submission', 'Inquiry', 'Clarification', 'Approval Request', 'Status Update', 'Other']. Please only give me the choice."
                res = self.llm.query(cs.llm.make_prompt(content, prompt))
                self.email_output.add_item({
                    "Content": content,
                    "purpose": res
                })

        self.email_input.for_each(filter_work).batch(by_count=2).for_each(filter_date).for_each(sum_by_content)
'''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.output_email_stream = cs.stream.create_stream(self, 'purpose_of_work_email')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record["purpose_of_work_email"].append(data)

        self.output_email_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'purpose_of_work_email')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record["purpose_of_work_email"].append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_emails = {"all_email": []}
        for email in self.email_data:
            sent_emails['all_email'].append(email)
            self.input_email_stream.add_item(email)
        return sent_emails
