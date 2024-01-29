import chainstream as cs


class ClothingRecommendation(cs.agent.Agent):
    """
       每天早上结合用户今天的日程内容和当地的天气情况给用户推荐衣物
       包括查找天气、读取日程、推荐衣服 
    """
    def __init__(self):
        self._source2 = cs.get_stream('schedule_stream')
        self._source1 = cs.get_stream('weather_stream')
        self._llm = cs.llm.get_llm('ChatGPT')
        self.schedule_buffer = cs.context.TextBuffer()
        self.weather_buffer = cs.context.TextBuffer()
        self.send_recommend_info = cs.action.timed_reminder()
        self.clothing_recommendation = cs.create_stream('clothing_recommendation')

    def start(self):

        def handle_new_schedule(schedule):
            self.schedule_buffer.save(schedule)

        def handle_new_weather(weather):
            self.weather_buffer.save(weather)
            prompt = cs.llm.make_prompt([self.schedule_buffer, self.weather_buffer, 'clothes recommended to wear'])
            response = self._llm.query(prompt)      #
            self.send_recommend_info({'message': response, 'time': '7:00,AM'})

        self._source1.register_listener(self, handle_new_weather)
        self._source2.register_listener(self, handle_new_schedule)

    def pause(self):
        self._source1.pause_listener(self)
        self._source2.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)
        self._source2.remove_listener(self)
