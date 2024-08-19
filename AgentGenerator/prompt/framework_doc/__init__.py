from .chainstream_doc import chainstream_english_doc
from .native_python_doc import NATIVE_PYTHON_CHAINSTREAM_ENGLISH_PROMPT
from .langchain_doc import LANGCHAIN_CHAINSTREAM_ENGLISH_PROMPT
from .native_gpt_doc import NATIVE_GPT_PROMPT


def get_framework_doc(framework, example_num=None):
    if framework == "chainstream":
        if example_num is not None:
            raise ValueError("Example number not supported for chainstream")
        return chainstream_english_doc
    elif framework == "native_python":
        return NATIVE_PYTHON_CHAINSTREAM_ENGLISH_PROMPT
    elif framework == "langchain":
        return LANGCHAIN_CHAINSTREAM_ENGLISH_PROMPT
    elif framework == "native_gpt":
        return NATIVE_GPT_PROMPT
    else:
        raise ValueError(f"Framework {framework} not supported")
