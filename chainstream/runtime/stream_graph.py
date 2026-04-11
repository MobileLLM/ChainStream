

class StreamGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_type, node):
        if node_type == 'stream':
            self._add_stream_node(node)
        elif node_type == 'agent':
            self._add_agent_node(node)

    def _add_stream_node(self, stream):
        pass

    def _add_agent_node(self, agent):
        pass

    def del_node(self, node_type, node_id):
        pass

    def add_edge(self, source, target, edge):
        pass

    def del_edge(self, source, target):
        pass

    def get_graph(self):
        pass

