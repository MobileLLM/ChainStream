import collections
import logging
from chainstream.stream import register_stream_manager
import time
from chainstream.stream import reset_stream

# from chainstream.stream.base_stream import BaseStream

logger = logging.getLogger(__name__)


class StreamAnalyzer:
    def __init__(self):
        super().__init__()
        self.streams = collections.OrderedDict()
        self.recorders = {}

    def get_stream_info(self):
        stream_info = [x.get_meta_data() for x in self.streams.values()]
        return stream_info

    def get_graph_statistics(self, file_path_to_agent_id):
        stream_info = [x.get_record_data() for x in self.streams.values()]

        agent_to_stream_edges = []
        stream_to_agent_edges = []
        for s_info in stream_info:
            new_agent_to_queue = {}
            for fun_k, fun_v in s_info['agent_to_queue'].items():
                new_agent_to_queue[(file_path_to_agent_id[fun_k[0]], fun_k[1])] = fun_v
                agent_to_stream_edges.append({
                    "source": str(file_path_to_agent_id[fun_k[0]]) + ":" + str(fun_k[1]),
                    "target": s_info['stream_id'],
                    "value": fun_v['statistics'][1]
                })
            s_info['agent_to_queue'] = new_agent_to_queue
            for fun_k, fun_v in s_info['queue_to_agent'].items():
                stream_to_agent_edges.append({
                    "source": s_info['stream_id'],
                    "target": str(fun_k[0]) + ":" + str(fun_k[1]),
                    "value": fun_v['statistics'][1]
                })
        # print("Agent to Stream Edges:")
        # print(agent_to_stream_edges)
        # print("Stream to Agent Edges:")
        # print(stream_to_agent_edges)

        stream_node = self.streams.keys()
        agent_node = set(key for s_info in stream_info for key in s_info['agent_to_queue'].keys()).union(
            set(key for s_info in stream_info for key in s_info['queue_to_agent'].keys()))

        # print("Stream Node:")
        # print(stream_node)
        # print("Agent Node:")
        # print(agent_node)
        agent_node = [str(x[0]) + ":" + str(x[1]) for x in agent_node]
        node = list(stream_node) + list(agent_node)
        node = [{'name': x} for x in node]
        edge = agent_to_stream_edges + stream_to_agent_edges

        return node, edge


class StreamManager(StreamAnalyzer):
    def __init__(self):
        super().__init__()
        register_stream_manager(self)
        self.thread_list = {}

    def register_stream(self, stream):
        if stream.metaData.stream_id in self.streams:
            raise KeyError(f"Stream with id {stream.metaData.stream_id} already exists")
        self.streams[stream.metaData.stream_id] = stream
        self.thread_list[stream.metaData.stream_id] = stream.thread
        self.recorders[stream.metaData.stream_id] = stream.recorder

    def unregister_stream(self, stream):
        self.streams.pop(stream.stream_id)

    def get_stream(self, stream_id):
        if stream_id not in self.streams:
            raise KeyError(f"Stream with id {stream_id} not found")
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

    def wait_all_stream_clear(self):
        from chainstream.llm import check_has_model_working
        # TODO: use threading.Event to wait for all streams to be clear
        count = 5
        while True:
            # print(f"count: {count}")
            if all(stream.is_clear.is_set() for stream in self.streams.values()) and not check_has_model_working():
                # print(f"coundown {count}")
                count -= 1
                if count == 0:
                    return True
            else:
                count = 5
            time.sleep(1)

    def shutdown(self):

        reset_stream()

        # print(self.thread_list)
        for stream in self.streams.values():
            stream.shutdown()
        # print(self.thread_list)
        for thread in self.thread_list.values():
            if thread.is_alive():
                thread.join()

        self.streams = collections.OrderedDict()

        return True
