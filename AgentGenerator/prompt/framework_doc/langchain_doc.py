
BATCH_LANGCHAIN_CHINESE_PROMPT = """
请你扮演一个数据处理程序员，帮助完成从源头数据流到目标数据流的处理流程。之后我回给出源头流和目标流的详细描述，你只需要将源头流和目标流看作dict中同名的list即可。

请你使用LangChain框架和常见Python库编写代码，最终返回一个封装好的数据处理函数，格式为：

```python
def process_data(input_streams: dict[str, list]):
    # your code here
    return target_stream: dict[str, list]
```

如果你的代码中需要大语言模型LLM，你可以直接使用openai库或者LangChain API，我们会提前配置好所需要的环境变量。

请你直接编写完整可运行的代码，我们不会 review 代码细节，只会测试代码的正确性。所有代码应符合PEP8规范。
"""

BATCH_LANGCHAIN_ENGLISH_PROMPT = """
Please act as a data processing programmer and help complete the processing workflow from the source data streams to the target data streams. I will provide detailed descriptions of the source and target streams later; for now, you can treat the source and target streams as lists with the same name in a dictionary.

Please write the code using the LangChain framework and common Python libraries, and return a wrapped data processing function in the following format:

```python
def process_data(input_streams: dict[str, list]):
    # your code here
    return target_stream: dict[str, list]
```

If your code requires a large language model (LLM), you can directly use the `openai` library or the LangChain API, and we will have the necessary environment variables pre-configured. For example:

```python
import os
from langchain.llms import OpenAI

openai_base_url = os.environ.get('OPENAI_BASE_URL')
openai_api_key = os.environ.get("OPENAI_API_KEY")

def process_data(input_streams: dict[str, list]):
    # your code here
    llm = OpenAI(base_url=openai_base_url, api_key=openai_api_key, model_name="gpt-4")
    response = llm("your prompt")
    return target_stream: dict[str, list]
```

Please write fully functional code directly. We will not review the code details but will test the correctness of the code. All code should adhere to PEP8 standards.
"""

STREAM_LANGCHAIN_ENGLISH_PROMPT = """"""
