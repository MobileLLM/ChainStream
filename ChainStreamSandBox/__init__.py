from ChainStreamSandBox.sandbox.chainstream_sandbox import ChainStreamSandBox
from ChainStreamSandBox.sandbox.batch_langchain_sandbox import LangChainBatchSandbox
from ChainStreamSandBox.sandbox.batch_native_python_sandbox import NativePythonBatchSandbox
from ChainStreamSandBox.sandbox import get_sandbox_class


# def get_sandbox_class(sandbox_type):
#     if sandbox_type == "chainstream":
#         return ChainStreamSandBox
#     elif sandbox_type == "langchain":
#         return LangChainBatchSandbox
#     elif sandbox_type == "native_python":
#         return NativePythonBatchSandbox
#     else:
#         raise ValueError("Invalid sandbox type")
