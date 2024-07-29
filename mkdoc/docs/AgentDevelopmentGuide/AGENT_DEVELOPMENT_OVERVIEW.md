# Agent Development Guide for ChainStream

!!! abstract

    This development guide provides detailed steps and guidance to help developers utilize the ChainStream framework for managing data flows and creating agents. With these guidelines, developers can effectively use ChainStream APIs and modules to develop agents, achieving efficient data flow management and responsive mechanisms to meet various complex data task requirements.

## Chainstream Agent Development Module Overview

### Stream Module

- **Description**: The `Stream` class forms the core of data streams, where each data stream is an instance of `Stream` identified by a `stream_id`. ChainStream enables data monitoring and processing by attaching listener functions to these data streams.
- API:
  - `chainstream.get_stream(stream_id)`: Retrieves a `Stream` object based on the provided `stream_id`, typically used when constructing an `Agent` instance to obtain input and output streams.
  - `chainstream.create_stream(stream_id)`: Creates a new data stream and returns a `Stream` instance identified by `stream_id`.
  - `chainstream.stream.Stream.for_each(agent, listener_func)`: Attaches a listener function to the `Stream` instance.
  - `chainstream.stream.Stream.unregister_all(agent)`: Unregisters all listener functions attached to the data stream.
  - `chainstream.stream.Stream.add_item(data)`: Pushes data into the data stream.

### Agent Module

- **Description**: One or more agents need to be created to accomplish user-specified tasks. Agent instances should inherit from the `chainstream.agent.Agent` class, passing an `agent_id` identifier to the superclass, and implement `__init__`, `start()`, and `stop()` methods to handle data stream monitoring, processing, and result output.
- API:
  - `__init__(agent_id)`: Initializes a new `Agent` object for task completion, where `agent_id` is a mandatory parameter used to identify the agent within the system. Initialization of resources and data streams can be done within this method.
  - `start()`: Defines the listener function for processing data streams and binds it to the respective data stream.
  - `stop()`: Unregisters all listener functions attached by the agent to the data stream upon completion.

### BufferContext Module

- **Description**: If data storage is required after processing, the `BufferContext` module can be used to create a data container—a queue where data can only be added at the tail and retrieved from the head.
- API:
  - `chainstream.context.BufferContext()`: Instantiates a new `BufferContext` object to create a data container.
  - `chainstream.context.BufferContext.add(data)`: Adds data to the tail of the data container.
  - `chainstream.context.BufferContext.get()`: Retrieves data from the head of the data container.

### LLM Module

- **Description**: The LLM (Language Learning Model) module integrates various models capable of handling different types of input data such as text, images, and audio. Models respond based on input processing requirements and provided data.
- API:
  - `chainstream.llm.get_model(type)`: Instantiates an LLM object to obtain a model for processing data.
  - `chainstream.llm.make_prompt(query, data)`: Converts processing requirements and input data into a format accepted by the model.
  - `chainstream.llm.query(prompt)`: Sends input prompt to the model and returns the model's response.

## Agent Development Guide

### Agent_id

In ChainStream, `Agent_id` is a string used to uniquely identify an agent instance.

When creating an agent, it's essential to specify a unique `Agent_id` to identify and manage different agents within the system.

- `Agent_id` can be any string that adheres to naming conventions, such as `test_agent`, `arxiv_processor`, etc.
- To avoid conflicts, descriptive names are recommended, and special characters or spaces should be avoided.

### API Usage

- When creating a new agent, inherit from the `chainstream.agent.Agent` class and implement its methods.
- In the `__init__` method, call the superclass constructor and initialize resources and data streams.
- In the `start` method, define the listener function for processing data streams and bind it to the respective data stream.
- Apart from the listener function, typical tasks include data preprocessing, parsing, model querying, response handling, and format conversion.
- In the `stop` method, unregister all listener functions attached by the agent to the data stream.

### Naming Conventions

Follow Python naming conventions for modules, classes, functions, and variables.

- Use lowercase letters and underscores `_` to separate words for module and file names.
- Use CamelCase for class names.
- Use lowercase letters and underscores `_` for function and variable names.

## Example Agent

!!! success

    This example demonstrates how to implement an agent in ChainStream to extract Arxiv abstracts. Let's start developing the agent following the provided APIs and adhering to the agent development guidelines!

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
                
        self.input_stream.for_each(self, process_paper)

    def stop(self):
        self.input_stream.unregister_all(self)
```

