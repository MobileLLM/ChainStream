from queue import Empty


class FakeAgent:
    def __init__(self, agent_id):
        self.agent_id = agent_id


class StreamInOutInterface:
    def __init__(self, recv_queue, stream):
        self.recv_queue = recv_queue
        self.stream_id = stream.stream_id
        self.stream = stream

    def put(self, item):
        self.stream.add_item(FakeAgent("fake_agent_for_stream_interface"), item)

    def get(self, timeout=1):
        try:
            item = self.recv_queue.get(timeout=timeout)
            return item
        except Empty:
            return None
