from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *


class WeatherTask7(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_weather_stream = None
        self.input_weather_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Easy, domain=Domain_Task_tag.Weather,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "A stream of the weather information",
            "fields": {
                "Location": "The location of the zone, string",
                "Date_Time": "The time of the zone with the format of '%Y/%m/%d %H:%M', datetime",
                "Temperature_C": "The temperature of the zone, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "weather_temperature",
                "description": "A stream of the temperature of the zones which is over 30 degree",
                "fields": {
                    "temperature_over_30": "The temperature of the zone which is over 30, float",
                    "Location": "The location of the zone, string",
                    "Date_Time": "The time of the zone with the format of '%Y/%m/%d %H:%M', datetime"
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
        self.output_stream = cs.create_stream(self,"weather_temperature")
    def start(self):
        def process_weather(weather):
            Temperature_C = weather["Temperature_C"]
            location = weather["Location"]
            time = weather["Date_Time"]
            if Temperature_C > 30:    
                self.output_stream.add_item({
                    "temperature_over_30": Temperature_C,
                    "Location": location,
                    "Date_Time": time
                })
        self.input_stream.for_each(process_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'temperature_over_30')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['temperature_over_30'].append(data)

        self.output_weather_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_weather_stream = cs.stream.get_stream(self, 'temperature_over_30')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['temperature_over_30'].append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        weather_dict = {'all_weather': []}
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)
            weather_dict['all_weather'].append(info)
        return weather_dict
