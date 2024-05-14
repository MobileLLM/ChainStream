chainstream_english_prompt_v1 = '''
# ChainStream Usage Guide

ChainStream is a Python-based framework designed for developing streaming LLM (Large Language Model) Agents. These agents are intended to process streaming sensor data and perform perception tasks. Sensors include hardware sensors (such as cameras, microphones, and location sensors) and software sensors (such as apps, web APIs, and screen captures). ChainStream leverages the general capabilities of LLMs to better understand the physical world, while also allowing the use of smaller models as tools to assist in perception tasks.

## Agent Module

### Description

The Agent module is the base class that each agent must inherit. Its main functions are to listen to streaming data, process the data, and output the results.

### API

- `__init__(self, agent_id)`: In the initialization method, allocate all necessary resources and pass the new agent's global identifier `agent_id` to the parent class's `__init__(agent_id)` method.
- `start(self)`: Bind the listening functions to the stream in the `start` method. Custom listening functions can be defined.
- `stop(self)`: Release resources in the `stop` method.


## Stream Module

### Description

The Stream module acts as a data pipeline, where multiple functions listen for incoming data and automatically call the listening functions for processing.

### API

- `chainstream.get_stream(stream_id)`: Get a Stream object based on the `stream_id`.
- `chainstream.create_stream(stream_id)`: Create a new Stream object and return it.
- `chainstream.stream.Stream.register_listener(agent, listener_func)`: Register a listening function with the Stream object.
- `chainstream.stream.Stream.unregister_listener(agent)`: Unregister a listening function from the Stream object.

NOTE: listener_func need to be a stastic method that takes a single argument `data`. So it's better to define it in start() or as a lambda function.


## Buffer Module

### Description

The Buffer module is a data container that allows you to add data to it or read data from it.

### API

- `chainstream.context.BufferContext()`: Create a new Buffer object and return it.
- `chainstream.context.BufferContext.add(data)`: Add data to the Buffer.
- `chainstream.context.BufferContext.get()`: Read data from the Buffer.


## LLM Module

### Description

The LLM module encapsulates various large models. You only need to focus on the modality of the required LLM to directly call the corresponding API to complete tasks.

### API

- `chainstream.llm.get_model(type)`: Create a new LLM object and return it. `type` can be a subset of `['text', 'image', 'audio']`.
- `chainstream.llm.make_prompt(str | image | audio | BufferContext | Memory)`: Create a new LLM prompt object and return it.
- `chainstream.llm.query(prompt)`: Send a prompt to the LLM model and return the model's response.


## Memory Module

### Description

The Memory module encapsulates various data storage methods. You can add data to it or read data from it.

### API

- `chainstream.memory.get_memory(memory_id)`: Get a Memory object based on `memory_id`.
- `chainstream.memory.create_memory(memory_id)`: Create a new Memory object and return it.
- `chainstream.memory.Memory.add(data)`: Add data to the Memory.
- `chainstream.memory.Memory.get()`: Read data from the Memory.

By integrating these modules, ChainStream enables developers to create powerful streaming LLM Agents that can process multimodal data and perform complex perception tasks. As a pragramming framework, you only need write agent, and the exec of it will be handled by ChainStream Runtime.

'''

chainstream_english_prompt_v2 = '''
# ChainStream Usage Guide

ChainStream is a Python-based framework designed for developing streaming LLM (Large Language Model) Agents. These agents are intended to process streaming sensor data and perform perception tasks. Sensors include hardware sensors (such as cameras, microphones, and location sensors) and software sensors (such as apps, web APIs, and screen captures). ChainStream leverages the general capabilities of LLMs to better understand the physical world, while also allowing the use of smaller models as tools to assist in perception tasks.

## Agent Module

### Description

The Agent module is the base class that each agent must inherit. Its main functions are to listen to streaming data, process the data, and output the results.

### API

- `__init__(self, agent_id)`: In the initialization method, allocate all necessary resources and pass the new agent's global identifier `agent_id` to the parent class's `__init__(agent_id)` method.
- `start(self)`: Bind the listening functions to the stream in the `start` method. Custom listening functions can be defined.
- `stop(self)`: Release resources in the `stop` method.

## Stream Module

### Description

The Stream module acts as a data pipeline, where multiple functions listen for incoming data and automatically call the listening functions for processing.

### API

- `chainstream.get_stream(stream_id)`: Get a Stream object based on the `stream_id`.
- `chainstream.create_stream(stream_id)`: Create a new Stream object and return it.
- `chainstream.stream.Stream.register_listener(agent, listener_func)`: Register a listening function with the Stream object.
- `chainstream.stream.Stream.unregister_listener(agent)`: Unregister a listening function from the Stream object.

> **NOTE:** `listener_func` needs to be a static method that takes a single argument `data`. So it's better to define it in `start()` or as a lambda function.

## Buffer Module

### Description

The Buffer module is a data container that allows you to add data to it or read data from it.

### API

- `chainstream.context.BufferContext()`: Create a new Buffer object and return it.
- `chainstream.context.BufferContext.add(data)`: Add data to the Buffer.
- `chainstream.context.BufferContext.get()`: Read data from the Buffer.

## LLM Module

### Description

The LLM module encapsulates various large models. You only need to focus on the modality of the required LLM to directly call the corresponding API to complete tasks.

### API

- `chainstream.llm.get_model(type)`: Create a new LLM object and return it. `type` can be a subset of `['text', 'image', 'audio']`.
- `chainstream.llm.make_prompt(data)`: Create a new LLM prompt object and return it. `data` can be a string, image, audio, BufferContext, or Memory.
- `chainstream.llm.query(prompt)`: Send a prompt to the LLM model and return the model's response.

## Memory Module

### Description

The Memory module encapsulates various data storage methods. You can add data to it or read data from it.

### API

- `chainstream.memory.get_memory(memory_id)`: Get a Memory object based on `memory_id`.
- `chainstream.memory.create_memory(memory_id)`: Create a new Memory object and return it.
- `chainstream.memory.Memory.add(data)`: Add data to the Memory.
- `chainstream.memory.Memory.get()`: Read data from the Memory.

## Integration and Use

By integrating these modules, ChainStream enables developers to create powerful streaming LLM Agents that can process multimodal data and perform complex per
ception tasks. As a programming framework, you only need to write the agent, and the execution of it will be handled by ChainStream Runtime.
'''

chainstream_english_prompt_v3 = '''
# ChainStream Usage Guide

ChainStream is a Python-based framework designed for developing streaming LLM (Large Language Model) Agents. These agents are intended to process streaming sensor data and perform perception tasks. Sensors include hardware sensors (such as cameras, microphones, and location sensors) and software sensors (such as apps, web APIs, and screen captures). ChainStream leverages the general capabilities of LLMs to better understand the physical world, while also allowing the use of smaller models as tools to assist in perception tasks.

## Agent Module

### Description

The Agent module is the base class that each agent must inherit. Its main functions are to listen to streaming data, process the data, and output the results.

### API

- `__init__(self, agent_id)`: In the initialization method, allocate all necessary resources and pass the new agent's global identifier `agent_id` to the parent class's `__init__(agent_id)` method.
- `start(self)`: Bind the listening functions to the stream in the `start` method. Custom listening functions can be defined.
- `stop(self)`: Release resources in the `stop` method.

## Stream Module

### Description

The Stream module acts as a data pipeline, where multiple functions listen for incoming data and automatically call the listening functions for processing.

### API

- `chainstream.get_stream(stream_id)`: Get a Stream object based on the `stream_id`.
- `chainstream.create_stream(stream_id)`: Create a new Stream object and return it.
- `chainstream.stream.Stream.register_listener(agent, listener_func)`: Register a listening function with the Stream object.
- `chainstream.stream.Stream.unregister_listener(agent)`: Unregister a listening function from the Stream object.

> **NOTE:** `listener_func` must to be a static method that must takes one single argument `data`. So it's better to define it in `start()` like this:

```python
class MyAgent(Agent):
    def start(self):
        def process_data(data):
            # process data here
            pass
        self.stream.register_listener(self, lambda data: process_data)
    
```

## Buffer Module

### Description

The Buffer module is a data container that allows you to add data to it or read data from it.

### API

- `chainstream.context.BufferContext()`: Create a new Buffer object and return it.
- `chainstream.context.BufferContext.add(data)`: Add data to the Buffer.
- `chainstream.context.BufferContext.get()`: Read data from the Buffer.

## LLM Module

### Description

The LLM module encapsulates various large models. You only need to focus on the modality of the required LLM to directly call the corresponding API to complete tasks. Note that you need to write task prompt as you need, and combine multi-modal source into one prompt by using `make_prompt` function. And you still need to call `query` function to get the model's response and do something with it.

### API

- `chainstream.llm.get_model(type)`: Create a new LLM object and return it. `type` can be a subset of `['text', 'image', 'audio']`.
- `chainstream.llm.make_prompt([text, image, audio, BufferContext, Memory])`: Create a new LLM prompt object and return it. `data` can be a string, image, audio, BufferContext, or Memory.
- `chainstream.llm.query(prompt)`: Send a prompt to the LLM model and return the model's response.

## Memory Module

### Description

The Memory module encapsulates various data storage methods. You can add data to it or read data from it.

### API

- `chainstream.memory.get_memory(memory_id)`: Get a Memory object based on `memory_id`.
- `chainstream.memory.create_memory(memory_id)`: Create a new Memory object and return it.
- `chainstream.memory.Memory.add(data)`: Add data to the Memory.
- `chainstream.memory.Memory.get()`: Read data from the Memory.

## Integration and Use

By integrating these modules, ChainStream enables developers to create powerful streaming LLM Agents that can process multimodal data and perform complex perception tasks. As a programming framework, you only need to write the agent, and the execution of it will be handled by ChainStream Runtime.
'''

