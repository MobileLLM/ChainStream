from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class OldWeatherTask6(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_weather_stream = None
        self.input_weather_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Living,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_wifi",
            "description": "A series of the wifi information",
            "fields": {
                "MAC.Address": "The mac address of the wifi signal, string",
                "Vendor": "The vendor of the wifi signal, string",
                "SSID": "The SSID of the wifi signal, string",
                "Signal": "The signal strength of the wifi signal, int",
                "Channel": "The channel of the wifi signal, int"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "weather_wind_speed",
                "description": "A series of the wind speed of the zones",
                "fields": {
                    "location": "The location of the zone, string",
                    "time": "The time of the zone, string",
                    "wind_speed": "The wind speed of the zone, float"
                }
            }
        ])
        self.weather_data = WeatherData().get_weather(10)
        self.agent_example = '''
import chainstream as cs
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_weather_agent")
        self.input_stream = cs.get_stream(self,"all_weather")
        self.output_stream = cs.get_stream(self,"weather_wind_speed")
    def start(self):
        def process_weather(weather):
            Wind_Speed_kmh = weather["Wind_Speed_kmh"]
            location = weather["Location"]
            time = weather["Date_Time"]                
            self.output_stream.add_item({
                "location": location,
                "time": time,
                "wind_speed": Wind_Speed_kmh
            })
        self.input_stream.for_each(process_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'weather_wind_speed')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_wind_speed'].append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        weather_dict = {'all_weather': []}
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)
            weather_dict['all_weather'].append(info)
        return weather_dict
