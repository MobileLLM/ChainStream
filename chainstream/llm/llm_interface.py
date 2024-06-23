from .llm_interface_recorder import LLMInterfaceRecorder
from chainstream.runtime.abstraction_layer.models.llm_router import LLMRouter
from queue import Queue


class LLMInterfaceBase:
    def __init__(self, agent, model_type):
        self.model_type = model_type
        self.agent = agent
        self.router = LLMRouter(model_type)
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
        super().__init__(agent, "text")
