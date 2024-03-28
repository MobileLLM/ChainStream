from ..app import app, chainstream_core
from flask import jsonify


@app.route('/api/monitor/agents', methods=['GET'])
def get_predefined_agents():
    data = chainstream_core.scan_predefined_agents_tree()
    return jsonify(data)


@app.route('/api/monitor/agents/getRunningAgents', methods=['GET'])
def get_running_agents():
    data = chainstream_core.get_running_agents_info_list()
    return jsonify(data)


@app.route('/api/monitor/agents/start/<agent_id>', methods=['POST'])
def start_agent(agent_id):
    res = chainstream_core.start_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@app.route('/api/monitor/agents/stop/<agent_id>', methods=['POST'])
def stop_agent(agent_id):
    res = chainstream_core.stop_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})
