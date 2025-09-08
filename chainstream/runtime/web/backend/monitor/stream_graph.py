from ..core import chainstream_core
from ..auth.auth import require_auth
from flask import jsonify, Blueprint

stream_graph_blueprint = Blueprint('stream_graph_blueprint', __name__)


@stream_graph_blueprint.route('/api/monitor/streamGraph', methods=['GET'])
@require_auth
def get_stream_graph(current_user):
    node, edge = chainstream_core.get_graph_statistics(current_user)
    print(f"DEBUG: get_stream_graph - user: {current_user.get_username() if current_user else 'None'}")
    print(f"DEBUG: get_stream_graph - node count: {len(node)}, edge count: {len(edge)}")
    print(f"DEBUG: get_stream_graph - nodes: {node}")
    print(f"DEBUG: get_stream_graph - edges: {edge}")
    return jsonify({"node": node, "edge": edge})
