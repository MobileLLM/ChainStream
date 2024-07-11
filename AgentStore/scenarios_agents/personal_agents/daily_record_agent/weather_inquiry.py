import pandas as pd
import requests
import chainstream as cs
from chainstream.runtime.stream_manager import StreamManager

class AMAPWeatherAgent(cs.agent.Agent):
    """
    A simple agent that retrieves weather information based on location input
    """
    def __init__(self, agent_id="weather_agent", stream_id="my_weather_stream"):
        super().__init__(agent_id)
        self._source =  StreamManager()  # instance of Stream
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)
        self.stream_id = stream_id
        self.url = 'https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={key}'
        self.city_df = pd.read_excel(
            'https://modelscope.oss-cn-beijing.aliyuncs.com/resource/agent/AMap_adcode_citycode.xlsx'
        )
        self.token = '6e68f4f5b914d5735d04d9726a3b4cfc'
        assert self.token != '', 'weather api token must be acquired through ' \
            'https://lbs.amap.com/api/webservice/guide/create-project/get-key and set by AMAP_TOKEN'
        self._source.register_stream(self.stream_id, self)  # Pass self as the stream argument

    def start(self):
        def handle_input(location):
            weather_info = self.get_weather_info(location)
            self.result_buffer.save(weather_info)

        try:
            self._source.for_each(self, handle_input)
            return True
        except Exception as e:
            print("Error in Weather Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)

    def get_city_adcode(self, city_name):
        filtered_df = self.city_df[self.city_df['中文名'] == city_name]
        if len(filtered_df['adcode'].values) == 0:
            raise ValueError(
                f'location {city_name} not found, availables are {self.city_df["中文名"]}'
            )
        else:
            return filtered_df['adcode'].values[0]

    def call(self, location: str) -> str:
        city_adcode = self.get_city_adcode(location)
        response = requests.get(self.url.format(city=city_adcode, key=self.token))
        data = response.json()
        if data['status'] == '0':
            raise RuntimeError(data)
        else:
            weather = data['lives'][0]['weather']
            temperature = data['lives'][0]['temperature']
            return f'{location}的天气是{weather},温度是{temperature}度。'

def main():
    weather_tool = AMAPWeatherAgent(agent_id="amap_weather_agent", stream_id="my_weather_stream")
    location = '海淀区'
    weather_info = weather_tool.call(location)
    print(weather_info)

if __name__ == "__main__":
    main()
