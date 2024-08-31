from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription
from ..task_tag import *

random.seed(6666)


class WeatherTask1(SingleAgentTaskConfigBase):
    def __init__(self, sensor_number=20):
        super().__init__()
        self.output_record = None
        self.clock_stream = None
        self.output_sensor_stream = None
        self.input_sensor_stream = None
        self.task_tag = TaskTag(difficulty=Difficulty_Task_tag.Hard, domain=Domain_Task_tag.Weather,
                                modality=Modality_Task_tag.Weather_Sensor)
        self.input_stream_description = StreamListDescription(streams=[{
            "stream_id": "all_weather",
            "description": "All weather information",
            "fields": {
                "Date_Time": "The time of the zone with the format of '%Y/%m/%d %H:%M', datetime",
                "Temperature_C": "temperature in degrees Celsius, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "clothing_recommendation",
                "description": "A stream of the recommendations of the suitable clothing according to the temperature "
                               "in May each year,with every two copies of weather data packaged as a batch after "
                               "filtering the weather in May each year chosen from ['T-shirt', 'Tank top', 'Sweater', "
                               "'Hoodie', 'Jacket']",
                "fields": {
                    "Temperature_C": "temperature in degrees Celsius, string",
                    "clothing": "the clothing recommended chosen from ['T-shirt', 'Tank top', 'Sweater', 'Hoodie', "
                                "'Jacket'], string "
                }
            }
        ])

        self.sensor_data = WeatherData().get_weather(sensor_number)
        self.agent_example = '''
import chainstream as cs
from datetime import datetime
class AgentExampleForSensorTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_1"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "clothing_recommendation")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_date(weather):
            date_str = weather.get('Date_Time')
            date = datetime.strptime(date_str, '%Y/%m/%d %H:%M')
            if date.month == 5:
                return weather
            return None  

        def recommend_clothing(weather_list):
            for weather in weather_list['item_list']:
                temperature = weather.get('Temperature_C')
                if temperature is not None:
                    prompt = "Recommend the suitable clothing today according to the temperature chosen from ['T-shirt', 'Tank top', 'Sweater', 'Hoodie', 'Jacket']."
                    res = self.llm.query(cs.llm.make_prompt(str(temperature), prompt))
                    self.sensor_output.add_item({
                        "Temperature_C": temperature,
                        "clothing": res
                    })
        self.sensor_input.for_each(filter_date).batch(by_count=2).for_each(recommend_clothing)
        '''

    def init_environment(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')
        self.output_sensor_stream = cs.stream.create_stream(self, 'clothing_recommendation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['clothing_recommendation'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def init_input_stream(self, runtime):
        self.input_sensor_stream = cs.stream.create_stream(self, 'all_weather')

    def init_output_stream(self, runtime):
        self.output_sensor_stream = cs.stream.get_stream(self, 'clothing_recommendation')

        self.output_record = {x.stream_id: [] for x in self.output_stream_description.streams}

        def record_output(data):
            self.output_record['clothing_recommendation'].append(data)

        self.output_sensor_stream.for_each(record_output)

    def start_task(self, runtime) -> dict:
        sent_weather = {'all_weather': []}
        for weather in self.sensor_data:
            sent_weather['all_weather'].append(weather)
            self.input_sensor_stream.add_item(weather)
        return sent_weather
