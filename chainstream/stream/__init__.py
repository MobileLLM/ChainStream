import inspect

available_streams = {}

stream_manager = None


def get_stream(agent, stream_id):
    if stream_manager is not None:
        from .base_stream import BaseStream, StreamForAgent
        stream = stream_manager.get_stream(stream_id)

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
    create_by_agent_file = inspect.stack()[1].filename
    if type == 'video':
        from .base_stream import BaseStream, StreamForAgent
        from .video_stream import VideoStream
        stream = VideoStream(stream_id)
        stream = StreamForAgent(agent, stream)
    else:
        from .base_stream import BaseStream, StreamForAgent
        if isinstance(stream_id, str):
            stream = BaseStream(stream_id, create_by_agent_file=create_by_agent_file)
        else:
            if isinstance(stream_id, dict) and "stream_id" in stream_id:
                stream_id_ = stream_id["stream_id"]
                stream = BaseStream(stream_id_, description=stream_id, create_by_agent_file=create_by_agent_file)
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
