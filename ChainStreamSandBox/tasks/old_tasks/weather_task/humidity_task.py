from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription


class OldWeatherTask1(SingleAgentTaskConfigBase):
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
                "stream_id": "humidity_percentage",
                "description": "A list of the humidity percentage of the zones",
                "fields": {
                    "humidity": "The humidity percentage of the zone,float",
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
        self.output_stream = cs.get_stream(self,"humidity_percentage")
    def start(self):
        def process_weather(weather):
            humidity = weather["Humidity_pct"]
            location = weather["Location"]
            time = weather["Date_Time"] 
            self.output_stream.add_item({
                "humidity":humidity,
                "location":location,
                "time":time
            })
        self.input_stream.for_each(process_weather)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_weather_stream = cs.stream.create_stream(self, 'humidity_percentage')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_weather_stream.for_each(record_output)

    def start_task(self, runtime):
        weather_list = []
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)
            weather_list.append(info)
        return weather_list
