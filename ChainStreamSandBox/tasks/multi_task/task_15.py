from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from ChainStreamSandBox.raw_data import DesktopData
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class TripMusicTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_music_stream = None
        self.gps_stream = None
        self.input_screenshot_stream = None
        self.is_travel_stream = None
        self.scene_stream = None
        self.is_listening_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "all of my GPS data",
            "fields": {
                "Street Address": "the street address information from the gps sensor,string",
                "Location Properties": "the property of the location,string"
            }
        }, {
            "stream_id": "all_screenshot",
            "description": "all of my cellphone screenshot",
            "fields": {
                "image_file": "image file in the Jpeg format processed using PIL,string"
            }
        },
            {
                "stream_id": "all_scene",
                "description": "all scene recorded outside the car",
                "fields": {
                    "frame": "image file in the Jpeg format processed using PIL,string"
                }
            }
        ])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "music_player",
                "description": "An intelligent music player that recommend music according to the scene",
                "fields": {
                    "Music": "the recommend music,string"
                }
            },
            {
                "stream_id": "is_travel",
                "description": "A trigger when the person is in a trip",
                "fields": {
                    "Status": "True or False"
                }
            },
            {
                "stream_id": "is_listening",
                "description": "A trigger when the person is listening to music",
                "fields": {
                    "Status": "True or False"
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.screenshot_data = DesktopData().get_random_sample()
        self.scene_data = SpharData().load_for_person_detection()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask10(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task10"):
        super().__init__(agent_id)
        self.gps_input = cs.get_stream(self, "all_gps")
        self.screenshot_input = cs.get_stream(self, "all_screenshot")
        self.music_output = cs.get_stream(self, "auto_play_music")
        self.scene_input = cs.get_stream(self, "all_scene")
        self.music_buffer = Buffer()
        self.llm = cs.llm.get_model("image")
        self.is_travel = cs.get_stream(self, "is_travel")
        self.is_listening = cs.get_stream(self, "is_listening")

    def start(self):
        def check_listening(ui_data):
            prompt = "Analyze whether I'm listening to music in an app from the screenshot.Simply answer y or n"
            res = self.llm.query(cs.llm.make_prompt(prompt,ui_data['image_file']))
            if res.lower() == "y":
                self.is_listening.add_item({"Status":"True"})
                return ui_data
        self.screenshot_input.for_each(check_listening)
        
        def check_place(gps_data):
            if gps_data["Location Properties"] == "Travel":
                self.is_travel.add_item({"Status":"True"})
                return gps_data
        self.gps_input.for_each(check_place)
        
        def recommend_music(scene_input):
            if self.is_listening == "True" and self.is_travel == "True":
                prompt = "Recommend me a music that matches the current scene."
                res = self.llm.query(cs.llm.make_prompt(prompt,scene_input))
                self.music_output.add_item({
                    "Music":res
                })
            return scene_input
        self.scene_input.for_each(recommend_music)


        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_screenshot_stream = cs.stream.create_stream(self, 'all_screenshot')
        self.output_music_stream = cs.stream.create_stream(self, 'auto_play_music')
        self.is_travel_stream = cs.stream.create_stream(self, 'is_travel')
        self.scene_stream = cs.stream.create_stream(self, 'all_scene')
        self.is_listening_stream = cs.stream.create_stream(self, 'is_listening')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_music_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_info = []
        for frame in self.screenshot_data:
            sent_info.append(frame)
            self.input_screenshot_stream.add_item(frame)
        for gps in self.gps_data:
            sent_info.append(gps)
            self.gps_stream.add_item(gps)
        for frame in self.scene_data:
            sent_info.append(frame)
            self.scene_stream.add_item({"frame": frame})
        return sent_info
