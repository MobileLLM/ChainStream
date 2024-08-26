from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *
random.seed(6666)


class GPSTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=100):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Location,
                                modality=Modality_Task_tag.GPS_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_locations",
            "description": "All locations information",
            "fields": {
                "PrimaryPropertyType": "the type of the primary property, string",
                "Street Address": "the street address of my location, string",
                "PropertyName": "the name of the primary property, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "street_of_school",
                "description": "A list of the street addresses of all the 'K-12 School' around (every two copies of "
                               "location data are packaged as a batch after filtering K-12 School property type)",
                "fields": {
                    "address": "the street address of my location, string",
                    "school": "the names of the schools around, string"
                }
            }
        ])

        self.sensor_data = LandmarkData().get_landmarks(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask3(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_gps_task_2"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_locations")
        self.sensor_output = cs.get_stream(self, "street_of_school")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_school(location):
            type = location['PrimaryPropertyType']
            if type == "K-12 School":
                return location

        def nearest_district(location_list):
            location_list = location_list['item_list']
            for location in location_list:
                address = location.get('Street Address')
                school = location.get('PropertyName')
                self.sensor_output.add_item({
                    "address": address,
                    "school": school
                })

        self.sensor_input.for_each(filter_school).batch(by_count=2).for_each(nearest_district)

        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_locations')
        self.output_sensor_stream = cs.stream.create_stream(self, 'street_of_school')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['street_of_school'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_gps = {'all_locations': []}
        for gps in self.sensor_data:
            sent_gps['all_locations'].append(gps)
            self.input_sensor_stream.add_item(gps)
        return sent_gps
