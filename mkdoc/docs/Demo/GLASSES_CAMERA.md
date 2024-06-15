# GLASSES CAMERA

We explored the application of ChainStream in smart glasses. We attempted to quickly deploy a simple visual perception Agent developed based on ChainStream onto the smart glasses.

Specifically, we wanted the glasses to constantly check if the toys appearing in the field of view are my toys. Of course, toys here refer to any recognizable objects and can be replaced with other objects, faces, etc., in actual applications.

## Designing the Agent

We designed the task in two steps: detecting whether there is a toy in the current field of view and identifying the specific toy. Then we conveniently wrote the following Agent based on ChainStream:

```python
import chainstream as cs

class ToyRecognitionAgent(cs.agent.Agent):
    is_agent = True

    def __init__(self, agent_id='toy_recognition_agent'):
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

            prompt = (f"Is there a toy in the first picture that I already recognize? If so, please answer yes first, "
                      f"and then tell me the names I gave them. The last few pictures are all the toys I know, "
                      f"and I named them {names}. Please note that I only recognize the toys shown except for the "
                      f"first picture. You cannot answer yes to a toy that is not on display even if you know the "
                      f"toy. And the names you answer must also correspond to the names I chose, even though these "
                      f"names may be strange or even inconsistent with common cognition.")

            response = self._llm.query(prompt, imgs)
            print(response)

        self._source.register_listener(self, handle_new_frame)
        self.has_toy.register_listener(self, recognize_toy)

        return True

    def pause(self):
        self._source.unregister_listener(self)

    def stop(self):
        self._source.remove_listener(self)
```

## Adding Memory

Next, we added images and names of the following three toys to the memory of the Agent:

<img src="../../img/demo_glass_memory.png" alt="Glass Memory">

## Configuring the Edge Sensor

We used the Thunderbird X2 smart glasses and installed the ChainStream Client App on them. When the app is launched, the device can be connected to ChainStream.

## Running the Agent

We wore the smart glasses and started the Agent written above, obtaining the following results:

<img src="../../img/demo_glass.png" alt="Demo Glass">

As can be seen, the Agent can perform our task fairly accurately. Although the accuracy is not perfect, the main goal of this demo is to showcase the convenience and flexibility of ChainStream. Object detection is also not the specialty of the GPT-4 model.

The accuracy depends on how the Agent is written. If you want to improve the task's effectiveness, you can use a specialized detection model like YOLO in the Agent.