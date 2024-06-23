from .openai.openai_llm_instance import OpenAITextGPT35, OpenAITextGPT4


LLM_INSTANCES_LIST = {
    "text": {
        "openai-gpt3-5": OpenAITextGPT35,
        "openai-gpt4": OpenAITextGPT4
    }
}