if __name__ == '__main__':
    from chainstream_doc import chainstream_english_doc, english_examples
    from native_python_doc import BATCH_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    from langchain_doc import BATCH_LANGCHAIN_ENGLISH_PROMPT, STREAM_LANGCHAIN_ENGLISH_PROMPT
    from native_gpt_doc import NATIVE_GPT_PROMPT
else:
    from .chainstream_doc import chainstream_english_doc, english_examples
    from .native_python_doc import BATCH_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    from .langchain_doc import BATCH_LANGCHAIN_ENGLISH_PROMPT, STREAM_LANGCHAIN_ENGLISH_PROMPT
    from .native_gpt_doc import NATIVE_GPT_PROMPT

import random


def get_framework_doc(framework, example_num=None):
    if framework == "chainstream":
        prompt = chainstream_english_doc
        if example_num is not None and example_num != 0:
            if example_num > len(english_examples) or example_num > 1:
                raise ValueError(f"Example number {example_num} is not valid for chainstream")
            else:
                # tmp_example = random.sample(english_examples, example_num)
                # prompt += f"Here's some example of how to use chainstream to solve the problem:\n"
                # for i in range(len(tmp_example)):
                #     prompt += f"Example {i}: {tmp_example[i]}\n"
                prompt += f"{english_examples[0]}"
        return prompt
    elif framework == "batch_native_python":
        return BATCH_NATIVE_PYTHON_ENGLISH_PROMPT
    elif framework == "batch_langchain":
        return BATCH_LANGCHAIN_ENGLISH_PROMPT
    elif framework == "stream_native_python":
        return STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    elif framework == "stream_langchain":
        return STREAM_LANGCHAIN_ENGLISH_PROMPT
    elif framework == "native_gpt":
        return NATIVE_GPT_PROMPT
    else:
        raise ValueError(f"Framework {framework} not supported")


if __name__ == '__main__':
    print(get_framework_doc("chainstream", 0))
    print(get_framework_doc("chainstream", 1))
    print(get_framework_doc("chainstream", 2))
    print(get_framework_doc("chainstream", 3))
