from modelscope import (
    snapshot_download, AutoModelForCausalLM, AutoTokenizer, GenerationConfig
)
import chainstream as cs
import torch

class DetectionAgent(cs.agent.Agent):
    """
    A simple agent that says hello to people in front camera
    """

    is_agent = True
    def __init__(self, agent_id="hello_agent",target=None):
        super().__init__(agent_id)
        model_id = 'qwen/Qwen-VL-Chat'
        revision = 'v1.1.0'
        torch.manual_seed(1234)
        model_dir = snapshot_download(model_id, revision=revision)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True,
                                                     fp16=True).eval()
        self.model.generation_config = GenerationConfig.from_pretrained(model_dir, trust_remote_code=True)

        self._source1 = cs.get_stream()  # instance of Stream
        self.detection_buffer = cs.context.TextBuffer(max_text_num=1024)
        self.target=target

    def start(self):
        def handle_new_image(image):
            # prompt = cs.llm.make_prompt([frame, 'Is there a person in the image? Simply answer Yes or No'])
            prompt = '输出'+self.target+'的检测框'
            response = self._llm.query(prompt, image['frame']).lower().strip()
            self.text_buffer.save(response)
        try:
            self._source1.for_each(self, handle_new_image)
        except Exception as e:
            print("Error in image caption agent: ", e)
            return False
        # self._source1.for_each(self, handle_new_frame)
        return True

    def pause(self):
        self._source1.pause_listener(self)

    def stop(self):
        self._source1.remove_listener(self)

