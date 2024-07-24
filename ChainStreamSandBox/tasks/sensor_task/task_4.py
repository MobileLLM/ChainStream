from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class WeatherTask1(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=20, eos_gap=4):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None

        self.eos_gap = eos_gap
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Date_Time": "date xxx, string",
                "Temperature_C": "temp xxx, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "clothing_recommendation",
                "description": "Recommend the suitable clothing according to the temperature this month(May)",
                "fields": {
                    "temperature":"xxx,string",
                    "clothing":"xxx,string"
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs
import pandas as pd

class AgentExampleForSensorTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_1"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "clothing_recommendation")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_date(weather):
            date_str = weather.get('Date_Time')
            date = pd.to_datetime(date_str, format='%Y/%m/%d %H:%M:%S', errors='coerce')
            if pd.isna(date):
                return None
            if date.year == 2024 and date.month == 5:
                return weather

        def recommend_clothing(weather_list):
            for weather in weather_list['item_list']:
                temperature = weather.get('Temperature_C')
                if temperature is not None:
                    prompt = "Recommend the suitable clothing today according to the temperature."
                    res = self.llm.query(cs.llm.make_prompt(str(temperature), prompt))
                    self.sensor_output.add_item({
                        "temperature": temperature,
                        "clothing": res
                    })
        self.sensor_input.for_each(filter_date).batch(by_count=2).for_each(recommend_clothing)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'clothing_recommendation')

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






