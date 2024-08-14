from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData


class OldGPSTask4(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_gps_stream = None
        self.input_gps_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_gps' and process the values corresponding to the 'CapitalName' key in the gps dictionary: "
            "Add the gps capital name to the output stream 'cs_gps'."
        )
        self.gps_data = GPSData().get_gps(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_gps_agent")
        self.input_stream = cs.get_stream(self,"all_gps")
        self.output_stream = cs.get_stream(self,"cs_gps")
        self.llm = get_model("Text")
    def start(self):
        def process_gps(gps):
            gps_capital = gps["CapitalName"]        
            self.output_stream.add_item(gps_capital)
        self.input_stream.for_each(process_gps)

        '''

    def init_environment(self, runtime):
        self.input_gps_stream = cs.stream.create_stream(self,'all_gps')
        self.output_gps_stream = cs.stream.create_stream(self,'cs_gps')
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

