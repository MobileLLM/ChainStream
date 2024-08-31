from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class GPSTask8(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_gps_stream = None
        self.input_gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Location,
                                modality=Modality_Task_tag.GPS_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "A stream of the gps data",
            "fields": {
                "ContinentName": "The continent to which the location belongs, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "gps_continent_in_French",
                "description": "A stream of the name of the continents which are translated into French",
                "fields": {
                    "continent_in_French": "The French name of the continent, string"}
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
        self.output_stream = cs.create_stream(self,"gps_continent_in_French")
        self.llm = get_model("Text")
    def start(self):
        def process_gps(gps):
            gps_continent = gps["ContinentName"]
            prompt = 'Please translate the continent name to French.Only give me the name'
            response = self.llm.query(cs.llm.make_prompt(prompt,gps_continent))        
            self.output_stream.add_item({
                "continent_in_French": response
            })
        self.input_stream.for_each(process_gps)

        '''

    def init_environment(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_gps_stream = cs.stream.create_stream(self, 'gps_continent_in_French')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['gps_continent_in_French'].append(data)

        self.output_gps_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')

    def init_output_stream(self, runtime):
        self.output_gps_stream = cs.stream.get_stream(self, 'gps_continent_in_French')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['gps_continent_in_French'].append(data)

        self.output_gps_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        gps_dict = {'all_gps': []}
        for info in self.gps_data:
            self.input_gps_stream.add_item(info)
            gps_dict['all_gps'].append(info)
        return gps_dict
