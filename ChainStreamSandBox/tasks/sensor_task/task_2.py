from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GPSTask2(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=30):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
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
                "stream_id": "nearest_hotel",
                "description": "A list of the hotel around according to the street address(every two copies of "
                               "location data are packaged as a batch after filtering hotel property type)",
                "fields": {
                    "address": "the street address of my location",
                    "hotel": "the names of the hotels around,string"
                }
            }
        ])

        self.sensor_data = LandmarkData().get_landmarks(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask2(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_gps_task_2"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_locations")
        self.sensor_output = cs.get_stream(self, "nearest_hotel")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_hotel(location):
            type = location['PrimaryPropertyType']
            if type == "Hotel":
                return location

        def nearest_hotel(location_list):
            location_list = location_list['item_list']
            for location in location_list:
                address = location.get('Street Address')
                hotel = location.get('PropertyName')
                self.sensor_output.add_item({
                    "address": address,
                    "hotel": hotel
                })

        self.sensor_input.for_each(filter_hotel).batch(by_count=2).for_each(nearest_hotel)

        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_locations')
        self.output_sensor_stream = cs.stream.create_stream(self, 'nearest_hotel')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['nearest_hotel'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_gps = {'all_locations': []}
        for gps in self.sensor_data:
            sent_gps['all_locations'].append(gps)
            self.input_sensor_stream.add_item(gps)
        return sent_gps
