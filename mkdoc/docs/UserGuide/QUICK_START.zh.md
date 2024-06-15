# 快速入门

## 系统结构

正如[ChainStream 应用场景](../../SystemOverview/SYSTEM_SCENARIOS/)中提到的，理想的ChainStream产品形态是包括边缘设备-本地服务器-云端服务器三级的。目前系统中已经实现了边缘设备和本地服务器的功能，云端服务器的功能正在开发中。

当前我们提供了面向Android系统的Edge Sensor App，在设备安装该App后即可快速将边缘设备连接到本地服务器中。

对于本地服务器目前需要手动配置环境和运行，后续我们会考虑支持docker并且发布打包好的应用程序。

## 本地服务器配置和启动

首先，从GitHub上clone项目代码：

``` bash
git clone https://github.com/MobileLLM/ChainStream.git
```

然后，根据需求在对应解释器中安装依赖：

``` bash
pip install -e .
```

最后，启动本地服务器：

``` bash
python start.py
```

随后，打开浏览器访问 http://localhost:6677/ ，即可看到本地服务器的欢迎页面。
