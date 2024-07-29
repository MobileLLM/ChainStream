chainstream_english_doc = '''
---

**First, I will introduce you to ChainStream, a development framework written in Python for processing streaming data. You need to learn how to use this framework to handle a series of data streams based on the tasks provided by the user. These data streams can be generated by either software or hardware. Examples of hardware-generated streams include image streams from cameras, audio streams from microphones, and location data streams from GPS devices. Examples of software-generated streams include data streams from apps and screenshots from computers. Your task is to select the appropriate data streams and design methods to process these streams according to the user's requirements. During this process, you can also create new data streams. Below, I will introduce the various modules of this framework and their usage:**

**Stream Module:**
**Description:**
- The `chainstream.stream.Stream` class is the core of data streams. Each data stream is an instance of `Stream`, distinguished by a `stream_id`. ChainStream uses listener functions to monitor and process data in the streams. Multiple listener functions can be registered to a single stream. When new data arrives, ChainStream automatically sends it to all registered listeners. The following methods are related to the Stream class:

**API:**
- `chainstream.get_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This method retrieves a `Stream` object based on `stream_id`, typically called in the `__init__()` method of the Agent instance. The first parameter, `agent`, refers to the Agent instance obtaining the stream, usually `self` in the `__init__()` method.
- `chainstream.create_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This method creates a new `Stream` object based on `stream_id`, typically called in the `__init__()` method of the Agent instance. The first parameter, `agent`, refers to the Agent instance creating the stream, usually `self` in the `__init__()` method.
- `chainstream.stream.Stream.for_each(listener_func: Callable[[Union[Dict, str]], Optional[Dict]], to_stream: chainstream.stream.Stream = None) -> chainstream.stream.Stream`: This method registers a listener function to the `Stream` instance. `listener_func` is the function to be registered, and `agent` is the Agent instance registering this function. The return value is an anonymous output stream created for the listener function, which receives the return item from the listener function, allowing for chaining multiple listener functions using `for_each().for_each()`. If `to_stream` is specified, the return value is the `Stream` instance specified by `to_stream` instead of an anonymous output stream. Please note that the listener function `listener_func` has only one input parameter, `item`, and it cannot be written as a member function of the `Agent`. We recommend defining all listener functions within the `Agent.start()` function.
- `chainstream.stream.Stream.batch(by_count: int = None, by_time: int = None, by_item: Union[Dict, str] = None, by_func: Callable[[Union[Dict, str], buffer=chainstream.context.Buffer], Union[Dict, str]] = None, to_stream: chainstream.stream.Stream = None) -> chainstream.stream.Stream`: This method enables batch processing of data streams. Three common batching methods are provided: splitting by count, splitting by time, and splitting by key. The `by_count` parameter indicates that the data is batched every `by_count` items. The `by_time` parameter indicates that the data is batched every `by_time` seconds. The `by_item` parameter indicates that the data is batched every time `by_item` items are received. The `by_func` parameter indicates that the data is grouped based on the return value of the `by_func` function. The return value of `.batch()` is a new anonymous stream instance, and this method can also be chained with the `.for_each()` method to implement listener functions for multiple batches. It is important to note that the data format returned by the three windowing functions is `{'item_list': [item1, item2,...]}`, so listener functions following `.batch()` need to handle the input data accordingly. If `to_stream` is specified, the return value is the `Stream` instance specified by `to_stream` instead of an anonymous output stream.
- `chainstream.stream.Stream.unregister_all(agent: chainstream.agent.Agent) -> None`: This method is used to unregister listener functions registered to the data stream. By specifying the agent instance, all listener functions and their chained anonymous streams created by this Agent will be unregistered.
- `chainstream.stream.Stream.add_item(item: Union[Dict, str, List]) -> None`: This method is used to push data item to the data stream, where the data item can be in any form, including images, audio, text, etc., but needs to be encapsulated in a dictionary format. We only recommend using `str` type items when using the batch processing function `.batch(by_item=...)`, such as passing "EOS" or special markers to indicate the end of a batch. It is important to note that if the item is in list form, each element in the list will be treated as an individual item and will be added to the data stream sequentially.

**Agent Module:**
**Description:**
- You need to create one or more Agents to accomplish the user's tasks. Your Agent instances should inherit from the `chainstream.agent.Agent` class, providing an `agent_id` identifier and implementing the `__init__`, `start()`, and `stop()` methods to manage data stream listening, processing, and output.

**API:**
- `__init__(agent_id: str = "xxx")`: This method instantiates a new Agent object. The `agent_id` parameter specifies the agent's identifier, which should also be passed to the parent class's `__init__(agent_id)` method. Initialization tasks, such as obtaining or creating data streams and getting LLM models, should be performed here.
- `start() -> None`: Define and bind data stream listener functions in this method.
- `stop() -> None`: Unregister all listener functions attached to the data streams by this Agent in this method.

**BufferContext Module:**
**Description:**
- Use the `Buffer` module to create data containers if you need to store processed data during task execution. This container is a queue where data can be added to the end and retrieved from the front. The main purposes of the `Buffer` tool are: first, to temporarily store batches within the function used in `.batch(by_func=func)`, and second, to temporarily store data when you need to listen to multiple input streams. Below, we will introduce the usage of this module:

**API:**
- `chainstream.context.Buffer()`: Instantiate a new `Buffer` object to create a data container.
- `chainstream.context.Buffer.append(data: Union[Dict, str]) -> None`: Add data to the end of the container. The data can be of any form, including images, text, and audio, but needs to be encapsulated in a dictionary format.
- `chainstream.context.Buffer.pop() -> Union[Dict, str]`: Retrieve the data at the front of the container.
- `chainstream.context.Buffer.pop_all() -> List[Union[Dict, str]]`: Retrieve all data from the container as a list.

**LLM Module:**
**Description:**
- The Large Language Model (LLM) module integrates various models capable of processing different types of input data, such as text, images, and audio. Describe your requirements in the processing request, and the model will respond accordingly. Note that ChainStream cannot guarantee the reliability of these llm responses, so you should adjust your llm prompt to describe your processing needs in detail .

**API:**
- `chainstream.llm.get_model(List[Union[Literal["text", "image", "audio"]]]) -> chainstream.llm.LLM`: Instantiate an `LLM` object to obtain a model for data processing. The parameter specifies the types of data the model needs to handle.
- `chainstream.llm.make_prompt(Union[Literal['str'], dict, chainstream.context.Buffer]) -> str`: Process and concatenate all input parameters, converting dictionaries and Buffer contents to strings, and returning a single prompt string. Note that the `make_prompt` method only directly processes and concatenates all input content without any additional processing, you must provide a task description prompt for LLM to describe your processing needs in detail.
- `chainstream.llm.LLM.query(prompt) -> str`: Send the input prompt to the model and return the response. The recommended usage is `LLM.query(make_prompt(...))`.

The main idea of the ChainStream framework is to complete user tasks through multiple steps of Stream transformation and processing. Note that in most tasks, you will need to use LLM to perform specific processing steps, such as text summarization and image understanding. Choose the appropriate model and provide a detailed prompt to describe your processing needs.

You can use other common Python libraries to fulfill your processing requirements, but only introduce additional libraries when necessary. You only need to complete the import and Agent class writing; you do not need to instantiate or invoke this class.

The returned code should follow PEP8 standards.

Now I will give you a specific example to demonstrate how you should use ChainStream to complete an Agent. Suppose you want to summarize all the emails sent by each sender, excluding advertisements. You can provide an Agent like this:

---
'''

english_examples = [
    '''
    
import chainstream as cs

class AgentExampleForEmailTask1(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_email_task_1"):
        super().__init__(agent_id)
        self.email_input = cs.get_stream(self, "all_email")
        self.email_output = cs.get_stream(self, "summary_by_sender")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_ads(email):
            prompt = "is this email an advertisement? answer y or n"
            res = self.llm.query(cs.llm.make_prompt(email['Content'], prompt))
            print("filter_ads", res)
            if res.lower() == 'n':
                return email

        def group_by_sender(email_list):
            email_list = email_list['item_list']
            sender_group = {}
            for email in email_list:
                if email['sender'] not in sender_group:
                    sender_group[email['sender']] = [email]
                else:
                    sender_group[email['sender']].append(email)

            print("group_by_sender", list(sender_group.values()))
            return list(sender_group.values())

        def sum_by_sender(sender_email):
            sender = sender_email[0]['sender']
            prompt = "Summarize these all email here"
            print("sum_by_sender: query", [x['Content'] for x in sender_email], prompt)
            res = self.llm.query(cs.llm.make_prompt([x['Content'] for x in sender_email], prompt))
            print("sum_by_sender", res)
            self.email_output.add_item({
                "sender": sender,
                "summary": res
            })

        self.email_input.for_each(filter_ads).batch(by_count=2).for_each(group_by_sender).for_each(sum_by_sender)
    ''',
    '''
    Now I will give you another example:Suppose you want to filter the temperatures for May and recommend clothing to users based on the temperatures. You can provide an Agent like this:

import chainstream as cs
import pandas as pd

class AgentExampleForSensorTask4(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_weather_task_1"):
        super().__init__(agent_id)
        self.sensor_input = cs.get_stream(self, "all_weather")
        self.sensor_output = cs.get_stream(self, "clothing_recommendation")
        self.llm = cs.llm.get_model("Text")

    def start(self):
        def filter_date(weather):
            date_str = weather.get('Date_Time')
            date = pd.to_datetime(date_str, format='%Y/%m/%d %H:%M:%S', errors='coerce')
            if pd.isna(date):
                return None
            if date.year == 2024 and date.month == 5:
                return weather

        def recommend_clothing(weather_list):
            for weather in weather_list['item_list']:
                temperature = weather.get('Temperature_C')
                if temperature is not None:
                    prompt = "Recommend the suitable clothing today according to the temperature."
                    res = self.llm.query(cs.llm.make_prompt(str(temperature), prompt))
                    self.sensor_output.add_item({
                        "temperature": temperature,
                        "clothing": res
                    })
        self.sensor_input.for_each(filter_date).batch(by_count=2).for_each(recommend_clothing)
    '''
]

