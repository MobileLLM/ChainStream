from .llm_interface_recorder import LLMInterfaceRecorder
from chainstream.runtime.abstraction_layer.models.llm_router import get_llm_router
from queue import Queue
from . import API_LLM_TYPE


class LLMInterfaceBase:
    def __init__(self, agent, model_type, router_type=None):
        self.model_type = model_type
        self.agent = agent
        self.router = get_llm_router(model_type, router_type)
        self.router.set_agent_info(agent)
        self.recorder = LLMInterfaceRecorder()
        self.response_queue = Queue()

    def query(self, prompt):
        self.recorder.record_query(prompt)

        self.router.query(prompt, self.response_queue)

        # queue.get() blocks until a response is available, so we don't need to wait for it here
        response = self.response_queue.get()

        self.recorder.record_response(response)

        return response

    def set_llm_instance_list(self, llm_instance_list):
        self.router.set_llm_instance_list(llm_instance_list)


class LLMTextInterface(LLMInterfaceBase):
    def __init__(self, agent):
        super().__init__(agent, API_LLM_TYPE['T'])


class LLMTextImageInterface(LLMInterfaceBase):
    def __init__(self, agent):
        super().__init__(agent, API_LLM_TYPE['TI'])


class LLMTextAudioInterface(LLMInterfaceBase):
    def __init__(self, agent):
        super().__init__(agent, API_LLM_TYPE['TA'])


class LLMTextImageAudioInterface(LLMInterfaceBase):
    def __init__(self, agent):
        super().__init__(agent, API_LLM_TYPE['TAI'])
