import json
from chainstream.runtime.stream_manager import StreamManager
import chainstream as cs
import os
from modelscope_agent.tools import register_tool
from modelscope_agent.tools.utils.output_wrapper import VideoWrapper
from modelscope.utils.constant import Tasks
from modelscope_agent.tools.modelscope_tools.pipeline_tool import ModelscopePipelineTool

class VideoGenerationAgent(cs.agent.Agent):
    """
    Agent for generating videos based on text descriptions.
    """
    def __init__(self, agent_id="video_gen_agent", stream_id="video_stream"):
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
            video_url = self.generate_video(params)
            self.result_buffer.save(video_url)

        try:
            self._source.register_listener(self, handle_input)
            return True
        except Exception as e:
            print("Error starting Video Generation Agent: ", e)
            return False

    def pause(self):
        self._source.pause_listener(self)

    def stop(self):
        self._source.remove_listener(self)

    def generate_video(self, params):
        """
        Generate a video based on the given text description.
        """
        params = json.loads(params)
        input_text = params.get('input', '')

        # Use the VideoGenerationTool to generate the video
        video_tool = VideoGenerationTool()
        video_url = video_tool.call({'input': input_text})
        return video_url
class VideoGenerationTool(ModelscopePipelineTool):
    """
    Tool for generating videos based on text descriptions.
    """
    default_model = 'damo/text-to-video-synthesis'
    description = '视频生成服务，针对英文文本输入，生成一段描述视频'
    name = 'video-generation'
    parameters: list = [{
        'name': 'input',
        'description': '用户输入的文本信息，仅支持英文文本描述',
        'required': True,
        'type': 'string'
    }]
    task = Tasks.text_to_video_synthesis
    url = 'https://api-inference.modelscope.cn/api-inference/v1/models/damo/text-to-video-synthesis'

    def call(self, params: str, **kwargs) -> str:
        result = super().call(params, **kwargs)
        video = result['Data']['output_video']
        return str(VideoWrapper(video))

    def _remote_call(self, params: dict, **kwargs):
        text = params['input']
        params['input'] = {'text': text}
        return super()._remote_call(params, **kwargs)


def main():
    # Instantiate the Video Generation Agent
    video_agent = VideoGenerationAgent()
    params = {
        'input': 'Captain America is saving the world'
    }
    params_str = json.dumps(params)
    video_url = video_agent.generate_video(params_str)
    print(video_url)

if __name__ == "__main__":
    main()
