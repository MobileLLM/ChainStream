# Agent Store 指南

在未来，我们之后会提供一个Agent Store服务器，其主要包括Agent包的发布流程、审核机制、版本管理、Agent搜索等功能。

目前，Agent Store还处于规划阶段，我们直接将目前初步实现的Agent放在了Github仓库的agents路径下。用户可以直接在Dashboard中搜索到这些Agent，并直接运行。

## Agent打包

对于一个Agent，需要配置以下内容：

- Agent名称、描述、Agent包（zip格式）
- ChainStream版本
- 设备类型：桌面、手机、眼镜、手表等（数量）
- 部署文档：如何部署设备
- 依赖：其他Agent/流/内存必须可用，以及各自版本
- LLM：必须可用模型
- 公共流/内存：其他Agent可见的输出流/内存

