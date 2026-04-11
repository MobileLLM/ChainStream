#!/usr/bin/env python3
"""
进程管理器 - 确保所有子进程随主进程一起终止
"""

import subprocess
import signal
import sys
import os
import time
import threading
from pathlib import Path

class ProcessManager:
    def __init__(self):
        self.processes = []
        self.running = True
        
    def add_process(self, cmd, cwd=None, shell=False):
        """添加一个子进程"""
        print(f"启动进程: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        process = subprocess.Popen(
            cmd, 
            cwd=cwd, 
            shell=shell,
            preexec_fn=os.setsid if os.name != 'nt' else None  # 创建新的进程组
        )
        self.processes.append(process)
        return process
    
    def cleanup(self):
        """清理所有子进程"""
        print("正在清理所有子进程...")
        self.running = False
        
        for process in self.processes:
            if process.poll() is None:  # 进程还在运行
                print(f"终止进程 PID {process.pid}")
                try:
                    if os.name != 'nt':
                        # Unix 系统：终止整个进程组
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    else:
                        # Windows 系统
                        process.terminate()
                    
                    # 等待进程结束
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        # 强制杀死
                        if os.name != 'nt':
                            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                        else:
                            process.kill()
                        process.wait()
                        
                except ProcessLookupError:
                    # 进程已经不存在
                    pass
                except Exception as e:
                    print(f"清理进程时出错: {e}")
    
    def signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"收到信号 {signum}，正在清理...")
        self.cleanup()
        sys.exit(0)
    
    def monitor_processes(self):
        """监控进程状态"""
        while self.running:
            for i, process in enumerate(self.processes):
                if process.poll() is not None:
                    print(f"进程 {i} (PID {process.pid}) 已结束")
                    self.processes.pop(i)
                    break
            time.sleep(1)
    
    def run(self):
        """运行进程管理器"""
        # 设置信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # 启动主程序
            main_process = self.add_process([
                sys.executable, '-m', 'chainstream.runtime.start'
            ])
            
            # 等待主程序启动
            time.sleep(3)
            
            # 启动 Java Agent
            java_dir = Path(__file__).parent / "chainstream" / "runtime" / "java"
            java_cmd = [
                'java', '-Xms128m', '-Xmx512m', '-Djava.awt.headless=true',
                '-cp', 'target/classes',
                'com.chainstream.agent.DebugHelloAgent'
            ]
            
            # 添加 Maven 依赖到 classpath
            try:
                result = subprocess.run(
                    ['mvn', 'dependency:build-classpath', '-Dmdep.outputFile=/dev/stdout', '-q'],
                    cwd=java_dir,
                    capture_output=True,
                    text=True,
                    check=True
                )
                classpath = result.stdout.strip()
                java_cmd[4] = f"target/classes:{classpath}"
            except subprocess.CalledProcessError:
                print("警告：无法获取 Maven 依赖，使用默认 classpath")
            
            java_process = self.add_process(java_cmd, cwd=java_dir)
            
            print(f"主进程 PID: {main_process.pid}")
            print(f"Java Agent PID: {java_process.pid}")
            print("按 Ctrl+C 停止所有进程")
            
            # 监控进程
            self.monitor_processes()
            
        except KeyboardInterrupt:
            print("收到中断信号")
        finally:
            self.cleanup()

if __name__ == "__main__":
    manager = ProcessManager()
    manager.run()

