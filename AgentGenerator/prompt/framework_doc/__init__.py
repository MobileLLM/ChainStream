if __name__ == '__main__':
    from chainstream_doc import chainstream_english_doc
    from native_python_doc import BATCH_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    from langchain_doc import BATCH_LANGCHAIN_ENGLISH_PROMPT, STREAM_LANGCHAIN_ENGLISH_PROMPT
    from native_gpt_doc import NATIVE_GPT_PROMPT
else:
    from .chainstream_doc import chainstream_english_doc
    from .native_python_doc import BATCH_NATIVE_PYTHON_ENGLISH_PROMPT, STREAM_NATIVE_PYTHON_ENGLISH_PROMPT
    from .langchain_doc import BATCH_LANGCHAIN_ENGLISH_PROMPT, STREAM_LANGCHAIN_ENGLISH_PROMPT
    from .native_gpt_doc import NATIVE_GPT_PROMPT


def get_framework_doc(framework, example_num=None):
    if framework == "chainstream":
        if example_num is not None and example_num != 0:
            raise ValueError("Example number not supported for chainstream")
        return chainstream_english_doc
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
    print(get_framework_doc("native_python"), end="\n*************\n")
    print(get_framework_doc("native_gpt"), end="\n*************\n")
    print(get_framework_doc("langchain"), end="\n*************\n")
    print(get_framework_doc("chainstream"), end="\n*************\n")
