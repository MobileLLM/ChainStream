class AgentDoc:
    def __init__(self, name=None, description=None, memory=None, stream=None):
        self.name = name
        self.description = description

    def __call__(self, cls):
        cls.__agent_name__ = self.name
        cls.__agent_description__ = self.description
        return cls


class StreamFuncDoc:
    def __init__(self, note):
        self.note = note

    def __call__(self, func):
        func.__stream_func_note__ = self.note
        return func
