import functools
import uuid
from chainstream.runtime import cs_server_core
from chainstream.runtime import ErrorType
import traceback
from .batch_function import BatchFunction


class AgentFunction:
    def __init__(self, agent, func, output_stream=None):
        self.id = str(uuid.uuid4())
        self.agent = agent
        self.is_batch_func = False
        if isinstance(func, BatchFunction):
            self.is_batch_func = True
            self.kwargs = func.kwargs

        self.func = func

        self.output_stream = output_stream

        # FIXME: This wrapper will broke the __call__ method with kwargs input of the BatchFunction, so here have to
        #  use self.kwargs to pass the kwargs to the BatchFunction, need to find a better way to handle this
        functools.update_wrapper(self, func)

        self.func_id = self.func.__name__ + "_" + self.id

        setattr(self.func, "func_id", self.func_id)

    def __call__(self, *args, **kwargs):
        result = None
        try:
            if self.is_batch_func:
                result, self.kwargs = self.func(args[0], self.kwargs)
                result = result[0]
            else:
                result = self.func(*args, **kwargs)
        except Exception as e:
            error_msg = {
                "exception": str(e),
                "function_id": self.func_id,
                "function_name": self.func.__name__,
                "agent_id": self.agent.agent_id,
                "output_stream_id": self.output_stream.stream_id if self.output_stream is not None else None,
            }
            cs_server_core.record_error(ErrorType.FUNCTION_ERROR.value, error_message=error_msg, error_traceback=traceback.format_exc())
            # raise RuntimeError(f"Error in agent function {self.func_id} from agent {self.agent.agent_id}: {e}")
        if self.output_stream is not None and result is not None:
            self.output_stream.add_item(result)

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        import inspect
        if SANDBOX_RECORDER is not None:
            func_id = self.func_id
            output_stream_id = self.output_stream.stream.stream_id if self.output_stream is not None else None
            agent_id = self.agent.agent_id
            func_result = result
            inspect_stack = inspect.stack()
            SANDBOX_RECORDER.record_call(func_id, output_stream_id, agent_id, args, kwargs, func_result, inspect_stack)

        return result

    def set_output_stream(self, output_stream):
        self.output_stream = output_stream
