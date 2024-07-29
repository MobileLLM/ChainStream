from .agent_function import AgentFunction
import uuid
import functools

class BatchFunction(Function):
    def __init__(self, agent, func, params):
        self.func = func
        functools.update_wrapper(self, func)

        self.kwargs = params

    def __call__(self, item):
        try:
            output, self.kwargs = self.func(item, **self.kwargs)
            # if output is not None:
            #     self.output_stream.put(output)
            if output is not None:
                return output
        except Exception as e:
            raise e.__class__(f"Error running {self.func} on {item}: {e}")


if __name__ == '__main__':
    def example_func(item, **kwargs):
        buffer = kwargs.get('buffer', [])
        if len(buffer) < 10:
            buffer.append(item)
            return None, kwargs
        else:
            buffer.append(item)
            all_items = buffer.pop_all()
            return {"item_list": all_items}, kwargs

