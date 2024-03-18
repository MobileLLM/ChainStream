from typing import List, Tuple, Optional, cast, Union,Dict
from pydantic import Field,BaseModel
from message import Message
import response
from utils import get_login_event,verify_first_message_correctness,openai_chat_completions_request,package_function_response

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
        open_ai_key:Optional[str]=None
    ):
        self.model = model
        self.model_endpoint_type = model_endpoint_type
        self.model_endpoint = model_endpoint
        self.model_wrapper = model_wrapper
        self.context_window = context_window
        self.open_ai_key=open_ai_key

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
        self.config=llm_config
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
        self.messages_total = 0
        self._append_to_messages(added_messages=[cast(Message, msg) for msg in init_messages_objs if msg is not None])

        self.messages_total_init=self.messages_total = (len(self._messages) - 1)

        print(f"Agent initialized, self.messages_total={self.messages_total}")

    def _append_to_messages(self, added_messages: List[Message]):

        assert all([isinstance(msg, Message) for msg in added_messages])
        new_messages = self._messages + added_messages  # append
        self._messages = new_messages
        self.messages_total += len(added_messages)
    def _get_openai_reply(
        self,
        message_sequence: List[dict],
        function_call: str = "auto",
        first_message: bool = False,  # hint
    ):
        """Get response from LLM API"""
        try:
            if self.config.open_ai_key is None:
                raise ValueError(f"OpenAI key is missing from config file")
            data = dict(
                model=self.model,
                messages=message_sequence,
                tools=[{"type": "function", "function": f} for f in self.function] if self.function else None,
                tool_choice=function_call,
            )
            response= openai_chat_completions_request(
                url=self.config.model_endpoint,
                api_key=self.config.openai_key,
                data=data,
                )
            # special case for 'length'
            if response.choices[0].finish_reason == "length":
                raise Exception("Finish reason was length (maximum context length)")

            # catches for soft errors
            if response.choices[0].finish_reason not in ["stop", "function_call", "tool_calls"]:
                raise Exception(f"API call finish with bad finish reason: {response}")

            # unpack with response.choices[0].message.content
            return response
        except Exception as e:
            raise e

    def _handle_ai_response(
            self, response_message: response.Message, override_tool_call_id: bool = True
    ) -> Tuple[List[Message], bool, bool]:
        messages = []
        if response_message.function_call or (
            response_message.tool_calls is not None and len(response_message.tool_calls) > 0):
            if response_message.function_call:
                raise DeprecationWarning(response_message)
            if response_message.tool_calls is not None and len(response_message.tool_calls) > 1:
                print(f">1 tool call not supported, using index=0 only\n{response_message.tool_calls}")
                response_message.tool_calls = [response_message.tool_calls[0]]
            assert response_message.tool_calls is not None and len(response_message.tool_calls) > 0

            tool_call_id = response_message.tool_calls[0].id
            assert tool_call_id is not None

            messages.append(
                Message.dict_to_message(
                    model=self.model,
                    openai_message_dict=response_message.model_dump(),
                )
            )
            function_call = (
                response_message.function_call if response_message.function_call is not None else
                response_message.tool_calls[0].function
            )
            function_name=function_call.name
            print(f"Function call message: {messages[-1]}")
            function_response_string=input("函数回复：")
            function_response = package_function_response(True, function_response_string)
            messages.append(
                Message.dict_to_message(
                    model=self.model,
                    openai_message_dict={
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                        "tool_call_id": tool_call_id,
                    },
                )
            )
        else :
            messages.append(
                Message.dict_to_message(
                    model=self.model,
                    openai_message_dict=response_message.model_dump(),
                )
            )
        return messages

    def step(self,
             user_message:Union[Message,str],
             first_message:bool=False,
             first_message_retry_limit: int=5) -> Tuple[List[dict], bool, bool, bool]:

        try:
            # add user message
            if user_message is not None:
                if isinstance(user_message,Message):
                    user_message_text=user_message.text
                elif isinstance(user_message,str):
                    user_message_text=user_message
                else:
                    raise ValueError(f"Bad type for user_message: {type(user_message)}")
                packed_user_message = {"role": "user", "content": user_message_text}

                packed_user_message_obj = Message.dict_to_message(
                                                        model=self.model,
                                                        openai_message_dict=packed_user_message,
                                                        )
                input_message_sequence = self.messages + [packed_user_message]

            else:
                input_message_sequence = self.messages
                packed_user_message = None
            if len(input_message_sequence) > 1 and input_message_sequence[-1]["role"] != "user":
                print(
                    f"You are attempting to run ChatCompletion without user as the last message in the queue")

            # send the conversation and available functions to GPT
            if first_message or self.messages_total == self.messages_total_init:
                print(f"This is the first message. Running extra verifier on AI response.")
                counter = 0
                while True:
                    response = self._get_ai_reply(
                        message_sequence=input_message_sequence,
                        first_message=True,  # passed through to the prompt formatter
                    )
                    if verify_first_message_correctness(response):
                        break
                    counter += 1
                    if counter > first_message_retry_limit:
                        raise Exception(f"Hit first message retry limit ({first_message_retry_limit})")
            else:
                response = self._get_ai_reply(
                    message_sequence=input_message_sequence,
                )

            #check if LLM wanted to call a function
            response_message = response.choices[0].message
            response_message.copy()

            all_response_message=self._handle_ai_response(response_message)

            #extend the message history

            if user_message is not None:
                if isinstance(user_message, Message):
                    all_new_messages = [user_message] + all_response_message
                else:
                    all_new_messages = [
                                        Message.dict_to_message(
                                            model=self.model,
                                            openai_message_dict=packed_user_message,
                                        )
                                       ] + all_response_message
            else:
                all_new_messages = all_response_message
            self._append_to_messages(all_new_messages)


        except Exception as e:
            print(f"step() failed\nuser_message = {user_message}\nerror = {e}")











