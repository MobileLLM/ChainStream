from .openai.openai_llm_text_instance import OpenAITextGPT35, OpenAITextGPT4
from chainstream.llm import API_LLM_TYPE


LLM_INSTANCES_LIST = {
    'TI': {
        OpenAITextGPT35.model_name: OpenAITextGPT35,
        OpenAITextGPT4.model_name: OpenAITextGPT4
    }
}