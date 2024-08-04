from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class EmailTaskTest(SingleAgentTaskConfigBase):
    def __init__(self, number=10, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.input_gps_stream = None
        self.is_office_event = None
        self.gps_output = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "name xxx, string",
                "Content": "text xxx, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply_in_office",
                "description": "Replied list of emails,excluding ads when I am in the office",
                "fields": {
                    "content": "xxx, string",
                    "tag": "Received, string"
                }
            }
        ])
        self.gps_data = LandmarkData().get_landmarks(number)
        self.email_data = EmailData().get_emails(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForEmailTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_4"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.gps_output = cs.get_stream(self, "gps_output")
        self.email_output = cs.get_stream(self, "auto_reply_in_office")
        self.email_buffer = Buffer()
        self.is_office_event = cs.get_stream(self, "is_office_event")
        self.llm = cs.llm.get_model("Text")
        
    def start(self):
        def save_email(email):
            self.email_buffer.append(email)
        self.email_input.for_each(save_email)
        
        def filter_ads(is_office_event):
            print(is_office_event)
            if is_office_event:
                emails = self.email_buffer.pop_all()
                print("emails",emails)
                matching_emails = []
                for email in emails:
                    prompt = "is this email an advertisement? answer y or n"
                    res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
                    print("filter_ads", res)
                    if res.lower() == 'n':
                        matching_emails.append(email)
                print("matching_emails", matching_emails)
                return matching_emails

        def auto_reply(email_list):
            print("auto_reply", email_list)
            email_list = email_list['item_list']
            for email in email_list:
                content = email.get('Content')
                if content:
                    self.email_output.add_item({
                        "email": content,
                        "tag": "Received!"
                    })
                else:
                    print(f"Email missing 'Content' field: {email}")
        def analysis_gps(gps):
            address = gps["Street Address"]
            if address == "3127 Edgemont Boulevard":
                print("True")
                self.is_office_event.add_item("True")
                return gps
            else:
                return None
            # else:
            #     print("False")
            #     self.is_office_event.add_item("False")
            # return gps
        self.gps_input.for_each(analysis_gps).for_each(filter_ads).batch(by_count=2).for_each(auto_reply)     
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_email_stream = cs.stream.create_stream(self, 'auto_reply_in_office')
        self.is_office_event = cs.stream.create_stream(self, 'is_office_event')
        self.gps_output = cs.stream.create_stream(self, 'gps_output')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_email_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.email_data:
            sent_messages.append(message)
            self.input_email_stream.add_item(message)
        for gps in self.gps_data:
            sent_messages.append(gps)
            self.input_gps_stream.add_item(gps)
        return sent_messages





