from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class GPSTask3(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=100, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None

        self.eos_gap = eos_gap

        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "school_street",
                "description": "Tell me the street address of all the schools in my city",
                "fields": {
                    "address":"xxx,string",
                    "hotel":"xxx,string"
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
                print(location)
                return location

        def nearest_district(location_list):
            # print(location_list)
            location_list = location_list['item_list']
            # print(location_list)
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

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.sensor_data:
            sent_messages.append(message)
            self.input_sensor_stream.add_item(message)
        return sent_messages






