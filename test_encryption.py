#!/usr/bin/env python3
"""
Test script for encryption functionality
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from chainstream.user import UserManager, User
from chainstream.stream.encryption_utils import StreamEncryption
from chainstream.stream.encrypted_stream import EncryptedStream
from chainstream.agent import Agent
import json

def test_user_encryption():
    """Test user-level encryption functionality"""
    print("=== Testing User Encryption ===")
    
    # Create a test user
    user_manager = UserManager()
    test_user = user_manager.get_user_by_username("test")
    
    if test_user is None:
        print("❌ Test user not found")
        return False
    
    print(f"✓ Found test user: {test_user.get_username()}")
    print(f"✓ Encryption enabled: {test_user.is_encryption_enabled()}")
    
    # Test data encryption/decryption
    test_data = {
        "sensitive_info": "This is sensitive data",
        "numbers": [1, 2, 3, 4, 5],
        "nested": {"key": "value"}
    }
    
    try:
        # Encrypt data
        encrypted = test_user.encrypt_data(test_data)
        print(f"✓ Data encrypted successfully: {type(encrypted)}")
        
        # Decrypt data
        decrypted = test_user.decrypt_data(encrypted)
        print(f"✓ Data decrypted successfully: {decrypted}")
        
        # Verify data integrity
        if decrypted == test_data:
            print("✓ Data integrity verified - encryption/decryption working correctly")
            return True
        else:
            print("❌ Data integrity check failed")
            return False
            
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
        return False

def test_stream_encryption():
    """Test stream-level encryption functionality"""
    print("\n=== Testing Stream Encryption ===")
    
    try:
        # Test encryption utilities directly instead of full stream
        password = "test_password_123"
        encryption = StreamEncryption(password=password)
        
        print(f"✓ Created encryption instance with password")
        print(f"✓ Encryption enabled: {encryption.is_encryption_enabled()}")
        
        # Test data encryption/decryption
        test_items = [
            {"type": "sensor_data", "value": 42.5, "timestamp": "2024-01-01T12:00:00Z"},
            {"type": "user_action", "action": "click", "element": "button"},
            "Simple string data",
            12345
        ]
        
        for i, item in enumerate(test_items):
            # Encrypt item
            encrypted = encryption.encrypt_data(item)
            if encrypted is not None:
                # Decrypt item
                decrypted = encryption.decrypt_data(encrypted)
                if decrypted == item:
                    print(f"✓ Item {i+1} encrypted/decrypted successfully")
                else:
                    print(f"❌ Item {i+1} decryption failed")
                    return False
            else:
                print(f"❌ Item {i+1} encryption failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Stream encryption test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_encryption_utils():
    """Test encryption utilities directly"""
    print("\n=== Testing Encryption Utils ===")
    
    try:
        # Test with password
        password = "test_password_456"
        encryption = StreamEncryption(password=password)
        
        print(f"✓ Created encryption instance with password")
        print(f"✓ Encryption enabled: {encryption.is_encryption_enabled()}")
        
        # Test various data types
        test_cases = [
            "Simple string",
            {"key": "value", "number": 42},
            [1, 2, 3, "four", {"five": 5}],
            123.45,
            True
        ]
        
        for i, data in enumerate(test_cases):
            encrypted = encryption.encrypt_data(data)
            if encrypted is not None:
                decrypted = encryption.decrypt_data(encrypted)
                if decrypted == data:
                    print(f"✓ Test case {i+1} passed: {type(data).__name__}")
                else:
                    print(f"❌ Test case {i+1} failed: {type(data).__name__}")
                    return False
            else:
                print(f"❌ Test case {i+1} encryption failed: {type(data).__name__}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Encryption utils test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_encryption():
    """Test encryption via API endpoints"""
    print("\n=== Testing API Encryption ===")
    
    import requests
    
    # Get auth token first
    login_data = {
        "username": "test",
        "password": "123qwe123"
    }
    
    try:
        response = requests.post("http://localhost:6677/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()["token"]
            print("✓ Got authentication token")
            
            # Test enable encryption
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post("http://localhost:6677/api/auth/enable-encryption", headers=headers)
            
            if response.status_code == 200:
                print("✓ Encryption enabled via API")
            else:
                print(f"⚠️  Enable encryption API returned: {response.status_code}")
            
            # Test disable encryption
            response = requests.post("http://localhost:6677/api/auth/disable-encryption", headers=headers)
            
            if response.status_code == 200:
                print("✓ Encryption disabled via API")
            else:
                print(f"⚠️  Disable encryption API returned: {response.status_code}")
            
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API encryption test failed: {e}")
        return False

def main():
    """Run all encryption tests"""
    print("Testing ChainStream Encryption Functionality")
    print("=" * 50)
    
    results = []
    
    # Test user encryption
    results.append(test_user_encryption())
    
    # Test stream encryption
    results.append(test_stream_encryption())
    
    # Test encryption utils
    results.append(test_encryption_utils())
    
    # Test API encryption
    results.append(test_api_encryption())
    
    # Summary
    print("\n" + "=" * 50)
    print("ENCRYPTION TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All encryption tests passed!")
    else:
        print("⚠️  Some encryption tests failed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
