from .chainstream_sandbox import ChainStreamSandBox
from .batch_native_python_sandbox import NativePythonBatchSandbox
from .batch_langchain_sandbox import LangChainBatchSandbox
from .stream_interface_sandbox import StreamInterfaceSandBox

from typing_extensions import Literal


SandboxType = Literal["chainstream", "native_python_batch", "langchain_batch", "stream_interface"]


def get_sandbox_class(sandbox_type: SandboxType):
    if sandbox_type == "chainstream":
        return ChainStreamSandBox
    elif sandbox_type == "native_python_batch":
        return NativePythonBatchSandbox
    elif sandbox_type == "langchain_batch":
        return LangChainBatchSandbox
    elif sandbox_type == "stream_interface":
        return StreamInterfaceSandBox
    else:
        raise ValueError("Invalid sandbox type")
