from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {
        "chartdata": [
            { "name": 'a' },
            { "name": 'b' },
            { "name": 'a1' },
            { "name": 'b1' },
            { "name": 'c' },
            { "name": 'e' }
        ],
        "chartlinks": [
            { "source": 'a', "target": 'a1', "value": 5 },
            { "source": 'e', "target": 'b', "value": 3 },
            { "source": 'a', "target": 'b1', "value": 3 },
            { "source": 'b1', "target": 'a1', "value": 1 },
            { "source": 'b1', "target": 'c', "value": 2 },
            { "source": 'b', "target": 'c', "value": 1 }
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

