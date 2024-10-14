# 快速开始

## 什么是 Agent Generator ？

ChainStream 框架的设计初衷是用于支撑更强大的 Agent，其中的重要内容就是 Agent 本身也是该框架的用户、开发者和管理员。Agent 要能够理解ChainStream框架的语法结构，能够基于此写出正确的代码。也就是从自然语言（NL）到代码的转换。

但 NL 距离底层的各种API来说还相差太远，上层的任务描述往往很抽象，而下层的各种API又太复杂。因此，ChainStream 的解决思路就是在上层和下层都进行封装，从而减少两边的差距。如图：

![generator_motivation.png](..%2Fimg%2Fgenerator_motivation.png)

具体的，ChainStream在下层设计了流式数据结构和一个流式框架将各种数据API统一成唯一的接口。而在上层则设计了一个增强用户自然语言描述的Query Optimizer，一个Agent仿真环境Sandbox，以及一套Agent生成过程，也就是 Agent Generator。

ChainStream 的 Agent Generator 能够接受自然语言的任务描述，生成 ChainStream 框架 Agent 代码，并能自主在 ChainStream Sandbox 上调试，以优化最终的生成结果。目前，Agent Generator 主要面向感知任务，并在我们设计的 NL-Sense Benchmark 上有较好的表现。

## 如何使用 Agent Generator 生成 Agent ？



## 如何在 NL-Sense Benchmark 上评测 Agenet Generator ？

### 单任务评测

### 多任务评测



