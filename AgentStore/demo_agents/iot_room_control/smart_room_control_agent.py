"""
智能会议室控制Agent - 根据传感器数据智能调节环境
具备在线学习、动态感知、应急规划三大核心能力
"""

import chainstream as cs
import time


class SmartRoomControlAgent(cs.agent.Agent):
    """智能会议室环境控制Agent"""
    is_agent = True
    
    def __init__(self, agent_id="smart_room_control"):
        super().__init__(agent_id)
        
        # === 内部状态变量（使用普通变量，不用cs.memory）===
        self.target_temperature = 23.0      # 默认目标温度
        self.learned_preferences = {}       # 学习到的用户偏好
        self.last_data = None               # 上一次的数据
        self.decision_count = 0             # 决策计数
        self.learning_history = []          # 学习历史记录
        
        # === 环境阈值配置 ===
        self.CO2_WARNING = 1000   # CO2警告阈值
        self.CO2_DANGER = 1200    # CO2危险阈值
        self.TEMP_WARNING = 27    # 温度警告阈值
        self.TEMP_DANGER = 29     # 温度危险阈值
        
        # === 性能统计指标 ===
        self.response_times = []   # 响应时间列表
        self.comfort_scores = []   # 舒适度评分列表
        
        # Stream引用（在start中初始化）
        self.sensor_stream = None
        self.control_stream = None
        
    def start(self):
        """启动Agent"""
        # 订阅传感器数据流
        try:
            self.sensor_stream = cs.get_stream(self, "room_sensor_data_stream")
        except KeyError:
            print("⚠️  警告: 传感器数据流尚未创建，请确保先启动传感器Agent")
            print("   正在等待传感器流创建...")
            time.sleep(2)
            self.sensor_stream = cs.get_stream(self, "room_sensor_data_stream")
        
        # 创建控制动作输出流
        self.control_stream = cs.create_stream(self, "room_control_action_stream")
        
        # 监听传感器数据（注意：回调函数必须是局部函数，不能是类方法）
        def handle_data(data):
            self.handle_sensor_data(data)
        
        self.sensor_stream.for_each(handle_data)
        
        print(f"\n{'='*70}")
        print(f"🤖 智能会议室控制Agent已启动")
        print(f"{'='*70}")
        print(f"📋 初始配置:")
        print(f"   - 目标温度: {self.target_temperature}°C")
        print(f"   - CO2警告阈值: {self.CO2_WARNING} ppm")
        print(f"   - CO2危险阈值: {self.CO2_DANGER} ppm")
        print(f"   - 温度警告阈值: {self.TEMP_WARNING}°C")
        print(f"   - 温度危险阈值: {self.TEMP_DANGER}°C")
        print(f"{'='*70}\n")
        
        return True
    
    def stop(self):
        """停止Agent"""
        if self.sensor_stream:
            self.sensor_stream.unregister_all(self)
    
    def handle_sensor_data(self, data):
        """
        处理传感器数据 - 核心判断逻辑
        Agent通过检查数据内容自动判断情况，无需event_type标签
        """
        start_time = time.time()
        self.decision_count += 1
        
        # === 打印接收到的数据 ===
        print(f"\n{'─'*70}")
        print(f"📊 [决策 #{self.decision_count}] 读取传感器数据")
        print(f"{'─'*70}")
        print(f"⏰ 时间戳: {data['timestamp']}")
        print(f"🌡️  温度: {data['temperature']:.1f}°C")
        print(f"💧 湿度: {data['humidity']:.1f}%")
        print(f"💨 CO2浓度: {data['co2']} ppm")
        print(f"👥 人数: {data['people_count']}人")
        print(f"❄️  空调功率: {data.get('ac_power', 'N/A')}%")
        
        # === 核心判断逻辑：根据数据内容自动识别情况 ===
        
        # 判断1: 检查是否有用户反馈（触发在线学习）
        if 'user_feedback' in data:
            self._handle_user_feedback(data)
        
        # 判断2: 检查数据是否异常波动（动态感知）
        if self.last_data is not None:
            self._detect_anomaly(data, self.last_data)
        
        # 判断3: 检查是否有设备故障或危险情况（应急规划）
        if self._check_emergency(data):
            self._handle_emergency(data)
        else:
            # 正常情况：标准决策
            self._make_normal_decision(data)
        
        # 记录本次数据供下次对比
        self.last_data = data
        
        # 计算并记录响应时间
        response_time = (time.time() - start_time) * 1000
        self.response_times.append(response_time)
        print(f"\n⏱️  本次响应延迟: {response_time:.2f} ms")
        print(f"{'─'*70}")
    
    def _handle_user_feedback(self, data):
        """
        能力1：在线学习 - 处理用户反馈并更新偏好
        """
        feedback = data['user_feedback']
        preferred_temp = data.get('user_preferred_temp', self.target_temperature)
        
        print(f"\n" + "="*70)
        print(f"🎓 【在线学习能力触发】")
        print(f"="*70)
        print(f"💬 检测到用户反馈字段: \"{feedback}\"")
        print(f"🎯 用户偏好温度: {preferred_temp}°C")
        print(f"\n📊 学习前状态:")
        print(f"   - 目标温度: {self.target_temperature}°C")
        print(f"   - 历史学习次数: {len(self.learning_history)}次")
        
        # 保存旧参数
        old_target = self.target_temperature
        
        # 更新参数（在线学习）
        self.target_temperature = preferred_temp
        self.learned_preferences['target_temp'] = self.target_temperature
        self.learned_preferences['last_feedback'] = feedback
        self.learned_preferences['update_time'] = data['timestamp']
        
        # 记录学习历史
        learning_record = {
            'timestamp': data['timestamp'],
            'old_target': old_target,
            'new_target': self.target_temperature,
            'feedback': feedback,
            'temperature_change': self.target_temperature - old_target
        }
        self.learning_history.append(learning_record)
        
        print(f"\n✅ 在线学习完成！")
        print(f"📈 学习后状态:")
        print(f"   - 新目标温度: {self.target_temperature}°C (变化: {self.target_temperature - old_target:+.1f}°C)")
        print(f"   - 历史学习次数: {len(self.learning_history)}次")
        print(f"   - 偏好已保存到内存")
        print(f"\n📝 学习记录已存储:")
        print(f"   {learning_record}")
        print(f"="*70)
    
    def _detect_anomaly(self, current_data, last_data):
        """
        能力2：动态感知 - 检测环境参数的剧烈变化
        """
        # 计算各项指标的变化量
        temp_change = abs(current_data['temperature'] - last_data['temperature'])
        people_change = abs(current_data['people_count'] - last_data['people_count'])
        co2_change = abs(current_data['co2'] - last_data['co2'])
        
        # 定义异常波动阈值
        TEMP_CHANGE_THRESHOLD = 1.5   # 温度变化 > 1.5度
        PEOPLE_CHANGE_THRESHOLD = 5   # 人数变化 > 5人
        CO2_CHANGE_THRESHOLD = 200    # CO2变化 > 200ppm
        
        anomalies = []
        
        # 检测各项异常
        if people_change >= PEOPLE_CHANGE_THRESHOLD:
            anomalies.append(f"人数剧变 ({last_data['people_count']} → {current_data['people_count']}人, Δ{people_change}人)")
        
        if temp_change >= TEMP_CHANGE_THRESHOLD:
            anomalies.append(f"温度剧变 ({last_data['temperature']:.1f} → {current_data['temperature']:.1f}°C, Δ{temp_change:.1f}°C)")
        
        if co2_change >= CO2_CHANGE_THRESHOLD:
            anomalies.append(f"CO2剧变 ({last_data['co2']} → {current_data['co2']}ppm, Δ{co2_change}ppm)")
        
        # 如果检测到异常，触发动态感知响应
        if anomalies:
            print(f"\n" + "="*70)
            print(f"⚡ 【动态感知能力触发】")
            print(f"="*70)
            print(f"📊 检测到环境参数剧烈波动:")
            for i, anomaly in enumerate(anomalies, 1):
                print(f"   {i}. {anomaly}")
            
            print(f"\n🔍 波动分析:")
            print(f"   - 温度变化率: {temp_change:.1f}°C/周期 {'⚠️ 异常' if temp_change >= TEMP_CHANGE_THRESHOLD else '✓ 正常'}")
            print(f"   - 人数变化率: {people_change}人/周期 {'⚠️ 异常' if people_change >= PEOPLE_CHANGE_THRESHOLD else '✓ 正常'}")
            print(f"   - CO2变化率: {co2_change}ppm/周期 {'⚠️ 异常' if co2_change >= CO2_CHANGE_THRESHOLD else '✓ 正常'}")
            
            print(f"\n⚡ 启动快速响应模式")
            
            # 生成快速响应动作
            action = {
                'action_type': 'rapid_adjustment',
                'timestamp': current_data['timestamp'],
                'detected_anomalies': anomalies,
                'adjustments': []
            }
            
            # 根据不同的异常类型调整策略
            current_power = current_data.get('ac_power', 60)
            
            if people_change >= PEOPLE_CHANGE_THRESHOLD:
                new_power = min(100, current_power + 15)
                action['adjustments'].append(f"人数突增，提高制冷功率: {current_power}% → {new_power}%")
                action['ac_power'] = new_power
            
            if temp_change >= TEMP_CHANGE_THRESHOLD:
                new_power = min(100, current_power + 20)
                action['adjustments'].append(f"温度快速上升，加强制冷: {current_power}% → {new_power}%")
                action['ac_power'] = new_power
            
            if co2_change >= CO2_CHANGE_THRESHOLD:
                action['adjustments'].append("CO2浓度快速上升，增强通风")
                action['ventilation_level'] = 'high'
            
            print(f"\n🎬 发送控制动作:")
            for adj in action['adjustments']:
                print(f"   - {adj}")
            
            # 发送动作到控制流
            self.control_stream.add_item(action)
            print(f"✅ 快速响应动作已发送到控制系统")
            print(f"="*70)
    
    def _check_emergency(self, data):
        """
        检查是否存在紧急情况
        返回True表示需要应急处理
        """
        # 检查1: 设备故障
        if 'device_status' in data:
            if data['device_status'].get('ac_cooling') == 'fault':
                return True
        
        # 检查2: 空调功率为0（可能故障）
        if data.get('ac_power', 100) == 0:
            return True
        
        # 检查3: 环境参数达到危险级别
        if data['temperature'] >= self.TEMP_DANGER:
            return True
        
        if data['co2'] >= self.CO2_DANGER:
            return True
        
        return False
    
    def _handle_emergency(self, data):
        """
        能力3：调整规划和行动 - 处理突发事件，重新规划应急方案
        """
        print(f"\n" + "="*70)
        print(f"🚨 【应急规划能力触发】")
        print(f"="*70)
        
        # 识别故障原因
        fault_reasons = []
        
        if 'device_status' in data and data['device_status'].get('ac_cooling') == 'fault':
            fault_reasons.append("空调制冷系统故障")
        
        if data.get('ac_power', 100) == 0:
            fault_reasons.append("空调无功率输出")
        
        if data['temperature'] >= self.TEMP_DANGER:
            fault_reasons.append(f"温度达到危险级别 ({data['temperature']:.1f}°C ≥ {self.TEMP_DANGER}°C)")
        
        if data['co2'] >= self.CO2_DANGER:
            fault_reasons.append(f"CO2浓度危险 ({data['co2']}ppm ≥ {self.CO2_DANGER}ppm)")
        
        if 'error_message' in data:
            fault_reasons.append(f"系统报错: {data['error_message']}")
        
        print(f"⚠️  紧急情况识别:")
        for i, reason in enumerate(fault_reasons, 1):
            print(f"   {i}. {reason}")
        
        # 原计划
        original_plan = f"标准温控：调节空调至目标温度{self.target_temperature}°C"
        print(f"\n📋 原定计划: {original_plan}")
        print(f"❌ 原计划不可行原因: {'、'.join(fault_reasons[:2])}")
        
        print(f"\n🔄 开始重新规划应急方案...")
        print(f"{'─'*70}")
        
        # 生成应急计划
        emergency_plan = {
            'action_type': 'emergency_response',
            'timestamp': data['timestamp'],
            'original_plan': original_plan,
            'fault_reasons': fault_reasons,
            'emergency_actions': [],
            'priority': 'critical'
        }
        
        # 根据可用资源制定应急方案
        print(f"\n📝 应急方案制定:")
        
        # 方案A: 最大化通风系统
        if 'device_status' in data:
            if data['device_status'].get('ventilation') == 'normal':
                emergency_plan['emergency_actions'].append({
                    'priority': 1,
                    'action': 'maximize_ventilation',
                    'parameter': 'ventilation_level=100%',
                    'expected_effect': '降低CO2浓度300-500ppm'
                })
                print(f"   ✓ [优先级1] 最大化新风系统通风")
                print(f"      └─ 参数: 通风等级设置为100%")
                print(f"      └─ 预期效果: 降低CO2浓度300-500ppm")
            
            # 方案B: 开窗通风
            if data['device_status'].get('windows') == 'closed':
                emergency_plan['emergency_actions'].append({
                    'priority': 2,
                    'action': 'open_windows',
                    'parameter': 'all_windows',
                    'expected_effect': '自然通风，温度降低1-2°C'
                })
                print(f"   ✓ [优先级2] 打开所有窗户进行自然通风")
                print(f"      └─ 参数: 打开所有可用窗户")
                print(f"      └─ 预期效果: 温度降低1-2°C")
        
        # 方案C: 人员疏散建议（CO2危险时）
        if data['co2'] >= self.CO2_DANGER:
            evacuate_count = data['people_count'] // 2
            emergency_plan['emergency_actions'].append({
                'priority': 3,
                'action': 'suggest_evacuation',
                'parameter': f'evacuate_{evacuate_count}_people',
                'expected_effect': f'CO2浓度预计降低{evacuate_count * 20}ppm'
            })
            print(f"   ✓ [优先级3] 建议部分人员疏散")
            print(f"      └─ 参数: 疏散约{evacuate_count}人至其他会议室")
            print(f"      └─ 预期效果: CO2浓度预计降低{evacuate_count * 20}ppm")
        
        # 方案D: 临时降温措施（高温时）
        if data['temperature'] >= self.TEMP_DANGER:
            emergency_plan['emergency_actions'].append({
                'priority': 4,
                'action': 'temporary_cooling',
                'parameter': 'deploy_portable_fans',
                'expected_effect': '体感温度降低2-3°C'
            })
            print(f"   ✓ [优先级4] 部署移动风扇等临时降温设备")
            print(f"      └─ 参数: 调用3台移动风扇")
            print(f"      └─ 预期效果: 体感温度降低2-3°C")
        
        # 方案E: 通知管理员
        emergency_plan['emergency_actions'].append({
            'priority': 5,
            'action': 'alert_admin',
            'parameter': 'critical_equipment_failure',
            'expected_effect': '技术人员5-10分钟内到达'
        })
        print(f"   ✓ [优先级5] 立即通知设施管理员")
        print(f"      └─ 参数: 发送紧急维修请求")
        print(f"      └─ 预期效果: 技术人员5-10分钟内到达")
        
        # 计算应急方案成功率
        print(f"\n{'─'*70}")
        print(f"📊 方案效果评估:")
        
        # 温度改善预期
        temp_reduction = 0
        if any(a['action'] == 'open_windows' for a in emergency_plan['emergency_actions']):
            temp_reduction += 1.5
        if any(a['action'] == 'temporary_cooling' for a in emergency_plan['emergency_actions']):
            temp_reduction += 2
        
        # CO2改善预期  
        co2_reduction = 0
        if any(a['action'] == 'maximize_ventilation' for a in emergency_plan['emergency_actions']):
            co2_reduction += 400
        if any(a['action'] == 'suggest_evacuation' for a in emergency_plan['emergency_actions']):
            co2_reduction += (data['people_count'] // 2) * 20
        
        # 计算成功率（基于预期改善效果）
        temp_score = min(50, (temp_reduction / 3.0) * 50) if data['temperature'] >= self.TEMP_DANGER else 50
        co2_score = min(50, (co2_reduction / 500.0) * 50) if data['co2'] >= self.CO2_DANGER else 50
        success_rate = temp_score + co2_score
        
        emergency_plan['expected_improvement'] = {
            'temperature_reduction': f"{temp_reduction:.1f}°C",
            'co2_reduction': f"{co2_reduction}ppm"
        }
        emergency_plan['success_rate'] = f"{success_rate:.0f}%"
        
        print(f"   - 预期温度降低: {temp_reduction:.1f}°C")
        print(f"   - 预期CO2降低: {co2_reduction}ppm")
        print(f"   - 应急方案成功率: {emergency_plan['success_rate']}")
        
        if success_rate >= 70:
            print(f"   - 评估结果: ✅ 方案可行 (成功率≥70%)")
        else:
            print(f"   - 评估结果: ⚠️  方案风险较高，建议立即疏散")
        
        # 发送应急方案到控制系统
        print(f"\n🎬 应急方案已生成，正在发送到控制系统...")
        self.control_stream.add_item(emergency_plan)
        print(f"✅ 应急方案已发送！共{len(emergency_plan['emergency_actions'])}项应急措施")
        print(f"="*70)
    
    def _make_normal_decision(self, data):
        """
        正常模式：标准温控决策
        """
        # 计算温度偏差
        temp_diff = data['temperature'] - self.target_temperature
        
        # 判断CO2状态
        if data['co2'] >= self.CO2_DANGER:
            co2_status = "🔴 危险"
        elif data['co2'] >= self.CO2_WARNING:
            co2_status = "🟡 警告"
        else:
            co2_status = "🟢 正常"
        
        print(f"\n{'─'*60}")
        print(f"🎯 【正常决策模式】")
        print(f"{'─'*60}")
        print(f"📌 控制目标:")
        print(f"   - 目标温度: {self.target_temperature}°C")
        print(f"   - 当前温度: {data['temperature']:.1f}°C")
        print(f"   - 温度偏差: {temp_diff:+.1f}°C")
        print(f"   - CO2状态: {co2_status} ({data['co2']}ppm)")
        
        # 生成控制动作
        action = {
            'action_type': 'normal_control',
            'timestamp': data['timestamp'],
            'target_temp': self.target_temperature,
            'current_temp': data['temperature'],
            'temp_diff': temp_diff
        }
        
        print(f"\n🎬 控制动作:")
        
        # 温度控制决策
        current_power = data.get('ac_power', 60)
        if abs(temp_diff) > 0.5:
            if temp_diff > 0:  # 当前温度高于目标
                new_power = min(100, current_power + 10)
                action['ac_adjustment'] = 'increase_cooling'
                action['ac_power'] = new_power
                print(f"   🔽 温度过高，增加制冷功率: {current_power}% → {new_power}%")
            else:  # 当前温度低于目标
                new_power = max(30, current_power - 10)
                action['ac_adjustment'] = 'decrease_cooling'
                action['ac_power'] = new_power
                print(f"   🔼 温度过低，降低制冷功率: {current_power}% → {new_power}%")
        else:
            action['ac_adjustment'] = 'maintain'
            action['ac_power'] = current_power
            print(f"   ✓ 温度适宜，保持当前功率: {current_power}%")
        
        # CO2控制决策
        if data['co2'] >= self.CO2_WARNING:
            action['ventilation'] = 'increase'
            ventilation_level = 'high' if data['co2'] >= self.CO2_DANGER else 'medium'
            action['ventilation_level'] = ventilation_level
            print(f"   💨 CO2浓度{co2_status}，增强通风至{ventilation_level}级别")
        else:
            action['ventilation'] = 'normal'
            action['ventilation_level'] = 'low'
            print(f"   ✓ CO2浓度正常，维持标准通风")
        
        # 计算环境舒适度评分
        comfort_score = self._calculate_comfort_score(data)
        action['comfort_score'] = comfort_score
        self.comfort_scores.append(comfort_score)
        
        print(f"\n📈 环境舒适度评分: {comfort_score:.1f}/100")
        
        # 发送控制动作
        self.control_stream.add_item(action)
        print(f"✅ 控制指令已发送")
    
    def _calculate_comfort_score(self, data):
        """
        计算环境舒适度评分（0-100分）
        """
        score = 100.0
        
        # 温度舒适度（偏差越大扣分越多）
        temp_diff = abs(data['temperature'] - self.target_temperature)
        score -= temp_diff * 5
        
        # CO2舒适度
        if data['co2'] > 1200:
            score -= 30  # 危险级别
        elif data['co2'] > 1000:
            score -= 15  # 警告级别
        elif data['co2'] > 800:
            score -= (data['co2'] - 800) / 20  # 轻微超标
        
        # 湿度舒适度（最佳范围40-60%）
        if data['humidity'] < 40:
            score -= (40 - data['humidity']) * 0.5
        elif data['humidity'] > 60:
            score -= (data['humidity'] - 60) * 0.5
        
        return max(0, min(100, score))
    
    def print_summary(self):
        """打印Agent运行统计摘要"""
        print(f"\n{'='*70}")
        print(f"📊 Agent运行统计摘要")
        print(f"{'='*70}")
        
        print(f"\n📈 基本统计:")
        print(f"   - 总决策次数: {self.decision_count}")
        
        if self.response_times:
            avg_response = sum(self.response_times) / len(self.response_times)
            max_response = max(self.response_times)
            min_response = min(self.response_times)
            print(f"   - 平均响应延迟: {avg_response:.2f} ms")
            print(f"   - 最大响应延迟: {max_response:.2f} ms")
            print(f"   - 最小响应延迟: {min_response:.2f} ms")
        
        if self.comfort_scores:
            avg_comfort = sum(self.comfort_scores) / len(self.comfort_scores)
            max_comfort = max(self.comfort_scores)
            min_comfort = min(self.comfort_scores)
            print(f"   - 平均舒适度评分: {avg_comfort:.1f}/100")
            print(f"   - 最高舒适度: {max_comfort:.1f}/100")
            print(f"   - 最低舒适度: {min_comfort:.1f}/100")
        
        if self.learning_history:
            print(f"\n🎓 在线学习记录: (共{len(self.learning_history)}次)")
            for i, record in enumerate(self.learning_history, 1):
                print(f"   {i}. 时间: {record['timestamp']}")
                print(f"      反馈: {record['feedback']}")
                print(f"      参数变化: {record['old_target']}°C → {record['new_target']}°C "
                      f"(Δ{record['temperature_change']:+.1f}°C)")
        
        if self.learned_preferences:
            print(f"\n💾 当前学习偏好:")
            for key, value in self.learned_preferences.items():
                print(f"   - {key}: {value}")
        
        print(f"\n🎯 当前配置:")
        print(f"   - 目标温度: {self.target_temperature}°C")
        
        print(f"\n{'='*70}\n")


if __name__ == '__main__':
    # 单独测试智能控制Agent
    print("测试智能会议室控制Agent")
    
    agent = SmartRoomControlAgent()
    agent.start()
    
    # 保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
        agent.print_summary()

