# Python Feedback 生成器接口集成 - 完整清单

## ✅ 已完成的改进

### 1. **后端 agents.py 修复（关键）**

#### 修复1: 参数支持
- ✅ 添加 `max_loop` 参数支持
- ✅ 添加 `only_print_last` 参数支持  
- ✅ 添加 `sandbox_type` 参数支持
- ✅ 添加 `framework_example_number` 参数支持
- ✅ 添加 `base_prompt_example_select_policy` 参数支持

**位置**：agents.py 第 310-320 行
```python
max_loop = data.get('max_loop', 20)
only_print_last = data.get('only_print_last', False)
sandbox_type = data.get('sandbox_type', 'chainstream')

gen = ChainStreamChatGeneratorPythonFeedback(
    framework_example_number=...,
    base_prompt_example_select_policy=...,
    max_loop=max_loop,
    sandbox_type=sandbox_type,
    only_print_last=only_print_last
)
```

#### 修复2: 返回值处理
- ✅ 修复 `python_feedback` 返回 5 个值的问题
- ✅ 正确提取 `(code, latency, tokens, loop_count, history)`
- ✅ 为非feedback类型保持向后兼容

**位置**：agents.py 第 345-365 行
```python
if generator_type == 'python_feedback':
    result = gen.generate_agent_chat_with_feedback(...)
    agent_code, latency, tokens, loop_count, feedback_history = result
    feedback_info = {'loop_count': loop_count, 'feedback_history': feedback_history}
else:
    agent_code, latency, tokens = gen.generate_agent_chat(...)
    feedback_info = {}
```

#### 修复3: 响应体扩展
- ✅ 在 `stats` 中添加 `loop_count`
- ✅ 在响应中添加 `feedback_history`（仅feedback模式）
- ✅ 保持响应结构的向后兼容性

**位置**：agents.py 第 385-405 行
```json
{
    "success": true,
    "reply": "...",
    "new_code": "...",
    "stats": {
        "prompt_tokens": 1500,
        "completion_tokens": 800,
        "total_tokens": 2300,
        "elapsed_ms": 15000,
        "model": "agent-generator:python_feedback",
        "loop_count": 5          // ✅ 新增
    },
    "new_memory": "...",
    "feedback_history": "..."   // ✅ 新增（仅feedback模式）
}
```

### 2. **新增后端接口（4个）**

#### ① `/api/generator/info` [GET]
获取所有可用生成器的信息和配置

**返回**：
```json
{
    "generators": {
        "python_single": {...},
        "python_feedback": {
            "name": "Python Feedback-Guided Generator",
            "parameters": [
                {"name": "max_loop", "type": "integer", "default": 20, ...},
                {"name": "sandbox_type", "type": "string", ...},
                ...
            ],
            "features": ["code_generation", "iterative_refinement", "sandbox_feedback", "history_tracking"],
            "sandbox_support": true
        },
        "java_single": {...}
    }
}
```

**前端用途**：
- 显示生成器选择器
- 动态渲染参数配置UI
- 显示生成器能力

---

#### ② `/api/generator/feedback-history` [POST]
保存某次生成的反馈历史

**请求**：
```json
{
    "session_id": "uuid-xxx",
    "feedback_history": "Thought 0: ...\nCode 0: ...\nObservation 0: ...",
    "generator_type": "python_feedback",
    "message": "用户输入的消息",
    "final_code": "最终生成的代码",
    "stats": {"loop_count": 5, "total_tokens": 2300, ...}
}
```

**返回**：
```json
{
    "success": true,
    "session_id": "uuid-xxx"
}
```

**存储位置**：
```
.generation_history/
├── {user_uuid}/
│   ├── {session_id}.json
│   ├── {session_id}.json
│   └── ...
```

**前端用途**：
- 生成完后保存历史
- 用于后续查询和对比

---

#### ③ `/api/generator/feedback-history/<session_id>` [GET]
获取某次生成的详细反馈历史

**返回**：
```json
{
    "session_id": "uuid-xxx",
    "user_id": "user_uuid",
    "generator_type": "python_feedback",
    "message": "原始消息",
    "final_code": "最终代码",
    "feedback_history": "完整的Thought-Code-Observation历史",
    "stats": {
        "loop_count": 5,
        "total_tokens": 2300,
        "elapsed_ms": 15000,
        "model": "agent-generator:python_feedback"
    },
    "timestamp": "2026-04-10T14:30:45.123456"
}
```

**前端用途**：
- 点击历史列表项查看详情
- 展示完整的迭代过程
- 对比不同版本

---

#### ④ `/api/generator/user-histories` [GET]
获取当前用户的生成历史列表

**查询参数**：
- `limit`: 最多返回数量 (default: 20)
- `offset`: 分页偏移 (default: 0)
- `generator_type`: 过滤生成器类型 (可选)

**返回**：
```json
{
    "total": 42,
    "items": [
        {
            "session_id": "uuid-1",
            "generator_type": "python_feedback",
            "timestamp": "2026-04-10T14:30:45.123456",
            "message_preview": "Create an agent that...",
            "loop_count": 5,
            "total_tokens": 2300,
            "elapsed_ms": 15000
        },
        {
            "session_id": "uuid-2",
            "generator_type": "python_single",
            "timestamp": "2026-04-10T14:25:12.654321",
            "message_preview": "Modify the agent to...",
            "loop_count": null,
            "total_tokens": 1500,
            "elapsed_ms": 5000
        },
        ...
    ],
    "limit": 20,
    "offset": 0
}
```

**前端用途**：
- 显示生成历史列表
- 支持分页加载
- 支持按生成器类型过滤
- 快速预览生成信息

---

## 🔄 前端需要的改进

### 前端请求格式（支持新参数）

#### 调用示例1：单次生成（python_single）
```javascript
POST /api/generator/chat
{
    "message": "Create an agent that summarizes emails",
    "code": "existing code here",
    "language": "python",
    "generator_type": "python_single",
    "path": "agents/email_summary.py"
}
```

#### 调用示例2：反馈式生成（python_feedback）- ✨ 新
```javascript
POST /api/generator/chat
{
    "message": "Create an agent that summarizes emails",
    "code": "",
    "language": "python",
    "generator_type": "python_feedback",      // 指定为反馈模式
    "path": "agents/email_summary.py",
    "max_loop": 10,                           // 最多迭代10次
    "sandbox_type": "chainstream",
    "only_print_last": false,
    "framework_example_number": 0,
    "base_prompt_example_select_policy": "random"
}
```

#### 调用示例3：保存生成历史
```javascript
POST /api/generator/feedback-history
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",  // UUID
    "feedback_history": "Thought 0: ...",
    "generator_type": "python_feedback",
    "message": "原始消息",
    "final_code": "最终生成代码",
    "stats": {"loop_count": 5, ...}
}
```

#### 调用示例4：获取生成器列表
```javascript
GET /api/generator/info

// 响应包含所有可用生成器及其参数配置
// 用于动态渲染UI
```

#### 调用示例5：获取用户历史
```javascript
GET /api/generator/user-histories?limit=20&offset=0&generator_type=python_feedback
```

---

## 📋 前端UI需要实现的功能

### 1. 生成器选择器
- [ ] 下拉菜单：python_single / python_feedback / java_single
- [ ] 调用 `/api/generator/info` 获取可用生成器列表

### 2. 参数配置面板（feedback模式特有）
- [ ] max_loop 滑块 (1-50)
- [ ] sandbox_type 下拉菜单
- [ ] only_print_last 切换开关
- [ ] framework_example_number 数字输入
- [ ] 参数说明提示

### 3. 生成进度/反馈显示（可选但推荐）
```
迭代进度:
[████████░░] 5 / 10 次

当前迭代 (Step 5):
思考: 我需要添加错误处理...
代码: (显示该步生成的代码)
观察: 沙箱反馈信息
```

### 4. 生成历史面板
- [ ] 历史列表：调用 `/api/generator/user-histories`
- [ ] 分页加载
- [ ] 按生成器类型过滤
- [ ] 点击展开详情：调用 `/api/generator/feedback-history/<session_id>`

### 5. 生成历史详情视图
- [ ] 显示原始消息
- [ ] 显示完整反馈历史（展开/折叠）
- [ ] 显示最终代码
- [ ] 显示统计信息（迭代次数、Token用量、耗时）
- [ ] 导出/下载功能

---

## 🔧 代码生成器 Python Feedback 配置

已在 ChainStreamChatGeneratorPythonFeedback 中实现：

```python
class ChainStreamChatGeneratorPythonFeedback(AgentGeneratorBase):
    def __init__(
        self,
        framework_example_number=0,
        base_prompt_example_select_policy='random',
        max_loop=20,              # 最大迭代次数
        sandbox_type='chainstream',  # 沙箱类型
        only_print_last=False     # 仅打印最后一次迭代
    ):
```

**主要方法**：
- `generate_agent_chat_with_feedback()` - 返回 (code, latency, tokens, loop_count, history)
- `get_last_response_metadata()` - 获取 new_history 和 message_to_user

---

## 📊 测试清单

### 后端测试
- [x] ✅ /api/generator/chat 支持 python_feedback 类型
- [x] ✅ 参数正确传递到生成器
- [x] ✅ 返回值正确处理（5个值）
- [ ] 测试各参数组合
- [ ] 测试边界情况（max_loop=1, max_loop=50）
- [ ] 测试错误处理

### 前端测试
- [ ] 基础对话生成（已有）
- [ ] 切换到 python_feedback 模式
- [ ] 配置参数并验证
- [ ] 查看生成历史列表
- [ ] 查看生成详情
- [ ] 测试响应式布局

---

## 🚀 后续可选优化

### Phase 2（推荐）
1. **WebSocket 实时反馈流**
   ```
   WebSocket: /ws/generator/feedback-stream
   实时推送每次迭代的反馈信息
   ```

2. **数据库持久化**
   - 将生成历史从文件存储改为数据库
   - 支持更复杂的查询

3. **生成对比功能**
   - 对比不同迭代版本
   - 对比不同生成器的输出

### Phase 3（高级）
1. **生成配置保存**
   - 保存常用的参数组合
   - 一键快速生成

2. **代码审计和审核**
   - 标记/注释特定迭代
   - 通过/拒绝某次迭代

3. **性能监控**
   - LLM调用成本统计
   - 生成时间趋势分析

---

## 📝 文件修改总结

### 修改文件
- ✅ `/chainstream/runtime/web/backend/monitor/agents.py`
  - 添加导入：`request`, `json`, `datetime`
  - 修改 `/api/generator/chat` 参数处理（第 310 行）
  - 修改返回值处理（第 345 行）
  - 添加 4 个新接口（第 688 行后）

### 新增文件（无需修改）
- ✅ `/AgentGenerator/generator/stream_mode/chainstream_chat_generator_python_feedback.py`
  - 已实现

### 配置文件
- 无需修改

---

## 🎯 下一步行动

1. **即刻进行**：验证后端修改是否正确
2. **1-2小时内**：前端开发参数配置UI
3. **2-3小时内**：前端开发历史列表视图
4. **后续**：WebSocket 实时反馈（可选）

---

生成时间：2026-04-10
最后更新：已集成所有关键接口
