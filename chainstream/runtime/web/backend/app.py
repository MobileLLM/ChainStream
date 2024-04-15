from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
from .monitor.agents import agents_blueprint
from .monitor.streams import streams_blueprint
from .monitor.stream_graph import stream_graph_blueprint

absolute_path = os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent, 'frontend/dist')

app = Flask(__name__)
app.register_blueprint(agents_blueprint)
app.register_blueprint(streams_blueprint)
app.register_blueprint(stream_graph_blueprint)

CORS(app, supports_credentials=True)


@app.route('/', methods=['GET'])
def hello_world():
    return send_from_directory(absolute_path, 'index.html')


@app.route('/assets/<path>')
def serve_static(path):
    return send_from_directory(os.path.join(absolute_path, 'assets'), path)


@app.route('/api/home/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6677)
