from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription


class OldWeatherTask5(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_weather_stream = None
        self.input_weather_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "A list of the weather information",
            "fields": {
                "Location": "The location of the zone,string",
                "Date_Time": "The time of the zone,string",
                "Temperature_C": "The temperature of the zone,float",
                "Humidity_pct": "The humidity percentage of the zone,float",
                "Precipitation_mm": "The precipitation of the zone,float",
                "Wind_Speed_kmh": "The wind speed of the zone,float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "weather_time",
                "description": "A list of the time of the zones",
                "fields": {
                    "location": "The location of the zone,string",
                    "time": "The time of the zone,string"
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
        self.output_stream = cs.get_stream(self,"weather_time")
    def start(self):
        def process_weather(weather):
            Location = weather["Location"]
            Date_Time = weather["Date_Time"]        
            self.output_stream.add_item({
                "location":Location,
                "time":Date_Time
            })
        self.input_stream.for_each(process_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'weather_time')
        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['weather_time'].append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        weather_dict = {'all_weather': []}
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)
            weather_dict['all_weather'].append(info)
        return weather_dict
