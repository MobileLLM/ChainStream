from ..core import chainstream_core
from ..auth.auth import require_auth
from flask import jsonify, Blueprint

statistics_blueprint = Blueprint('statistics_blueprint', __name__)


@statistics_blueprint.route('/api/monitor/statistics', methods=['GET'])
@require_auth
def get_statistics(current_user):
    """
    Get system statistics (running agents count, active streams count)
    """
    try:
        # Get running agents count
        running_agents = chainstream_core.agent_manager.get_running_agents_info_list(current_user)
        running_agents_count = len(running_agents)
        
        # Get active streams count
        streams = chainstream_core.stream_manager.get_stream_info_by_user(current_user)
        active_streams_count = len(streams)
        
        return jsonify({
            'running_agents_count': running_agents_count,
            'active_streams_count': active_streams_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
