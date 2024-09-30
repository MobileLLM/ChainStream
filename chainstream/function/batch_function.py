# from .agent_function import AgentFunction
import uuid
import functools
from chainstream.context import Buffer


class BatchFunction:
    """
    BatchFunction is a wrapper around a function for `Stream.batch(by_func=BatchFunction)`. It takes two arguments,
    first is same as `AgentFunction` and second is a dictionary of parameters to be passed to the function,
    which is used to save golbal batch state.
    """

    def __init__(self, func, params):
        self.kwargs = params
        self.func = func
        # functools.update_wrapper(self, func)

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
        buffer = kwargs.get('buffer', Buffer())
        if len(buffer) < 10:
            buffer.append(item)
            return None, kwargs
        else:
            buffer.append(item)
            all_items = buffer.pop_all()
            return {"item_list": all_items}, kwargs


    def is_ads(item):
        pass


    def filter_func(item, **kwargs):
        man_buffer = kwargs.get('buffer_man', Buffer())
        woman_buffer = kwargs.get('buffer_woman', Buffer())

        if item['gender'] == "man":
            if len(man_buffer) < 10:
                man_buffer.append(item)
                return None, kwargs
            else:
                man_buffer.append(item)
                all_items = man_buffer.pop_all()
                return {"item_list": all_items}, kwargs
        else:
            if len(woman_buffer) < 10:
                woman_buffer.append(item)
                return None, kwargs
            else:
                woman_buffer.append(item)
                all_items = woman_buffer.pop_all()
                return {"item_list": all_items}, kwargs


    def overlapped_two_frames(item, **kwargs):
        by_count = 10
        buffer = kwargs.get('buffer', Buffer(maxlen=by_count))
        if len(buffer) < by_count - 1:
            buffer.append(item)
            return None, kwargs
        else:
            buffer.append(item)
            all_items = buffer.get_all()
            buffer.popright()
            buffer.popright()
            return {"item_list": all_items}, kwargs


    all_email_stream = ...
    all_email_stream.batch(by_func=filter_func).for_each(...)
