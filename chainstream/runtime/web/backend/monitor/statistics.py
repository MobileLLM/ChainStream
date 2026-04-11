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
        print(f"🔍 DEBUG: get_statistics - user: {current_user.get_username() if current_user else 'None'}")
        print(f"🔍 DEBUG: get_statistics - user level: {current_user.get_level() if current_user else 'None'}")
        print(f"🔍 DEBUG: get_statistics - user UUID: {current_user.get_uuid() if current_user else 'None'}")
        
        # 暂时绕过用户限制，获取所有信息用于调试
        print("🔍 DEBUG: === BYPASSING USER FILTER FOR DEBUG ===")
        all_agents = chainstream_core.agent_manager.get_running_agents_info_list(None)
        all_streams = chainstream_core.stream_manager.get_stream_info()
        print(f"🔍 DEBUG: All agents count: {len(all_agents)}")
        print(f"🔍 DEBUG: All streams count: {len(all_streams)}")
        for agent in all_agents:
            print(f"🔍 DEBUG: Agent: {agent}")
        for stream in all_streams:
            print(f"🔍 DEBUG: Stream: {stream}")
        
        # Get running agents count
        running_agents = chainstream_core.agent_manager.get_running_agents_info_list(current_user)
        running_agents_count = len(running_agents)
        
        # Get active streams count
        streams = chainstream_core.stream_manager.get_stream_info_by_user(current_user)
        active_streams_count = len(streams)
        
        print(f"🔍 DEBUG: Filtered agents count: {running_agents_count}")
        print(f"🔍 DEBUG: Filtered streams count: {active_streams_count}")
        
        return jsonify({
            'running_agents_count': running_agents_count,
            'active_streams_count': active_streams_count
        })
    except Exception as e:
        print(f"🔍 DEBUG: Error in get_statistics: {e}")
        import traceback
        print(f"🔍 DEBUG: Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500
