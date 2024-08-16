from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription


class OldGPSTask1(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_landmarks",
            "description": "A list of landmarks information",
            "fields": {
                "Electricity(kWh)": "The electricity consumed by the landmark,float",
                "GHGEmissions(MetricTonsCO2e)": "The green house gas emissions by the landmark,float",
                "NaturalGas(therms)": "The natural gas emissions by the landmark,float",

            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "landmarks_electricity",
                "description": "A list of the calculation of the electricity consumed by the landmark",
                "fields": {
                    "electricity": "The electricity consumed by the landmark,float"}
            }
        ])
        self.landmark_data = LandmarkData().get_landmarks(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_landmark_agent")
        self.input_stream = cs.get_stream(self,"all_landmarks")
        self.output_stream = cs.get_stream(self,"landmarks_electricity")
        self.llm = get_model("Text")
    def start(self):
        def process_landmark(landmark):
            Electricity = landmark["Electricity(kWh)"]        
            self.output_stream.add_item({
                "electricity":Electricity
            })
        self.input_stream.for_each(process_landmark)
        '''

    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream(self, 'all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream(self, 'landmarks_electricity')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_landmark_stream.for_each(record_output)

    def start_task(self, runtime):
        gps_list = []
        for info in self.landmark_data:
            self.input_landmark_stream.add_item(info)
            gps_list.append(info)
        return gps_list
