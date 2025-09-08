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
    # Get streams filtered by current user
    data = chainstream_core.stream_manager.get_stream_info_by_user(current_user)
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
