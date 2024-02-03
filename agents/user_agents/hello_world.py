import chainstream as cs


class HelloAgent(cs.agent.Agent):
    """
    A simple agent that says hello to people in front camera
    """
    def __init__(self, agent_id):
        super().__init__(agent_id)
        self._source1 = cs.get_stream('front_camera_video_01')  # instance of Stream
        self._llm = cs.llm.get_model('gpt-4-vision')
        self.video_buffer = cs.context.VideoBuffer(duration=10)
        self.has_people = cs.create_stream('front_camera_has_people')

    def start(self):
        def handle_new_frame(frame):
            self.video_buffer.save(frame)
            prompt = cs.llm.make_prompt([frame, 'Is there a person in the image? Simply answer Yes or No'])
            response = self._llm.query(prompt).lower().strip()
            if response.startswith('yes'):
                self.has_people.send_item({'message': 'hello', 'frame': frame})
        self._source1.register_listener(handle_new_frame)

    def pause(self):
        self._source1.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)

