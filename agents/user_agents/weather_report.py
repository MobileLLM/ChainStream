import chainstream as cs


class WeatherReport(cs.agent.Agent):
    """
       A simple agent that displays local weather information on front camera when user asks
    """
    def __init__(self):
        self._source1 = cs.get_stream('front_camera_video_01')
        self._source2 = cs.get_stream('microphone')
        self._source3 = cs.get_stream('position')
        self.get_weather_info = cs.tools.access_Internet.SearchEngine('location', 'weather')
        self._llm = cs.llm.get_llm('ChatGPT')
        self.video_buffer = cs.context.VideoBuffer(duration=10)
        self.audio_buffer = cs.context.AudioBuffer(duration=10)
        self.position_buffer = cs.context.TextBuffer()
        self.asking_weather = cs.create_stream('user_asking_weather')

    def start(self):
        def handle_new_frame(frame):
            self.video_buffer.save(frame)

        def handle_new_position(position):
            self.position_buffer.save(position)

        def search_weather():
            self.weather_info_list = self.get_weather_info.split()      # [temperature, weather, ...]

        def handle_new_audio(audio):
            self.audio_buffer.save(audio)
            prompt = cs.llm.make_prompt([self.audio_buffer, 'is user asking about weather? Simply answer Yes or No'])
            response = self._llm.query(prompt)      # detect whether user is asking about the weather with LLM
            is_asking = cs.llm.parse_response(response, ['Yes', 'No']) == 'Yes'
            if is_asking:  # if detected, create a new event to the 'user_asking_weather' stream
                self.asking_weather.send_item({'message': self.weather_info_list, 'frame': self.video_buffer})

        self._source1.register_listener(self, handle_new_frame)
        self._source2.register_listener(self, handle_new_audio)
        self._source3.register_listener(self, handle_new_position)
        self.asking_weather.register_listener(self, search_weather)

    def pause(self):
        self._source1.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)
