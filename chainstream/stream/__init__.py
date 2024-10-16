import inspect

available_streams = {}

stream_manager = None


def reset_stream():
    """
    Reset all streams and stream manager. Used for Runtime or sandbox restart.
    """
    global available_streams
    global stream_manager

    for k, v in available_streams.items():
        v.shutdown()
        del v

    available_streams = {}
    stream_manager = None


def get_stream_interface(stream_id):
    """
    Get the stream interface for a given stream_id. Used for providing a stream data for non-chainstream agent code,
    mainly for sandbox evaluation.

    For example, assuming we have an agent from native python code, we can get the stream interface for a given
    stream_id:

    ```python
    from chainstream.stream import get_stream_interface

    stream_id = "my_stream_id"
    CSStream = get_stream_interface(stream_id)

    while True:
        data = CSStream.get()

        # do something with data

        CSStream.put(data)

    ```

    The `CSStream.get()` will block until there is data available in the stream, and `CSStream.put(data)` will add
    data to the stream.

    """
    global available_streams
    global stream_manager

    if stream_id is None:
        raise ValueError("stream_id should not be None")
    if not isinstance(stream_id, str):
        raise ValueError(f"stream_id should be a string, not {type(stream_id)}")

    if stream_manager is not None:
        try:
            stream = stream_manager.get_stream(stream_id)
        except KeyError:
            raise KeyError(f"stream_id {stream_id} not found in stream_manager")
        except Exception as e:
            raise e

        stream_interface = stream.create_stream_interface()

        return stream_interface


def get_stream(agent, stream_id):
    """
    `chainstream.get_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This
    method retrieves a `Stream` object based on `stream_id`, typically called in the `__init__()` method of the Agent
    instance. The first parameter, `agent`, refers to the Agent instance obtaining the stream, usually `self` in the
    `__init__()` method.

    """
    global available_streams
    global stream_manager

    from chainstream.agent import Agent
    if agent is None:
        raise ValueError("agent should not be None")
    if not isinstance(agent, Agent):
        raise ValueError(f"agent should be an instance of Agent, not {type(agent)}")

    if stream_id is None:
        raise ValueError("stream_id should not be None")
    if not isinstance(stream_id, str):
        raise ValueError(f"stream_id should be a string, not {type(stream_id)}")

    if stream_manager is not None:
        from .base_stream import BaseStream, StreamForAgent

        try:
            stream = stream_manager.get_stream(stream_id)
        except KeyError:
            raise KeyError(f"stream_id {stream_id} not found in stream_manager")
        except Exception as e:
            raise e

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        if SANDBOX_RECORDER is not None:
            inspect_stack = inspect.stack()
            stream_id = stream_id
            is_stream_manager = stream_manager is not None
            find_stream = stream is not None
            SANDBOX_RECORDER.record_get_stream(agent, stream_id, is_stream_manager, find_stream, inspect_stack)

        return StreamForAgent(agent, stream)

    if stream_id in available_streams:
        from .base_stream import BaseStream, StreamForAgent
        stream = available_streams[stream_id]

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        if SANDBOX_RECORDER is not None:
            inspect_stack = inspect.stack()
            stream_id = stream_id
            is_stream_manager = stream_manager is not None
            find_stream = stream is not None
            SANDBOX_RECORDER.record_get_stream(agent, stream_id, is_stream_manager, find_stream, inspect_stack)

        return StreamForAgent(agent, stream)
    else:

        from chainstream.sandbox_recorder import SANDBOX_RECORDER
        if SANDBOX_RECORDER is not None:
            inspect_stack = inspect.stack()
            stream_id = stream_id
            is_stream_manager = stream_manager is not None
            find_stream = False
            SANDBOX_RECORDER.record_get_stream(agent, stream_id, is_stream_manager, find_stream, inspect_stack)

        raise RuntimeError(f'unknown stream_id: {stream_id}')


def create_stream(agent, stream_id, type=None):
    """
    `chainstream.create_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This
    method creates a new `Stream` object based on `stream_id`, typically called in the `__init__()` method of the
    Agent instance. The first parameter, `agent`, refers to the Agent instance creating the stream, usually `self` in
    the `__init__()` method.

    """
    global available_streams
    global stream_manager

    from chainstream.agent import Agent
    if agent is None:
        raise ValueError("agent should not be None")
    if not isinstance(agent, Agent):
        raise ValueError(f"agent should be an instance of Agent, not {type(agent)}")

    if stream_id is None:
        raise ValueError("stream_id should not be None")
    if not isinstance(stream_id, str):
        raise ValueError(f"stream_id should be a string, not {type(stream_id)}")

    create_by_agent_file = inspect.stack()[1].filename
    if type == 'video':
        from .base_stream import BaseStream, StreamForAgent
        from .video_stream import VideoStream
        stream = VideoStream(stream_id)
        stream = StreamForAgent(agent, stream)
    else:
        from .base_stream import BaseStream, StreamForAgent
        if isinstance(stream_id, str):
            try:
                stream = BaseStream(stream_id, create_by_agent_file=create_by_agent_file)
            except KeyError as e:
                raise KeyError(f"Failed to create stream with id {stream_id}: {str(e)}")
            except Exception as e:
                raise e
        else:
            if isinstance(stream_id, dict) and "stream_id" in stream_id:
                stream_id_ = stream_id["stream_id"]
                try:
                    stream = BaseStream(stream_id_, description=stream_id, create_by_agent_file=create_by_agent_file)
                except KeyError as e:
                    raise KeyError(e)
                except Exception as e:
                    raise e
            else:
                raise ValueError("stream_id should be a string or a dictionary with a key 'stream_id'")
        stream = StreamForAgent(agent, stream)

    if stream_manager is None:
        available_streams[stream_id] = stream

    from chainstream.sandbox_recorder import SANDBOX_RECORDER
    if SANDBOX_RECORDER is not None:
        inspect_stack = inspect.stack()
        stream_id = stream_id
        agent_id = agent.agent_id
        is_stream_manager = stream_manager is not None
        success_create = stream is not None
        SANDBOX_RECORDER.record_create_stream(agent_id, stream_id, is_stream_manager, success_create, inspect_stack)

    return stream


def register_stream_manager(manager):
    global stream_manager
    stream_manager = manager


class Stream:
    """
    You must create or get a stream by using get_stream or create_stream functions, not directly.
    This class is used to provide an exception for LLM-based agent generator.
    """
    def __init__(self):
        raise RuntimeError("must create or get a stream by using get_stream or create_stream functions, not directly")

    def for_each(self, func):
        raise RuntimeError("must create or get a stream by using get_stream or create_stream functions, not directly")

    def batch(self, *args, **kwargs):
        raise RuntimeError("must create or get a stream by using get_stream or create_stream functions, not directly")

