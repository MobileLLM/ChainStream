from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app, supports_credentials=True)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "chartdata": [
            {"name": 'a'},
            {"name": 'b'},
            {"name": 'a1'},
            {"name": 'b1'},
            {"name": 'c'},
            {"name": 'e'}
        ],
        "chartlinks": [
            {"source": 'a', "target": 'a1', "value": 5},
            {"source": 'e', "target": 'b', "value": 3},
            {"source": 'a', "target": 'b1', "value": 3},
            {"source": 'b1', "target": 'a1', "value": 1},
            {"source": 'b1', "target": 'c', "value": 2},
            {"source": 'b', "target": 'c', "value": 1}
        ]
    }
    return jsonify(data)


@app.route('/', methods=['GET'])
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route('/api/home/checkConnection', methods=['GET'])
def check_connection():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=6677)
