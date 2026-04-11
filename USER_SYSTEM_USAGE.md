# ChainStream 用户系统使用指南

## 概述

ChainStream 现在支持完整的用户认证和授权系统，包括：
- 用户注册和登录
- 密码哈希和JWT认证
- 用户级别的权限控制
- Stream数据加密
- Agent和Stream的用户隔离

## 主要功能

### 1. 用户管理

#### 创建用户
```python
from chainstream.user import UserManager

# 创建用户管理器
user_manager = UserManager()

# 创建新用户
user = user_manager.create_user(
    username="alice",
    password="secure_password",
    level=1,  # 用户级别
    enable_encryption=True  # 启用加密
)
```

#### 用户登录
```python
# 用户登录
user = user_manager.login("alice", "secure_password")
if user:
    print(f"登录成功: {user.get_username()}")
else:
    print("登录失败")
```

### 2. Agent 用户关联

#### 创建带用户的Agent
```python
from chainstream.agent import Agent

class MyAgent(Agent):
    def __init__(self, user):
        super().__init__(agent_id="my_agent", user=user)
    
    def start(self):
        # Agent逻辑
        pass
```

#### 获取用户的Agent
```python
from chainstream.runtime import cs_server_core

# 获取当前用户的Agent列表
user_agents = cs_server_core.agent_manager.get_agents_by_user(user)
print(f"用户 {user.get_username()} 有 {len(user_agents)} 个Agent")
```

### 3. Stream 加密

#### 创建加密Stream
```python
from chainstream.stream import create_stream

# 创建加密Stream
encrypted_stream = create_stream(
    agent=my_agent,
    stream_id="encrypted_data_stream",
    encrypted=True,
    password="stream_password"  # 可选：使用密码派生密钥
)

# 或者使用预生成的密钥
import base64
from cryptography.fernet import Fernet

key = Fernet.generate_key()
encrypted_stream = create_stream(
    agent=my_agent,
    stream_id="encrypted_data_stream",
    encrypted=True,
    encryption_key=key
)
```

#### 使用加密Stream
```python
# 添加数据（自动加密）
encrypted_stream.add_item(my_agent, {"sensitive": "data"})

# 监听数据（自动解密）
def process_data(data):
    print(f"接收到解密数据: {data}")

encrypted_stream.for_each(my_agent, process_data)
```

### 4. Web API 认证

#### 登录API
```bash
curl -X POST http://localhost:6677/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secure_password"}'
```

#### 使用认证Token
```bash
# 获取用户Agent列表
curl -X GET http://localhost:6677/api/monitor/agents/getRunningAgents \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

#### 注册新用户
```bash
curl -X POST http://localhost:6677/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "bob", "password": "new_password", "level": 1}'
```

### 5. 前端使用

#### 登录界面
前端现在包含完整的登录界面，支持：
- 用户登录
- 新用户注册
- 密码修改
- 加密设置

#### 用户权限
- Level 1: 基础用户，只能访问自己的资源
- Level 5: 高级用户，可以访问更多功能
- Level 10: 管理员，可以访问所有资源

## 安全特性

### 1. 密码安全
- 使用SHA-256哈希存储密码
- 支持PBKDF2密钥派生
- JWT token认证

### 2. 数据加密
- Stream数据自动加密/解密
- 支持Fernet对称加密
- 用户级别的加密密钥管理

### 3. 权限控制
- Agent和Stream按用户隔离
- API端点需要认证
- 管理员权限控制

## 配置

### 环境变量
```bash
# JWT密钥（生产环境必须设置）
export JWT_SECRET_KEY="your-secret-key"

# 用户数据文件路径
export USERS_FILE_PATH="/path/to/users.json"
```

### 依赖安装
```bash
pip install cryptography PyJWT
```

## 示例：完整的用户工作流

```python
from chainstream.user import UserManager
from chainstream.agent import Agent
from chainstream.stream import create_stream

# 1. 创建用户管理器
user_manager = UserManager()

# 2. 创建用户
user = user_manager.create_user("alice", "password123", level=1)

# 3. 创建Agent
class DataProcessor(Agent):
    def __init__(self, user):
        super().__init__(agent_id="data_processor", user=user)
        
    def start(self):
        # 创建加密Stream
        self.encrypted_stream = create_stream(
            agent=self,
            stream_id="sensitive_data",
            encrypted=True,
            password="stream_secret"
        )
        
        # 监听数据
        self.encrypted_stream.for_each(self, self.process_data)
    
    def process_data(self, data):
        print(f"处理数据: {data}")
        # 数据已经自动解密

# 4. 启动Agent
agent = DataProcessor(user)
agent.start()

# 5. 发送数据
agent.encrypted_stream.add_item(agent, {"message": "Hello, encrypted world!"})
```

## 注意事项

1. **生产环境安全**：
   - 使用强JWT密钥
   - 定期轮换加密密钥
   - 启用HTTPS

2. **性能考虑**：
   - 加密会增加CPU开销
   - 大量数据时考虑异步处理

3. **备份**：
   - 定期备份用户数据文件
   - 保存加密密钥的备份

4. **监控**：
   - 监控登录失败次数
   - 记录敏感操作日志
