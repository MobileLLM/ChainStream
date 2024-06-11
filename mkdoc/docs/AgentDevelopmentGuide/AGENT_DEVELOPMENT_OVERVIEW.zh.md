# Agent development guide for chainstream

ChainStream 是一个处理流式数据的开发框架，用 Python 编写。它允许开发者根据用户提供的任务要求处理各种数据流，这些数据流可以由软件或硬件产生。硬件产生的数据流可能包括摄像头的图像流、麦克风的音频流、GPS 的位置信息流，而软件产生的数据流可能是应用程序产生的数据流、电脑截屏图像流等。


## Chainstream Agent模块介绍

### Stream 模块

- **描述**：Stream 类是数据流的核心，每一个数据流都是 Stream 的实例，通过 stream_id 区分不同的数据流。ChainStream 通过挂载监听函数到数据流上完成对数据的监听与处理。
- **API**：
  - `chainstream.get_stream(stream_id)`: 根据 stream_id 获取一个 Stream 对象，通常在构建 Agent 实例时需要使用此方法获取输入和输出流。
  - `chainstream.create_stream(stream_id)`: 创建一个新的数据流，并返回 Stream 实例，以 stream_id 作为标识符。
  - `chainstream.stream.Stream.register_listener(agent, listener_func)`: 向 Stream 实例挂载监听函数。
  - `chainstream.stream.Stream.unregister_listener(agent)`: 注销数据流上挂载的监听函数。
  - `chainstream.stream.Stream.add_item(data)`: 向数据流推送数据。

### Agent 模块

- **描述**：需要创建一个或多个 Agent 来完成用户指定的任务。Agent 实例需要继承 `chainstream.agent.Agent` 类，并向父类传入 agent_id 作为标识符，并实现 `__init__`, `start()`, `stop()` 方法完成对相关数据流的监听、处理和结果输出。
- **API**：
  - `__init__(agent_id)`: 实例化一个新的 Agent 对象来创建完成任务的 Agent，agent_id 是必要的参数，用于指定 Agent 的标识符，需要传入父类中。在该方法中，您可以初始化资源和数据流。
  - `start()`: 定义处理数据流的监听函数，并将其绑定到相应的数据流上。
  - `stop()`: 注销该 Agent 挂载到数据流上的所有监听函数。

### BufferContext 模块

- **描述**：如果需要对处理后的数据进行存储，可以使用 BufferContext 模块创建数据容器，这个数据容器是一个队列，只能在队尾添加数据，队首取出存储的数据。
- **API**：
  - `chainstream.context.BufferContext()`: 实例化一个新的 BufferContext 对象来创建数据容器。
  - `chainstream.context.BufferContext.add(data)`: 向数据容器的队尾添加数据。
  - `chainstream.context.BufferContext.get()`: 取出数据容器队首的数据。

### LLM 模块

- **描述**：LLM 模块集成了多种模型，可以处理多种类型的输入数据，包括文本、图像和声音。模型会根据输入的处理要求以及提供的数据进行相应的回复。
- **API**：
  - `chainstream.llm.get_model(type)`: 实例化一个 LLM 对象，获得处理数据的模型。
  - `chainstream.llm.make_prompt(query ,data)`: 将处理要求和输入数据转换成模型能够接受的输入。
  - `chainstream.llm.query(prompt)`: 向模型发送输入 prompt，返回模型的回复。

## Agent 编写指南

### API 使用

- 创建新的 Agent 时，需要继承 `chainstream.agent.Agent` 类，并实现其中的方法。
- 在 `__init__` 方法中，需要调用父类的构造方法，并初始化资源和数据流。
- 在 `start` 方法中，定义处理数据流的监听函数，并将其绑定到相应的数据流上。
- 在 `stop` 方法中，注销该 Agent 挂载到数据流上的所有监听函数。

### Package 规范

- **包名称**：使用小写字母和下划线来分隔单词。
- **版本管理**：遵循语义化版本控制（MAJOR.MINOR.PATCH）。
- **依赖关系**：在 `requirements.txt` 或 `setup.py` 文件中指定依赖关系，使用 `pip` 或其他适当的工具来管理依赖关系。

### Agent ID、版本号和依赖

- 每个 Agent 需要有一个唯一的 `agent_id` 来标识。
- 更新包版本时，应遵循语义化版本控制。
- 明确指定依赖关系及其版本，以确保 Agent 的兼容性和正常运行。

## 示例 Agent

```python
import chainstream as cs
from chainstream.llm import get_model

class TestAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream("all_arxiv")
        self.output_stream = cs.get_stream("cs_arxiv")
        self.llm = get_model(["text"])
        
    def start(self):
        def process_paper(paper):
            paper_content = paper["abstract"]
            prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
            prompt = [{"role": "user", "content": prompt+paper_content}]
            response = self.llm.query(prompt)
            print(response)
            if response == 'Yes':
                print(paper)
                self.output_stream.add_item(paper)
                
        self.input_stream.register_listener(self, process_paper)

    def stop(self):
        self.input_stream.unregister_listener(self)
```