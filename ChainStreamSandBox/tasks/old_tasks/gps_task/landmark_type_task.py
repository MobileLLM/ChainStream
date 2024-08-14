from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData


class OldGPSTask14(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_landmarks' and process the values corresponding to the 'PrimaryPropertyType' key in the landmark dictionary: "
            "Add the primary property type of the buliding to the output stream 'cs_landmarks'."
        )
        self.landmark_data = LandmarkData().get_landmarks(10)
        self.agent_example = '''
import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_landmark_agent")
        self.input_stream = cs.get_stream(self,"all_landmarks")
        self.output_stream = cs.get_stream(self,"cs_landmarks")
        self.llm = get_model("Text")
    def start(self):
        def process_landmark(landmark):
            PrimaryPropertyType = landmark["PrimaryPropertyType"]        
            self.output_stream.add_item(PrimaryPropertyType)
        self.input_stream.for_each(process_landmark)

        '''
    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream(self, 'all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream(self, 'cs_landmarks')
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



