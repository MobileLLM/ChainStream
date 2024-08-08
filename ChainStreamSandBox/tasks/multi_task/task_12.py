from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import GPSData
from ChainStreamSandBox.raw_data import Ego4DData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class ReadingLightTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.input_one_person_stream = None
        self.input_gps_stream = None
        self.input_light_stream = None
        self.adjust_light_stream = None
        self.is_reading_stream = None
        self.input_stream_description1 = StreamListDescription(streams=[{
            "stream_id": "all_one_person",
            "description": "one_person perspective data",
            "fields": {
                "frame": "image file in the Jpeg format processed using PIL,string"
            }
        }, {
            "stream_id": "all_gps",
            "description": "GPS data",
            "fields": {
                "Street Address": "the street address information from the gps sensor,str",
                "Navigation_endanger": "the detection of whether it is a dangerous road section,bool"
            }
        }, {
            "stream_id": "light_intensity",
            "description": "A real-time light_intensity check information,every two copies of light intensity data "
                           "are packaged as a batch",
            "fields": {
                "Light intensity outdoor": "the light intensity information outdoor right now,float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "adjust_light",
                "description": "A automatic command to adjust the light in the study",
                "fields": {
                    "Light intensity indoor": "the light intensity information indoor right now,float"
                }
            },
            {
                "stream_id": "is_reading",
                "description": "Check whether the person is reading or not,every two copies of video data are "
                               "packaged as a batch after judging the home street address gps data",
                "fields": {
                    "Status": "True or False"
                }
            }
        ])
        self.gps_data = GPSData().get_gps(number)
        self.video_data = Ego4DData().load_for_action()
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask12(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task12"):
        super().__init__(agent_id)
        self.gps_input = cs.get_stream(self, "all_gps")
        self.video_input = cs.get_stream(self, "all_one_person")
        self.command_output = cs.get_stream(self, "adjust_light")
        self.light_input = cs.get_stream(self, "light_intensity")
        self.is_reading = cs.get_stream(self, "is_reading")
        self.llm = cs.llm.get_model("image")
        self.video_buffer = Buffer()
    
    def start(self):
        def save_video(video_data):
            self.video_buffer.append(video_data)
        self.video_input.for_each(save_video)

        def check_light(light_inputs):
            light_input = light_inputs["item_list"]
            if self.is_reading == "True":
                for light in light_input:
                    prompt = "Do you think the light_intensity is enough for reading books?If not,tell me the best light intensity."
                    res = self.llm.query(cs.llm.make_prompt(prompt,light_input["Light intensity outdoor"]))
                    self.command_output.add_item({
                        "Light intensity indoor": res
                    })
        self.light_input.batch(by_count=2).for_each(check_light)
        
        def check_place(gps_data):
            if gps_data["Street Address"] == "123 Main St":
                one_person_data = self.video_buffer.pop_all()
                return one_person_data

        def check_reading(one_person_data):
            data_list = one_person_data["item_list"]
            prompt = "Please check whether I am reading books.Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,one_person_data))
            if res.lower()== "y" :
                self.is_reading.add_item({"Status":"True"})
                return one_person_data
            else:
                return None

        self.video_input.for_each(check_place).batch(by_count=2).for_each(check_reading)
        '''

    def init_environment(self, runtime):
        self.input_one_person_stream = cs.stream.create_stream(self, 'all_one_person')
        self.input_gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_light_stream = cs.stream.create_stream(self, 'light_intensity')
        self.adjust_light_stream = cs.stream.create_stream(self, 'adjust_light')
        self.is_reading_stream = cs.stream.create_stream(self, 'is_reading')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.adjust_light_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_info = []
        for frame in self.video_data:
            sent_info.append(frame)
            self.input_one_person_stream.add_item({"frame": frame})
        for gps in self.gps_data:
            sent_info.append(gps)
            self.input_gps_stream.add_item(gps)
        for _ in range(10):
            light_intensity = random.uniform(0, 1000)
            self.input_light_stream.add_item({"Light intensity outdoor": light_intensity})
        return sent_info
