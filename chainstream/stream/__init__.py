import inspect

available_streams = {}

stream_manager = None


def get_stream(stream_id):
    if stream_manager is not None:
        return stream_manager.get_stream(stream_id)
    if stream_id in available_streams:
        return available_streams[stream_id]
    else:
        raise RuntimeError(f'unknown stream_id: {stream_id}')


def create_stream(stream_id, type=None):
    create_by_agent_file = inspect.stack()[1][1]
    if type == 'video':
        from .video_stream import VideoStream
        stream = VideoStream(stream_id)
    else:
        from .base_stream import BaseStream
        stream = BaseStream(stream_id, create_by_agent_file=create_by_agent_file)
    if stream_manager is None:
        available_streams[stream_id] = stream
    return stream


def register_stream_manager(manager):
    global stream_manager
    stream_manager = manager
