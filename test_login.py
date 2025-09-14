#!/usr/bin/env python3
"""
Test script to debug login issues
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chainstream.user import UserManager
import hashlib

def test_login():
    print("Testing UserManager login...")
    
    # Initialize user manager
    user_manager = UserManager()
    
    # Test with correct credentials
    username = "test"
    password = "123qwe123"
    
    print(f"Testing login with username: {username}")
    print(f"Password: {password}")
    
    # Calculate expected hash
    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"Expected password hash: {expected_hash}")
    
    # Get user by username
    user = user_manager.get_user_by_username(username)
    if user:
        print(f"Found user: {user.get_username()}")
        print(f"User password hash: {user.get_password_hash()}")
        print(f"Hash match: {user.get_password_hash() == expected_hash}")
    else:
        print("User not found!")
        return
    
    # Test login
    result = user_manager.login(username, password)
    if result:
        print("Login successful!")
        print(f"Logged in user: {result.get_username()}")
    else:
        print("Login failed!")

if __name__ == "__main__":
    test_login()
