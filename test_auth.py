#!/usr/bin/env python3
"""
Test script to debug authentication flow
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chainstream.user import UserManager
from chainstream.runtime.web.backend.auth.auth import AuthManager
import traceback

def test_auth_flow():
    print("Testing complete authentication flow...")
    
    try:
        # Initialize managers
        user_manager = UserManager()
        auth_manager = AuthManager()
        
        # Test credentials
        username = "test"
        password = "123qwe123"
        
        print(f"Testing authentication with username: {username}")
        
        # Test user manager login
        print("\n1. Testing UserManager.login()...")
        user = user_manager.login(username, password)
        if user:
            print(f"✓ UserManager login successful: {user.get_username()}")
        else:
            print("✗ UserManager login failed!")
            return
        
        # Test auth manager login
        print("\n2. Testing AuthManager.login()...")
        result = auth_manager.login(username, password)
        print(f"AuthManager result: {result}")
        
        if result['success']:
            print("✓ AuthManager login successful!")
            print(f"Token: {result['token'][:50]}...")
            print(f"User info: {result['user']}")
        else:
            print(f"✗ AuthManager login failed: {result['message']}")
            
    except Exception as e:
        print(f"✗ Error during authentication test: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_auth_flow()
