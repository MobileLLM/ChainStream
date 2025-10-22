"""
模拟传感器Agent - 生成会议室环境数据
支持四种测试模式：normal, learning, dynamic, emergency
"""

import chainstream as cs
import random
import time
import threading


class SimulatedSensorAgent(cs.agent.Agent):
    """模拟会议室传感器数据生成Agent"""
    is_agent = True
    
    def __init__(self, agent_id="simulated_sensor", mode="normal"):
        super().__init__(agent_id)
        self.mode = mode
        self.enabled = False
        self.sensor_thread = None
        
        # 创建传感器数据流
        self.sensor_data_stream = cs.create_stream(
            self, 
            "room_sensor_data_stream"
        )
        
    def start(self):
        """启动传感器数据生成"""
        self.enabled = True
        self.sensor_thread = threading.Thread(target=self._generate_data)
        self.sensor_thread.start()
        print(f"[传感器Agent] 已启动，模式: {self.mode}")
        
    def stop(self):
        """停止传感器"""
        self.enabled = False
        if self.sensor_thread:
            self.sensor_thread.join()
    
    def _generate_data(self):
        """根据模式生成数据"""
        if self.mode == "normal":
            self._generate_normal_data()
        elif self.mode == "learning":
            self._generate_learning_data()
        elif self.mode == "dynamic":
            self._generate_dynamic_data()
        elif self.mode == "emergency":
            self._generate_emergency_data()
    
    def _generate_normal_data(self):
        """模式1：正常稳定数据 - 用于基准测试"""
        print("\n" + "="*70)
        print("📡 [传感器] 模式：正常稳定数据生成 (Baseline测试)")
        print("="*70)
        
        for i in range(10):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": round(24 + random.uniform(-0.5, 0.5), 1),
                "humidity": round(50 + random.uniform(-3, 3), 1),
                "co2": 650 + random.randint(-50, 50),
                "people_count": 8,
                "ac_power": 60
            }
            
            print(f"\n[传感器] 时间={data['timestamp']} | "
                  f"温度={data['temperature']}°C | "
                  f"湿度={data['humidity']}% | "
                  f"CO2={data['co2']}ppm | "
                  f"人数={data['people_count']}人")
            
            self.sensor_data_stream.add_item(data)
            time.sleep(1)
    
    def _generate_learning_data(self):
        """模式2：包含用户反馈的数据 - 用于在线学习测试"""
        print("\n" + "="*70)
        print("📡 [传感器] 模式：包含用户反馈数据 (在线学习测试)")
        print("="*70)
        
        # 第一阶段：发送正常数据（学习前）
        print("\n--- 阶段1：学习前基准数据 ---")
        for i in range(3):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": 23.0,
                "humidity": 50.0,
                "co2": 600,
                "people_count": 10,
                "ac_power": 70
            }
            
            print(f"[传感器] 时间={data['timestamp']} | 温度={data['temperature']}°C (无反馈)")
            self.sensor_data_stream.add_item(data)
            time.sleep(1)
        
        # 第二阶段：发送带用户反馈的数据（触发学习）
        print("\n--- 阶段2：用户反馈触发 ---")
        feedback_data = {
            "timestamp": time.strftime("%H:%M:%S"),
            "temperature": 23.0,
            "humidity": 50.0,
            "co2": 600,
            "people_count": 10,
            "ac_power": 70,
            # 关键字段：用户反馈
            "user_feedback": "太冷了，能调高一点温度吗？",
            "user_preferred_temp": 25.5
        }
        
        print(f"\n⭐ [传感器] 发送用户反馈数据！")
        print(f"    💬 反馈内容: \"{feedback_data['user_feedback']}\"")
        print(f"    🎯 偏好温度: {feedback_data['user_preferred_temp']}°C")
        
        self.sensor_data_stream.add_item(feedback_data)
        time.sleep(1)
        
        # 第三阶段：发送更多数据验证学习效果
        print("\n--- 阶段3：学习后验证数据 ---")
        for i in range(5):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": round(24.0 + random.uniform(-0.3, 0.3), 1),
                "humidity": 50.0,
                "co2": 620 + random.randint(-20, 20),
                "people_count": 10,
                "ac_power": 65
            }
            
            print(f"[传感器] 时间={data['timestamp']} | 温度={data['temperature']}°C (学习后)")
            self.sensor_data_stream.add_item(data)
            time.sleep(1)
    
    def _generate_dynamic_data(self):
        """模式3：剧烈波动的数据 - 用于动态感知测试"""
        print("\n" + "="*70)
        print("📡 [传感器] 模式：环境剧烈波动数据 (动态感知测试)")
        print("="*70)
        print("模拟场景：会议突然开始，人数激增，温度和CO2快速上升\n")
        
        # 模拟会议开始，环境参数剧烈变化
        scenarios = [
            {"desc": "会议前-空房间", "temp": 23, "people": 2, "co2": 450, "ac": 40},
            {"desc": "少数人进入", "temp": 23.5, "people": 5, "co2": 500, "ac": 45},
            {"desc": "人数快速增加", "temp": 24.5, "people": 12, "co2": 650, "ac": 55},
            {"desc": "会议开始-满员", "temp": 26, "people": 18, "co2": 850, "ac": 65},
            {"desc": "温度继续升高", "temp": 27.5, "people": 18, "co2": 1100, "ac": 75},
            {"desc": "CO2超标", "temp": 28.5, "people": 18, "co2": 1300, "ac": 85},
            {"desc": "降温中", "temp": 27.5, "people": 18, "co2": 1150, "ac": 90},
            {"desc": "逐渐改善", "temp": 26, "people": 18, "co2": 950, "ac": 90},
        ]
        
        for i, scenario in enumerate(scenarios):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": scenario["temp"],
                "humidity": round(55 + random.uniform(-2, 2), 1),
                "co2": scenario["co2"],
                "people_count": scenario["people"],
                "ac_power": scenario["ac"]
            }
            
            # 计算变化量（如果不是第一条）
            change_marker = ""
            if i > 0:
                prev = scenarios[i-1]
                temp_change = data["temperature"] - prev["temp"]
                people_change = data["people_count"] - prev["people"]
                co2_change = data["co2"] - prev["co2"]
                
                if abs(temp_change) >= 1.5 or abs(people_change) >= 5 or abs(co2_change) >= 150:
                    change_marker = " ⚡ [剧烈变化]"
            
            print(f"\n[传感器] 场景: {scenario['desc']}{change_marker}")
            print(f"    时间={data['timestamp']} | 温度={data['temperature']}°C | "
                  f"人数={data['people_count']}人 | CO2={data['co2']}ppm")
            
            self.sensor_data_stream.add_item(data)
            time.sleep(1.2)
    
    def _generate_emergency_data(self):
        """模式4：突发设备故障 - 用于应急规划测试"""
        print("\n" + "="*70)
        print("📡 [传感器] 模式：突发设备故障数据 (应急规划测试)")
        print("="*70)
        print("模拟场景：空调系统突然故障，需要应急处置\n")
        
        # 第一阶段：正常运行
        print("--- 阶段1：设备正常运行 ---")
        for i in range(3):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": 24 + i * 0.3,
                "humidity": 52.0,
                "co2": 700,
                "people_count": 15,
                "ac_power": 70,
                "device_status": {
                    "ac_cooling": "normal",
                    "ventilation": "normal",
                    "windows": "closed"
                }
            }
            
            print(f"[传感器] 时间={data['timestamp']} | 温度={data['temperature']:.1f}°C | "
                  f"设备状态: 正常运行 ✓")
            
            self.sensor_data_stream.add_item(data)
            time.sleep(1)
        
        # 第二阶段：空调突然故障
        print("\n--- 阶段2：空调系统故障！---")
        fault_data = {
            "timestamp": time.strftime("%H:%M:%S"),
            "temperature": 25.5,
            "humidity": 56.0,
            "co2": 800,
            "people_count": 15,
            "ac_power": 0,  # 功率降为0表示故障
            "device_status": {
                "ac_cooling": "fault",  # 故障标记
                "ventilation": "normal",
                "windows": "closed"
            },
            "error_message": "空调压缩机故障，制冷功能失效"
        }
        
        print(f"\n🚨 [传感器] 设备故障警报！")
        print(f"    故障设备: 空调制冷系统")
        print(f"    错误信息: {fault_data['error_message']}")
        print(f"    当前温度: {fault_data['temperature']}°C | AC功率: {fault_data['ac_power']}%")
        
        self.sensor_data_stream.add_item(fault_data)
        time.sleep(1)
        
        # 第三阶段：故障后环境持续恶化
        print("\n--- 阶段3：环境持续恶化 ---")
        for i in range(5):
            if not self.enabled:
                break
                
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "temperature": round(25.5 + (i+1) * 0.7, 1),
                "humidity": round(56 + (i+1) * 2.5, 1),
                "co2": 800 + (i+1) * 150,
                "people_count": 15,
                "ac_power": 0,
                "device_status": {
                    "ac_cooling": "fault",
                    "ventilation": "normal",
                    "windows": "closed"
                }
            }
            
            warning = ""
            if data["temperature"] >= 28:
                warning += " 🌡️ 高温警告"
            if data["co2"] >= 1200:
                warning += " 💨 CO2危险"
            
            print(f"[传感器] 时间={data['timestamp']} | 温度={data['temperature']}°C↑ | "
                  f"CO2={data['co2']}ppm↑{warning}")
            
            self.sensor_data_stream.add_item(data)
            time.sleep(1)


if __name__ == '__main__':
    # 单独测试传感器Agent
    print("测试模拟传感器Agent")
    
    # 测试各种模式
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "normal"
    
    agent = SimulatedSensorAgent(mode=mode)
    agent.start()
    
    # 等待完成
    time.sleep(20)
    agent.stop()

