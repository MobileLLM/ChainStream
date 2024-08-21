from .chainstream_sandbox import ChainStreamSandBox
from .batch_native_python_sandbox import NativePythonSandbox
from .batch_langchain_sandbox import LangChainSandbox


def get_sandbox_class(sandbox_type):
    if sandbox_type == "chainstream":
        return ChainStreamSandBox
    elif sandbox_type == "native_python":
        return NativePythonSandbox
    elif sandbox_type == "langchain":
        return LangChainSandbox
    else:
        raise ValueError("Invalid sandbox type")
