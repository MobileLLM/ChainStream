import uuid
import json
import os
import hashlib
import logging
from pathlib import Path

from .user import User

logger = logging.getLogger(__name__)


class UserManager:
    def __init__(self, users_file_path=None):
        self._all_users = {}
        self.users_file_path = users_file_path or os.path.join(os.getcwd(), 'users.json')
        self._load_users()

    def __len__(self):
        return len(self._all_users)

    def _load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file_path):
            try:
                with open(self.users_file_path, 'r') as f:
                    users_data = json.load(f)
                    for user_data in users_data:
                        user = User.from_dict(user_data)
                        self._all_users[user.get_uuid()] = user
                logger.info(f"Loaded {len(self._all_users)} users from {self.users_file_path}")
            except Exception as e:
                logger.error(f"Failed to load users: {e}")
        else:
            logger.info("No users file found, starting with empty user database")

    def _save_users(self):
        """Save users to JSON file"""
        try:
            users_data = [user.to_dict() for user in self._all_users.values()]
            with open(self.users_file_path, 'w') as f:
                json.dump(users_data, f, indent=2)
            logger.info(f"Saved {len(self._all_users)} users to {self.users_file_path}")
        except Exception as e:
            logger.error(f"Failed to save users: {e}")

    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, level=1, enable_encryption=True):
        """Create a new user with password"""
        # Check if username already exists
        for user in self._all_users.values():
            if user.get_username() == username:
                raise ValueError(f"Username '{username}' already exists")
        
        tmp_uuid = str(uuid.uuid4())
        password_hash = self._hash_password(password)
        
        new_user = User(
            username=username, 
            level=level, 
            uuid=tmp_uuid,
            password_hash=password_hash
        )
        
        if enable_encryption:
            new_user.generate_encryption_key()
        
        self._all_users[tmp_uuid] = new_user
        self._save_users()
        
        logger.info(f"Created new user: {username}")
        return new_user

    def get_user(self, uuid):
        """Get user by UUID"""
        return self._all_users.get(uuid)

    def get_user_by_username(self, username):
        """Get user by username"""
        for user in self._all_users.values():
            if user.get_username() == username:
                return user
        return None

    def set_level(self, uuid, level):
        """Set user level"""
        if uuid in self._all_users:
            self._all_users[uuid].set_level(level)
            self._save_users()

    def destroy_user(self, uuid):
        """Remove user"""
        if uuid in self._all_users:
            username = self._all_users[uuid].get_username()
            self._all_users.pop(uuid, None)
            self._save_users()
            logger.info(f"Destroyed user: {username}")

    def login(self, username, password) -> User:
        """Authenticate user login"""
        user = self.get_user_by_username(username)
        if user is None:
            logger.warning(f"Login attempt with non-existent username: {username}")
            return None
        
        password_hash = self._hash_password(password)
        if user.get_password_hash() == password_hash:
            logger.info(f"Successful login for user: {username}")
            return user
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return None

    def change_password(self, uuid, old_password, new_password):
        """Change user password"""
        user = self.get_user(uuid)
        if user is None:
            return False
        
        old_hash = self._hash_password(old_password)
        if user.get_password_hash() != old_hash:
            return False
        
        user._password_hash = self._hash_password(new_password)
        self._save_users()
        logger.info(f"Password changed for user: {user.get_username()}")
        return True

    def get_all_users(self):
        """Get all users (for admin purposes)"""
        return list(self._all_users.values())

    def enable_encryption(self, uuid, password=None):
        """Enable encryption for user"""
        user = self.get_user(uuid)
        if user is None:
            return False
        
        user.generate_encryption_key(password)
        self._save_users()
        logger.info(f"Encryption enabled for user: {user.get_username()}")
        return True

    def disable_encryption(self, uuid):
        """Disable encryption for user"""
        user = self.get_user(uuid)
        if user is None:
            return False
        
        user.set_encryption_key(None)
        self._save_users()
        logger.info(f"Encryption disabled for user: {user.get_username()}")
        return True






