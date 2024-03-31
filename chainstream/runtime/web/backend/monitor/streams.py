from ..core import chainstream_core
from flask import jsonify, Blueprint

streams_blueprint = Blueprint('streams_blueprint', __name__)


@streams_blueprint.route('/api/monitor/streams')
def get_streams():
    data = chainstream_core.stream_manager.get_stream_info()
    return jsonify(data)
