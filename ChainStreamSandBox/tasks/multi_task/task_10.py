from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from ChainStreamSandBox.raw_data import SpharData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class RemindDriverTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.music_stream = None
        self.output_music_stream = None
        self.gps_stream = None
        self.car_check_stream = None
        self.is_tired_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=[Domain_Task_tag.Activity, Domain_Task_tag.Location],
                                scene=Scene_Task_tag.Traffic,
                                modality=[Modality_Task_tag.Text, Modality_Task_tag.Video])
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "GPS data for navigation of the driver",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str",
                "Navigation_endanger": "the detection of whether it is a dangerous road section,bool"
            }
        }, {
            "stream_id": "all_monitor",
            "description": "On-board driver surveillance camera",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }, {
            "stream_id": "music_data",
            "description": "All car disk music data",
            "fields": {
                "song_name": "the name of the song,string",
                "singer": "the singer of the song,string",
                "type": "the type of the song,string",
                "lyrics": "the lyrics of the song,string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "music_player",
                "description": "A rock n roll music player when the driver is tired in the dangerous road section("
                               "every two copies of music data are packaged as a batch after checking the status of "
                               "the driver and the road condition",
                "fields": {
                    "song_name": "the name of the song,string",
                    "singer": "the singer of the song,string",
                    "lyrics": "the lyrics of the song,string"
                }
            },
            {
                "stream_id": "is_tired",
                "description": "A check on whether the driver is tired or not",
                "fields": {
                    "Status": "True or False,bool"
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.video_data = SpharData().load_for_traffic()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask10(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task10"):
        super().__init__(agent_id)
        self.gps_input = cs.get_stream(self, "all_gps")
        self.monitor_input = cs.get_stream(self, "all_monitor")
        self.music_input = cs.get_stream(self, "music_data")
        self.music_output = cs.get_stream(self, "auto_play_music")
        self.music_buffer = Buffer()
        self.is_tired = cs.get_stream(self, "is_tired")
        self.llm = cs.llm.get_model("image")

    def start(self):
        def save_music(music_data):
            self.music_buffer.append(music_data)
        self.music_input.for_each(save_music)

        def check_danger(gps_data):
            if self.is_tired == "True":
                if gps_data["Navigation_endanger"] == "True":
                    music_data = self.music_buffer.pop_all()
                    return music_data

        def check_tiredness(three_person_data):
            prompt = "Is the driver tired? Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,three_person_data["frame"]))
            if res.lower() == "y":
                self.is_tired.add_item({"Status":"True"})
                return three_person_data
            else:
                return None
        
        def play_music(music_data):
            data_list = music_data["item_list"]
            for data in data_list:
                if data['type'] == "Rock N Roll":
                    self.music_output.add_item({
                        "song_name":data['song_name'],
                        "singer":data['singer'],
                        "lyrics":data['lyrics']
                    })
            return music_data

        self.monitor_input.for_each(check_tiredness).for_each(check_danger).batch(by_count=2).for_each(play_music)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.car_check_stream = cs.stream.create_stream(self, 'all_monitor')
        self.music_stream = cs.stream.create_stream(self, 'music_data')
        self.output_music_stream = cs.stream.create_stream(self, 'auto_play_music')
        self.is_tired_stream = cs.stream.create_stream(self, 'is_tired')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_play_music'].append(data)
            self.output_record['is_tired'].append(data)

        self.output_music_stream.for_each(record_output)
        self.is_tired_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_gps': [], 'all_monitor': []}
        for frame in self.video_data:
            sent_info['all_monitor'].append(frame)
            self.car_check_stream.add_item({"frame": frame})
        for gps in self.gps_data:
            sent_info['all_gps'].append(gps)
            self.gps_stream.add_item(gps)
        return sent_info


if __name__ == '__main__':
    from faker import Faker

    fake = Faker()
    task = RemindDriverTask()
    for _ in range(10):
        song_name = fake.word()
        singer = fake.name()
        lyrics = fake.text(max_nb_chars=100)
        task.music_stream.add_item({"song_name": song_name, "singer": singer, "lyrics": lyrics})
