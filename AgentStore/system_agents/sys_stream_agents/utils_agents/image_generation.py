import json
from chainstream.runtime.stream_manager import StreamManager
import dashscope
from dashscope import ImageSynthesis
import os
import chainstream as cs

class ImageGenerationAgent(cs.agent.Agent):
    """
    Agent for generating images based on text descriptions and resolution.
    """
    def __init__(self, agent_id="image_gen_agent", stream_id="image_stream"):
        self._source = StreamManager()
        self.agent_id = agent_id
        self.stream_id = stream_id
        self.result_buffer = cs.context.TextBuffer(max_text_num=1024)
        self._source.register_stream(self.stream_id, self)

        self.recorder = None
    def start(self):
        """
        Start the agent.
        """
        def handle_input(params):
            image_url = self.generate_image(params)
            self.result_buffer.save(image_url)

        try:
            self._source.for_each(self, handle_input)
            return True
        except Exception as e:
            print("Error starting Image Generation Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)
    def generate_image(self, params):
        """
        Generate an image based on the given parameters (text description and resolution).
        """
        params = json.loads(params)
        text = params.get('text', '')
        resolution = params.get('resolution', '1280*720')

        # Check if resolution is valid
        if resolution not in ['1024*1024', '720*1280', '1280*720']:
            resolution = '1280*720'

        # Generate the image
        dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
        response = ImageSynthesis.call(
            model='wanx-v1',
            prompt=text,
            n=1,
            size=resolution,
            steps=10
        )
        image_url = response.output['results'][0]['url']
        return image_url

def main():
    # Instantiate the Image Generation Agent
    image_agent = ImageGenerationAgent()
    params = {
        'text': '生成一个超级英雄，拯救世界',
        'resolution': '1024*1024'
    }
    params_str = json.dumps(params)
    image_url = image_agent.generate_image(params_str)
    print(image_url)

if __name__ == "__main__":
    main()
