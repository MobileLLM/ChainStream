from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import Ego4DData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WorkReminderTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_video_stream = None
        self.input_gps_stream = None
        self.is_office_event = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Office,
                                modality=str([Modality_Task_tag.GPS_Sensor, Modality_Task_tag.Video]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_location",
            "description": "all of my gps information",
            "fields": {
                "PropertyName": "the street address information from the gps sensor, string"
            }
        }, {
            "stream_id": "all_first_person",
            "description": "Everything I saw from a first-person perspective",
            "fields": {
                "image_file": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_command",
                "description": "A stream of recordings when the GPS detects that I am in the office buliding and the "
                               "surveillance video detects that I am talking in the office conference room.("
                               "PropertyName: 'Century Technology Light Building')",
                "fields": {
                    "command": "The automatic command to record the conversations in the conference, string = 'Start "
                               "recording the conversation!' "
                }
            }, {
                "stream_id": "is_office_event",
                "description": "A check for whether I am is in the office building",
                "fields": {
                    "Status": "True or False, bool"
                }
            }
        ])
        self.landmark_data = LandmarkData().get_landmarks(number)
        self.first_person_data = Ego4DData().load_for_meeting()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task_4"):
        super().__init__(agent_id)
        self.video_input = cs.get_stream(self, "all_first_person")
        self.gps_input = cs.get_stream(self, "all_location")
        self.command_output = cs.create_stream(self, "auto_command")
        self.video_buffer = Buffer()
        self.is_office_event = cs.create_stream(self, "is_office_event")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def save_video(video):
            self.video_buffer.append(video)
        self.video_input.for_each(save_video)

        def check_communicating(is_office_event):
            if is_office_event is not None:
                videos = self.video_buffer.get_all()
                for video in videos:
                    prompt = "Am I talking in the office? Simply answer y or n"
                    res = self.llm.query(cs.llm.make_prompt(video['frame'], prompt))
                    if res.lower() == 'y':
                        self.command_output.add_item({
                            "command": "Start recording the conversation!"
                        })
            return is_office_event

        def analysis_gps(gps):
            address = gps["PropertyName"]
            if address == "Century Technology Light Building":
                self.is_office_event.add_item({"Status": True})
                return gps
            else:
                return None
        self.gps_input.for_each(analysis_gps).for_each(check_communicating)
        '''

    def init_environment(self, runtime):
        self.input_video_stream = cs.stream.create_stream(self, 'all_first_person')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_location')
        self.output_message_stream = cs.stream.create_stream(self, 'auto_command')
        self.is_office_event = cs.stream.create_stream(self, 'is_office_event')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output1(data):
            self.output_record['auto_command'].append(data)

        def record_output2(data):
            self.output_record['is_office_event'].append(data)

        self.output_message_stream.for_each(record_output1)
        self.is_office_event.for_each(record_output2)

    def init_input_stream(self, runtime):
        self.input_video_stream = cs.stream.create_stream(self, 'all_first_person')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_location')

    def init_output_stream(self, runtime):
        self.output_message_stream = cs.stream.get_stream(self, 'auto_command')
        self.is_office_event = cs.stream.get_stream(self, 'is_office_event')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output1(data):
            self.output_record['auto_command'].append(data)

        def record_output2(data):
            self.output_record['is_office_event'].append(data)

        self.output_message_stream.for_each(record_output1)
        self.is_office_event.for_each(record_output2)

    def start_task(self, runtime) -> dict:
        properties = [
            {
                'PrimaryPropertyType': 'Mid-Rise Multifamily',
                'PropertyName': 'Century Technology Light Building',
                'Street Address': '123 Innovation Street',
                'Neighborhood': 'Tech Park',
                'YearBuilt': 2010,
                'NumberofFloors': 15,
                'Electricity(kWh)': 450000.0,
                'NaturalGas(therms)': 9000.0,
                'GHGEmissions(MetricTonsCO2e)': 72.30
            },
            {
                'PrimaryPropertyType': 'Office Building',
                'PropertyName': 'Century Technology Light Building',
                'Street Address': '456 Development Avenue',
                'Neighborhood': 'Business District',
                'YearBuilt': 2015,
                'NumberofFloors': 20,
                'Electricity(kWh)': 600000.0,
                'NaturalGas(therms)': 12000.0,
                'GHGEmissions(MetricTonsCO2e)': 95.50
            },
            {
                'PrimaryPropertyType': 'High-Rise Multifamily',
                'PropertyName': 'Century Technology Light Building',
                'Street Address': '789 Future Boulevard',
                'Neighborhood': 'Innovation Hub',
                'YearBuilt': 2018,
                'NumberofFloors': 25,
                'Electricity(kWh)': 750000.0,
                'NaturalGas(therms)': 15000.0,
                'GHGEmissions(MetricTonsCO2e)': 118.75
            }
        ]
        self.landmark_data.extend(properties)
        sent_info = {'all_first_person': [], 'all_location': []}
        for frame in self.first_person_data:
            sent_info['all_first_person'].append(frame)
            self.input_video_stream.add_item({"frame": frame})
        for landmark in self.landmark_data:
            sent_info['all_location'].append(landmark)
            self.input_gps_stream.add_item(landmark)
        return sent_info
