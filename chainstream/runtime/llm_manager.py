from abstraction_layer import LLM_INSTANCES_LIST
from collections import OrderedDict


class LLMManager:
    def __init__(self):
        self.llm_instances_class_list = LLM_INSTANCES_LIST
        self.llm_instances = OrderedDict()
        self.llm_interface = OrderedDict()
        pass

    def register_llm(self, agent, llm_interface):
        llm_type = llm_interface.llm_type
        if llm_type not in self.llm_instances:
            raise ValueError("LLM type not found")
        llm_interface.set_llm_instance_list(self.llm_instances[llm_type])
        pass

    def unregister_llm(self, agent, llm):
        pass

    def _init_llm_instance(self):
        pass
