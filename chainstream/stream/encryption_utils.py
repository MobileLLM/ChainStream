"""
Encryption utilities for Stream data
"""
import base64
import json
import logging
from typing import Any, Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)


class StreamEncryption:
    """
    Handles encryption and decryption of stream data
    """
    
    def __init__(self, encryption_key: Optional[bytes] = None, password: Optional[str] = None):
        """
        Initialize encryption with either a key or password
        
        Args:
            encryption_key: Pre-generated encryption key (bytes)
            password: Password to derive key from (str)
        """
        if encryption_key:
            self.fernet = Fernet(encryption_key)
        elif password:
            self.fernet = Fernet(self._derive_key_from_password(password))
        else:
            self.fernet = None
    
    def _derive_key_from_password(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: Password string
            salt: Salt bytes (if None, will generate new salt)
        
        Returns:
            Derived encryption key
        """
        if salt is None:
            salt = b'chainstream_salt_2024'  # Fixed salt for consistency
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data: Any) -> Optional[bytes]:
        """
        Encrypt stream data
        
        Args:
            data: Data to encrypt (any serializable type)
        
        Returns:
            Encrypted data as bytes, or None if encryption is disabled
        """
        if self.fernet is None:
            return None
        
        try:
            # Serialize data to JSON string
            if isinstance(data, (str, int, float, bool, list, dict)):
                json_data = json.dumps(data, ensure_ascii=False)
            else:
                # For complex objects, try to serialize as string
                json_data = json.dumps(str(data), ensure_ascii=False)
            
            # Encrypt the JSON string
            encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))
            return encrypted_data
            
        except Exception as e:
            logger.error(f"Failed to encrypt data: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: bytes) -> Optional[Any]:
        """
        Decrypt stream data
        
        Args:
            encrypted_data: Encrypted data as bytes
        
        Returns:
            Decrypted data, or None if decryption fails
        """
        if self.fernet is None:
            return None
        
        try:
            # Decrypt the data
            decrypted_bytes = self.fernet.decrypt(encrypted_data)
            json_data = decrypted_bytes.decode('utf-8')
            
            # Deserialize from JSON
            data = json.loads(json_data)
            return data
            
        except Exception as e:
            logger.error(f"Failed to decrypt data: {e}")
            return None
    
    def is_encryption_enabled(self) -> bool:
        """
        Check if encryption is enabled
        
        Returns:
            True if encryption is enabled, False otherwise
        """
        return self.fernet is not None


class EncryptedItem:
    """
    Wrapper for encrypted stream items
    """
    
    def __init__(self, encrypted_data: bytes, is_encrypted: bool = True):
        self.encrypted_data = encrypted_data
        self.is_encrypted = is_encrypted
    
    def __str__(self):
        if self.is_encrypted:
            return f"<EncryptedItem: {len(self.encrypted_data)} bytes>"
        else:
            return str(self.encrypted_data)
    
    def __repr__(self):
        return self.__str__()
