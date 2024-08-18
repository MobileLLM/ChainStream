from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GPSTask1(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_locations",
            "description": "All locations information",
            "fields": {
                "ContinentName": "the name of the continent, string",
                "CapitalLatitude": "the latitude of my location, string",
                "CapitalLongitude": "the longitude of my location, string",
                "CapitalName": "the name of the capital, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "city_identification",
                "description": "A list of the city identifications according to the longitude and latitude sensor in "
                               "North America(every two copies of location data are packaged as a batch after "
                               "filtering the gps data in North America)",
                "fields": {
                    "longitude": "the longitude of my location, string",
                    "latitude": "the latitude of my location, string",
                    "city": "the name of my city, string"
                }
            }
        ])

        self.sensor_data = GPSData().get_gps(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_gps_task_1"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_locations")
        self.sensor_output = cs.get_stream(self, "city_identification")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_location(location):
            continent = location['ContinentName']
            if continent == "North America":
                return location

        def analysis_location(location_list):
            location_list = location_list['item_list']
            for location in location_list:
                latitude = location.get('CapitalLatitude')
                longitude = location.get('CapitalLongitude')
                capital = location.get('CapitalName')
                self.sensor_output.add_item({
                    "latitude": latitude,
                    "longitude": longitude,
                    "city":capital
                })

        self.sensor_input.for_each(filter_location).batch(by_count=2).for_each(analysis_location)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_locations')
        self.output_sensor_stream = cs.stream.create_stream(self, 'city_identification')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['city_identification'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_gps = {'all_locations': []}
        for gps in self.sensor_data:
            sent_gps['all_locations'].append(gps)
            self.input_sensor_stream.add_item(gps)
        return sent_gps
