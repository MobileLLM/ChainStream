from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import LandmarkData
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class CloseWindowTask(SingleAgentTaskConfigBase):
    def __init__(self, number=10):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_action_stream = None
        self.input_weather_stream = None
        self.gps_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard,
                                domain=str([Domain_Task_tag.Living, Domain_Task_tag.Weather]),
                                modality=str([Modality_Task_tag.GPS_Sensor, Modality_Task_tag.Weather_Sensor]))
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_gps",
            "description": "all of my gps data",
            "fields": {
                "PropertyName": "the property name in my gps data, string"
            }
        }, {
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Humidity_pct": "the humidity percentage right now, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "auto_close_window",
                "description": "A stream of commands of automatically closing the window when the humidity percentage "
                               "is over 60 but no one is home(home property name:'Maple Ridge Apartments'), with every "
                               "two copies of weather data packaged as a batch after judging the home street address "
                               "from gps data",
                "fields": {
                    "humidity": "humidity percentage, float",
                    "action": "An auto command, string = 'Close all the windows!'"
                }
            }
        ])
        self.landmark_data = LandmarkData().get_landmarks(number)
        self.weather_data = WeatherData().get_weather(number)
        self.agent_example = '''
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask9(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task9"):
        super().__init__(agent_id)
        self.weather_input = cs.get_stream(self, "all_weather")
        self.gps_input = cs.get_stream(self, "all_gps")
        self.action_output = cs.create_stream(self, "auto_close_window")
        self.weather_buffer = Buffer()
        self.llm = cs.llm.get_model("text")

    def start(self):
        def save_weather(weather_data):
            self.weather_buffer.append(weather_data)
        self.weather_input.for_each(save_weather)

        def check_place(gps_data):
            if gps_data['PropertyName'] != "Maple Ridge Apartments":
                weather_data = self.weather_buffer.pop_all()
                return weather_data

        def close_window(weather_data):
            data_list = weather_data["item_list"]
            for data in data_list:
                if data['Humidity_pct'] >= 60:
                    self.action_output.add_item({
                        'humidity': data['Humidity_pct'],
                        "action":"Close all the windows!"
                    })
            return weather_data

        self.gps_input.for_each(check_place).batch(by_count=2).for_each(close_window)
        '''

    def init_environment(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_action_stream = cs.stream.create_stream(self, 'auto_close_window')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_close_window'].append(data)

        self.output_action_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.gps_stream = cs.stream.create_stream(self, 'all_gps')
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_action_stream = cs.stream.get_stream(self, 'auto_close_window')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['auto_close_window'].append(data)

        self.output_action_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_info = {'all_gps': [], 'all_weather': []}
        for weather in self.weather_data:
            sent_info['all_weather'].append(weather)
            self.input_weather_stream.add_item(weather)
        for landmark in self.landmark_data:
            sent_info['all_gps'].append(landmark)
            self.gps_stream.add_item(landmark)
        return sent_info
