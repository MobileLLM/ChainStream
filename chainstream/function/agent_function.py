import functools
import uuid
from chainstream.runtime import ErrorType
import traceback
from .batch_function import BatchFunction


class AgentFunction:
    """
    AgentFunction is a wrapper class for agent listening functions. It is responsible for handling the function call
    and output stream, as well as recording the function behavior.

    Note the function in `Stream.batch(by_func=func)` is wrapped by `BatchFunction` class, which is treated as a
    special type of `AgentFunction`. BatchFunction is responsible for handling the batch processing of the input
    stream, so ti has a `kwargs` attribute to store the state of the batch processing.

    Another notable attribute is `output_stream`, it's designed to support multiple `Stream.for_each` functions,
    each of which can have its own anonymous output stream to connect to the next function, which is the
    `output_stream` here.

    """
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
                # BatchFunction has a `kwargs` attribute to store the state of the batch processing, so we pass it to
                # the function as the second argument
                result, self.kwargs = self.func(args[0], self.kwargs)
            else:
                # Non-batch function just call the function with the input arguments
                result = self.func(*args, **kwargs)

            if self.output_stream is not None and result is not None:
                self.output_stream.add_item(result)

        except Exception as e:
            error_msg = {
                "exception": str(e),
                "function_id": self.func_id,
                "function_name": self.func.__name__,
                "agent_id": self.agent.agent_id,
                "output_stream_id": self.output_stream.stream_id if self.output_stream is not None else None,
            }
            from chainstream.runtime import cs_server_core
            cs_server_core.record_error(ErrorType.FUNCTION_ERROR.value, error_message=error_msg,
                                        error_traceback=traceback.format_exc())
            # raise RuntimeError(f"Error in agent function {self.func_id} from agent {self.agent.agent_id}: {e}")

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
