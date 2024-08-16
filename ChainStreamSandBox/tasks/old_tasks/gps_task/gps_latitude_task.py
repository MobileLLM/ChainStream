from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription


class OldGPSTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_gps_stream = None
        self.input_gps_stream = None
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
                "stream_id": "gps_latitude",
                "description": "A list of the capital latitude extracted from the gps data",
                "fields": {
                    "gps_latitude": "The capital latitude of the location,float"}
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
        self.output_stream = cs.get_stream(self,"gps_latitude")
        self.llm = get_model("Text")
    def start(self):
        def process_gps(gps):
            # print(gps)
            gps_latitude = gps["CapitalLatitude"]
            print(gps_latitude)       
            self.output_stream.add_item({
                "gps_latitude":gps_latitude
            })
        self.input_stream.for_each(process_gps)
        '''

    def init_environment(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.output_gps_stream = cs.stream.create_stream(self, 'gps_latitude')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_gps_stream.for_each(record_output)

    def start_task(self, runtime):
        gps_list = []
        for info in self.gps_data:
            self.input_gps_stream.add_item(info)
            gps_list.append(info)
        return gps_list
