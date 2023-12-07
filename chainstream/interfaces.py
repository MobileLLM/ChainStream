class AgentInterface:
    def start(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def query(self, query):
        pass


class StreamInterface:
    def add_item(self, data_item):
        pass

    def register_listener(self, agent, listener_func):
        pass

    def unregister_listener(self, agent, listener_func=None):
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

