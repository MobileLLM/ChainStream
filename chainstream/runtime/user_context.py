"""
User Context Manager for ChainStream
Provides thread-local user context management without modifying existing agent code
"""
import threading
import logging
from typing import Optional
from chainstream.user.user import User

logger = logging.getLogger(__name__)

class UserContextManager:
    """
    Thread-local user context manager that allows agents to access current user
    without requiring user parameter in their __init__ methods
    """
    
    def __init__(self):
        self._local = threading.local()
    
    def set_current_user(self, user: User) -> None:
        """
        Set the current user for this thread
        
        Args:
            user: User object to set as current user
        """
        self._local.current_user = user
        logger.debug(f"Set current user: {user.get_username() if user else None}")
    
    def get_current_user(self) -> Optional[User]:
        """
        Get the current user for this thread
        
        Returns:
            User object if set, None otherwise
        """
        return getattr(self._local, 'current_user', None)
    
    def clear_current_user(self) -> None:
        """
        Clear the current user for this thread
        """
        if hasattr(self._local, 'current_user'):
            delattr(self._local, 'current_user')
        logger.debug("Cleared current user")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically clear user context"""
        self.clear_current_user()

# Global user context manager instance
user_context_manager = UserContextManager()
