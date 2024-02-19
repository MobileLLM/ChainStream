import chainstream as cs


class ToyRecognitionAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='toy_recognition_agent'):

        from ChainStreamTest.memory.recognize_toy_memory import set_toy_memory
        set_toy_memory()

        super().__init__(agent_id)
        self._source = cs.get_stream('socket_front_camera_video')
        self.know_toy = cs.memory.fetch('known_toy').select_keys(['name', 'img'])
        self._llm = cs.llm.get_model('gpt-4-vision')
        self.video_buffer = cs.context.VideoBuffer(duration=10)

        self.has_toy = cs.create_stream('has_toy')

    def start(self):
        def handle_new_frame(frame):
            self.video_buffer.save(frame['frame'])
            prompt = "Is there a toy in the frame? Simply answer Yes or No"
            img = self.video_buffer.snapshot()
            img.show()
            response = self._llm.query(prompt, img).lower().strip()
            print(response)
            if response.startswith('yes'):
                self.has_toy.send_item({'video_frame': img})

        def recognize_toy(has_toy):
            now_toy_frame = has_toy['video_frame']
            imgs = [now_toy_frame]
            names = ""
            for toy in self.know_toy:
                imgs.append(toy['img'])
                if len(imgs) == 2:
                    names += f"'{toy['name']}'"
                elif len(imgs) == len(self.know_toy) + 1:
                    names += f" ,and '{toy['name']}'"
                else:
                    names += f", '{toy['name']}'"

            # prompt = (f"Is there a toy in the first picture that I already recognize? If so, please answer yes first, "
            #           f"and then tell me the names I gave them. The last few pictures are all the toys I know, "
            #           f"and I named them {names}. Please note that I only recognize the toys shown except for the "
            #           f"first picture. You cannot answer yes to a toy that is not on display even if you know the "
            #           f"toy. And the names you answer must also correspond to the names I chose, even though these "
            #           f"names may be strange or even inconsistent with common cognition.")
            prompt = (f"请问第一张图片中是否存在其他图片中列出的玩具？如果有请先回答yes，然后分别说出我给他们取的名字。从第二张开始到最后的所有图片是我所展示的所有玩具，我依次给他们取名为 {names}"
                      f"。请注意我只希望你根据除第一张外的图片来推测第一张图片中存在的玩具，对于不在展示中的玩具，即使你认识该玩具你也不可以回答yes"
                      f"。并且你所回答的名字也必须对应我取的名字，即使这些名字可能很奇怪甚至和通常认知不对应。")
            # print(prompt)
            # for img in imgs:
            #     img.show()
            response = self._llm.query(prompt, imgs)
            print(response)

        self._source.register_listener(self, handle_new_frame)
        self.has_toy.register_listener(self, recognize_toy)

        return True

    def pause(self):
        self._source.unregister_listener(self)

    def stop(self):
        self._source.remove_listener(self)

if __name__ == '__main__':
    ip = '192.168.43.41'
    from agents.system_agents.socket_sensor.mobile_video import VideoSocketSensors
    video_agent = VideoSocketSensors(ip=ip)
    video_agent.start()
    agent = ToyRecognitionAgent()
    agent.start()