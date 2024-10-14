from AgentGenerator.prompt.framework_doc.chainstream_doc import chainstream_english_doc
from AgentGenerator.prompt.framework_doc.native_python_doc import BATCH_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_EXAMPLE
from AgentGenerator.prompt.framework_doc.langchain_doc import BATCH_LANGCHAIN_ENGLISH_PROMPT, STREAM_LANGCHAIN_ENGLISH_PROMPT, STREAM_NATIVE_LANGCHAIN_EXAMPLE
from AgentGenerator.prompt.framework_doc.native_gpt_doc import NATIVE_GPT_PROMPT
from AgentGenerator.prompt.agent_example_selector import AgentExampleSelector

# FIXME: This is a temporary solution to import the task instances from ChainStreamSandBox
from ChainStreamSandBox.tasks.tmp_task_instances import get_all_task_instances


def get_framework_doc(framework, example_num=None, task_now=None, example_select_policy='random'):
    if example_select_policy not in ['random', 'llm']:
        raise ValueError('example_select_policy must be random or llm')
    if framework == "chainstream":
        prompt = chainstream_english_doc
        if example_num is not None and example_num != 0:
            if task_now is None:
                raise ValueError("Task name must be provided for example generation")
            # selector = AgentExampleSelector(get_all_task_instances(), task_now)
            selector = AgentExampleSelector(task_now)
            prompt += f"\nHere's {example_num} example of how to use chainstream to solve the problem:\n"
            for i in range(example_num):
                if example_select_policy == 'random':
                    prompt += f"Example {i}:\n```python\n{selector.get_random_agent_example()}\n```\n"
                elif example_select_policy == 'llm':
                    prompt += f"Example {i}:\n```python\n{selector.get_llm_agent_example()}\n```\n"
        return prompt
    elif framework == "batch_native_python":
        return BATCH_NATIVE_PYTHON_ENGLISH_PROMPT
    elif framework == "batch_langchain":
        return BATCH_LANGCHAIN_ENGLISH_PROMPT
    elif framework == "stream_native_python":
        if example_num is not None and example_num != 0:
            if example_num > 1:
                raise ValueError("stream native python must be greater than 1")
            prompt = STREAM_NATIVE_PYTHON_ENGLISH_PROMPT + f"\nHere's an example of how to use native python to solve the problem:\n{STREAM_NATIVE_PYTHON_EXAMPLE}\n"
            return prompt
        return STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    elif framework == "stream_langchain":
        if example_num is not None and example_num != 0:
            if example_num > 1:
                raise ValueError("stream langchain must be greater than 1")
            prompt = STREAM_LANGCHAIN_ENGLISH_PROMPT + f"\nHere's an example of how to use langchain to solve the problem:\n{STREAM_NATIVE_LANGCHAIN_EXAMPLE}\n"
            return prompt
        return STREAM_LANGCHAIN_ENGLISH_PROMPT
    elif framework == "native_gpt":
        return NATIVE_GPT_PROMPT
    else:
        raise ValueError(f"Framework {framework} not supported")


if __name__ == '__main__':
    print(get_framework_doc("stream_langchain", 1, task_now="StockTask2"))
