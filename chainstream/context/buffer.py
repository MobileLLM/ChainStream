from chainstream.interfaces import ContextInterface


class BufferContext(ContextInterface):
    pass


class VideoBuffer(BufferContext):
    pass


class AudioBuffer(BufferContext):
    pass


class TextBuffer(BufferContext):
    pass

