from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class WeatherTask2(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=20):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Humidity_pct": "the percentage of the humidity, float",
                "Date_Time": "the '%Y/%m/%d %H:%M:%S' datetime format, string"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "alarm_wet",
                "description": "A list of reminders when the relative humidity exceeds 70%(every two copies of "
                               "weather data are packaged as a batch after filtering the humidity percentage which is "
                               "over 70%)",
                "fields": {
                    "date_time": "the '%Y/%m/%d %H:%M:%S' datetime format, string",
                    "humidity": "the percentage of the humidity,string",
                    "reminder": "When walking on the road, pay attention to wet and slippery!"
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs
import pandas as pd

class AgentExampleForSensorTask5(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_5"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "alarm_wet")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_humidity(weather):
            humidity = weather['Humidity_pct']
            if humidity >= 70:
                return weather

        def reminder(weather_list):
            for weather in weather_list['item_list']:
                humidity = weather.get('Humidity_pct')
                date_time = weather.get('Date_Time')
                self.sensor_output.add_item({
                    "date_time": date_time,
                    "humidity": str(humidity)+"%",
                    "reminder": "When walking on the road, pay attention to wet and slippery!"
                })
        self.sensor_input.for_each(filter_humidity).batch(by_count=2).for_each(reminder)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'alarm_wet')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['alarm_wet'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_weather = {'all_weather': []}
        for weather in self.sensor_data:
            sent_weather['all_weather'].append(weather)
            self.input_sensor_stream.add_item(weather)
        return sent_weather
