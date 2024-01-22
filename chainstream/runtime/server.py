import logging
import collections
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class ChainStreamServer(object):
    """
    the serving system of ChainStream
    """
    def __init__(self):
        self.logger = logging.getLogger(name='ChainStreamServer')
        self.verbose = False
        self.output_dir = None
        self.monitor_mode = 'shell'  # can be web or shell
        self.streams = collections.OrderedDict()
        self.agents = collections.OrderedDict()

    def config(self, output_dir=None, ip='0.0.0.0', port=8848, monitor_mode='shell', verbose=False):
        self.output_dir = output_dir
        self.ip = ip
        self.port = port
        self.monitor_mode = monitor_mode
        self.verbose = verbose
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

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
        self.streams[stream.stream_id] = stream

    def unregister_stream(self, stream):
        self.streams.pop(stream.stream_id)

    def register_agent(self, agent):
        self.agents[agent.agent_id] = agent

    def unregister_stream(self, agent):
        self.agents.pop(agent.agent_id)

    def start(self):
        self.logger.info(f"Starting ChainStream server...")
        server_dir = os.path.join(self.output_dir, 'server')
        if not os.path.exists(server_dir):
            os.makedirs(server_dir)
        if self.monitor_mode == 'shell':
            self.start_shell()
    
    def start_shell(self):
        while True:
            cmd = input('> ')
            if cmd == 'q' or cmd == 'exit':
                break
            else:
                # print(f'cmd: {cmd}')
                out = self.handle_command(cmd)
                print(out)

    def start_http_server(self):
        # Create an HTTP server with the custom request handler
        http_server = HTTPServer((self.ip, self.port), CustomHTTPRequestHandler)

        # Start the HTTP server
        self.logger.info(f"Server running at {self.ip}:{self.port}...")
        try:
            http_server.serve_forever()
        except KeyboardInterrupt as e:
            http_server.shutdown()

    def handle_command(self, cmd):
        out = ''
        if cmd == 'help':
            out += ' list streams ---- list all available streams\n'
            out += ' list agents ----- list all available agents\n'
        elif cmd == 'list streams':
            out += 'available streams:\n'
            for i, (name, stream) in enumerate(self.streams):
                out += f'  {i}: {name}\n'
        elif cmd == 'list agents':
            out += 'available agents:\n'
            for i, (name, agent) in enumerate(self.agents):
                out += f'  {i}: {name}\n'
        else:
            out += f'unknown command: {cmd}'
        return out


# Create a custom request handler class
# TODO implement this
class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                # Serve the index.html file when the root URL is requested
                self.path = '/index.html'
            # Construct the absolute path to the file
            file_path = os.path.join(root_directory, self.path[1:])

            # Check if the file exists
            if os.path.exists(file_path):
                # Open the file and read its contents
                with open(file_path, 'rb') as file:
                    file_data = file.read()

                # Send a 200 OK response and specify the content type
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                # Send the file content to the client
                self.wfile.write(file_data)
            else:
                # File not found, send a 404 Not Found response
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"404 Not Found")

        except Exception as e:
            # Handle any exceptions that may occur
            print(f"Error: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error")

