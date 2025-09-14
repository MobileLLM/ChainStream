from ..core import chainstream_core
from ..auth.auth import require_auth
from chainstream.runtime.user_context import user_context_manager
from flask import jsonify, Blueprint
import logging

logger = logging.getLogger(__name__)

agents_blueprint = Blueprint('agents_blueprint', __name__)


@agents_blueprint.route('/api/monitor/agents', methods=['GET'])
@require_auth
def get_predefined_agents(current_user):
    """
    Get predefined agents (filtered by user level)
    """
    data = chainstream_core.scan_predefined_agents_tree()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/getRunningAgents', methods=['GET'])
@require_auth
def get_running_agents(current_user):
    """
    Get running agents (filtered by user)
    """
    logger.info(f"get_running_agents API called with current_user: {current_user}")
    if current_user:
        logger.info(f"Current user UUID: {current_user.get_uuid()}")
    else:
        logger.info("Current user is None!")
    
    # Get agents filtered by current user
    data = chainstream_core.agent_manager.get_running_agents_info_list(current_user)
    logger.info(f"Returning {len(data)} agents")
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/all', methods=['GET'])
@require_auth
def get_all_running_agents(current_user):
    """
    Get all running agents (admin only)
    """
    # Check if user has admin privileges
    if current_user.get_level() < 10:
        return jsonify({'message': 'Admin privileges required'}), 403
    
    # Get all agents without filtering
    data = chainstream_core.agent_manager.get_running_agents_info_list()
    return jsonify(data)


@agents_blueprint.route('/api/monitor/agents/start/<agent_id>', methods=['POST'])
@require_auth
def start_agent(agent_id, current_user):
    # Set user context before starting agent - don't use with statement to avoid clearing context
    user_context_manager.set_current_user(current_user)
    res = chainstream_core.start_agent_by_id(agent_id, current_user)

    return jsonify({'res': "ok"} if res else {'res': "error"})


@agents_blueprint.route('/api/monitor/agents/stop/<agent_id>', methods=['POST'])
@require_auth
def stop_agent(agent_id, current_user):
    res = chainstream_core.stop_agent_by_id(agent_id, current_user)

    return jsonify({'res': "ok"} if res else {'res': "error"})
