from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import SpharData
from ChainStreamSandBox.raw_data import GPSData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class CatFoodTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_message_stream = None
        self.input_video_stream = None
        self.gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Home, Domain_Task_tag.Location]),
                                modality=str([Modality_Task_tag.Text, Modality_Task_tag.Video]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_location",
            "description": "all of my gps data",
            "fields": {
                "Street Address": "the street address information from the gps sensor, string"
            }
        }, {
            "stream_id": "all_video",
            "description": "all video data in the cat room",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "cat_food_reminder",
                "description": "A reminder stream for refilling the cat food if the bowl is empty when I am not at "
                               "home (home street address: 123 Main St), with every two copies of video data packaged "
                               "into a batch after determining the home street address from GPS data",
                "fields": {
                    "reminder": "There is no cat food already. Please refill it."
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask6(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task6"):
        super().__init__(agent_id)
        self.video_input = cs.get_stream(self, "all_video")
        self.gps_input = cs.get_stream(self, "all_location")
        self.message_output = cs.create_stream(self, "cat_food_reminder")
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
        
        def check_cat(three_person_data):
            data_list = three_person_data["item_list"]
            for data in data_list:
                prompt = "Please check if there is any cat food left in the cat bowl.Simply answer y or n."
                res = self.llm.query(cs.llm.make_prompt(prompt,data["frame"]))
                if res.lower()== "n" :
                    self.message_output.add_item({
                        "reminder":"There is no cat food already. Please refill it."
                    })
            return three_person_data

        self.video_input.for_each(check_place).batch(by_count=2).for_each(check_cat)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_location')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')
        self.output_message_stream = cs.stream.create_stream(self, 'cat_food_reminder')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['cat_food_reminder'].append(data)

        self.output_message_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_location')
        self.input_video_stream = cs.stream.create_stream(self, 'all_video')

    def init_output_stream(self, runtime):
        self.output_message_stream = cs.stream.get_stream(self, 'cat_food_reminder')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['cat_food_reminder'].append(data)

        self.output_message_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_location': [], 'all_video': []}
        for frame in self.video_data:
            sent_info['all_video'].append(frame)
            self.input_video_stream.add_item({"frame": frame})
        for gps in self.gps_data:
            sent_info['all_location'].append(gps)
            self.gps_stream.add_item(gps)
        return sent_info
