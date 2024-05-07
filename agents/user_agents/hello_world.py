import chainstream as cs


@cs.agent.AgentDoc(name="Hello Agent",
                   description="A simple agent that says hello to people in front camera",
                   memory=None,
                   stream=None
                   )
class HelloAgent(cs.agent.Agent):
    """
    A simple agent that says hello to people in front camera
    """

    is_agent = True

    def __init__(self, agent_id="hello_agent"):
        super().__init__(agent_id)
        self._source1 = cs.get_stream('socket_front_camera_video')  # instance of Stream
        self._llm = cs.llm.get_model('gpt-4-vision')
        self.new_stream = cs.stream.create_stream("name", "hello_agent")
        self.video_buffer = cs.context.VideoBuffer(duration=10)
        self.has_people = cs.create_stream('front_camera_has_people')
        self.doc = None

    def start(self):
        @cs.agent.StreamFuncDoc("function to handle new frame from front camera")
        def handle_new_frame(frame):
            self.video_buffer.save(frame)
            # prompt = cs.llm.make_prompt([frame, 'Is there a person in the image? Simply answer Yes or No'])
            prompt = 'Is there a person in the image? Simply answer Yes or No'
            response = self._llm.query(prompt, frame['frame']).lower().strip()
            print(response)
            if response.startswith('yes'):
                self.has_people.send_item({'message': 'hello', 'frame': frame})

        try:
            self._source1.register_listener(self, handle_new_frame)
        except Exception as e:
            print("Error in hello agent: ", e)
            return False
        # self._source1.register_listener(self, handle_new_frame)
        return True

    def pause(self):
        self._source1.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)
