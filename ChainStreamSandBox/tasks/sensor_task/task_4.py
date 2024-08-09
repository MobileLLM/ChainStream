from ChainStreamSandBox.tasks.task_config_base import SingleAgentTaskConfigBase
import random
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData
from AgentGenerator.io_model import StreamListDescription

random.seed(6666)


class WeatherTask1(SingleAgentTaskConfigBase):
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
                "Date_Time": "the '%Y/%m/%d %H:%M:%S' datetime format, string",
                "Temperature_C": "temperature in degrees Celsius, float"
            }
        }])
        self.output_stream_description = StreamListDescription(streams=[
            {
                "stream_id": "clothing_recommendation",
                "description": "A list of the recommendations of the suitable clothing according to the temperature "
                               "in May,2024(every two copies of weather data are packaged as a batch after filtering "
                               "the weather in May,2024)",
                "fields": {
                    "temperature": "temperature in degrees Celsius,string",
                    "clothing": "the clothing recommended,string"
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
            if date.year == 2024 and date.month == 5:
                return weather
            return None  

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
        sent_weather = []
        for weather in self.sensor_data:
            sent_weather.append(weather)
            self.input_sensor_stream.add_item(weather)
        return sent_weather
