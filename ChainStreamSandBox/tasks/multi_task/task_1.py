from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import EmailData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


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
                                modality=str([Modality_Task_tag.Text, Modality_Task_tag.GPS_Sensor]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_email",
            "description": "All email messages",
            "fields": {
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
                "description": "A stream of replied emails, excluding advertisements in the office (office street "
                               "address: '3127 Edgemont Boulevard'), with every two emails packaged into a batch after "
                               "filtering out the advertisements.",
                "fields": {
                    "Content": "the content of the emails, string",
                    "receipt Acknowledgment": "An auto reply message, string = 'Received!'"
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
        self.email_output = cs.create_stream(self, "auto_reply_in_office")
        self.email_buffer = Buffer()
        self.is_office_event = cs.create_stream(self, "is_office_event")
        self.llm = cs.llm.get_model("Text")
        
    def start(self):
        def save_email(email):
            self.email_buffer.append(email)
        self.email_input.for_each(save_email)
        
        def filter_advertisements(is_office_event):
            if is_office_event is not None:
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
                        "Content": content,
                        "receipt Acknowledgment": "Received!"
                    })
                    
        def analysis_location(location):
            address = location["Street Address"]
            if address == "3127 Edgemont Boulevard":
                self.is_office_event.add_item({"Status": True})
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

        def record_output_1(data):
            self.output_record['auto_reply_in_office'].append(data)

        self.output_email_stream.for_each(record_output_1)

        def record_output_2(data):
            self.output_record['is_office_event'].append(data)

        self.is_office_event.for_each(record_output_2)

    def init_input_stream(self, runtime):
        self.input_email_stream = cs.stream.create_stream(self, 'all_email')
        self.input_location_stream = cs.stream.create_stream(self, 'all_location')

    def init_output_stream(self, runtime):
        self.output_email_stream = cs.stream.get_stream(self, 'auto_reply_in_office')
        self.is_office_event = cs.stream.get_stream(self, 'is_office_event')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output_1(data):
            self.output_record['auto_reply_in_office'].append(data)

        self.output_email_stream.for_each(record_output_1)

        def record_output_2(data):
            self.output_record['is_office_event'].append(data)

        self.is_office_event.for_each(record_output_2)

    def start_task(self, runtime) -> dict:
        hotels = [
            {
                'PrimaryPropertyType': 'Hotel',
                'PropertyName': 'SUNSET VIEW HOTEL',
                'Street Address': '3127 Edgemont Boulevard',
                'Neighborhood': 'MIDTOWN',
                'YearBuilt': 1985,
                'NumberofFloors': 8,
                'Electricity(kWh)': 750000.0,
                'NaturalGas(therms)': 9500.0,
                'GHGEmissions(MetricTonsCO2e)': 180.25
            },
            {
                'PrimaryPropertyType': 'Hotel',
                'PropertyName': 'LUXURY INN',
                'Street Address': '3127 Edgemont Boulevard',
                'Neighborhood': 'DOWNTOWN',
                'YearBuilt': 2000,
                'NumberofFloors': 15,
                'Electricity(kWh)': 1200000.0,
                'NaturalGas(therms)': 11000.0,
                'GHGEmissions(MetricTonsCO2e)': 220.75
            },
            {
                'PrimaryPropertyType': 'Hotel',
                'PropertyName': 'CITYSCAPE RESORT',
                'Street Address': '3127 Edgemont Boulevard',
                'Neighborhood': 'UPTOWN',
                'YearBuilt': 2010,
                'NumberofFloors': 10,
                'Electricity(kWh)': 950000.0,
                'NaturalGas(therms)': 10500.0,
                'GHGEmissions(MetricTonsCO2e)': 195.60
            }
        ]
        self.location_data.extend(hotels)
        sent_info = {"all_email": [], "all_location": []}
        for email in self.email_data:
            sent_info["all_email"].append(email)
            self.input_email_stream.add_item(email)
        for location in self.location_data:
            sent_info["all_location"].append(location)
            self.input_location_stream.add_item(location)
        return sent_info
