from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class WeatherTask4(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=40):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Wind_Speed_kmh": "the wind speed sensor in kmh, float",
                "Date_Time": "the '%Y/%m/%d %H:%M:%S' datetime format, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "take_clothes_down",
                "description": "A list of reminders to take down clothes in the balcony if the wind speed is over 20 "
                               "kmh",
                "fields": {
                    "date_time": "the '%Y/%m/%d %H:%M:%S' datetime format, string",
                    "wind_speed_kmh": "the wind speed sensor in kmh, float",
                    "reminder": "Collect the clothes in the balcony!"
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs

class AgentExampleForSensorTask7(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_6"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "take_clothes_down")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_precipitation(weather):
            wind_speed = weather['Wind_Speed_kmh']
            if wind_speed >= 20:
                return weather

        def reminder(weather_list):
            for weather in weather_list['item_list']:
                wind_speed = weather.get('Wind_Speed_kmh')
                date_time = weather.get('Date_Time')
                self.sensor_output.add_item({
                    "date_time": date_time,
                    "wind_speed": str(wind_speed)+"km/h",
                    "reminder": "Collect the clothes in the balcony!"
                })
        self.sensor_input.for_each(filter_precipitation).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'take_clothes_down')

        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> list:
        sent_messages = []
        for message in self.sensor_data:
            sent_messages.append(message)
            self.input_sensor_stream.add_item(message)
        return sent_messages
