
BATCH_NATIVE_PYTHON_CHINESE_PROMPT = """
请你扮演一个数据处理程序员，帮助完成从源头数据流到目标数据流的处理流程。之后我回给出源头流和目标流的详细描述，你只需要将源头流和目标流看作dict中同名的list即可。

请你使用常见python库编写代码，最终返回一个封装好的数据处理函数，格式为：

```python
def process_data(input_streams: dict[str, list]):
    # your code here
    return target_stream: dict[str, list]
```

如果你的代码中需要大语言模型LLM，你可以直接使用openai库，我们会提前配置好所需要的环境变量。

请你直接编写完整可运行的代码，我们不会 review 代码细节，只会测试代码的正确性。所有代码应符合PEP8规范。
"""

BATCH_NATIVE_PYTHON_ENGLISH_PROMPT = """
Please act as a data processing programmer and help complete the processing workflow from the source data streams to the target data streams. I will provide detailed descriptions of the source and target streams later; for now, you can treat the source and target streams as lists with the same name in a dictionary.

Please write the code using common Python libraries and return a wrapped data processing function in the following format:

```python
def process_data(input_streams: dict[str, list]):
    # your code here
    return target_stream: dict[str, list]
```

If your code requires a large language model (LLM), you can directly use the `openai` library, and we will have the necessary environment variables pre-configured. For example:

```python
import os
import openai

openai.base_url = os.environ.get("OPENAI_BASE_URL")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def process_data(input_streams: dict[str, list]):
    # your code here
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Your System Prompt"},
            {"role": "user", "content": "Your User Prompt"},
        ]
    )
    return target_stream: dict[str, list]
```

Please write fully functional code directly. We will not review the code details but will test the correctness of the code. All code should adhere to PEP8 standards.
"""

STREAM_NATIVE_PYTHON_CHINESE_PROMPT = """
请你扮演一个数据处理程序员，帮助完成从源头数据流到目标数据流的处理流程。之后我回给出源头流和目标流的详细描述，你需要使用我提供的stream接口完成任务。

我提供的stream接口包括：
chainstream.stream.get_stream_interface(`stream_id`) -> chainstream.stream.StreamInterface: 获取指定stream的接口
chainstream.stream.StreamInterface.get(timeout=`timeout`) -> StreamItem | None: 阻塞等待获取一个item，如果超时则返回None
chainstream.stream.StreamInterface.put(item: StreamItem) -> None: 向stream中写入一个item

请你使用常见python库编写代码，最终返回一个封装好的数据处理函数，格式为：

```python
def process_data(is_stop: threading.Event) -> None:
    # your code here, your code should stop and return when is_stop.is_set() is True
```

如果你需要使用LLM，你可以直接使用openai库，我们会提前配置好所需要的环境变量。例如：

```python
import os
import openai

openai.base_url = os.environ.get("OPENAI_BASE_URL")
openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Your System Prompt"},
            {"role": "user", "content": "Your User Prompt"},
        ]
    )
```

"""

STREAM_NATIVE_PYTHON_ENGLISH_PROMPT = """
Please act as a data processing programmer. Your task is to create a workflow that processes data from a source stream to a target stream. I will provide detailed descriptions of both streams later. You will need to use the provided stream interface to complete this task.

The stream interface includes:

- `chainstream.stream.get_stream_interface('stream_id') -> chainstream.stream.StreamInterface`: Retrieves the interface for a specified stream.
- `chainstream.stream.StreamInterface.get(timeout='timeout') -> StreamItem | None`: Blocks and waits for an item from the stream; returns `None` if it times out.
- `chainstream.stream.StreamInterface.put(item: StreamItem) -> None`: Writes an item to the stream.

Your goal is to write a Python function using standard libraries, which processes the data and stops when signaled. The function should have the following format:

```python
def process_data(is_stop: threading.Event) -> None:
    # Your code here. The function should stop and return when is_stop.is_set() is True.
```

If you need to use an LLM, you can use the `openai` library. The necessary environment variables will be preconfigured. For example:

```python
import os
import openai

openai.base_url = os.environ.get("OPENAI_BASE_URL")
openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Your system prompt here"},
            {"role": "user", "content": "Your user prompt here"},
        ]
    )
```

"""
