import logging
import collections

class ChainStreamServer(object):
    """
    the serving system of ChainStream
    """
    def __init__(self, output_dir, verbose=False):
        self.logger = logging.getLogger(name='ChainStreamServer')
        self.verbose = verbose
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.output_dir = output_dir
        self.streams = collections.OrderedDict()
        self.agents = collections.OrderedDict()

    def stream_flow_graph(self):
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
    
    def register_stream(self, stream):
        self.streams[stream.name] = stream

    def unregister_stream(self, stream):
        self.streams.pop(stream.name)

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def unregister_stream(self, agent):
        self.agents.pop(agent.name)

    def start(self):
        pass

