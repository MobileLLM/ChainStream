from flask import Flask, jsonify
from flask_cors import CORS
# from chainstream.runtime.runtime_core import RuntimeCore
from .monitor.agents import agents_blueprint
from .monitor.streams import streams_blueprint
from .monitor.stream_graph import stream_graph_blueprint

app = Flask(__name__)
app.register_blueprint(agents_blueprint)
app.register_blueprint(streams_blueprint)
app.register_blueprint(stream_graph_blueprint)

CORS(app, supports_credentials=True)


@app.route('/', methods=['GET'])
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/api/home/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6677)
