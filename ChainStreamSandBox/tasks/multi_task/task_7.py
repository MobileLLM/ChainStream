from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
import time
from ..task_tag import *

random.seed(6666)


class WaterFlowerTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_video_stream = None
        self.gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Living, Domain_Task_tag.Location]),
                                modality=str([Modality_Task_tag.Text, Modality_Task_tag.Video]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "all of my gps data",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str"
            }
        }, {
            "stream_id": "all_video",
            "description": "all video data in the balcony with plants",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "reminder",
                "description": "A reminder series for watering the flowers after a period of time if I am not at home ("
                               "home street address: 123 Main St), with every two copies of video data packaged into "
                               "a batch after determining the home street address from GPS data",
                "fields": {
                    "reminder": "You have not watered the flowers for a period of time. Please water the flowers."
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask7(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task7"):
        super().__init__(agent_id)
        self.video_input = cs.get_stream(self, "all_video")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.message_output = cs.get_stream(self, "reminder")
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

        def check_flower(three_person_data):
            data_list = three_person_data["item_list"]
            for data in data_list:
                prompt = "Please check if the flowers are watered.Simply answer y or n."
                res = self.llm.query(cs.llm.make_prompt(prompt,data["frame"]))
                if res.lower()== "n" :
                    self.message_output.add_item({
                        "reminder":"You have not watered the flowers for a period of time. Please water the flowers."
                    })
            return three_person_data
            
        self.video_input.for_each(check_place).batch(by_time=1).for_each(check_flower)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')
        self.output_message_stream = cs.stream.create_stream(self, 'reminder')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['reminder'].append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_gps': [], 'all_video': []}
        for frame in self.video_data:
            sent_info['all_video'].append(frame)
            time.sleep(2)
            self.input_video_stream.add_item({"frame": frame})
        for gps in self.gps_data:
            sent_info['all_gps'].append(gps)
            self.gps_stream.add_item(gps)
        return sent_info
