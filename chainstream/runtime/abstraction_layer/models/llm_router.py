class LLMRouterBase:
    def __init__(self, model_type):
        self.model_type = model_type
        pass

    def query(self, prompt, response_queue):
        pass

    def set_llm_instance_list(self, llm_instance_list):
        pass


class LLMRouter(LLMRouterBase):
    pass
