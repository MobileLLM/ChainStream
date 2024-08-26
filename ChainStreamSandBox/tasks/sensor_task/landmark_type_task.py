from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class OldGPSTask14(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Location,
                                modality=Modality_Task_tag.GPS_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_landmarks",
            "description": "A list of landmarks information",
            "fields": {
                "NumberofFloors": "The number of the floors in the landmark, int",
                "Street Address": "The street address of the landmark, string",
                "PropertyName": "The property name of the landmark, string",
                "Neighborhood": "The neighborhood of the landmark, string",
                "YearBuilt": "The construction time of the landmark, string",
                "landmark_type": "The type of the landmark, string",
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "landmarks_type",
                "description": "A list of the type of the landmarks",
                "fields": {
                    "landmark_type": "The type of the landmark, string"}
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
        self.output_stream = cs.get_stream(self,"landmarks_type")
        self.llm = get_model("Text")
    def start(self):
        def process_landmark(landmark):
            PrimaryPropertyType = landmark["PrimaryPropertyType"]        
            self.output_stream.add_item({
                "landmark_type": PrimaryPropertyType
            })
        self.input_stream.for_each(process_landmark)

        '''

    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream(self, 'all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream(self, 'landmarks_type')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['landmarks_type'].append(data)

        self.output_landmark_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        gps_dict = {'all_landmarks': []}
        for info in self.landmark_data:
            self.input_landmark_stream.add_item(info)
            gps_dict['all_landmarks'].append(info)
        return gps_dict
