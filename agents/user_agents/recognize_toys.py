import chainstream as cs


class ToyRecognitionAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='toy_recognition_agent'):
        super().__init__(agent_id)
        self._source = cs.get_stream('socket_front_camera_video')
        self.know_toy = cs.memory.fetch('known_toy')['name', 'img']
        self._llm = cs.llm.get_model('gpt-4-vision')
        self.video_buffer = cs.context.VideoBuffer(duration=10)

        self.has_toy = cs.create_stream('has_toy')

    def start(self):
        def handle_new_frame(frame):
            self.video_buffer.save(frame['frame'])
            prompt = "Is there a toy in the frame? Simply answer Yes or No"
            img = self.video_buffer.snapshot()
            response = self._llm.query(prompt, img).lower().strip()
            print(response)
            if response.startswith('yes'):
                self.has_toy.send_item({'video_frame': img})

        def recognize_toy(has_toy):
            now_toy_frame = has_toy['video_frame']
            imgs = [now_toy_frame]
            names = ""
            for name, img in self.know_toy.items():
                imgs.append(img)
                if len(imgs) == 1:
                    names += name
                elif len(imgs) == len(self.know_toy):
                    names += " ,and " + name
                else:
                    names += ", " + name

            prompt = (f"Is there a toy in the first picture that I already recognize? If so, please answer yes first, "
                      f"and then tell me the names I gave them. The last few pictures are all the toys I know, "
                      f"and I named them {names}. Please note that I only recognize the toys shown except for the "
                      f"first picture. You cannot answer yes to a toy that is not on display even if you know the "
                      f"toy. And the names you answer must also correspond to the names I chose, even though these "
                      f"names may be strange or even inconsistent with common cognition.")

            response = self._llm.query(prompt, imgs)
            print(response)

        self._source.register_listener(self, handle_new_frame)
        # self.has_toy.register_listener(recognize_toy)

        return True

    def pause(self):
        self._source.unregister_listener(self)

    def stop(self):
        self._source.remove_listener(self)
