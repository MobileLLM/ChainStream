from ..core import chainstream_core
from flask import jsonify, Blueprint

agents_blueprint = Blueprint('agents_blueprint', __name__)


@agents_blueprint.route('/api/monitor/agents', methods=['GET'])
def get_predefined_agents():
    data = chainstream_core.scan_predefined_agents_tree()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/getRunningAgents', methods=['GET'])
def get_running_agents():
    data = chainstream_core.get_running_agents_info_list()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/start/<agent_id>', methods=['POST'])
def start_agent(agent_id):
    res = chainstream_core.start_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@agents_blueprint.route('/api/monitor/agents/stop/<agent_id>', methods=['POST'])
def stop_agent(agent_id):
    res = chainstream_core.stop_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})
