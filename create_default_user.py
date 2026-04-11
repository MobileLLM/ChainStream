#!/usr/bin/env python3
"""
Script to create a default user for ChainStream
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chainstream.user import UserManager

def create_default_user():
    """Create a default admin user"""
    user_manager = UserManager()
    
    # Create default admin user
    try:
        admin_user = user_manager.create_user(
            username="admin",
            password="admin123",
            level=10,  # Admin level
            enable_encryption=True
        )
        print(f"✅ Created default admin user:")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Level: 10 (Admin)")
        print(f"   UUID: {admin_user.get_uuid()}")
        
        # Also create a regular user
        regular_user = user_manager.create_user(
            username="user",
            password="user123",
            level=1,  # Regular user level
            enable_encryption=True
        )
        print(f"\n✅ Created default regular user:")
        print(f"   Username: user")
        print(f"   Password: user123")
        print(f"   Level: 1 (Regular)")
        print(f"   UUID: {regular_user.get_uuid()}")
        
        print(f"\n📁 Users saved to: {user_manager.users_file_path}")
        
    except ValueError as e:
        print(f"❌ Error creating user: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔧 Creating default users for ChainStream...")
    success = create_default_user()
    if success:
        print("\n🎉 Default users created successfully!")
        print("\nYou can now login to the web interface at http://127.0.0.1:6677")
    else:
        print("\n❌ Failed to create default users")
        sys.exit(1)
