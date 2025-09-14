#!/usr/bin/env python3
"""
生成gRPC Python代码
"""

import os
import subprocess
import sys

def generate_grpc_code():
    """生成gRPC Python代码"""
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_dir = os.path.join(current_dir, "..", "java", "proto")
    output_dir = os.path.join(current_dir, "..", "java")
    
    # 检查proto文件是否存在
    proto_file = os.path.join(proto_dir, "chainstream_bridge.proto")
    if not os.path.exists(proto_file):
        print(f"Error: Proto file not found: {proto_file}")
        return False
    
    # 生成Python gRPC代码
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        proto_file
    ]
    
    print(f"Generating gRPC Python code...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("gRPC Python code generated successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error generating gRPC code: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

if __name__ == "__main__":
    success = generate_grpc_code()
    if success:
        print("✅ gRPC code generation completed successfully!")
    else:
        print("❌ gRPC code generation failed!")
        sys.exit(1)
