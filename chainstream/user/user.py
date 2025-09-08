import datetime
import hashlib
import secrets
import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class User:
    """
        User class for dashboard, mainly used for project security check
    """
    def __init__(self, username, level, uuid=None, password_hash=None, encryption_key=None):
        if uuid is None:
            raise TypeError('uuid cannot be None')

        self._uuid = uuid
        self._level = level
        self._username = username
        self._password_hash = password_hash
        self._encryption_key = encryption_key
        self._encryption_enabled = encryption_key is not None

        self.create_at = datetime.datetime.now()

    def set_level(self, level):
        self._level = level

    def get_uuid(self):
        return self._uuid
    
    def get_username(self):
        return self._username
    
    def get_level(self):
        return self._level
    
    def get_password_hash(self):
        return self._password_hash
    
    def get_encryption_key(self):
        return self._encryption_key
    
    def is_encryption_enabled(self):
        return self._encryption_enabled
    
    def set_encryption_key(self, key):
        self._encryption_key = key
        self._encryption_enabled = key is not None
    
    def generate_encryption_key(self, password=None):
        """Generate a new encryption key for this user"""
        if password is None:
            # Generate a random key
            key = Fernet.generate_key()
        else:
            # Derive key from password
            salt = secrets.token_bytes(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        self._encryption_key = key
        self._encryption_enabled = True
        return key
    
    def encrypt_data(self, data):
        """Encrypt data using user's encryption key"""
        if not self._encryption_enabled:
            return data
        
        try:
            f = Fernet(self._encryption_key)
            if isinstance(data, str):
                data = data.encode()
            elif isinstance(data, dict):
                data = json.dumps(data).encode()
            return f.encrypt(data)
        except Exception as e:
            raise ValueError(f"Encryption failed: {e}")
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data using user's encryption key"""
        if not self._encryption_enabled:
            return encrypted_data
        
        try:
            f = Fernet(self._encryption_key)
            decrypted = f.decrypt(encrypted_data)
            # Try to decode as JSON first, then as string
            try:
                return json.loads(decrypted.decode())
            except:
                return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    def to_dict(self):
        """Convert user to dictionary for storage"""
        return {
            'uuid': str(self._uuid),
            'username': self._username,
            'level': self._level,
            'password_hash': self._password_hash,
            'encryption_key': self._encryption_key.decode() if self._encryption_key else None,
            'create_at': self.create_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user from dictionary"""
        encryption_key = data.get('encryption_key')
        if encryption_key:
            encryption_key = encryption_key.encode()
        
        user = cls(
            username=data['username'],
            level=data['level'],
            uuid=data['uuid'],
            password_hash=data.get('password_hash'),
            encryption_key=encryption_key
        )
        user.create_at = datetime.datetime.fromisoformat(data['create_at'])
        return user
