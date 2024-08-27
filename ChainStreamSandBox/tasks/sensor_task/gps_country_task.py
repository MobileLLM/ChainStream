from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class GPSTask9(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_gps_stream = None
        self.input_gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Location,
                                modality=Modality_Task_tag.GPS_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "A series of the gps data",
            "fields": {
                "CountryName": "The country to which the location belongs, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "gps_country",
                "description": "A series of the country name extracted from the gps data",
                "fields": {
                    "CountryName": "The name of the country to which the location belongs, string"}
            }
        ])
        self.gps_data = GPSData().get_gps(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_gps_agent")
        self.input_stream = cs.get_stream(self,"all_gps")
        self.output_stream = cs.get_stream(self,"gps_country")
        self.llm = get_model("Text")
    def start(self):
        def process_gps(gps):
            gps_country = gps["CountryName"]        
            self.output_stream.add_item({
                "CountryName": gps_country
            })
        self.input_stream.for_each(process_gps)

        '''

    def init_environment(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_gps_stream = cs.stream.create_stream(self, 'gps_country')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['gps_country'].append(data)

        self.output_gps_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        gps_dict = {'all_gps': []}
        for info in self.gps_data:
            self.input_gps_stream.add_item(info)
            gps_dict['all_gps'].append(info)
        return gps_dict
