from ..app import app, chainstream_core
from flask import jsonify

@app.route('/api/monitor/streams')
def get_streams():
    pass