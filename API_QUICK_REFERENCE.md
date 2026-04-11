# 前后端接口快速参考表

## 📡 后端接口一览

| 接口 | 方法 | 功能 | 新增？ | 状态 |
|------|------|------|--------|------|
| `/api/generator/chat` | POST | 生成Agent代码（支持反馈模式）| ❌ 修改 | ✅ 完成 |
| `/api/generator/info` | GET | 获取生成器信息 | ✅ 新增 | ✅ 完成 |
| `/api/generator/feedback-history` | POST | 保存生成历史 | ✅ 新增 | ✅ 完成 |
| `/api/generator/feedback-history/<sid>` | GET | 获取生成详情 | ✅ 新增 | ✅ 完成 |
| `/api/generator/user-histories` | GET | 获取用户历史列表 | ✅ 新增 | ✅ 完成 |

---

## 🎯 关键改进一览

### 1️⃣ 参数支持 ✅
```python
# 前端现在可以传递这些参数
max_loop              # int, 最大迭代次数 (1-50)
only_print_last       # bool, 仅打印最后一次迭代
sandbox_type          # str, 沙箱类型
framework_example_number      # int, 示例数量
base_prompt_example_select_policy  # str, 选择策略
```

### 2️⃣ 返回值扩展 ✅
```json
{
    "stats": {
        "loop_count": 5,      // ✨ 新增 - 迭代次数
        "elapsed_ms": 15000,
        "total_tokens": 2300
    },
    "feedback_history": "..."  // ✨ 新增 - 完整迭代历史
}
```

### 3️⃣ 新增查询接口 ✅
- 获取可用生成器列表和配置
- 保存/查询生成历史
- 获取用户历史列表

---

## 💡 前端需要做的工作

| 功能 | 优先级 | 难度 | 工作量 |
|------|--------|------|--------|
| 生成器选择器 | 🔴 | ⭐ | 2h |
| 参数配置面板 | 🔴 | ⭐⭐ | 3h |
| 修改请求格式 | 🔴 | ⭐ | 1h |
| 历史列表视图 | 🟡 | ⭐⭐ | 4h |
| 历史详情视图 | 🟡 | ⭐⭐⭐ | 5h |
| 实时反馈显示 | 🟢 | ⭐⭐⭐⭐ | 8h |

---

## 🔗 请求/响应示例

### 示例 A：生成器选择 (前端)
```javascript
// 1. 获取可用生成器
GET /api/generator/info

// 2. 用户选择 python_feedback，配置参数
// 3. 发起生成请求
POST /api/generator/chat
{
    "message": "Create email summary agent",
    "code": "",
    "language": "python",
    "generator_type": "python_feedback",  // ✨ 选择反馈模式
    "max_loop": 10,                        // ✨ 配置迭代次数
    "sandbox_type": "chainstream"
}
```

### 示例 B：生成响应 (后端)
```json
{
    "success": true,
    "reply": "已完成Agent生成，经过5次迭代优化...",
    "new_code": "def agent():\n    ...",
    "stats": {
        "prompt_tokens": 1500,
        "completion_tokens": 800,
        "total_tokens": 2300,
        "elapsed_ms": 15000,
        "model": "agent-generator:python_feedback",
        "loop_count": 5                    // ✨ 新增
    },
    "new_memory": "...",
    "feedback_history": "Thought 0: ...\nCode 0: ...\nObservation 0: ..."  // ✨ 新增
}
```

### 示例 C：保存历史 (前端)
```javascript
// 生成完成后调用
POST /api/generator/feedback-history
{
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "feedback_history": response.feedback_history,
    "generator_type": "python_feedback",
    "message": "Create email summary agent",
    "final_code": response.new_code,
    "stats": response.stats
}
```

### 示例 D：查看历史 (前端)
```javascript
// 获取用户历史列表
GET /api/generator/user-histories?limit=20&offset=0

// 点击某条历史查看详情
GET /api/generator/feedback-history/550e8400-e29b-41d4-a716-446655440000

// 响应包含完整的迭代过程
{
    "session_id": "...",
    "feedback_history": "Thought 0: ...",
    "stats": {"loop_count": 5, ...},
    "timestamp": "2026-04-10T14:30:45..."
}
```

---

## ⚠️ 注意事项

### 后端已处理
- ✅ 参数验证和默认值
- ✅ 返回值兼容性（feedback vs non-feedback）
- ✅ 错误处理和fallback
- ✅ 用户隔离（历史按用户存储）

### 前端需要处理
- ❌ 动态参数UI（根据generator_type显示不同参数）
- ❌ 长时间运行提示（feedback模式可能耗时）
- ❌ 历史分页加载
- ❌ 响应式布局（特别是历史详情展示）

### 性能提示
- 反馈模式可能比单次生成慢 3-5 倍（因为有多次LLM调用）
- 建议给用户提示迭代进度
- 考虑添加中止/停止功能

---

## 🧪 快速测试清单

### 后端测试 (curl)
```bash
# 测试单次生成（已有）
curl -X POST http://localhost:5000/api/generator/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "test",
    "code": "",
    "language": "python",
    "generator_type": "python_single"
  }'

# 测试反馈式生成（✨新）
curl -X POST http://localhost:5000/api/generator/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "test",
    "code": "",
    "language": "python",
    "generator_type": "python_feedback",
    "max_loop": 5
  }'

# 获取生成器信息
curl http://localhost:5000/api/generator/info

# 获取用户历史
curl http://localhost:5000/api/generator/user-histories?limit=10
```

---

## 📚 相关文件

- 📄 [完整分析](./GENERATOR_FEEDBACK_API_ANALYSIS.md)
- 📄 [实现清单](./PYTHON_FEEDBACK_INTEGRATION_CHECKLIST.md)
- 🐍 [后端实现](./chainstream/runtime/web/backend/monitor/agents.py)
- 🐍 [生成器实现](./AgentGenerator/generator/stream_mode/chainstream_chat_generator_python_feedback.py)

---

## 🚀 部署检查清单

在部署前检查：

- [ ] agents.py 中的 4 个新接口已启用
- [ ] 导入语句正确（datetime, json, request）
- [ ] 生成历史存储目录 `.generation_history/` 可访问
- [ ] 用户UUID正确传递（require_auth装饰器）
- [ ] 错误处理和日志输出正常
- [ ] 前端已支持新的生成器类型选择
- [ ] 前端已支持新的请求参数格式

---

**最后更新**: 2026-04-10  
**版本**: 1.0  
**状态**: ✅ 后端完全就绪，等待前端集成
