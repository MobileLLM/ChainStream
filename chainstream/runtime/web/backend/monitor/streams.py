from ..core import chainstream_core
from ..auth.auth import require_auth
from flask import jsonify, Blueprint

streams_blueprint = Blueprint('streams_blueprint', __name__)


@streams_blueprint.route('/api/monitor/streams')
@require_auth
def get_streams(current_user):
    """
    Get streams (filtered by user)
    """
    print(f"🔍 DEBUG: get_streams - user: {current_user.get_username() if current_user else 'None'}")
    print(f"🔍 DEBUG: get_streams - user level: {current_user.get_level() if current_user else 'None'}")
    print(f"🔍 DEBUG: get_streams - user UUID: {current_user.get_uuid() if current_user else 'None'}")
    
    # 暂时绕过用户限制，获取所有stream信息用于调试
    print("🔍 DEBUG: === BYPASSING USER FILTER FOR DEBUG ===")
    all_streams = chainstream_core.stream_manager.get_stream_info()
    print(f"🔍 DEBUG: All streams count: {len(all_streams)}")
    for stream in all_streams:
        print(f"🔍 DEBUG: Stream: {stream}")
    
    # Get streams filtered by current user
    data = chainstream_core.stream_manager.get_stream_info_by_user(current_user)
    print(f"🔍 DEBUG: Filtered streams count: {len(data)}")
    print(f"🔍 DEBUG: Filtered streams: {data}")
    return jsonify(data)


@streams_blueprint.route('/api/monitor/streams/all')
@require_auth
def get_all_streams(current_user):
    """
    Get all streams (admin only)
    """
    # Check if user has admin privileges
    if current_user.get_level() < 10:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Get all streams without filtering
    data = chainstream_core.stream_manager.get_stream_info()
    return jsonify(data)
