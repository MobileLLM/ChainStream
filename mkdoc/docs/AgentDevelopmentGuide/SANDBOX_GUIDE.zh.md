# 沙盒测试指南

!!! abstract

    Sandbox是一个安全的环境，用于执行和测试特定Task下的Agent代码。通过本指南，您将了解如何利用Sandbox框架进行Agent和Task的集成测试。包括初始化ChainStream环境、启动测试Agent和评估Task结果的流程。

## Task数据源

- **daily news**（每日新闻）
- **daily dialogue**（语音转录后的文本信息）
- **chat message**（聊天记录）
- **email history**（邮件历史记录）
- **daily arxiv paper**（日常arxiv论文）
- **daily stock**（股票资讯）

更多的数据源更新中...

您也可以拓展更多的数据源，并置于文件夹test_data下。

## Task评测指标

  - **运行成功率**：agent start后能不能不报错
 - **输入输出选取正确性**：input、output stream是否正确选取
 - **静态评测**：Agent Generator生成代码与人类例程的差别
 - **动态评测**：Agent Generator生成代码的output stream与人类例程output stream的差别

更多的评测指标更新中...

您也可以拓展更多的评测指标，并写在evaluate_task函数中。

## Task框架开发

- 选定待评测的人工写的Agent，可选用scripts文件夹下已开发好的Agent，也可自行编写Agent，具体流程可参考[`ChainStream Agent开发指南`](http://127.0.0.1:8000/ChainStream/zh/AgentDevelopmentGuide/AGENT_DEVELOPMENT_OVERVIEW/)。

- 选择待评测的Task，可参考tasks文件夹下各类tasks，或者自行新建一个Task，但需继承task_config_base.py的TaskConfig类，加入特定的task描述，定义好输入输出流，并覆写三个方法：
  
  ```
  1. init_environment：初始化task环境，创建测试用的agent和stream
  2. start_task： 启动源头stream
  3. evaluate_task：对Agent处理后的output stream数据进行评测，返回评测结果
  ```

+ 将待评测的Agent和Task置于Sandbox中运行

!!! note

    可将您的Task加入到tasks文件夹下__init__.py文件,存储在名为 ALL_TASKS 的字典中进行集中管理，方便后续轻松调用。

## 沙盒框架开发

!!! note

    需要有一个运行着的Runtime，并且该Runtime打开了评测模式，可以监控测试Agent的动作，监控的动作包括Chainstream Agent模块的各种API。

### 1. 初始化

- **ChainStream 初始化**: 设置所使用的Task和Agent。
- **获取运行时环境**: 使用 `get_chainstream_core()` 初始化Runtime。
- **Agent 设置**: 根据文件格式读取 Agent 脚本内容。

```python
def __init__(self, task, agent_file):
    cs_server.init(server_type='core')
    cs_server.start()
    self.runtime = cs_server.get_chainstream_core()
    self.task = task
    if isinstance(agent_file, str) and agent_file.endswith('.py'):
        with open(agent_file, 'r') as f:
            agent_file = f.read()
    self.agent_str = agent_file
    self.result = {}
```

### 2. 启动测试 Agent

- **初始化任务环境**: 调用 `init_environment` 在Runtime中初始化Task环境。
- **启动 Agent**: 调用 `_start_agent` 创建Agent实例并启动，配置各动作监听。
- **开始任务流**: 调用 `start_task` 启动Task数据源。
- **评估任务**: 调用 `evaluate_task` 数据源结束后收集测试结果，存档并调用评测函数。

```python
def start_test_agent(self):
    self.task.init_environment(self.runtime)
    self._start_agent()
    self.task.start_task(self.runtime)
    self.task.evaluate_task(self.runtime)
```

```python
def _start_agent(self):
    namespace = {}
    exec(self.agent_str, globals(), namespace)

    class_object = None
    globals().update(namespace)
    for name, obj in namespace.items():
        if isinstance(obj, type):
            class_object = obj
            break

    if class_object is not None:
        self.agent_instance = class_object()
        self.agent_instance.start()
```

!!! tip

    在开发阶段，您可加入多个自定义异常类，例如 `ExecError`, `StartError`, `RunningError` 等，用于捕获和处理不同阶段可能出现的异常情况，提高测试效率。

### 3. 测试示例

!!! success

    下面以一个示例展示如何使用 `SandBox` 类进行具体任务的测试

下面展示了如何使用 `SandBox` 类进行具体任务的测试：

```python
if __name__ == "__main__":
    from tasks import ALL_TASKS
    ArxivTaskConfig = ALL_TASKS['ArxivTask']

    agent_file = '''
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
                if "abstract" in paper:
                    paper_title = paper["title"]
                    paper_content = paper["abstract"]
                    paper_versions = paper["versions"]
                    stage_tags = ['Conceptual', 'Development', 'Testing', 'Deployment', 'Maintenance','Other']
                    prompt = "Give you an abstract of a paper: {} and the version of this paper:{}. What tag would you like to add to this paper? Choose from the following: {}".format(paper_content,paper_versions, ', '.join(stage_tags))
                    prompt_message = [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                    response = self.llm.query(prompt_message)
                    print(paper_title+" : "+response)
                    self.output_stream.add_item(paper_title+" : "+response)

            self.input_stream.register_listener(self, process_paper)

        def stop(self):
            self.input_stream.unregister_listener(self)
    '''

    oj = SandBox(ArxivTaskConfig(), agent_file)
    oj.start_test_agent()
```

在这个示例中，我们定义好了特定的Task，`agent_file` 中加入了需要执行此Task的Agent，便可以将 `TestAgent` 实例化并启动，测试其表现。
