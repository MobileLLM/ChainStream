class AgentInterface:
    def start(self):
        pass

    def stop(self):
        pass


class StreamInterface:
    def add_item(self, agent, data_item):
        pass

    def for_each(self, agent, listener_func):
        pass

    def unregister_all(self, agent, listener_func=None):
        pass


class MemoryInterface:
    def add_item(self, data_item):
        pass

    def remove_item(self, data_item):
        pass

    def backup(self, file_path):  # save the memory to file
        pass

    def load(self, file_path):  # load the memory from file
        pass


class LLM_Interface:
    def query(self, prompt):
        pass


class ContextInterface:
    def to_prompt(self):
        pass


class ActionInterface:
    def execute(self):
        pass

