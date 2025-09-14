from ..core import chainstream_core
from ..auth.auth import require_auth
from flask import jsonify, Blueprint

stream_graph_blueprint = Blueprint('stream_graph_blueprint', __name__)


@stream_graph_blueprint.route('/api/monitor/streamGraph', methods=['GET'])
@require_auth
def get_stream_graph(current_user):
    print(f"🔍 DEBUG: get_stream_graph - user: {current_user.get_username() if current_user else 'None'}")
    print(f"🔍 DEBUG: get_stream_graph - user level: {current_user.get_level() if current_user else 'None'}")
    print(f"🔍 DEBUG: get_stream_graph - user UUID: {current_user.get_uuid() if current_user else 'None'}")
    
    # 暂时绕过用户限制，获取所有stream信息用于调试
    print("🔍 DEBUG: === BYPASSING USER FILTER FOR DEBUG ===")
    all_streams = chainstream_core.stream_manager.get_stream_info()
    print(f"🔍 DEBUG: All streams count: {len(all_streams)}")
    for stream in all_streams:
        print(f"🔍 DEBUG: Stream: {stream}")
    
    node, edge = chainstream_core.get_graph_statistics(current_user)
    print(f"🔍 DEBUG: get_stream_graph - node count: {len(node)}, edge count: {len(edge)}")
    print(f"🔍 DEBUG: get_stream_graph - nodes: {node}")
    print(f"🔍 DEBUG: get_stream_graph - edges: {edge}")
    return jsonify({"node": node, "edge": edge})
