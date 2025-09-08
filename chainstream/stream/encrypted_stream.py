"""
Encrypted Stream implementation
"""
import logging
import threading
from typing import Any, Optional

from .base_stream import BaseStream, StreamMeta
from .encryption_utils import StreamEncryption, EncryptedItem
from chainstream.user.user import User

logger = logging.getLogger(__name__)


class EncryptedStream(BaseStream):
    """
    Stream with encryption support for data items
    """
    
    def __init__(self, stream_id: str, description: str = None, 
                 create_by_agent_file: str = None, is_anonymous: bool = False, 
                 user: Optional[User] = None, encryption_key: Optional[bytes] = None,
                 password: Optional[str] = None):
        """
        Initialize encrypted stream
        
        Args:
            stream_id: Unique stream identifier
            description: Stream description
            create_by_agent_file: File path of agent that created this stream
            is_anonymous: Whether stream is anonymous
            user: User who owns this stream
            encryption_key: Pre-generated encryption key
            password: Password to derive encryption key from
        """
        super().__init__(stream_id, description, create_by_agent_file, is_anonymous, user)
        
        # Initialize encryption
        self.encryption = StreamEncryption(encryption_key=encryption_key, password=password)
        self.encryption_enabled = self.encryption.is_encryption_enabled()
        
        # Override metadata to include encryption info
        self.metaData = StreamMeta(
            stream_id=stream_id,
            description=description,
            create_by_agent_file=create_by_agent_file,
            is_anonymous=is_anonymous,
            user=user
        )
        
        # Add encryption metadata
        self.metaData.encryption_enabled = self.encryption_enabled
        
        logger.info(f"Created encrypted stream '{stream_id}' with encryption: {self.encryption_enabled}")
    
    def add_item(self, agent, item: Any):
        """
        Add item to stream with encryption
        
        Args:
            agent: Agent adding the item
            item: Item to add (will be encrypted if encryption is enabled)
        """
        if self.encryption_enabled:
            # Encrypt the item before adding to queue
            encrypted_data = self.encryption.encrypt_data(item)
            if encrypted_data is not None:
                encrypted_item = EncryptedItem(encrypted_data, is_encrypted=True)
                super().add_item(agent, encrypted_item)
            else:
                logger.error(f"Failed to encrypt item for stream {self.stream_id}")
                # Fallback: add unencrypted item
                super().add_item(agent, item)
        else:
            # No encryption, add item as-is
            super().add_item(agent, item)
    
    def process_item(self):
        """
        Process items from queue with decryption
        """
        while True:
            item = self.queue.get()
            
            if item is self.STOP_SIGNAL:
                break
            
            if item is not None:
                self.logger.debug(f'stream {self.metaData.stream_id} process an item type: {type(item)}')
                self.is_clear.clear()
                
                # Decrypt item if it's encrypted
                processed_item = self._process_item_for_listeners(item)
                
                # Send to all receivers
                for recv_queue in self.recv_queue_list:
                    recv_queue.put(processed_item)
                    self.recorder.record_send_item("fake_agent_for_stream_interface",
                                                   "fake_listener_func_for_stream_interface")
                
                # Send to all listeners
                for agent_, listener_func_ in self.listeners:
                    listener_func_(processed_item)
                    self.recorder.record_send_item(agent_, listener_func_.func_id)
                
                self.is_clear.set()
    
    def _process_item_for_listeners(self, item: Any) -> Any:
        """
        Process item for listeners (decrypt if needed)
        
        Args:
            item: Item to process
        
        Returns:
            Processed item (decrypted if it was encrypted)
        """
        if isinstance(item, EncryptedItem) and item.is_encrypted:
            # Decrypt the item
            decrypted_data = self.encryption.decrypt_data(item.encrypted_data)
            if decrypted_data is not None:
                return decrypted_data
            else:
                logger.error(f"Failed to decrypt item for stream {self.stream_id}")
                return item  # Return original item if decryption fails
        else:
            # Item is not encrypted, return as-is
            return item
    
    def get_meta_data(self):
        """
        Get stream metadata including encryption info
        
        Returns:
            Dictionary containing stream metadata
        """
        data = super().get_meta_data()
        data['encryption_enabled'] = self.encryption_enabled
        return data
    
    def enable_encryption(self, encryption_key: Optional[bytes] = None, password: Optional[str] = None):
        """
        Enable encryption for this stream
        
        Args:
            encryption_key: Pre-generated encryption key
            password: Password to derive encryption key from
        """
        self.encryption = StreamEncryption(encryption_key=encryption_key, password=password)
        self.encryption_enabled = self.encryption.is_encryption_enabled()
        self.metaData.encryption_enabled = self.encryption_enabled
        
        logger.info(f"Encryption enabled for stream {self.stream_id}")
    
    def disable_encryption(self):
        """
        Disable encryption for this stream
        """
        self.encryption = StreamEncryption()
        self.encryption_enabled = False
        self.metaData.encryption_enabled = False
        
        logger.info(f"Encryption disabled for stream {self.stream_id}")
    
    def is_encrypted(self) -> bool:
        """
        Check if encryption is enabled
        
        Returns:
            True if encryption is enabled, False otherwise
        """
        return self.encryption_enabled
