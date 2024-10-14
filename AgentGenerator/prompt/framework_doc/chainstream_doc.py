chainstream_chinese_doc = '''
接下来我将向你介绍ChainStream，这是一个由python代码编写的处理流式数据的开发框架。你需要掌握这一框架的使用方法，按照用户提供给你的任务要求处理一系列数据流，这些数据流由软件或硬件产生。由硬件产生的数据流可以是摄像头产生的图片流，麦克风产生的音频流，GPS产生的位置信息流；由软件产生的数据流可以是由app产生的数据流，电脑的截屏图像流等。你需要选择合适的数据流并设计这些数据流的处理方式来完成用户制定的任务，在这一过程中你也可以创建新的数据流。下面我将介绍这一框架的各个模块以及使用方法：

Stream模块:
Description:
    `chainstream.stream.Stream`类是数据流的核心，每一个数据流都是`Stream`的实例，ChainStream使用`stream_id`用来区分不同的数据流。ChainStream通过在数据流上挂载监听函数的方式完成对数据流的中数据的监听与处理，一个数据流上可能挂载多个监听函数，当数据流中有数据进入时，ChainStream会自动将新数据发送给所有监听函数。下面将介绍有关Stream类的方法
API:
    - `chainstream.get_stream(agent:chainstream.agent.Agent, stream_id:str)->chainstream.stream.Stream`：这一方法能够根据`stream_id`获取一个`Stream`对象，通常情况下在Agent实例的`__init__()`方法中调用`get_stream()`方法来获取系统中已有的数据流对象。第一个参数`agent`是获取该流的Agent实例，通常是`self`。
    - `chainstream.create_stream(agent:chainstream.agent.Agent, stream_id:str)->chainstream.stream.Stream`：这一方法能够根据`stream_id`创建一个新的`Stream`对象，通常情况下构建在Agent实例的`__init__()`方法中调用`create_stream()`方法来创建新的数据流对象。第一个参数`agent`是获取该流的Agent实例，通常是`self`。
    - `chainstream.stream.Stream.for_each(listener_func:Callable[[Union[Dict, str]], Optional[Dict]])->chainstream.stream.Stream`：这一方法能够向`Stream`实例挂载监听函数。`listener_func`是要挂载的监听函数，`agent`是挂载这一函数的`Agent`实例。该函数的返回值是系统为该监听函数自动创建的匿名输出流，监听函数`return`返回的数据都会在该流中。返回`Stream`使得你可以实现`for_each().for_each()`的链式调用，将多个监听函数串联起来。需要注意的是，监听函数`listener_func`的输入参数仅有一个`item`，不可以写成Agent的成员函数。我们推荐将所有监听函数在`Agent.start()`函数内定义。
    - `chainstream.stream.Stream.batch(by_count:int=None, by_time:int=None, by_item:Union[Dict, str]=None, by_func:Callable[[Union[Dict, str], buffer=chainstream.context.Buffer], Union[Dict, str]]=None)->chainstream.stream.Stream`：这一方法能够实现数据流的批次切分，或者称之为分窗。其中提供了三种常用的分窗方式，分别是按数量切分，按时间切分，按键值切分。`by_count`参数表示每`by_count`个数据进行一次批次切分，`by_time`参数表示每`by_time`秒进行一次批次切分，`by_item`参数表示每次接收到`by_item`的数据进行一次批次切分，`by_func`参数表示根据`by_func`函数的返回值进行分组。`.batch()`的返回值`Stream`是新的匿名流实例，该方法同样可以和`.for_each()`方法串联起来，实现多个批次切分的监听函数。需要注意的是，三个分窗函数返回的数据格式都是`{'item_list': [item1, item2,...]}`，所有在`.batch()`之后的监听函数需要注意对输入数据的处理。
    - `chainstream.stream.Stream.unregister_all(agent:chainstream.agent.Agent)->None`:这一方法用于注销数据流上挂载的监听函数，指定agent实例，由这一Agent挂载的所有监听函数及其链式匿名流都会被注销。
    - `chainstream.stream.Stream.add_item(item:Union[Dict, str, List])->None`:这一方法用于向数据流推送数据，其中数据可以是任意形式的数据，包括图像，音频，文本等，但需要封装为字典形式。我们仅推荐针对分窗函数`..batch(by_item=...)`时使用str的item，比如传入"EOS"或者特殊标志标识分批结束。需要注意的是，如果item是列表形式，则会将列表中的每个元素都视为一个item，并将其依次添加到数据流中。
    
Agent模块:
Description:
    你需要创建一个或多个Agent来完成用户指定的任务，你创建的Agent实例需要继承`chainstream.agent.Agent`类，并向父类传入`agent_id`作为标识符号，并实现`__init__`,`start()`,`stop()`方法以完成对相关数据流的监听，处理和结果输出。
API:
    - `__init__(agent_id: str="xxx")`:这一方法通过实例化一个新的Agent对象来创建完成任务的Agent，`agent_id`是必要的参数，用于指定agent的标识符，你也需要将这一参数传入父类__init__(agent_id)中。你也需要在这个方法中进行获取或创建数据流，获取llm模型等初始化资源的操作，为任务的执行进行数据准备。
    - `start()->None`:在这一方法中，你需要定义处理数据流的监听函数，并将这些监听函数绑定到相应的数据流上
    - `stop()->None`:在这一方法中，你需要注销这个Agent挂载到数据流上的所有监听函数。

BufferContext模块:
Description:
    如果在执行任务的过程中需要对处理后的数据进行存储，你可以使用`Buffer`模块创建数据容器。这个数据容器是一个队列，你只能在队尾添加数据，队首取出存储的数据。`Buffer`工具的主要作用一是在`.batch(by_func=func)`的func中用于批次暂存，二是在需要监听多个输入流的时候用作数据的暂存。下面将介绍这一模块的使用方法：
API:
    - `chainstream.context.Buffer()`:这一方法通过实例化一个新的`Buffer`对象来创建数据容器
    - `chainstream.context.Buffer.append(data:Union[Dict, str])->None`:通过这一方法向数据容器的队尾添加数据，你可以存储任何形式的数据，包括图像，文本，音频等。
    - `chainstream.context.Buffer.pop()->Union[Dict, str]`:通过这一方法取出数据容器队首的数据，原来队首的下一个存储的数据会成为新的队首数据。
    - `chainstream.context.Buffer.pop_all()->List[Union[Dict, str]]`:通过这一方法取出数据容器中所有的数据，并返回一个列表。

LLM模块:
Description:
    Large Language Model (LLM) 模块集成了多种模型，这些模型能够根据输入的处理要求，处理多种类型的输入数据，包括文本、图像和声音。你可以在处理要求中描述你的需求，模型会根据你的要求以及你提供的数据进行相应的回复。请注意，ChainStream并不能保证这些模型的回复一定可靠，你需要通过调整prompt尽可能详细地描述你的处理需求。
API:
    - `chainstream.llm.get_model(List[Union[Literal["text", "image", "audio"]]])->chainstream.llm.LLM`:这一方法通过实例化一个`LLM`对象，来获得处理数据的模型。传入参数用来指定模型的type，描述获得的模型需要处理的数据类型。
    - `chainstream.llm.make_prompt(Union[Literal['str'], dict, chainstream.context.Buffer])->str`:这一方法将依次处理和拼接传入的所有参数，比如将dict转换为字符串，将Buffer中的所有数据转换为字符串，并最终将这些字符串拼接成一个prompt并返回。请注意，`make_prompt`仅会拼接所有输入的内容，你必须传入描述任务内容的prompt。
    - `chainstream.llm.LLM.query(prompt)->str`：这是llm对象内的方法，向模型发送输入prompt，返回模型的回复。我们推荐的用法是`LLM.query(make_prompt(...))`
    
ChainStream框架的主要思想是通过多步对于Stream的转换和处理来来完成用户的任务。
需要注意的是，在大多数任务中你都需要借助LLM来实现具体的任务处理步骤，比如文本摘要、图像理解等。你需要根据用户的需求选择合适的模型，并提供足够的prompt来描述你的处理需求。
除了chainstream外，你也可以使用其他的常见Python库来实现你的处理需求，但请只在必要时引入额外的库。
你只需要完成import和Agent class的编写，你不需要对该类进行实例化或者调用等操作。
返回代码需遵循PEP8规范。

'''

chinese_one_example = '''
接下来，我将给你一个具体的例子，来展示你应该如何使用ChainStream来完成一个Agent。假设用户想要筛选新消息队列中的英文消息，你可以提供一个这样的Agent：

import chainstream as cs
from chainstream.llm import get_model
class testAgent(cs.agent.Agent):
    def __init__(self):
        super().__init__("test_arxiv_agent")
        self.input_stream = cs.get_stream("all_arxiv")
        self.output_stream = cs.get_stream("cs_arxiv")
        self.llm = get_model(["text"])
        
    def start(self):
        def process_paper(paper):
            paper_content = paper["abstract"]#[:500]        
            prompt = "Is this abstract related to edge LLM agent? Say 'yes' or 'no'."
            prompt = [
                {
                    "role": "user",
                    "content": prompt+paper_content
                }
            ]
            response = self.llm.query(prompt)
            print(response)
            if response == 'Yes':
                print(paper)
                self.output_stream.add_item(paper)
        self.input_stream.for_each(self, process_paper)

    def stop(self):
        self.input_stream.unregister_all(self)
设计之前你必须要导入chainstream模块，你可以仿照上述代码创建不止一个Agent，让它们互相配合来完成用户任务。除非用户提供了函数工具，你只能使用ChainStream中的LLM模块来解决用户的需求。你提供的Agent必须是完整的，可运行的，你需要完成Agent中的每一个函数，用户不会再对你提供的Agent进行修改。你不能使用各个模块没有提供的函数。
如果你已经掌握了ChainStream框架，并可以使用该框架编写Agent处理用户任务，并准备处理用户的需求。请仅生成一个包含三个单引号（注意不是反引号）的代码块，但不要在代码中包含“python”关键字，不要实例化及生成多余的注释。


'''

chainstream_english_doc = '''
Please act as a data processing programmer and help complete the processing workflow from the source data streams to the target data streams.

---

**First, I will introduce you to ChainStream, a development framework written in Python for processing streaming data. You need to learn how to use this framework to handle a series of data streams based on the tasks provided by the user. These data streams can be generated by either software or hardware. Examples of hardware-generated streams include image streams from cameras, audio streams from microphones, and location data streams from GPS devices. Examples of software-generated streams include data streams from apps and screenshots from computers. Your task is to select the appropriate data streams and design methods to process these streams according to the user's requirements. During this process, you can also create new data streams. Below, I will introduce the various modules of this framework and their usage:**

**Stream Module:**
**Description:**
- The `chainstream.stream.Stream` class is the core of data streams. Each data stream is an instance of `Stream`, distinguished by a `stream_id`. ChainStream uses listener functions to monitor and process data in the streams. Multiple listener functions can be registered to a single stream. When new data arrives, ChainStream automatically sends it to all registered listeners. The following methods are related to the Stream class:

**API:**
- `chainstream.get_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This method retrieves a `Stream` object based on `stream_id`, typically called in the `__init__()` method of the Agent instance. The first parameter, `agent`, refers to the Agent instance obtaining the stream, usually `self` in the `__init__()` method.
- `chainstream.create_stream(agent: chainstream.agent.Agent, stream_id: str) -> chainstream.stream.Stream`: This method creates a new `Stream` object based on `stream_id`, typically called in the `__init__()` method of the Agent instance. The first parameter, `agent`, refers to the Agent instance creating the stream, usually `self` in the `__init__()` method.
- `chainstream.stream.Stream.for_each(listener_func: Callable[[Union[Dict, str]], Optional[Dict]], to_stream: chainstream.stream.Stream = None) -> chainstream.stream.Stream`: This method registers a listener function to the `Stream` instance. `listener_func` is the function to be registered, and `agent` is the Agent instance registering this function. The return value is an anonymous output stream created for the listener function, which receives the return item from the listener function, allowing for chaining multiple listener functions using `for_each().for_each()`. If `to_stream` is specified, the return value is the `Stream` instance specified by `to_stream` instead of an anonymous output stream. Please note that the listener function `listener_func` has only one input parameter, `item`, and it cannot be written as a member function of the `Agent`. We recommend defining all listener functions within the `Agent.start()` function.
- `chainstream.stream.Stream.batch(by_count: int = None, by_time: int = None, by_item: Union[Dict, str] = None, by_func: Callable[[Union[Dict, str], Dict], Tuple[Optional[Dict], Dict]] = None, to_stream: chainstream.stream.Stream = None) -> chainstream.stream.Stream`: This method enables batch processing of data streams. Three common batching methods are provided: splitting by count, splitting by time, and splitting by key. The `by_count` parameter indicates that the data is batched every `by_count` items. The `by_time` parameter indicates that the data is batched every `by_time` seconds. The `by_item` parameter indicates that the data is batched every time `by_item` items are received. The `by_func` parameter indicates that the return values of `batch` are determined by the passed `func`, which must have two inputs and two outputs. The second input and output are a `Dict` with a global lifecycle, initially an empty dictionary. You are responsible for maintaining this dictionary as needed. The first input represents an item, and the first output can be `None`. When the first output is not `None`, the `batch` function will pass this value forward. The return value of `.batch()` is a new anonymous stream instance, and this method can also be chained with the `.for_each()` method to implement listener functions for multiple batches. It is important to note that the data format returned by the three windowing functions is `{'item_list': [item1, item2,...]}`, so listener functions following `.batch()` need to handle the input data accordingly. If `to_stream` is specified, the return value is the `Stream` instance specified by `to_stream` instead of an anonymous output stream.
- `chainstream.stream.Stream.unregister_all(agent: chainstream.agent.Agent) -> None`: This method is used to unregister listener functions registered to the data stream. By specifying the agent instance, all listener functions and their chained anonymous streams created by this Agent will be unregistered.
- `chainstream.stream.Stream.add_item(item: Union[Dict, str, List]) -> None`: This method is used to push data item to the data stream, where the data item can be in any form, including images, audio, text, etc., but needs to be encapsulated in a dictionary format. We only recommend using `str` type items when using the batch processing function `.batch(by_item=...)`, such as passing "EOS" or special markers to indicate the end of a batch. It is important to note that if the item is in list form, each element in the list will be treated as an individual item and will be added to the data stream sequentially.
Note: You must instantiate a new `Stream` using `create_stream` and obtain an existing `Stream` instance using `get_stream`. Instantiating and passing `Stream` through inheritance or other means is not supported.

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
- `chainstream.context.Buffer() -> chainstream.context.Buffer`: Instantiate a new `Buffer` object to create a data container.
- `chainstream.context.Buffer.append(data: Union[Dict, str]) -> None`: Add data to the end of the container. The data can be of any form, including images, text, and audio, but needs to be encapsulated in a dictionary format.
- `chainstream.context.Buffer.pop() -> Union[Dict, str]`: Retrieve the data at the front of the container and remove it from the container.
- `chainstream.context.Buffer.pop_all() -> List[Union[Dict, str]]`: Retrieve all data from the container as a list and remove them from the container.
- `chainstream.context.Buffer.get(idx: int) -> Union[Dict, str]`: Retrieve the data at the specified index in the container but do not remove it from the container.
- `chainstream.context.Buffer.get_all() -> List[Union[Dict, str]]`: Retrieve all data from the container as a list but do not remove them from the container.

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
'''

english_examples = [
    '''
Now I will give you a specific example to demonstrate how you should use ChainStream to complete an Agent. Suppose you want to summarize all the emails sent by each sender, excluding advertisements. You can provide an Agent like this:  

```python
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
```
    ''',
    '''
Suppose you are reading a book at home, if it's getting dark outside, there is an auto-generated command that can adjust the lighting in the room. You can provide an Agent like this:

```python
import chainstream as cs
from chainstream.context import Buffer
class AgentExampleForMultiTask12(cs.agent.Agent):
    def __init__(self, agent_id="agent_example_for_multi_task12"):
        super().__init__(agent_id)
        self.gps_input = cs.get_stream(self, "all_gps")
        self.video_input = cs.get_stream(self, "all_first_person")
        self.command_output = cs.get_stream(self, "adjust_light")
        self.light_input = cs.get_stream(self, "light_intensity")
        self.is_reading = cs.get_stream(self, "is_reading")
        self.llm = cs.llm.get_model("image")
        self.video_buffer = Buffer()

    def start(self):
        def save_video(video_data):
            self.video_buffer.append(video_data)
        self.video_input.for_each(save_video)

        def check_light(light_inputs):
            light_input = light_inputs["item_list"]
            if self.is_reading == "True":
                for light in light_input:
                    prompt = "Do you think the light_intensity is enough for reading books?If not,tell me the best light intensity."
                    res = self.llm.query(cs.llm.make_prompt(prompt,light_input["Light intensity outdoor"]))
                    self.command_output.add_item({
                        "Light intensity indoor": res
                    })
        self.light_input.batch(by_count=2).for_each(check_light)

        def check_place(gps_data):
            if gps_data["Street Address"] == "123 Main St":
                first_person_data = self.video_buffer.pop_all()
                return first_person_data

        def check_reading(first_person_data):
            data_list = first_person_data["item_list"]
            prompt = "Please check whether I am reading books.Simply answer y or n."
            res = self.llm.query(cs.llm.make_prompt(prompt,first_person_data))
            if res.lower()== "y" :
                self.is_reading.add_item({"Status":"True"})
                return first_person_data
            else:
                return None

        self.video_input.for_each(check_place).batch(by_count=2).for_each(check_reading)
```
    '''
]

chainstream_english_doc_with_1_example = chainstream_english_doc + english_examples[0]
chainstream_english_doc_with_2_example = chainstream_english_doc + english_examples[0] + english_examples[1]

