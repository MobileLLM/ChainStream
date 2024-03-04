from typing import Optional, List, Dict,cast
from pydantic import Field,BaseModel
from .message import Message
from .utils import get_login_event

LLM_MAX_TOKENS = {
    "DEFAULT": 8192,
    ## OpenAI models: https://platform.openai.com/docs/models/overview
    # gpt-4
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4-0613": 8192,
    "gpt-4-32k-0613": 32768,
    "gpt-4-0314": 8192,  # legacy
    "gpt-4-32k-0314": 32768,  # legacy
    # gpt-3.5
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo": 4096,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-0613": 4096,  # legacy
    "gpt-3.5-turbo-16k-0613": 16385,  # legacy
    "gpt-3.5-turbo-0301": 4096,  # legacy
}
# The amount of tokens b
class LLMConfig:
    def __init__(
        self,
        model: Optional[str] = "gpt-4",
        model_endpoint_type: Optional[str] = "openai",
        model_endpoint: Optional[str] = "https://api.openai.com/v1",
        model_wrapper: Optional[str] = None,
        context_window: Optional[int] = None,
    ):
        self.model = model
        self.model_endpoint_type = model_endpoint_type
        self.model_endpoint = model_endpoint
        self.model_wrapper = model_wrapper
        self.context_window = context_window

        if context_window is None:
            self.context_window = LLM_MAX_TOKENS[self.model] if self.model in LLM_MAX_TOKENS else LLM_MAX_TOKENS["DEFAULT"]
        else:
            self.context_window = context_window
class Preset(BaseModel):
    name: str = Field(..., description="The name of the preset.")
    description: Optional[str] = Field(None, description="The description of the preset.")
    system: str = Field(..., description="The system prompt of the preset.")
    functions_schema: List[Dict] = Field(..., description="The functions schema of the preset.")

def initialize_message_sequence(
    model: str,
    system: str,
):
    first_user_message = get_login_event()  # event letting MemGPT know the user just logged in

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": first_user_message},
    ]

    return messages

class Agent(object):
    def __init__(self, preset: Optional[Preset] = None,llm_config:Optional[LLMConfig]=None):
        self.model=llm_config.model
        self.system = preset.system
        self.function=preset.functions_schema
        #self.functions_python = {k: v["python_function"] for k, v in
                                 #link_functions(function_schemas=self.functions).items()}

        self._messages: List[Message] = []

        init_messages = initialize_message_sequence(
            self.model,
            self.system,
        )
        init_messages_objs = []
        for msg in init_messages:
            init_messages_objs.append(
                Message.dict_to_message(
                    model=self.model,
                    openai_message_dict=msg))
        assert all([isinstance(msg, Message) for msg in init_messages_objs]), (init_messages_objs, init_messages)

        self._append_to_messages(added_messages=[cast(Message, msg) for msg in init_messages_objs if msg is not None])
        self.messages_total = 0
        self.messages_total = (len(self._messages) - 1)


