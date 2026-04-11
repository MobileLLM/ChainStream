# 快速开始

## 什么是 Agent Generator ？

ChainStream 框架的设计初衷是用于支撑更强大的 Agent，其中的重要内容就是 Agent 本身也是该框架的用户、开发者和管理员。Agent 要能够理解ChainStream框架的语法结构，能够基于此写出正确的代码。也就是从自然语言（NL）到代码的转换。

但 NL 距离底层的各种API来说还相差太远，上层的任务描述往往很抽象，而下层的各种API又太复杂。因此，ChainStream 的解决思路就是在上层和下层都进行封装，从而减少两边的差距。如图：

![generator_motivation.png](..%2Fimg%2Fgenerator_motivation.png)

具体的，ChainStream在下层设计了流式数据结构和一个流式框架将各种数据API统一成唯一的接口。而在上层则设计了一个增强用户自然语言描述的Query Optimizer，一个Agent仿真环境Sandbox，以及一套Agent生成过程，也就是 Agent Generator。

ChainStream 的 Agent Generator 能够接受自然语言的任务描述，生成 ChainStream 框架 Agent 代码，并能自主在 ChainStream Sandbox 上调试，以优化最终的生成结果。目前，Agent Generator 主要面向感知任务，并在我们设计的 NL-Sense Benchmark 上有较好的表现。

## 如何使用 Agent Generator 生成 Agent ？

在 [AgentGenerator/generator](https://github.com/MobileLLM/ChainStream/tree/main/AgentGenerator/generator) 目录下，截止到2024年10月，该路径下提供了这些 Generator 的脚本：

``` 
AgentGenerator/generator
├── generator_base.py   # 基类
├── batch_mode          # 生成批量模式Agent的Generator，主要指的是Agent在Sandbox和Runtime中的运行模式，详情见Sandbox部分
│   ├── batch_langchain_zeroshot_generator.py   # 编写batch模式下LangChain Agent的Generator，没有参考例子
│   ├── batch_native_gpt_zeroshot_generator.py  # batch模式下使用GPT直接执行感知任务的Agent，是一个特殊的baseline，不会生成新的Agent，而会返回一段调用GPT的感知脚本
│   ├── batch_native_python_feedback_guided_without_real_task.py    # 编写batch模式下原生Python Agent的Generator，没有参考例子，但会自动在Sandbox中进行调试
│   └── batch_native_python_zeroshot_generator.py   # 编写batch模式下原生Python Agent的Generator，没有参考例子，不会在Sandbox中进行调试
└── stream_mode         # 生成流式模式Agent的Generator，包括使用监听类API的ChainStream Agent，以及使用阻塞类API的Python和LangChain Agent
    ├── chainstream_cot_generator.py    # 编写流式模式下ChainStream Agent的Generator，没有参考例子，使用Chain-of-Thought模式生成
    ├── chainstream_feedback_guided_generator_for_starting.py   # 编写流式模式下ChainStream Agent的Generator，没有参考例子，会自动在Sandbox中进行调试，但没有真实仿真数据，仅能读取硬报错信息
    ├── chainstream_feedback_guided_generator_for_debugging.py  # 编写流式模式下ChainStream Agent的Generator，没有参考例子，会自动在Sandbox中进行调试，但没有真实仿真数据，能读取硬报错信息并能自主发送测试用例和获取输出
    ├── chainstream_feedback_guided_generator_for_real_task.py  # 编写流式模式下ChainStream Agent的Generator，没有参考例子，会自动在Sandbox中进行调试，有真实仿真数据，能获取error、output、stdout信息。是论文中的主方法
    ├── chainstream_feedback_guided_generator_for_real_task_with_example.py  # 编写流式模式下ChainStream Agent的Generator，有参考例子，会自动在Sandbox中进行调试，有真实仿真数据，能获取error、output、stdout信息。是论文中的主方法
    ├── chainstream_few_shot_generator.py    # 编写流式模式下ChainStream Agent的Generator，有参考例子，没有Sandbox调试。是论文中无迭代的方法
    ├── stream_langchain_zeroshot_generator.py    # 编写流式模式下LangChain Agent的Generator，没有参考例子，没有Sandbox调试
    ├── stream_native_python_feedback_with_real_task.py   # 编写流式模式下原生Python Agent的Generator，会自动在Sandbox中进行调试，有真实仿真数据，能获取error、output、stdout信息
    └── stream_native_python_zeroshot_generator.py    # 编写流式模式下原生Python Agent的Generator，没有参考例子，不会在Sandbox中进行调试
```

每个脚本下有形如如下代码的运行方式：

``` python
if __name__ == '__main__':
    from ChainStreamSandBox.tasks import ALL_TASKS
    generator = ChainstreamFeedbackGuidedGeneratorForRealTask(framework_example_number=0)  # 选择一个Generator
    task = ALL_TASKS["HealthTask4"]()  # 选择一个感知任务
    haha = generator.generate_agent(
        StreamListDescription(streams=[     # 描述任务
            {
                "stream_id": "remind_rest",
                "description": "A stream of reminders to take a rest when the heart rate is over 75 in every 2 seconds.",
                "fields": {
                    "Heart Rate": "the heart rate data from the health sensor, float",
                    "reminder": "Heart rate is too high!Remember to rest yourself!"
                }
            }
        ]),
        input_description=task.input_stream_description,    # 指定输入流范围
        task=task,      # 指定任务
    )

    agent_code, latency, tokens = haha[0], haha[1], haha[2]  # 得到生成的Agent代码，延迟，以及生成的token数量

    print(agent_code)
    print(latency)
    print(tokens)
```

只需要选择对应的Generator脚本，编写好任务描述，就可以生成 Agent 代码。


## 如何在 NL-Sense Benchmark 上评测 Agenet Generator ？

详情见 [NL-Sense Benchmark](../../NLSenseBenchmark/QUICK_START/) 部分。



