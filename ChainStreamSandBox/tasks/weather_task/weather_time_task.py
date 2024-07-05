from ..task_config_base import SingleAgentTaskConfigBase
import chainstream as cs
from ChainStreamSandBox.raw_data import WeatherData


class WeatherTimeConfig(SingleAgentTaskConfigBase):
    def __init__(self):
        super().__init__()
        self.output_record = None
        self.output_weather_stream = None
        self.input_weather_stream = None
        self.task_description = (
            "Retrieve data from the input stream 'all_weather' and process the values corresponding to the "
            "'Date_Time' key in the weather dictionary: Add the time information to the output stream "
            "'cs_weather'. "
        )
        self.weather_data = WeatherData().get_weather(10)
        self.agent_example = '''
        import chainstream as cs
        class testAgent(cs.agent.Agent):
            def __init__(self):
                super().__init__("test_weather_agent")
                self.input_stream = cs.get_stream("all_weather")
                self.output_stream = cs.get_stream("cs_weather")
            def start(self):
                def process_weather(weather):
                    Date_Time = weather["Date_Time"]        
                    self.output_stream.add_item(Date_Time)
                self.input_stream.register_listener(self, process_weather)

            def stop(self):
                self.input_stream.unregister_listener(self)
        '''

    def init_environment(self, runtime):
        self.input_weather_stream = cs.stream.create_stream('all_weather')
        self.output_weather_stream = cs.stream.create_stream('cs_weather')
        self.output_record = []

        def record_output(data):
            self.output_record.append(data)

        self.output_weather_stream.register_listener(self, record_output)

    def start_task(self, runtime):
        for info in self.weather_data:
            self.input_weather_stream.add_item(info)


if __name__ == '__main__':
    config = WeatherTimeConfig()
