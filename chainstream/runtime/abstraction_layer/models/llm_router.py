class LLMRouterBase:
    router_name = None

    def __init__(self, model_type):
        self.model_type = model_type
        self.llm_instance_list = {}

    def query(self, prompt, response_queue) -> object:
        raise NotImplementedError("query method not implemented")

    def set_llm_instance_list(self, llm_instance_list):
        self.llm_instance_list = llm_instance_list


class LLMRouter(LLMRouterBase):
    pass
