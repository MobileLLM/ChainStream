from .runtime_core import ChainStreamServerBase

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
            for i, (name, agent) in enumerate(self.chainstream_core.get_running_agents_name_list()):
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