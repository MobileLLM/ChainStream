"""
Authentication routes for ChainStream Web API
"""
from flask import Blueprint, request, jsonify
from .auth import auth_manager, require_auth

auth_blueprint = Blueprint('auth_blueprint', __name__)


@auth_blueprint.route('/api/auth/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Expected JSON payload:
    {
        "username": "string",
        "password": "string"
    }
    
    Returns:
    {
        "success": bool,
        "token": "string" (if success),
        "user": {...} (if success),
        "message": "string" (if error)
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        result = auth_manager.login(username, password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@auth_blueprint.route('/api/auth/register', methods=['POST'])
def register():
    """
    User registration endpoint
    
    Expected JSON payload:
    {
        "username": "string",
        "password": "string",
        "level": int (optional, default: 1)
    }
    
    Returns:
    {
        "success": bool,
        "user": {...} (if success),
        "message": "string"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        level = data.get('level', 1)
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        if not isinstance(level, int) or level < 1:
            return jsonify({
                'success': False,
                'message': 'Level must be a positive integer'
            }), 400
        
        result = auth_manager.register(username, password, level)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@auth_blueprint.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user(current_user):
    """
    Get current user information
    
    Requires: Authorization header with Bearer token
    
    Returns:
    {
        "success": bool,
        "user": {
            "uuid": "string",
            "username": "string",
            "level": int,
            "encryption_enabled": bool
        }
    }
    """
    return jsonify({
        'success': True,
        'user': {
            'uuid': current_user.get_uuid(),
            'username': current_user.get_username(),
            'level': current_user.get_level(),
            'encryption_enabled': current_user.is_encryption_enabled()
        }
    }), 200


@auth_blueprint.route('/api/auth/change-password', methods=['POST'])
@require_auth
def change_password(current_user):
    """
    Change user password
    
    Expected JSON payload:
    {
        "old_password": "string",
        "new_password": "string"
    }
    
    Returns:
    {
        "success": bool,
        "message": "string"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return jsonify({
                'success': False,
                'message': 'Old password and new password are required'
            }), 400
        
        success = auth_manager.user_manager.change_password(
            current_user.get_uuid(), 
            old_password, 
            new_password
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Password changed successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid old password'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@auth_blueprint.route('/api/auth/enable-encryption', methods=['POST'])
@require_auth
def enable_encryption(current_user):
    """
    Enable encryption for current user
    
    Expected JSON payload:
    {
        "password": "string" (optional, for password-based key derivation)
    }
    
    Returns:
    {
        "success": bool,
        "message": "string"
    }
    """
    try:
        data = request.get_json() or {}
        password = data.get('password')
        
        success = auth_manager.user_manager.enable_encryption(
            current_user.get_uuid(), 
            password
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Encryption enabled successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to enable encryption'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@auth_blueprint.route('/api/auth/disable-encryption', methods=['POST'])
@require_auth
def disable_encryption(current_user):
    """
    Disable encryption for current user
    
    Returns:
    {
        "success": bool,
        "message": "string"
    }
    """
    try:
        success = auth_manager.user_manager.disable_encryption(
            current_user.get_uuid()
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Encryption disabled successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to disable encryption'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
