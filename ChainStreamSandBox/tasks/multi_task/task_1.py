from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class EmailTaskTest(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_email_stream = None
        self.input_email_stream = None
        self.input_location_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Office, Domain_Task_tag.Location]),
                                modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
                "sender": "the name of the sender, string",
                "Content": "the content of the email, string"
            }
        }, {
            "stream_id": "all_location",
            "description": "all of my location data",
            "fields": {
                "Street Address": "the street address information from the location sensor, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_reply_in_office",
                "description": "A series of replied emails, excluding advertisements in the office (office street "
                               "address: 3127 Edgemont Boulevard), with every two emails packaged into a batch after "
                               "filtering out the advertisements.",
                "fields": {
                    "content": "the content of the emails, string",
                    "tag": "An auto reply message, string = Received!"
                }
            }, {
                "stream_id": "is_office_event",
                "description": "A bool to check whether the person is in the office",
                "fields": {
                    "Status": "True or False, bool"
                }
            }
        ])
        self.location_data = LandmarkData().get_landmarks(number)
        self.email_data = EmailData().get_emails(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.location_input = cs.get_stream(self, "all_location")
        self.email_output = cs.get_stream(self, "auto_reply_in_office")
        self.email_buffer = Buffer()
        self.is_office_event = cs.get_stream(self, "is_office_event")
        self.llm = cs.llm.get_model("Text")
        
    def start(self):
        def save_email(email):
            self.email_buffer.append(email)
        self.email_input.for_each(save_email)
        
        def filter_advertisements(is_office_event):
            if is_office_event:
                emails = self.email_buffer.pop_all()
                matching_emails = []
                for email in emails:
                    prompt = "is this email an advertisement? answer y or n"
                    res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
                    if res.lower() == 'n':
                        matching_emails.append(email)
                return matching_emails

        def auto_reply(email_list):
            email_list = email_list['item_list']
            for email in email_list:
                content = email.get('Content')
                if content:
                    self.email_output.add_item({
                        "content": content,
                        "tag": "Received!"
                    })
                    
        def analysis_location(location):
            address = location["Street Address"]
            if address == "3127 Edgemont Boulevard":
                self.is_office_event.add_item({"Status": "True"})
                return location
            else:
                return None
        self.location_input.for_each(analysis_location).for_each(filter_advertisements).batch(by_count=2).for_each(auto_reply)     
        '''

    def init_environment(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.input_location_stream = cs.stream.create_stream(self, 'all_location')
        self.output_email_stream = cs.stream.create_stream(self, 'auto_reply_in_office')
        self.is_office_event = cs.stream.create_stream(self, 'is_office_event')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_reply_in_office'].append(data)
            self.output_record['is_office_event'].append(data)

        self.output_email_stream.for_each(record_output)
        self.is_office_event.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {"all_email": [], "all_location": []}
        for email in self.email_data:
            sent_info["all_email"].append(email)
            self.input_email_stream.add_item(email)
        for location in self.location_data:
            sent_info["all_location"].append(location)
            self.input_location_stream.add_item(location)
        return sent_info
