from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class GPSTask17(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_landmark_stream = None
        self.input_landmark_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Medium, domain=Domain_Task_tag.Location,
                                modality=Modality_Task_tag.GPS_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_landmarks",
            "description": "A stream of landmarks information",
            "fields": {
                "landmark_type": "The type of the landmark, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "same_type_landmarks",
                "description": "A stream of the landmarks grouped by the specific type of them with each six items "
                               "grouped as a batch.",
                "fields": {
                    "type": "The specific type of the landmark, string",
                    "names": "The list of the names of the properties grouped by the same type, list"}
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
        self.output_stream = cs.create_stream(self,"same_type_landmarks")
        self.llm = get_model("Text")
    def start(self):
        def grouped_landmark_type(landmark):
            landmark_list = landmark['item_list']
            type_group = {}
            for building in landmark_list:
                if building['PrimaryPropertyType'] not in type_group:
                    type_group[building['PrimaryPropertyType']] = [building['PropertyName']]
                else:
                    type_group[building['PrimaryPropertyType']].append(building['PropertyName'])
            self.output_stream.add_item({
                'type': building['PrimaryPropertyType'],
                'names': list(type_group.values())
            })
            return list(type_group.values())
        self.input_stream.batch(by_count=6).for_each(grouped_landmark_type)
        '''

    def init_environment(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream(self, 'all_landmarks')
        self.output_landmark_stream = cs.stream.create_stream(self, 'same_type_landmarks')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['same_type_landmarks'].append(data)

        self.output_landmark_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_landmark_stream = cs.stream.create_stream(self, 'all_landmarks')

    def init_output_stream(self, runtime):
        self.output_landmark_stream = cs.stream.get_stream(self, 'same_type_landmarks')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['same_type_landmarks'].append(data)

        self.output_landmark_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        gps_dict = {'all_landmarks': []}
        for info in self.landmark_data:
            self.input_landmark_stream.add_item(info)
            gps_dict['all_landmarks'].append(info)
        return gps_dict
