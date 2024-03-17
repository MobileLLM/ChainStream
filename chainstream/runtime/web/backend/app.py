from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, supports_credentials=True)

chainstream_core = None


def set_core(core):
    global chainstream_core
    chainstream_core = core


@app.route('/api/monitor/agents', methods=['GET'])
def get_data():
    data = chainstream_core.scan_predefined_agents_tree()
    return jsonify(data)

@app.route('/api/monitor/agents/start/<agent_id>', methods=['POST'])
def start_agent(agent_id):
    res = chainstream_core.start_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@app.route('/api/monitor/agents/stop/<agent_id>', methods=['POST'])
def stop_agent(agent_id):
    res = chainstream_core.stop_agent_by_id(agent_id)

    return jsonify({'res': "ok"} if res else {'res': "error"})

@app.route('/', methods=['GET'])
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/api/home/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6677)
