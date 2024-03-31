import collections
import logging
from chainstream.stream import register_stream_manager
from .agent_manager import AgentManager

# from chainstream.stream.base_stream import BaseStream

logger = logging.getLogger(__name__)


class StreamAnalyzer:
    def __init__(self):
        super().__init__()
        self.streams = collections.OrderedDict()
        self.recorders = {}

    def get_graph_statistics(self, file_path_to_agent_id):
        stream_info = [x.get_record_data() for x in self.streams.values()]
        for s_info in stream_info:
            new_agent_to_queue = {}
            for fun_k, fun_v in s_info['agent_to_queue'].items():
                new_agent_to_queue[(file_path_to_agent_id[fun_k[0]], fun_k[1])] = fun_v
            s_info['agent_to_queue'] = new_agent_to_queue
        # print(stream_info)
        edge_statistics = []
        stream_node = []
        # print(self.streams.keys())

        # trans agent file path to agent id

        # concat all stream info to graph



class StreamManager(StreamAnalyzer):
    def __init__(self):
        super().__init__()
        register_stream_manager(self)
        self.thread_list = {}

    def register_stream(self, stream):
        if stream.metaData.stream_id in self.streams:
            raise ValueError(f"Stream with id {stream.metaData.stream_id} already exists")
        self.streams[stream.metaData.stream_id] = stream
        self.thread_list[stream.metaData.stream_id] = stream.thread
        self.recorders[stream.metaData.stream_id] = stream.recorder

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
