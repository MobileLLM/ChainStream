from queue import Queue


def get_llm_router(model_type, router_type):
    if router_type == "direct":
        return DirectLLMRouter(model_type)
    elif router_type == "parallel":
        return ParallelLLMRouter(model_type)
    elif router_type == "switched":
        return SwitchedLLMRouter(model_type)
    else:
        raise ValueError("Invalid router type")


class LLMRouterBase:
    router_name = None

    def __init__(self, model_type):
        self.agent_id = None
        self.agent = None
        self.model_type = model_type
        self.llm_instance_list = {}

        self.instance_response_queue = Queue()

    def query(self, prompt, interface_response_queue) -> object:
        response = self.route_and_query(prompt)
        interface_response_queue.put(response)

        return response

    def route_and_query(self, prompt) -> object:
        raise NotImplementedError("route_and_query method not implemented")

    def query_llm_instance(self, prompt, llm_instance_id) -> object:
        """
        All queries in router must use this method to query an LLM instance.
        :param prompt:
        :param llm_instance_id:
        :return:
        """

        if llm_instance_id not in self.llm_instance_list:
            raise ValueError("Invalid LLM instance id")

        llm_instance = self.llm_instance_list[llm_instance_id]

        query_info = self._make_query_info(prompt)

        llm_instance.send_query(prompt, self.instance_response_queue, query_info)

        response = self.instance_response_queue.get()

        return response

    def _make_query_info(self, prompt):
        pass

    def set_llm_instance_list(self, llm_instance_list):
        self.llm_instance_list = llm_instance_list

    def set_agent_info(self, agent):
        self.agent = agent
        self.agent_id = agent.id


class LLMRouter(LLMRouterBase):
    pass


class DirectLLMRouter(LLMRouter):
    pass


class ParallelLLMRouter(LLMRouter):
    pass


class SwitchedLLMRouter(LLMRouter):
    pass
