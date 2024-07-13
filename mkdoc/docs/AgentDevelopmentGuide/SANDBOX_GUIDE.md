# Sandbox Testing Guide

!!! abstract

    Sandbox is a secure environment used to execute and test Agent code for specific Tasks. This guide will show you how to use the Sandbox framework for integrated testing of Agents and Tasks. It covers initializing the ChainStream environment, starting test Agents, and evaluating Task results.

## Task Data Sources

- **daily news**
- **daily dialogue** (text from voice transcription)
- **chat message records**
- **email history**
- **daily arxiv papers**
- **daily stock market updates**

More data sources coming soon...

You can also expand on additional data sources and place them in the `test_data` folder.

## Task Evaluation Metrics

- **Success Rate**: Does the agent start without errors?
- **Input/Output Correctness**: Are input and output streams correctly selected?
- **Static Evaluation**: Differences between Agent Generator code and human routines.
- **Dynamic Evaluation**: Differences between Agent Generator output streams and human routine output streams.

More evaluation metrics coming soon...

You can also expand on additional evaluation metrics and write them in the `evaluate_task` function.

## Task Framework Development

- Select a manually written Agent for evaluation. You can use pre-developed Agents from the `scripts` folder or write your own. For the process, refer to the [ChainStream Agent Development Guide](http://127.0.0.1:8000/ChainStream/AgentDevelopmentGuide/AGENT_DEVELOPMENT_OVERVIEW/).

- Choose a Task for evaluation. You can refer to various tasks in the `tasks` folder or create a new Task, ensuring it inherits from `task_config_base.py`'s TaskConfig class. Define specific task descriptions, input-output streams, and override three methods:

```
1. init_environment: Initialize task environment, create test agents and streams.
2. start_task: Start the source stream.
3. evaluate_task: Evaluate output stream data processed by the Agent, and return evaluation results.
```

- Run the selected Agent and Task in the Sandbox.

!!! note

    You can add your Task to the `__init__.py` file in the `tasks` folder and store it in a dictionary named `ALL_TASKS` for centralized management and easier future referencing.

## Sandbox Framework Development

!!! note

    Requires a running Runtime with evaluation mode enabled, capable of monitoring actions of the testing Agent, including various APIs of the Chainstream Agent module.

### 1. Initialization

- **ChainStream Initialization**: Set the Task and Agent to be used.
- **Get Runtime Environment**: Initialize the Runtime using `get_chainstream_core()`.
- **Agent Setup**: Read Agent script content based on file format.

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

### 2. Start Testing Agent

- **Initialize Task Environment**: Call `init_environment` to initialize the Task environment within Runtime.
- **Start Agent**: Call `_start_agent` to create an Agent instance, start it, and configure various action listeners.
- **Begin Task Flow**: Call `start_task` to start the Task data source.
- **Evaluate Task**: Call `evaluate_task` to collect test results after the data source ends, archive them, and invoke evaluation functions.

```python
def start_test_agent(self):
    self.task.init_environment(self.runtime)
    self._start_agent()
    self.task.start_task(self.runtime)
    self.task.record_output(self.runtime)
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

    During development, you can add multiple custom exception classes like `ExecError`, `StartError`, `RunningError`, etc., to capture and handle different stages' potential error scenarios, improving testing efficiency.

### 3. Testing Example

!!! success

    Below is an example demonstrating how to use the `SandBox` class for specific Task testing.

Here's how you can use the `SandBox` class for specific Task testing:

```python
if __name__ == "__main__":
    from tasks import ALL_TASKS_OLD

    ArxivTaskConfig = ALL_TASKS_OLD['ArxivTask']

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

            self.input_stream.for_each(self, process_paper)

        def stop(self):
            self.input_stream.unregister_all(self)
    '''

    oj = SandBox(ArxivTaskConfig(), agent_file)
    oj.start_test_agent()
```

In this example, we have defined a specific Task. The `agent_file` includes the Agent required to execute this Task. This allows us to instantiate and start the `TestAgent`, testing its performance.