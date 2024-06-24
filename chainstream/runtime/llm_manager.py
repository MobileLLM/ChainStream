from abstraction_layer import LLM_INSTANCES_LIST
from collections import OrderedDict
from chainstream.llm import API_LLM_TYPE


class LLMManager:
    def __init__(self):
        self.llm_instances_class_list = LLM_INSTANCES_LIST
        self.llm_instances = OrderedDict()
        for k, v in API_LLM_TYPE.items():
            self.llm_instances[v] = {}
        self.llm_interface = OrderedDict()

    def register_llm(self, agent, llm_interface):
        """
        we just register all the llm instance to the router in each interface, but we don't register interface and
        router to each llm instance.
        """
        if agent.agent_id not in self.llm_interface:
            self.llm_interface[agent.agent_id] = {
                "agent": agent,
                "llm_interface": [llm_interface]
            }
        else:
            self.llm_interface[agent.agent_id]["llm_interface"].append(llm_interface)

        llm_type = llm_interface.llm_type
        if llm_type not in self.llm_instances:
            raise ValueError("LLM instance type not found")
        llm_interface.set_llm_instance_list(self.llm_instances[llm_type])

    def unregister_llm(self, agent):
        pass

    def _init_llm_instance(self):
        for model_type, model_list in self.llm_instances_class_list.items():
            for model_name, model_class in model_list.items():
                self.llm_instances[model_type][model_name] = model_class()
