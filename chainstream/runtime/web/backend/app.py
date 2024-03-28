from flask import Flask, jsonify
from flask_cors import CORS
from chainstream.runtime.server_base import ChainStreamCore

app = Flask(__name__)

CORS(app, supports_credentials=True)

chainstream_core: ChainStreamCore = None


def set_core(core):
    global chainstream_core
    chainstream_core = core


@app.route('/', methods=['GET'])
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/api/home/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6677)
