# IoT智能会议室控制系统 Demo

## 📋 项目概述

本Demo展示了一个基于ChainStream框架开发的**智能会议室环境控制系统**，用于验证AI Agent的三大核心能力：

1. **在线学习能力** - Agent能够根据用户反馈动态调整控制策略
2. **动态感知能力** - Agent能够实时感知环境变化并快速响应
3. **调整规划和行动能力** - Agent能够在突发事件中重新规划应急方案

## 🎯 应用场景

智能会议室温控与空气质量管理系统：
- **输入**: 多传感器数据（温度、湿度、CO2、人数）
- **输出**: 智能控制决策（空调功率、通风等级）
- **目标**: 保持舒适的室内环境（目标温度、空气质量）

## 🏗️ 系统架构

```
┌─────────────────────────┐
│ SimulatedSensorAgent    │  模拟传感器数据生成
│  - 正常数据模式           │
│  - 用户反馈模式           │
│  - 环境波动模式           │
│  - 设备故障模式           │
└────────┬────────────────┘
         │
         ▼ room_sensor_data_stream
         │
┌────────┴────────────────┐
│ SmartRoomControlAgent   │  智能环境控制
│  - 在线学习               │
│  - 动态感知               │
│  - 应急规划               │
└────────┬────────────────┘
         │
         ▼ room_control_action_stream
         │
┌────────┴────────────────┐
│ 控制执行 & 日志记录        │
└─────────────────────────┘
```

## 📦 文件结构

```
iot_room_control/
├── simulated_sensor_agent.py      # 模拟传感器Agent
├── smart_room_control_agent.py    # 智能控制Agent
├── run_demo.py                    # 测试运行脚本
└── README.md                      # 本文档
```

## 🚀 快速开始

### 1. 环境要求

```bash
# 确保已安装ChainStream
cd /path/to/ChainStream
pip install -e .
```

### 2. 运行测试

```bash
cd AgentStore/demo_agents/iot_room_control

# 测试1: 基准测试（正常数据）
python run_demo.py --test normal

# 测试2: 在线学习测试
python run_demo.py --test learning

# 测试3: 动态感知测试
python run_demo.py --test dynamic

# 测试4: 应急规划测试
python run_demo.py --test emergency

# 运行全部测试
python run_demo.py --test all
```

## 📊 四组测试数据详解

### 测试1: 基准测试（Normal）

**数据特征**: 正常稳定的环境数据
- 温度: 24±0.5°C (小幅波动)
- 湿度: 50±3%
- CO2: 650±50 ppm
- 人数: 8人 (稳定)

**Agent行为**: 
- 使用默认控制策略
- 维持目标温度23°C
- 正常调节空调功率

**验证指标**:
- ✓ 响应时间 < 500ms
- ✓ 决策准确性
- ✓ 舒适度评分

**日志示例**:
```
📊 [决策 #1] 读取传感器数据
🌡️  温度: 24.3°C
💨 CO2浓度: 670 ppm
🎯 【正常决策模式】
   目标温度: 23.0°C
   🔽 温度过高，增加制冷功率: 60% → 70%
⏱️  本次响应延迟: 185.23 ms
```

---

### 测试2: 在线学习（Learning）

**数据特征**: 包含用户反馈的数据
- 阶段1: 正常数据（温度23°C）
- 阶段2: **用户反馈** - "太冷了，能调高一点温度吗？"
- 阶段3: 验证学习效果

**关键字段**:
```python
{
    "user_feedback": "太冷了，能调高一点温度吗？",
    "user_preferred_temp": 25.5
}
```

**Agent行为**:
- 检测到`user_feedback`字段
- 触发在线学习机制
- 更新目标温度: 23°C → 25.5°C
- 保存学习记录到内部变量
- 后续决策使用新的目标温度

**验证指标**:
- ✓ 学习前后参数对比
- ✓ 性能提升（舒适度评分↑）
- ✓ 无需重新训练
- ✓ 学习记录完整

**日志示例**:
```
🎓 【在线学习能力触发】
💬 检测到用户反馈字段: "太冷了，能调高一点温度吗？"
🎯 用户偏好温度: 25.5°C
📊 学习前状态:
   - 目标温度: 23.0°C
✅ 在线学习完成！
📈 学习后状态:
   - 新目标温度: 25.5°C (变化: +2.5°C)
   - 历史学习次数: 1次
📝 学习记录已存储
```

---

### 测试3: 动态感知（Dynamic）

**数据特征**: 环境参数剧烈变化
- 模拟场景: 会议突然开始
- 人数: 2 → 18人 (2分钟内激增)
- 温度: 23°C → 28.5°C (快速上升)
- CO2: 450 → 1300 ppm (严重超标)

**Agent行为**:
- 实时对比当前数据与上一次数据
- **自动检测**异常波动:
  - 人数变化 > 5人 → 触发
  - 温度变化 > 1.5°C → 触发
  - CO2变化 > 200ppm → 触发
- 启动快速响应模式
- 发送紧急调整动作

**验证指标**:
- ✓ 感知延迟 < 500ms
- ✓ 100%检测到变化
- ✓ 实时更新内部状态
- ✓ 日志与输入数据一致

**日志示例**:
```
⚡ 【动态感知能力触发】
📊 检测到环境参数剧烈波动:
   1. 人数剧变 (5 → 18人, Δ13人)
   2. 温度剧变 (24.5 → 26.0°C, Δ1.5°C)
   3. CO2剧变 (650 → 850ppm, Δ200ppm)
🔍 波动分析:
   - 温度变化率: 1.5°C/周期 ⚠️ 异常
   - 人数变化率: 13人/周期 ⚠️ 异常
⚡ 启动快速响应模式
🎬 发送控制动作:
   - 人数突增，提高制冷功率: 55% → 70%
   - CO2浓度快速上升，增强通风
⏱️  本次响应延迟: 245.67 ms
```

---

### 测试4: 应急规划（Emergency）

**数据特征**: 突发设备故障
- 阶段1: 设备正常运行
- 阶段2: **空调突然故障** (ac_power=0, device_status.ac_cooling="fault")
- 阶段3: 环境持续恶化

**关键字段**:
```python
{
    "ac_power": 0,  # 功率为0
    "device_status": {
        "ac_cooling": "fault",  # 故障标记
        "ventilation": "normal",
        "windows": "closed"
    },
    "error_message": "空调压缩机故障，制冷功能失效"
}
```

**Agent行为**:
- 检测到故障字段或ac_power=0
- 识别原计划不可行
- **重新规划**应急方案:
  - Plan A: 标准温控 ❌ (设备故障)
  - Plan B: 应急方案 ✅
    1. 最大化通风系统
    2. 打开窗户自然通风
    3. 建议人员疏散
    4. 部署临时降温设备
    5. 通知管理员
- 计算方案成功率
- 执行应急方案

**验证指标**:
- ✓ 识别突发事件
- ✓ 原计划 vs 新计划对比
- ✓ 方案合理性
- ✓ 成功率 ≥ 70%

**日志示例**:
```
🚨 【应急规划能力触发】
⚠️  紧急情况识别:
   1. 空调制冷系统故障
   2. 空调无功率输出
   3. CO2浓度危险 (1300ppm ≥ 1200ppm)
📋 原定计划: 标准温控：调节空调至目标温度23.0°C
❌ 原计划不可行原因: 空调制冷系统故障、空调无功率输出
🔄 开始重新规划应急方案...

📝 应急方案制定:
   ✓ [优先级1] 最大化新风系统通风
      └─ 预期效果: 降低CO2浓度300-500ppm
   ✓ [优先级2] 打开所有窗户进行自然通风
      └─ 预期效果: 温度降低1-2°C
   ✓ [优先级3] 建议部分人员疏散
      └─ 预期效果: CO2浓度预计降低150ppm
   ✓ [优先级4] 部署移动风扇等临时降温设备
      └─ 预期效果: 体感温度降低2-3°C
   ✓ [优先级5] 立即通知设施管理员

📊 方案效果评估:
   - 预期温度降低: 3.5°C
   - 预期CO2降低: 550ppm
   - 应急方案成功率: 75%
   - 评估结果: ✅ 方案可行 (成功率≥70%)

🎬 应急方案已生成，正在发送到控制系统...
✅ 应急方案已发送！共5项应急措施
```

---

## 📈 性能指标说明

### 在线学习能力指标
- **学习前基准**: 记录初始参数和性能
- **学习触发**: 检测并处理用户反馈
- **参数更新**: 目标温度等参数动态调整
- **性能提升**: 学习后舒适度评分提高
- **稳定性**: 持续运行无性能退化

### 动态感知能力指标
- **响应延迟**: 平均 < 200ms，最大 < 500ms
- **检测准确率**: 100% 检测到数据变化
- **日志一致性**: 感知日志与输入完全匹配
- **实时性**: 毫秒级延迟

### 调整规划能力指标
- **事件识别**: 准确识别突发事件
- **规划调整**: 清晰的原计划→新计划过渡
- **方案合理性**: 符合实际情况和安全规范
- **成功率**: 应急方案成功率 ≥ 70%

## 🔍 核心代码亮点

### 1. 无标签自然判断

```python
def handle_sensor_data(self, data):
    # 不依赖event_type标签，根据数据内容自动判断
    
    # 判断1: 检查是否有用户反馈
    if 'user_feedback' in data:
        self._handle_user_feedback(data)
    
    # 判断2: 检查数据异常波动
    if self.last_data is not None:
        self._detect_anomaly(data, self.last_data)
    
    # 判断3: 检查设备故障
    if self._check_emergency(data):
        self._handle_emergency(data)
    else:
        self._make_normal_decision(data)
```

### 2. 在线学习实现

```python
def _handle_user_feedback(self, data):
    # 保存旧参数
    old_target = self.target_temperature
    
    # 更新参数（在线学习）
    self.target_temperature = data['user_preferred_temp']
    
    # 记录学习历史（普通变量，不用cs.memory）
    self.learning_history.append({
        'old_target': old_target,
        'new_target': self.target_temperature,
        'feedback': data['user_feedback']
    })
```

### 3. 动态感知实现

```python
def _detect_anomaly(self, current_data, last_data):
    # 计算变化率
    temp_change = abs(current_data['temperature'] - last_data['temperature'])
    people_change = abs(current_data['people_count'] - last_data['people_count'])
    
    # 自动检测异常
    if people_change >= 5 or temp_change >= 1.5:
        print("⚡ 检测到异常波动，启动快速响应")
        # 发送紧急调整动作
        self.control_stream.add_item(self, action)
```

### 4. 应急规划实现

```python
def _handle_emergency(self, data):
    # 识别故障
    if data.get('ac_power') == 0:
        print("🚨 检测到设备故障")
    
    # 原计划
    original_plan = "标准温控"
    print(f"❌ 原计划不可行")
    
    # 重新规划
    emergency_plan = {
        'original_plan': original_plan,
        'emergency_actions': [
            {'action': 'maximize_ventilation'},
            {'action': 'open_windows'},
            {'action': 'suggest_evacuation'}
        ]
    }
    
    # 计算成功率
    success_rate = self._calculate_success_rate(data, emergency_plan)
    print(f"✅ 应急方案成功率: {success_rate}%")
```

## 📝 测试结果示例

运行 `python run_demo.py --test all` 后的输出：

```
================================================================================
  测试结果总结
================================================================================

  ✅ 通过  基准测试
  ✅ 通过  在线学习测试
  ✅ 通过  动态感知测试
  ✅ 通过  应急规划测试

  总计: 4/4 项测试通过

================================================================================
```

## 🛠️ 自定义扩展

### 添加新的传感器数据

在 `simulated_sensor_agent.py` 中添加新的数据生成模式：

```python
def _generate_custom_data(self):
    data = {
        "timestamp": time.strftime("%H:%M:%S"),
        "temperature": 25.0,
        "custom_field": "custom_value",  # 新字段
    }
    self.sensor_data_stream.add_item(self, data)
```

### 添加新的控制策略

在 `smart_room_control_agent.py` 中添加新的判断逻辑：

```python
def handle_sensor_data(self, data):
    # ... 现有判断逻辑 ...
    
    # 新的判断逻辑
    if 'custom_field' in data:
        self._handle_custom_logic(data)
```

## 📞 联系方式

如有问题或建议，请联系项目团队。

## 📄 许可证

本Demo遵循ChainStream项目的许可证。

