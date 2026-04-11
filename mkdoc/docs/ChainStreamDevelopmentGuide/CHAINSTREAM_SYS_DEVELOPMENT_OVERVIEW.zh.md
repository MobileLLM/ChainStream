# ChainStream 系统开发概览

## 系统架构

主要参考 [ChainStream 系统架构设计](../../SystemOverview/SYSTEM_SCENARIOS/)。

## 主要模块

- **ChainStream Runtime**：运行时模块，负责执行 ChainStream 应用，包括应用的调度、资源管理、数据流转等。
- **ChainStream SDK**：SDK 模块，提供开发者接口，包括应用开发、数据流转、资源管理等。
- **ChainStream Agent Generator**：Agent 生成器模块，负责根据应用描述文件生成 Agent 代码。
- **ChainStream Dashboard**：控制面板模块，提供可视化的应用管理、监控、报警等功能。
- **ChainStream Agent Store**：Agent 仓库模块，提供 Agent 代码的存储、分发、更新等功能。
- **ChainStream SandBox**：沙箱模块，提供开发者在线调试、测试功能。
- **ChainStream Doc**：文档模块，提供 ChainStream 相关文档的编写、发布、管理等功能。
- **ChainStream Edge Sensor**：边缘传感器模块，提供边缘计算设备的接入、管理、数据采集等功能。

## 参与开发

### 项目交流

目前主要通过开源软件Zulip进行项目管理，推荐所有开发者加入ChainStream Zulip，加入讨论。链接为：[mobilellm.zulipchat.com](https://mobilellm.zulipchat.com/#narrow/stream/419866-web-public/topic/ChainStream)

通过Zulip可以直接联系到ChainStream主要成员，也可以通过邮件 [jia.cheng.liu@qq.com](mailto:jia.cheng.liu@qq.com) 联系到我们。

### 项目管理

Zulip承担一部分项目管理工作。

Github Project和Issue承担一部分项目管理，可以关注[ChainStream-Team planning](https://github.com/orgs/MobileLLM/projects/2)和[ChainStream Issues](https://github.com/MobileLLM/ChainStream/issues)。

### 分支管理

* 主分支：main
* 开发分支：dev
* 功能分支：feature/xxx
* 修复分支：fix/xxx
* 文档分支：docs/xxx
* 临时分支：temp/xxx
* 文档页面：gh-pages

### 开发规范

目前暂时没有特别明确的开发规范，包括issue、PR、commit message等，欢迎大家提出建议。

主要的注意事项就是:

1. 建议通过各种渠道和我们沟通，包括邮件、Zulip、Github Issue等，让我们知道你对项目的想法和意见。
2. 代码风格和命名规范。
3. 推荐使用单元测试和集成测试。
4. 尽量在PR中描述清楚你的修改。
