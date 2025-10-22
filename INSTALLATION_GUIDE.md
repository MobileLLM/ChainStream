# ChainStream 系统安装与初始化指南

本文档详细描述如何在新电脑上从零开始安装和配置 ChainStream 系统，包括 Python 环境、Java 环境、Node.js 环境、LLM API 配置、Android 客户端安装等所有必要步骤。

## 目录

- [系统要求](#系统要求)
- [1. 克隆项目](#1-克隆项目)
- [2. Python 环境配置](#2-python-环境配置)
- [3. Java 环境配置](#3-java-环境配置)
- [4. Node.js 环境配置（前端）](#4-nodejs-环境配置前端)
- [5. LLM API 配置](#5-llm-api-配置)
- [6. 初始化系统](#6-初始化系统)
- [7. Android 客户端安装](#7-android-客户端安装)
- [8. 验证安装](#8-验证安装)
- [9. 故障排除](#9-故障排除)

---

## 系统要求

### 操作系统
- **macOS**: 10.15+ (推荐)
- **Linux**: Ubuntu 20.04+ / Debian 11+
- **Windows**: Windows 10/11 (需要 WSL2 或原生支持)

### 硬件要求
- **CPU**: 4核及以上
- **内存**: 8GB+ (推荐16GB)
- **硬盘**: 10GB+ 可用空间
- **网络**: 稳定的互联网连接（用于访问 LLM API）

---

## 1. 克隆项目

首先，克隆 ChainStream 项目到本地：

```bash
git clone https://github.com/MobileLLM/ChainStream.git
cd ChainStream
```

---

## 2. Python 环境配置

### 2.1 安装 Python 3.12

ChainStream 需要 Python 3.12 版本。

#### macOS
使用 Homebrew 安装：
```bash
brew install python@3.12
```

#### Linux (Ubuntu/Debian)
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-dev
```

#### 验证安装
```bash
python3.12 --version
# 应输出: Python 3.12.x
```

### 2.2 创建虚拟环境

推荐使用 Conda 或 venv 创建虚拟环境。

#### 使用 Conda（推荐）

安装 Anaconda 或 Miniconda：
```bash
# macOS (使用 Homebrew)
brew install --cask anaconda

# 或使用官方安装脚本
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

创建虚拟环境：
```bash
# 使用项目提供的 environment.yml（如果存在）
conda env create -f environment.yml

# 或手动创建
conda create -n chainstream python=3.12
conda activate chainstream
```

#### 使用 venv
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

### 2.3 安装 Python 依赖

```bash
# 确保已激活虚拟环境
pip install --upgrade pip

# 安装 ChainStream 及其依赖
pip install -e .

# 安装额外的依赖（如果需要）
pip install grpcio grpcio-tools protobuf
```

#### 核心依赖说明

根据 `setup.py`，ChainStream 的核心依赖包括：
- `torch`: 深度学习框架
- `pandas`: 数据处理
- `flask`, `flask_cors`: Web 服务器
- `pillow`: 图像处理
- `pydub`: 音频处理
- `websocket`, `websocket-client`: WebSocket 通信
- `openai`: OpenAI API 客户端
- `ffprobe`: 音视频处理

---

## 3. Java 环境配置

ChainStream 支持 Java Agent，需要配置 Java 环境和 Maven。

### 3.1 安装 JDK 11+

ChainStream Java Runtime 需要 JDK 11 或更高版本。

#### macOS
```bash
brew install openjdk@11
# 或安装最新版本
brew install openjdk
```

配置环境变量：
```bash
echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install openjdk-11-jdk
```

#### 验证安装
```bash
java -version
# 应输出: openjdk version "11.x.x" 或更高
```

### 3.2 安装 Maven

#### macOS
```bash
brew install maven
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install maven
```

#### 验证安装
```bash
mvn -version
# 应输出: Apache Maven 3.x.x
```

### 3.3 编译 Java Runtime

```bash
cd chainstream/runtime/java

# 清理并编译项目
mvn clean compile

# 编译 Protocol Buffers
mvn protobuf:compile protobuf:compile-custom

# 打包（可选）
mvn package
```

#### 常见编译问题

1. **protobuf 插件错误**
   ```bash
   # 确保安装了正确的 Maven 插件
   mvn clean install
   ```

2. **依赖下载失败**
   ```bash
   # 检查网络连接
   # 或配置 Maven 镜像（国内用户）
   # 编辑 ~/.m2/settings.xml，添加阿里云镜像
   ```

---

## 4. Node.js 环境配置（前端）

ChainStream 的 Web 界面需要 Node.js 和 npm。

### 4.1 安装 Node.js

#### macOS
```bash
brew install node
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 验证安装
```bash
node --version  # 应输出: v18.x.x 或更高
npm --version   # 应输出: 9.x.x 或更高
```

### 4.2 安装前端依赖

```bash
cd chainstream/runtime/web/frontend

# 安装依赖
npm install
```

#### 前端依赖说明

根据 `package.json`，主要依赖包括：
- **Vue 3**: 前端框架
- **Element Plus**: UI 组件库
- **ECharts**: 数据可视化
- **Monaco Editor**: 代码编辑器
- **Vue Router**: 路由管理
- **Axios**: HTTP 客户端
- **Vite**: 构建工具

### 4.3 编译前端

```bash
# 开发模式（热重载）
npm run dev

# 生产构建
npm run build
```

编译后的文件将输出到 `chainstream/runtime/web/frontend/dist/` 目录。

---

## 5. LLM API 配置

ChainStream 需要配置 LLM API 才能使用 AI 功能。

### 5.1 支持的 LLM 提供商

- **OpenAI**: GPT-4, GPT-3.5
- **Ernie Bot**: 百度文心一言
- **Qwen**: 阿里通义千问
- **其他兼容 OpenAI API 的服务**

### 5.2 配置环境变量

#### 方式一：设置系统环境变量（推荐）

**macOS / Linux**:
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
export GPT_API_URL="https://api.openai.com/v1"
export GPT_API_KEY="your-api-key-here"

# 如果使用百度文心一言
export ERNIE_API_KEY="your-ernie-api-key"

# 使配置生效
source ~/.zshrc  # 或 source ~/.bashrc
```

**Windows**:
```cmd
# 在系统环境变量中添加
setx GPT_API_URL "https://api.openai.com/v1"
setx GPT_API_KEY "your-api-key-here"
```

#### 方式二：使用 .env 文件

在项目根目录创建 `.env` 文件：
```bash
# 在项目根目录
cat > .env << EOF
GPT_API_URL=https://api.openai.com/v1
GPT_API_KEY=your-api-key-here
# 可选：如果使用代理
HTTP_PROXY=http://127.0.0.1:7897
HTTPS_PROXY=http://127.0.0.1:7897
EOF
```

然后在 Python 中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 5.3 国内用户配置建议

如果使用国内 API 服务（如文心一言、通义千问）或 OpenAI 中转服务：

```bash
# 使用国内中转 API
export GPT_API_URL="https://your-proxy-service.com/v1"
export GPT_API_KEY="your-key"

# 或使用代理
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"
```

### 5.4 验证 API 配置

创建测试脚本 `test_llm.py`:
```python
import os
from chainstream.llm import get_model, make_prompt

# 验证环境变量
print(f"GPT_API_URL: {os.getenv('GPT_API_URL')}")
print(f"GPT_API_KEY: {'已设置' if os.getenv('GPT_API_KEY') else '未设置'}")

# 测试 LLM
try:
    llm = get_model('text')
    prompt = make_prompt("你好，请回复'测试成功'")
    response = llm.query(prompt)
    print(f"LLM 响应: {response}")
except Exception as e:
    print(f"LLM 测试失败: {e}")
```

运行测试：
```bash
python test_llm.py
```

---

## 6. 初始化系统

### 6.1 初始化用户系统

ChainStream 使用用户管理系统。首次启动需要创建默认用户。

```bash
# 使用提供的脚本创建默认用户
python create_default_user.py

# 或手动创建用户（如果 users.json 不存在）
cat > users.json << EOF
{
  "users": [
    {
      "username": "liou",
      "password": "hashed_password",
      "level": 1,
      "uuid": "dddc590c-51ec-46db-acc8-b43a958017d3"
    }
  ]
}
EOF
```

### 6.2 启动 ChainStream 服务器

```bash
# 在项目根目录
python start.py
```

启动参数说明：
- `--platform web`: 使用 Web 界面（默认）
- `--platform shell`: 使用命令行界面
- `--enable-java`: 启用 Java Agent 支持
- `-o <dir>`: 指定输出目录

#### 完整启动命令示例
```bash
# 启动带 Java 支持的 Web 服务器
python start.py --platform web --enable-java -o ./output
```

### 6.3 访问 Web 界面

启动成功后，在浏览器中访问：
```
http://localhost:6677
```

默认端口说明：
- **Web 服务器**: `6677`
- **gRPC 服务器**: `50051` （用于 Java Agent 通信）
- **前端开发服务器**: `3000` （仅开发模式）

---

## 7. Android 客户端安装

ChainStream 提供 Android 客户端应用，可以将 Android 设备的传感器数据（摄像头、麦克风、位置等）实时传输到服务器。

### 7.1 获取 APK

项目根目录提供预编译的 APK：
```
ChainStreamClient-debug.apk
```

### 7.2 通过 ADB 安装

#### 7.2.1 安装 ADB

**macOS**:
```bash
brew install android-platform-tools
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt install adb
```

**Windows**:
下载 [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)

#### 7.2.2 连接 Android 设备

1. **启用开发者选项**
   - 进入 `设置` > `关于手机`
   - 连续点击 `版本号` 7次

2. **启用 USB 调试**
   - 进入 `设置` > `开发者选项`
   - 开启 `USB 调试`

3. **连接设备**
   ```bash
   # 连接设备到电脑
   # 验证连接
   adb devices
   # 应显示: List of devices attached
   #         <device-id>  device
   ```

#### 7.2.3 安装 APK

```bash
# 确保在项目根目录
adb install ChainStreamClient-debug.apk

# 如果需要覆盖安装
adb install -r ChainStreamClient-debug.apk

# 如果安装失败，尝试卸载旧版本
adb uninstall io.github.privacystreams.ChainStreamClient
adb install ChainStreamClient-debug.apk
```

### 7.3 配置客户端

1. **打开 ChainStream Client 应用**

2. **配置服务器地址**
   - 在应用设置中输入服务器 IP 地址
   - 默认端口: `6666` (WebSocket)
   - 例如: `ws://192.168.1.100:6666`

3. **授予权限**
   - 授予相机权限
   - 授予麦克风权限
   - 授予位置权限
   - 授予存储权限

4. **连接到服务器**
   - 点击 "连接" 按钮
   - 连接成功后，应用会开始传输传感器数据

### 7.4 从源码编译（可选）

如果需要自定义客户端：

```bash
cd ChainStreamClient

# 使用 Gradle 编译
./gradlew assembleDebug

# 编译后的 APK 位于
# ChainStreamClient/build/outputs/apk/debug/ChainStreamClient-debug.apk
```

#### 编译要求
- **Android Studio**: 最新版本
- **Android SDK**: API Level 33
- **Gradle**: 7.0+

---

## 8. 验证安装

### 8.1 验证 Python 环境

```bash
python -c "import chainstream; print(chainstream.__version__)"
```

### 8.2 验证 Java 环境

```bash
cd AgentStore/多语言
javac -cp "../../chainstream/runtime/java/target/*" DebugHelloAgent.java
java -cp ".:../../chainstream/runtime/java/target/*" DebugHelloAgent
```

### 8.3 验证 Web 服务

```bash
# 启动服务器
python start.py

# 在另一个终端测试 API
curl http://localhost:6677/api/monitor/agents
```

### 8.4 验证 Android 客户端

1. 启动 ChainStream 服务器
2. 启动 Android 客户端并连接
3. 在 Web 界面的 `Streams` 页面查看是否有来自客户端的数据流

---

## 9. 故障排除

### 9.1 Python 相关问题

#### 问题: `ModuleNotFoundError: No module named 'chainstream'`
**解决方案**:
```bash
# 确保在正确的虚拟环境中
conda activate chainstream  # 或 source venv/bin/activate

# 重新安装
pip install -e .
```

#### 问题: `ImportError: cannot import name 'get_model' from 'chainstream.llm'`
**解决方案**:
```bash
# 检查 Python 版本
python --version  # 应该是 3.12

# 清除缓存重新安装
pip cache purge
pip install -e . --force-reinstall
```

### 9.2 Java 相关问题

#### 问题: `mvn: command not found`
**解决方案**:
```bash
# macOS
brew install maven

# Linux
sudo apt install maven
```

#### 问题: gRPC 连接失败
**解决方案**:
```bash
# 确保 Python 服务器正在运行
python start.py --enable-java

# 检查端口是否被占用
lsof -i :50051  # macOS/Linux
netstat -ano | findstr :50051  # Windows

# 如果端口被占用，杀死进程
kill -9 <PID>
```

### 9.3 前端相关问题

#### 问题: `npm install` 失败
**解决方案**:
```bash
# 清理缓存
npm cache clean --force

# 使用国内镜像（国内用户）
npm config set registry https://registry.npmmirror.com

# 重新安装
rm -rf node_modules package-lock.json
npm install
```

#### 问题: 前端编译后浏览器显示旧版本
**解决方案**:
```bash
# 清除浏览器缓存
# Chrome: Ctrl+Shift+Delete / Cmd+Shift+Delete

# 硬刷新页面
# Chrome: Ctrl+Shift+R / Cmd+Shift+R

# 重新编译
npm run build
```

### 9.4 LLM API 问题

#### 问题: `Please set GPT_API_URL and GPT_API_KEY environment variables`
**解决方案**:
```bash
# 检查环境变量
echo $GPT_API_URL
echo $GPT_API_KEY

# 如果未设置，添加到 shell 配置文件
echo 'export GPT_API_URL="your-url"' >> ~/.zshrc
echo 'export GPT_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc
```

#### 问题: `HTTPStatusError: Client error '400 Bad Request'`
**解决方案**:
```bash
# 检查 API key 是否有效
# 检查 API URL 是否正确
# 检查网络连接和代理设置

# 测试 API 连接
curl -X POST $GPT_API_URL/chat/completions \
  -H "Authorization: Bearer $GPT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-3.5-turbo","messages":[{"role":"user","content":"Hello"}]}'
```

### 9.5 Android 客户端问题

#### 问题: `adb: device not found`
**解决方案**:
```bash
# 检查 USB 连接
# 确保启用了 USB 调试
# 重新连接设备
adb kill-server
adb start-server
adb devices
```

#### 问题: 应用安装失败
**解决方案**:
```bash
# 卸载旧版本
adb uninstall io.github.privacystreams.ChainStreamClient

# 清理缓存
adb shell pm clear io.github.privacystreams.ChainStreamClient

# 重新安装
adb install -r ChainStreamClient-debug.apk
```

#### 问题: 客户端无法连接到服务器
**解决方案**:
1. 确保手机和电脑在同一局域网
2. 检查服务器 IP 地址是否正确
3. 检查防火墙设置
4. 使用 `ping` 测试网络连通性
```bash
# 在手机上 ping 服务器 IP
ping 192.168.1.100
```

---

## 10. 快速启动脚本

为方便使用，可以创建快速启动脚本。

### 10.1 创建 `start_chainstream.sh`

```bash
#!/bin/bash

# ChainStream 快速启动脚本

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ChainStream 系统启动脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 1. 检查虚拟环境
if [ -z "$CONDA_DEFAULT_ENV" ] && [ ! -d "venv" ]; then
    echo -e "${YELLOW}警告: 未检测到虚拟环境${NC}"
    echo "请先激活虚拟环境: conda activate chainstream"
    exit 1
fi

# 2. 检查环境变量
if [ -z "$GPT_API_KEY" ]; then
    echo -e "${RED}错误: GPT_API_KEY 未设置${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 环境检查通过${NC}"

# 3. 启动服务器
echo -e "${YELLOW}正在启动 ChainStream 服务器...${NC}"
python start.py --platform web --enable-java

echo -e "${GREEN}✓ ChainStream 已启动${NC}"
echo -e "Web 界面: ${GREEN}http://localhost:6677${NC}"
```

### 10.2 使用脚本

```bash
# 添加执行权限
chmod +x start_chainstream.sh

# 运行
./start_chainstream.sh
```

---

## 11. 进阶配置

### 11.1 配置 Systemd 服务（Linux）

创建 `/etc/systemd/system/chainstream.service`:

```ini
[Unit]
Description=ChainStream Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/ChainStream
Environment="PATH=/path/to/conda/envs/chainstream/bin"
Environment="GPT_API_URL=your-api-url"
Environment="GPT_API_KEY=your-api-key"
ExecStart=/path/to/conda/envs/chainstream/bin/python start.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务:
```bash
sudo systemctl enable chainstream
sudo systemctl start chainstream
sudo systemctl status chainstream
```

### 11.2 使用 Docker（规划中）

目前 ChainStream 尚不提供官方 Docker 镜像，但您可以创建自定义镜像：

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install -e .
EXPOSE 6677 50051

CMD ["python", "start.py"]
```

---

## 12. 相关文档

- [用户指南](mkdoc/docs/UserGuide/QUICK_START.md)
- [Java Agent 开发指南](chainstream/runtime/java/README.md)
- [API 文档](https://mobilellm.github.io/ChainStream/)
- [问题反馈](https://github.com/MobileLLM/ChainStream/issues)

---

## 13. 常见使用场景

### 场景一：开发 Python Agent

```bash
# 1. 激活环境
conda activate chainstream

# 2. 创建 Agent
cd AgentStore/user_agents
cp template_agent.py my_agent.py

# 3. 编辑 Agent
# 编辑 my_agent.py

# 4. 运行 Agent
python my_agent.py
```

### 场景二：开发 Java Agent

```bash
# 1. 编译 Java Runtime
cd chainstream/runtime/java
mvn clean compile

# 2. 创建 Agent
cd ../../AgentStore/多语言
cp DebugHelloAgent.java MyAgent.java

# 3. 编译运行
javac -cp "../../chainstream/runtime/java/target/*:../../chainstream/runtime/java/target/classes" MyAgent.java
java -cp ".:../../chainstream/runtime/java/target/*:../../chainstream/runtime/java/target/classes" MyAgent
```

### 场景三：使用 Android 传感器数据

```bash
# 1. 启动服务器
python start.py

# 2. 安装并启动 Android 客户端
adb install ChainStreamClient-debug.apk

# 3. 在客户端配置服务器地址并连接

# 4. 在 Web 界面查看传感器数据流
# http://localhost:6677/#/monitor/Streams
```

---

## 支持与反馈

如果您在安装过程中遇到问题，请：

1. 查看本文档的[故障排除](#9-故障排除)章节
2. 搜索 [GitHub Issues](https://github.com/MobileLLM/ChainStream/issues)
3. 加入 [Zulip 讨论组](https://mobilellm.zulipchat.com/#narrow/stream/419866-web-public/topic/ChainStream)
4. 提交新的 [Issue](https://github.com/MobileLLM/ChainStream/issues/new)

---

**版本**: v1.0  
**最后更新**: 2025-10-13  
**维护者**: ChainStream Team, Tsinghua AIR

