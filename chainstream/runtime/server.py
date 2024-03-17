import logging
from .stream_manager import StreamManager



class ChainStreamCore(StreamManager):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(name='ChainStreamCore')
        self.verbose = False
        self.output_dir = None


class ChainStreamServerBase(object):
    def __init__(self):
        self.chainstream_core = ChainStreamCore()

    def start(self):
        pass

    def config(self, *args, **kwargs):
        pass

    def get_chainstream_core(self):
        return self.chainstream_core


class ChainStreamServerShell(ChainStreamServerBase):
    def __init__(self):
        super().__init__()
        self.output_dir = None
        self.verbose = None

    def start(self):
        print(self._handle_command("help"))
        while True:
            cmd = input('> ')
            if cmd == 'q' or cmd == 'exit':
                break
            else:
                # print(f'cmd: {cmd}')
                out = self._handle_command(cmd)
                print(out)

    def config(self, output_dir=None, verbose=False):
        self.output_dir = output_dir
        self.verbose = verbose

    def _handle_command(self, cmd):
        out = ''
        if cmd == 'help':
            out += ' list streams (LS) ---- list all available streams\n'
            out += ' list agents (LA) ----- list all available agents\n'
            out += ' start agent (S) ----- choose an agent to start and run\n'
        elif cmd == 'list streams' or cmd == 'LS':
            out += 'available streams:\n'
            for i, (name, stream) in enumerate(self.chainstream_core.get_stream_list()):
                out += f'  {i}: {name}\n'
        elif cmd == 'list agents' or cmd == 'LA':
            out += 'available agents:\n'
            for i, (name, agent) in enumerate(self.chainstream_core.get_agents_list()):
                out += f'  {i}: {name}\n'
        elif cmd.startswith('start agent') or cmd == 'S':
            # agents_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'agents'))
            agents_path = "agents/"
            # List all files inside the agents folder
            agent_list = self.chainstream_core.scan_predefined_agents()
            while True:
                for i, agent in enumerate(agent_list):
                    print(f"{[i]}: {agent}")
                agent_id = input('choose an agent index to start: ')
                if agent_id.isdigit() and int(agent_id) < len(agent_list):
                    chosen_agent = agent_list[int(agent_id)]
                    break
                else:
                    out += f'invalid agent id: {agent_id}\n'

            res = self.chainstream_core.start_agent(chosen_agent)
            if res:
                out += f'agent started successfully\n'
        return out


class ChainStreamServerWeb(ChainStreamServerBase):
    def __init__(self):
        super().__init__()
        self.ip = None
        self.port = None
        from .web.backend.app import app, set_core
        self.app = app
        set_core(self.chainstream_core)

    def config(self, *args, **kwargs):
        self.ip = kwargs.get('ip', '127.0.0.1')
        self.port = kwargs.get('port', 6677)

    def start(self):
        print(self.ip, self.port)
        self.app.run(host=self.ip, port=self.port)
        pass

# Create a custom request handler class
# TODO implement this
# class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         try:
#             if self.path == '/':
#                 # Serve the index.html file when the root URL is requested
#                 self.path = '/index.html'
#             # Construct the absolute path to the file
#             file_path = os.path.join(root_directory, self.path[1:])
#
#             # Check if the file exists
#             if os.path.exists(file_path):
#                 # Open the file and read its contents
#                 with open(file_path, 'rb') as file:
#                     file_data = file.read()
#
#                 # Send a 200 OK response and specify the content type
#                 self.send_response(200)
#                 self.send_header("Content-type", "text/html")
#                 self.end_headers()
#
#                 # Send the file content to the client
#                 self.wfile.write(file_data)
#             else:
#                 # File not found, send a 404 Not Found response
#                 self.send_response(404)
#                 self.send_header("Content-type", "text/html")
#                 self.end_headers()
#                 self.wfile.write(b"404 Not Found")
#
#         except Exception as e:
#             # Handle any exceptions that may occur
#             print(f"Error: {e}")
#             self.send_response(500)
#             self.send_header("Content-type", "text/html")
#             self.end_headers()
#             self.wfile.write(b"500 Internal Server Error")
