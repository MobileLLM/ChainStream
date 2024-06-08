import chainstream as cs


class CaptionAgent(cs.agent.Agent):
    """
    A simple agent that says hello to people in front camera
    """

    is_agent = True
    def __init__(self, agent_id="hello_agent"):
        super().__init__(agent_id)
        self._source1 = cs.get_stream()  # instance of Stream
        self._llm = cs.llm.get_model('gpt-4-vision')
        self.text_buffer = cs.context.TextBuffer(max_text_num=1024)

    def start(self):
        def handle_new_image(image):
            # prompt = cs.llm.make_prompt([frame, 'Is there a person in the image? Simply answer Yes or No'])
            prompt = '请描述这张图片'
            response = self._llm.query(prompt, image['frame']).lower().strip()
            self.text_buffer.save(response)
        try:
            self._source1.register_listener(self, handle_new_image)
        except Exception as e:
            print("Error in image caption agent: ", e)
            return False
        # self._source1.register_listener(self, handle_new_frame)
        return True

    def pause(self):
        self._source1.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)

