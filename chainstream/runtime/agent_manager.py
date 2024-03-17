import collections
import importlib
import importlib.util
from pathlib import Path
import os
import inspect
import logging
import json

logger = logging.getLogger(__name__)

def _path_to_json(paths):
    json_data = {}

    for path in paths:
        directories = path.split('/')
        current_dict = json_data

        for directory in directories:
            if directory != '':
                if directory not in current_dict:
                    current_dict[directory] = {}
                current_dict = current_dict[directory]

    def process_dict(node):
        tmp_list = []
        for key, value in node.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    tmp_list.append({
                        "label": key,
                    })
                else:
                    tmp_list.append({
                        "label": key,
                        "disabled": True,
                        "children": process_dict(value)
                    })
            else:
                node[key] = {"name": value}
                tmp_list.append({
                    "label": value
                })
        return tmp_list

    list_data = process_dict(json_data)

    return list_data

class AgentManager:
    def __init__(self):
        self.agents = collections.OrderedDict()
        self.predefined_agents_path = Path(os.path.dirname(__file__)).parent.parent / 'agents'

    def register_agent(self, agent):
        self.agents[agent.agent_id] = agent

    def unregister_stream(self, agent):
        self.agents.pop(agent.agent_id)

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def get_agents_list(self):
        return list(self.agents.keys())

    def scan_predefined_agents(self):
        agent_list = []
        for root, dirs, files in os.walk(self.predefined_agents_path):
            for file in files:
                if file.endswith('.py'):
                    agent_list.append(os.path.join(root, file))
        return agent_list

    def scan_predefined_agents_tree(self):
        agent_list = []
        for root, dirs, files in os.walk(self.predefined_agents_path):
            for file in files:
                if file.endswith('.py'):
                    # agent_list.append(os.path.join(root, file))
                    agent_list.append(os.path.relpath(os.path.join(root, file), start=self.predefined_agents_path))
        agent_list = _path_to_json(agent_list)
        return agent_list

    def start_agent(self, path):
        if not path.startswith('/'):
            path = str(self.predefined_agents_path / path)
        if not os.path.exists(path) or not path.endswith('.py'):
            raise Exception(f'agent not found: {path}')
        module_name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        from chainstream.agent import Agent
        for name, obj in module.__dict__.items():
            if inspect.isclass(obj) and issubclass(obj, Agent) and obj.is_agent:
                print(name, obj)
                try:
                    new_agent = obj()
                    res = new_agent.start()
                    if res:
                        logger.info(f'agent {name} started successfully')
                except Exception as e:
                    logger.error(f'failed to start agent {name}: {e}')
        return True


if __name__ == '__main__':
    print(Path(os.path.dirname(__file__)).parent.parent / 'agents')
