from chainstream.interfaces import StreamInterface
from .base_stream import BaseStream


class VideoStream(BaseStream):
    def __init__(self, stream_id) -> None:
        super().__init__(stream_id)

