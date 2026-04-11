# 指标

* 指标3.1：基于飞桨框架和文心一言，构建面向交通、物联网、健康、教育等不同行业场景的 4 套工具链，并发布到星河社区。工具链能够为开发者提供行业应用相关的算法、模型、工具等核心功能，同时具备Agent 的定制化开发、规划、记忆、调用等能力
* 指标3.2：AI Agent 工具链功能模块数量不少于 3 个，工具链提供对已开发 Agent的性能、安全评估，以及对用户数据的加密鉴权功能
* 指标3.3：AI Agent 工具链兼容平台数量不少于 2 个，工具链提供Agent 跨平台运行的兼容性保障，支持Windows、Linux等多操作系统部署，支持 Python、等多语言开发
* 指标3.4：Agent数量4个，基于课题研制的AI Agent工具链构建面向交通、物联网、健康、教育等不同行业场景的4个AI Agent，并发布到星河社区。AI Agent具备在线学习能力，能动态感知周边环境或业务相关结构化数据，并调整规划和行动能力。


# 待升级内容

* 3.1：
  * 感觉还好，工具链中的Buffer凑乎算Memory（done）
* 3.2：
  * 性能：在dashboard中增加一个agent吞吐率和平均延时
  * 安全：stream根据user做隔离、加taint tracking
  * 加密鉴权：系统增加登陆功能
* 3.3：
  * 兼容Win、Linux：Python Runtime打包到兼容两种平台
  * 支持Python、Java：Agent Func的挂载需注明语言类型，执行时调用对应的虚拟机，使用SDK时转向唯一的Python Runtime
* 3.4：
  * Agent：Prompt增加例子（需要支持双语）， Sandbox能够调试，多轮debug能支持多平台和多语言，在prompt种增加memory部分


