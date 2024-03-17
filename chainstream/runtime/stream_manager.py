import collections
import logging
from chainstream.stream import register_stream_manager
from .agent_manager import AgentManager

logger = logging.getLogger(__name__)


class StreamManager(AgentManager):
    def __init__(self):
        super().__init__()
        self.streams = collections.OrderedDict()
        register_stream_manager(self)

    def register_stream(self, stream):
        if stream.stream_id in self.streams:
            raise ValueError(f"Stream with id {stream.stream_id} already exists")
        self.streams[stream.stream_id] = stream

    def unregister_stream(self, stream):
        self.streams.pop(stream.stream_id)

    def get_stream(self, stream_id):
        if stream_id not in self.streams:
            raise ValueError(f"Stream with id {stream_id} not found")
        return self.streams.get(stream_id)

    def get_stream_list(self):
        return list(self.streams.keys())


    def get_stream_flow_graph(self):
        """
        TODO finish this
        """
        edges = []  # tuples of (source_agent, stream, target_agent)
        for name, stream in self.streams:
            source_agent = stream.source_agent
            target_agents = stream.get_registered_agents()
            for target_agent in target_agents:
                edges.append((source_agent, stream, target_agent))
        return edges
