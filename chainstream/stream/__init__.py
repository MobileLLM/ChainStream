available_streams = {}


def get_stream(stream_id):
    if stream_id in available_streams:
        return available_streams[stream_id]
    else:
        raise RuntimeError(f'unknown stream_id: {stream_id}')


def create_stream(stream_id, type=None):
    if type == 'video':
        from .video_stream import VideoStream
        stream = VideoStream(stream_id)
    else:
        from .base_stream import BaseStream
        stream = BaseStream(stream_id)
    available_streams[stream_id] = stream
    return stream

