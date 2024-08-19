from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class OldGPSTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_gps_stream = None
        self.input_gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Location,
                                scene=Scene_Task_tag.Travel, modality=Modality_Task_tag.Text)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "A list of the gps data",
            "fields": {
                "CapitalName": "The capital city to which the location belongs,string",
                "ContinentName": "The continent to which the location belongs,string",
                "CountryName": "The country to which the location belongs,string",
                "CapitalLatitude": "The capital latitude of the location,float",
                "CapitalLongitude": "The capital longitude of the location,float",
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "gps_capital",
                "description": "A list of the capital name extracted from the gps data",
                "fields": {
                    "gps_capital": "The name of the capital city to which the location belongs,string"}
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
        self.output_stream = cs.get_stream(self,"gps_capital")
        self.llm = get_model("Text")
    def start(self):
        def process_gps(gps):
            gps_capital = gps["CapitalName"]        
            self.output_stream.add_item({
                "gps_capital":gps_capital
            })
        self.input_stream.for_each(process_gps)

        '''

    def init_environment(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_gps_stream = cs.stream.create_stream(self, 'gps_capital')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['gps_capital'].append(data)

        self.output_gps_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        gps_dict = {'all_gps': []}
        for info in self.gps_data:
            self.input_gps_stream.add_item(info)
            gps_dict['all_gps'].append(info)
        return gps_dict
