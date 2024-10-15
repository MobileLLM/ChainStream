# 快速入门

## 1.什么是 NL-Sense Benchmark？

ChainStream框架旨在支撑更强大Agent的开发和运行，其核心为流式架构，该架构下的Agent代码较难进行Debug和评估，所以我们设计了专门用于Agent测试和评估的Sandbox。

ChainStream的一大主要功能就是根据自然语言生成Agent代码，我们设计了Agent Generator来实现从NL到Code的转换，并在当前主要关注其在感知任务上的效果。但当前缺少从NL直接到感知任务的数据集，所以我们设计了NL-Sense Benchmark作为该领域的评测数据集。

NL-Sense Benchmark是一个开源的NL-to-Sense任务数据集，由多个Task和一套评测 metric 组成。评测的原理是在Sandbox中构造一个拟合真实感知场景的环境，并观测待评测的agent在其中的行为，并分析其输出得到仿真结果，每个Task都代表某一种环境。

具体的，一个task主要包含：
- 任务描述：任务的自然语言描述
- 仿真环境：包括数据、数据在sandbox中的输入顺序、时机等，以及要监听的输出
- 标准程序：人工编写并检查过的 Agent 代码，用于评测仿真结果

由于感知任务的复杂性，难以直接人为标注每个任务输出的标准答案，所以NL-Sense Benchmark的评测方法是比较待测试Agent的输出与标准Agent输出的相似度。

## 2.NL-Sense Benchmark 的构成

NL-Sense Benchmark 共包含Task、Metric和 Sandbox 三个部分。

### 2.1.Sandbox

实际上，ChainStream中支持三类Sandbox，对应了ChainStream Runtime中支持的三种Agent的API类型：

![sandbox_type.png](..%2Fimg%2Fsandbox_type.png)

具体的：

- ChainStream监听函数式：是ChainStream框架Agent的主要API，核心是继承 `chainstream.Agent` 类，编写流转换函数，并通过 `stream.for_each` 等方法完成函数和流的拓扑连接。构造完成后的Agent被分散到各处，其并发运行由ChainStream Runtime统一维护。
- Batch式：为其他框架Agent设计的批次转换式API。Sandbox自动收集所有输入流数据，统一转换为批次数据后传入Agent，Agent返回结果后再统一分发至各个输出流。无法并发，仅作为Sandbox测试API使用，不推荐使用。
- StreamInterface式：为其他框架使用ChainStream流数据设计的API。通过 `stream.get` 和 `stream.put` 等方法与流式 API 交互，实现ChainStream快速融入其他框架。其中 `stream.get` 和 `stream.put` 支持事件驱动，可以实现异步数据传输。

### 2.2.Task

截止到2024年10月，NL-Sense Benchmark共包含覆盖常见感知领域的100+个Task，其中数据来自于10+不同领域各种模态的数据集。在未来，我们希望能够不断扩充Task数量。

### 2.3.Metric

目前，NL-Sense Benchmark的评测方法是比较Agent的运行成功率以及待测试Agent的输出与标准Agent输出的相似度。其中结果相似度主要依靠动态规划寻找结果序列的最优匹配。

此外，我们还实现了一个代码相似度的评估方法，用于衡量Agent生成的代码与标准答案的相似度。由于代码的多样性，该指标仅供残稿而不作为正式评测标准。

## 3.使用 NL-Sense Benchmark 评测
### 3.1.准备

1. Clone ChainStream项目后，Benchmark主要位于 `ChainStreamSandBox` 目录下。
2. Benchmark所使用的原始数据位于 `ChainStreamSandBox/raw_data` 目录下，部分数据以压缩包形式提供。需要手动解压。

### 3.2.开始仿真

#### 3.2.1.单任务

你可以选择Benchmark中的某个特定任务来仿真Agent，你只需要选择三类Sandbox中的一种，然后传入agent代码和任务即可。具体来说，如 2.1.Sandbox 所示，我们提供了三种sandbox：

```
ChainStreamSandbox
├── __init__.py
├── batch_langchain_sandbox.py    # Batch模式有LangChain环境Sandbox
├── batch_native_python_sandbox.py  # Batch模式有Python环境Sandbox
├── stream_interface_sandbox.py    # StreamInterface模式Sandbox
├── chainstream_sandbox.py          # ChainStream监听函数式Sandbox
├── results                         # 存放仿真结果
│   ├── xxx.json
├── sandbox_base.py                 # 基类
└── utils.py    
```

以ChainStream监听函数式Sandbox为例，其中有脚本如：

```python

if __name__ == "__main__":
    from ChainStreamSandBox.tasks import ALL_TASKS

    Config = ALL_TASKS['HealthTask4']    # 选择任务

    agent_file = '''    # 编写Agent代码
import chainstream as cs
from chainstream.agent import Agent

class HealthMonitorAgent(Agent):
    def __init__(self, agent_id: str = "health_monitor_agent"):
        super().__init__(agent_id)
        self.all_health_stream = cs.get_stream(self, "all_health")
        self.remind_rest_stream = cs.get_stream(self, "remind_rest")

    def start(self) -> None:
        def process_heart_rate_batch(items):
            print(f"Received {items}")
            for item in items:
                heart_rate = item.get("HeartRate")
                if heart_rate and heart_rate > 75:
                    reminder = {"reminder": "Heart rate is {heart_rate}! Remember to rest yourself!"}
                    self.remind_rest_stream.add_item(reminder)
                    break  
    
        self.all_health_stream.batch(by_count=1).for_each(process_heart_rate_batch)

    '''
    task_config = Config()
    oj = ChainStreamSandBox(task_config, agent_file, save_result=True, only_init_agent=False)    # 初始化Sandbox

    res = oj.start_test_agent(return_report_path=True)    # 启动仿真
    print(res)
```

只需修改对应脚本参数即可开始 Agent 仿真。Sandbox支持将仿真结果存储到指定路径。结果会被保存成report.json文件，包含了仿真的配置、运行时间、运行结果等信息。

#### 3.2.2.多任务

对于批次测试多个task的需求，我们提供了批次测试脚本，其主要位于 `ChainStreamSandBox/batch_simulation_scripts` 路径下，每个批次脚本都是 `SandboxBatchInterface` 的子类，其会生成log文件来记录一次生成的多个report文件、支持重复运行、支持断点续跑等功能。

### 3.3.结果评估

对于最终的结果，我们提供两种评估方式：运行成功率和结果相似度。
#### 3.3.1.运行成功率

成功率评估代码位于 `ChainStreamSandBox/report_evaluator/eval_success_rate.py` 中，该脚本接受某次批量仿真的log文件，能自动计算该次仿真内的成功率。

#### 3.3.2.结果相似度

结果相似度计算较为复杂，我们比较标准程序和待测试Agent的输出的相似度，具体来说，一个Agent的输出包含多个流，每个流内是包含多个Item的序列，每个序列是由多个不同类型字段组成的。

我们设计了一个基于动态规划算法的序列比较方法来计算结果相似度，具体公示请参考论文。

代码位于 `ChainStreamSandBox/report_evaluator/eval_output_similarity.py` 中，该脚本接受某次批量仿真的log文件，能自动计算该次仿真内的结果相似度。

## 4.定制化

NL-Sense Benchmark 是一个开源项目，你可以根据自己的需求进行定制化。

最主要的定制化包含以下几方面，定制化仅需继承其对应基类即可：

1. 新增原始数据：将数据放置于 `ChainStreamSandBox/raw_data` 目录下，并为新数据撰写一个DataInterface接口类。
2. 新增Task：继承 `ChainStreamSandBox/tasks/task_config_base.py` 类，并在 `ChainStreamSandBox/tasks/__init__.py` 中注册。
3. 新增Generator： 继承 `AgentGenerator/generator/generator_base.py` 类，并在 `AgentGenerator/generator/__init__.py` 中注册。
4. 新增Sandbox： 继承 `ChainStreamSandBox/sandbox_base.py` 类，并在 `ChainStreamSandBox/__init__.py` 中注册。
5. 新增批次测试脚本： 继承 `ChainStreamSandBox/batch_simulation_scripts/sandbox_interface.py` 类，并在 `ChainStreamSandBox/batch_simulation_scripts/__init__.py` 中注册。
6. 新增评测指标： 继承 `ChainStreamSandBox/report_evaluator/evaluator_base.py` 类，并在 `ChainStreamSandBox/report_evaluator/__init__.py` 中注册。

