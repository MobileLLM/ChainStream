# ChainStream框架架构

<img src="../../../img/ChainStreamArchNew.png" alt="ChainStream"/>

上图展示了狭义上的ChainStream框架架构。ChainStream框架主要包含以下几层：

1. **Agent层**：包括用户Agent和系统Agent，类似于Android系统中的用户App和系统App。用户Agent是用户可以自由选装和卸载的，执行具体的用户需求，系统Agent则是系统运行所必须的组件，负责系统的核心功能。
2. **Libraries层**：提供ChainStream的核心抽象，主要包括Stream、Agent、Models、Memory和Prompt等部分。
3. **Runtime层**：负责维护全局流计算图、执行优化和调度、管理和分配资源等。
4. **Abstraction层**：提供对资源的统一虚拟化，主要包括计算模型资源、接口资源、数据源资源等。
5. **Infrastructure层**：管理底层的硬件资源，包括CPU、GPU、网络、存储等。
