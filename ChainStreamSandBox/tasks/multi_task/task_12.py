from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class ReadingLightTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_first_person_stream = None
        self.input_gps_stream = None
        self.input_light_stream = None
        self.adjust_light_stream = None
        self.is_reading_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Living, Domain_Task_tag.Weather]),
                                modality=str([Modality_Task_tag.GPS_Sensor, Modality_Task_tag.Video,
                                              Modality_Task_tag.Light_Sensor]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_first_person",
            "description": "first_person perspective camera data in my study",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, PIL.Image"
            }
        }, {
            "stream_id": "all_gps",
            "description": "all of my GPS information",
            "fields": {
                "PropertyName": "the property name from the gps sensor, string",
            }
        }, {
            "stream_id": "light_intensity",
            "description": "A real-time light_intensity check information",
            "fields": {
                "Light intensity outdoor": "the light intensity information outdoor right now, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "adjust_light",
                "description": "A automatic command to adjust the light in the study when the camera detects that I "
                               "am reading a book at home(the property name is: 'Maple Ridge Apartments').If the "
                               "light exceeds 500, draw the curtains closed. If the light is less than 300, "
                               "turn on the desk lamp.",
                "fields": {
                    "command": "the command to turn on the desk lamp or draw the curtains closed, string = 'Please "
                               "turn on the desk lamp.' if the light intensity is lower than 300, or 'Please draw the "
                               "curtains closed.'if the light intensity is over 500 "
                }
            },
            {
                "stream_id": "is_reading",
                "description": "Check whether the person is reading or not",
                "fields": {
                    "Status": "True or False, bool"
                }
            }
        ])
        self.gps_data = LandmarkData().get_landmarks(number)
        self.video_data = Ego4DData().load_for_object_detection()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask12(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task12"):
        super().__init__(agent_id)
        self.gps_input = cs.get_stream(self, "all_gps")
        self.video_input = cs.get_stream(self, "all_first_person")
        self.command_output = cs.create_stream(self, "adjust_light")
        self.light_input = cs.get_stream(self, "light_intensity")
        self.is_reading = cs.create_stream(self, "is_reading")
        self.llm = cs.llm.get_model("image")
        self.video_buffer = Buffer()
    
    def start(self):
        def save_video(video_data):
            self.video_buffer.append(video_data)
        self.video_input.for_each(save_video)
        
        def check_place(gps_data):
            if gps_data["PropertyName"] == "Maple Ridge Apartments":
                first_person_data = self.video_buffer.pop_all()
                return first_person_data

        def check_reading(first_person_data):
            prompt = "Please check whether I am reading books.Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_data["frame"]))
            print(res)
            if res.lower()== "y" :
                self.is_reading.add_item({"Status":True})
                return first_person_data
            else:
                return None
        def check_light(light_inputs):
            if self.is_reading is not None:
                intensity = light_inputs["Light intensity outdoor"]
                if intensity<300 :
                    self.command_output.add_item({
                        "light_intensity": intensity,
                        "command": 'Please turn on the desk lamp.'
                    })
                elif intensity>500:
                    self.command_output.add_item({
                        "light_intensity": intensity,
                        "command": 'Please draw the curtains closed.'
                    })
            return light_inputs
        self.gps_input.for_each(check_place).for_each(check_reading)
        self.light_input.for_each(check_light)
        '''

    def init_environment(self, runtime):
        self.input_first_person_stream = cs.stream.create_stream(self, 'all_first_person')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_light_stream = cs.stream.create_stream(self, 'light_intensity')
        self.adjust_light_stream = cs.stream.create_stream(self, 'adjust_light')
        self.is_reading_stream = cs.stream.create_stream(self, 'is_reading')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output1(data):
            self.output_record['adjust_light'].append(data)

        def record_output2(data):
            self.output_record['is_reading'].append(data)

        self.adjust_light_stream.for_each(record_output1)
        self.is_reading_stream.for_each(record_output2)

    def init_input_stream(self, runtime):
        self.input_first_person_stream = cs.stream.create_stream(self, 'all_first_person')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_light_stream = cs.stream.create_stream(self, 'light_intensity')

    def init_output_stream(self, runtime):
        self.adjust_light_stream = cs.stream.get_stream(self, 'adjust_light')
        self.is_reading_stream = cs.stream.get_stream(self, 'is_reading')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output1(data):
            self.output_record['adjust_light'].append(data)

        def record_output2(data):
            self.output_record['is_reading'].append(data)

        self.adjust_light_stream.for_each(record_output1)
        self.is_reading_stream.for_each(record_output2)

    def start_task(self, runtime) -> dict:
        import random
        tmp_random = random.Random(42)
        properties = [
            {
                'PrimaryPropertyType': 'Mid-Rise Multifamily',
                'PropertyName': 'Maple Ridge Apartments',
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
                'PropertyName': 'Maple Ridge Apartments',
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
                'PropertyName': 'Maple Ridge Apartments',
                'Street Address': '789 Future Boulevard',
                'Neighborhood': 'Innovation Hub',
                'YearBuilt': 2018,
                'NumberofFloors': 25,
                'Electricity(kWh)': 750000.0,
                'NaturalGas(therms)': 15000.0,
                'GHGEmissions(MetricTonsCO2e)': 118.75
            }
        ]
        self.gps_data.extend(properties)
        sent_info = {'all_first_person': [], 'all_gps': [], 'light_intensity': []}
        for frame in self.video_data:
            sent_info['all_first_person'].append(frame)
            self.input_first_person_stream.add_item({"frame": frame})
        for gps in self.gps_data:
            sent_info['all_gps'].append(gps)
            self.input_gps_stream.add_item(gps)
        for _ in range(10):
            light_intensity = tmp_random.uniform(0, 1000)
            sent_info['light_intensity'].append(light_intensity)
            self.input_light_stream.add_item({"Light intensity outdoor": light_intensity})
        return sent_info
