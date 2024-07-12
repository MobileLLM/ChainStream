import functools
import uuid


class AgentFunction:
    def __init__(self, agent, func, output_stream=None):
        self.id = str(uuid.uuid4())
        self.agent = agent
        self.func = func

        self.output_stream = output_stream
        functools.update_wrapper(self, func)  # This updates the wrapper to have the attributes of the wrapped function

        self.func_id = self.func.__name__ + "_" + self.id

        setattr(self.func, "func_id", self.func_id)

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if self.output_stream is not None:
            self.output_stream.add_item(result)
        return result

    def set_output_stream(self, output_stream):
        self.output_stream = output_stream
