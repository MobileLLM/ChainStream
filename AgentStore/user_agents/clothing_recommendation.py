import chainstream as cs


class ClothingRecommendation(cs.agent.Agent):
    """
       每天早上当用户醒来后，结合用户今天的日程内容和当地的天气情况给用户推荐衣物
    """
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self._source2 = cs.get_stream('schedule_stream')
        self._source1 = cs.get_stream('weather_stream')
        self._source3 = cs.get_stream('wakeup_stream')          # wakeup stream，由一个专门负责检测起床的 agent 来发布事件
        self._llm = cs.llm.get_model('ChatGPT')
        self.schedule_buffer = cs.context.TextBuffer()  # TODO
        self.weather_buffer = cs.context.TextBuffer()   # TODO
        self.wakeup_buffer = cs.context.TextBuffer()    # TODO
        self.send_recommend_info = cs.action.message_reminder() # TODO
        self.clothing_recommendation = cs.create_stream('clothing_recommendation')

    def start(self):

        def handle_new_schedule(schedule):
            self.schedule_buffer.save(schedule)

        def handle_new_weather(weather):
            self.weather_buffer.save(weather)

        def handle_new_wakeup(wakeup):
            self.wakeup_buffer.save(wakeup)
            prompt = cs.llm.make_prompt([self.schedule_buffer, self.weather_buffer, 'clothes recommended to wear'])
            response = self._llm.query(prompt)  #
            self.send_recommend_info({'message': response})

        self._source1.for_each(self, handle_new_weather)
        self._source2.for_each(self, handle_new_schedule)
        self._source3.for_each(self, handle_new_wakeup)

    def pause(self):
        self._source1.pause_listener(self)
        self._source2.pause_listener(self)
        self._source3.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)
        self._source2.remove_listener(self)
        self._source3.remove_listener(self)
