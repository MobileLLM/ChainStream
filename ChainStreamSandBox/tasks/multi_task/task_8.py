from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from ChainStreamSandBox.raw_data import LandmarkData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class KitchenSafetyTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_warning_stream = None
        self.input_video_stream = None
        self.gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Living, Domain_Task_tag.Location]),
                                modality=str([Modality_Task_tag.Text, Modality_Task_tag.Video]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_video",
            "description": "all video data in my kitchen",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }, {
            "stream_id": "all_gps",
            "description": "all of my gps data",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "alarm_message",
                "description": "An alarm message series when the gas stove is turned on but no one is there(home "
                               "street address:123 Main St), with every two copies of video data are packaged as a "
                               "batch after judging not the home street address from gps data",
                "fields": {
                    "alarm": "You have not turned off the stove.Please notice!"
                }
            }
        ])
        self.location_data = LandmarkData().get_landmarks(number)
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask8(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task8"):
        super().__init__(agent_id)
        self.video_input = cs.get_stream(self, "all_video")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.message_output = cs.get_stream(self, "alarm_message")
        self.video_buffer = Buffer()
        self.llm = cs.llm.get_model("image")

    def start(self):
        def save_video(video_data):
            self.video_buffer.append(video_data)
        self.video_input.for_each(save_video)

        def check_place(gps_data):
            if gps_data["Street Address"] != "123 Main St":
                three_person_data = self.video_buffer.pop_all()
            return three_person_data

        def check_stove(three_person_data):
            frames = three_person_data["frame"]
            for frame in frames:
                prompt = "Please assess if there is any risk with the gas stove.Simply answer y or n."
                res = self.llm.query(cs.llm.make_prompt(prompt,frame))
                if res.lower()== "n" :
                    self.message_output.add_item({
                        "alarm":"Your gas stove is safe right now."
                    })
            return three_person_data

        self.gps_input.for_each(check_place).for_each(check_stove)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')
        self.output_warning_stream = cs.stream.create_stream(self, 'alarm_message')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['alarm_message'].append(data)

        self.output_warning_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')

    def init_output_stream(self, runtime):
        self.output_warning_stream = cs.stream.get_stream(self, 'alarm_message')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['alarm_message'].append(data)

        self.output_warning_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_gps': [], 'all_video': []}
        for frame in self.video_data:
            sent_info['all_video'].append(frame)
            self.input_video_stream.add_item({"frame": frame})
        for gps in self.location_data:
            sent_info['all_gps'].append(gps)
            self.gps_stream.add_item(gps)
        return sent_info
