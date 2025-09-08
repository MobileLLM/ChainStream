"""
Authentication module for ChainStream Web API
"""
import jwt
import logging
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from chainstream.user import UserManager
from chainstream.user.user import User

logger = logging.getLogger(__name__)

# Global user manager instance
user_manager = UserManager()

# JWT configuration
JWT_SECRET_KEY = 'chainstream_jwt_secret_2024'  # In production, use environment variable
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


class AuthManager:
    """
    Manages user authentication and authorization
    """
    
    def __init__(self):
        self.user_manager = user_manager
    
    def generate_token(self, user: User) -> str:
        """
        Generate JWT token for user
        
        Args:
            user: User object
        
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user.get_uuid(),
            'username': user.get_username(),
            'level': user.get_level(),
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        logger.info(f"Generated token for user: {user.get_username()}")
        return token
    
    def verify_token(self, token: str) -> dict:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token string
        
        Returns:
            Token payload if valid, None if invalid
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    def get_current_user(self, token: str) -> User:
        """
        Get current user from token
        
        Args:
            token: JWT token string
        
        Returns:
            User object if valid, None if invalid
        """
        payload = self.verify_token(token)
        if payload is None:
            return None
        
        user_id = payload.get('user_id')
        if user_id is None:
            return None
        
        return self.user_manager.get_user(user_id)
    
    def login(self, username: str, password: str) -> dict:
        """
        Authenticate user login
        
        Args:
            username: Username
            password: Password
        
        Returns:
            Dictionary with success status and token/user info
        """
        user = self.user_manager.login(username, password)
        if user is None:
            return {
                'success': False,
                'message': 'Invalid username or password'
            }
        
        token = self.generate_token(user)
        return {
            'success': True,
            'token': token,
            'user': {
                'uuid': user.get_uuid(),
                'username': user.get_username(),
                'level': user.get_level(),
                'encryption_enabled': user.is_encryption_enabled()
            }
        }
    
    def register(self, username: str, password: str, level: int = 1) -> dict:
        """
        Register new user
        
        Args:
            username: Username
            password: Password
            level: User level
        
        Returns:
            Dictionary with success status and message
        """
        try:
            user = self.user_manager.create_user(username, password, level)
            return {
                'success': True,
                'message': 'User created successfully',
                'user': {
                    'uuid': user.get_uuid(),
                    'username': user.get_username(),
                    'level': user.get_level()
                }
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            return {
                'success': False,
                'message': 'Failed to create user'
            }


# Global auth manager instance
auth_manager = AuthManager()


def require_auth(f):
    """
    Decorator to require authentication for API endpoints
    
    Usage:
        @require_auth
        def protected_endpoint():
            # current_user is available in the function
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Verify token and get user
        current_user = auth_manager.get_current_user(token)
        if current_user is None:
            return jsonify({'message': 'Invalid or expired token'}), 401
        
        # Add current_user to kwargs
        kwargs['current_user'] = current_user
        return f(*args, **kwargs)
    
    return decorated_function


def require_admin(f):
    """
    Decorator to require admin privileges (level >= 10)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = kwargs.get('current_user')
        if current_user is None:
            return jsonify({'message': 'Authentication required'}), 401
        
        if current_user.get_level() < 10:
            return jsonify({'message': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
