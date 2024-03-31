from ..core import chainstream_core
from flask import jsonify, Blueprint

stream_graph_blueprint = Blueprint('stream_graph_blueprint', __name__)


@stream_graph_blueprint.route('/api/monitor/streamGraph', methods=['GET'])
def get_stream_graph():
    # print("Getting stream graph statistics")
    node, edge = chainstream_core.get_graph_statistics()
    print(node, edge)
    return jsonify({"node": node, "edge": edge})
