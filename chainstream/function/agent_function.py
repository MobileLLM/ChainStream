

class AgentFunction:
    def __init__(self, func, output_stream=None):
        self.func = func
        self.output_stream = output_stream

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        if self.output_stream is not None:
            self.output_stream.add_item(result)

    def __name__(self):
        return self.func.__name__

    def __str__(self):
        return self.func.__str__()

    def __repr__(self):
        return self.func.__repr__()

    def __doc__(self):
        return self.func.__doc__

    def set_output_stream(self, output_stream):
        self.output_stream = output_stream
