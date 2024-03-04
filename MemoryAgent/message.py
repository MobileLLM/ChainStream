from typing import Optional,Dict,List

class ToolCall(object):
    def __init__(
        self,
        id: str,
        # NOTE: called ToolCall.type in official OpenAI schema
        tool_call_type: str,  # only 'function' is supported
        # function: { 'name': ..., 'arguments': ...}
        function: Dict[str, str],
    ):
        self.id = id
        self.tool_call_type = tool_call_type
        self.function = function

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.tool_call_type,
            "function": self.function,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.tool_call_type,
            "function": self.function,
        }
class Message(object):
    def __init__(
        self,
        role: str,
        text: str,
        model: Optional[str] = None,  # model used to make function call
        tool_calls: Optional[List[ToolCall]] = None,  # list of tool calls requested
        tool_call_id: Optional[str] = None,
        ):
        self.text = text
        self.model = model
        assert role in ["system", "assistant", "user", "tool"]
        self.role = role

        # if role == "assistant", this MAY be specified
        # if role != "assistant", this must be null
        assert tool_calls is None or isinstance(tool_calls, list)
        self.tool_calls = tool_calls

        if role == "tool":
            assert tool_call_id is not None
        else:
            assert tool_call_id is None
        self.tool_call_id = tool_call_id

    @staticmethod
    def dict_to_message(
            openai_message_dict: dict,
            model: Optional[str] = None,  # model used to make function call
    ):
        assert "role" in openai_message_dict, openai_message_dict
        assert "content" in openai_message_dict, openai_message_dict
        if openai_message_dict["role"] == "function":
            assert "tool_call_id" in openai_message_dict, openai_message_dict

            return Message(
                model=model,
                # standard fields expected in an OpenAI ChatCompletion message object
                role="tool",  # NOTE
                text=openai_message_dict["content"],
                tool_calls=openai_message_dict["tool_calls"] if "tool_calls" in openai_message_dict else None,
                tool_call_id=openai_message_dict["tool_call_id"] if "tool_call_id" in openai_message_dict else None,
            )

        elif "function_call" in openai_message_dict and openai_message_dict["function_call"] is not None:
            assert openai_message_dict["role"] == "assistant", openai_message_dict
            assert "tool_call_id" in openai_message_dict, openai_message_dict

            tool_calls = [
                ToolCall(
                    id=openai_message_dict["tool_call_id"],  # NOTE: unconventional source, not to spec
                    tool_call_type="function",
                    function={
                        "name": openai_message_dict["function_call"]["name"],
                        "arguments": openai_message_dict["function_call"]["arguments"],
                    },
                )
            ]

            return Message(
                model=model,
                # standard fields expected in an OpenAI ChatCompletion message object
                role=openai_message_dict["role"],
                text=openai_message_dict["content"],
                tool_calls=tool_calls,
                tool_call_id=None,  # NOTE: None, since this field is only non-null for role=='tool'
            )

    def to_openai_dict(self):
        if self.role == "system":
            assert all([v is not None for v in [self.role]]), vars(self)
            openai_message = {
                "content": self.text,
                "role": self.role,
            }
        elif self.role == "user":
            assert all([v is not None for v in [self.text, self.role]]), vars(self)
            openai_message = {
                "content": self.text,
                "role": self.role,
            }
        elif self.role == "assistant":
            assert self.tool_calls is not None or self.text is not None
            openai_message = {
                "content": self.text,
                "role": self.role,
            }
            if self.tool_calls is not None:
                openai_message["tool_calls"] = [tool_call.to_dict() for tool_call in self.tool_calls]

        elif self.role == "tool":
            assert all([v is not None for v in [self.role, self.tool_call_id]]), vars(self)
            openai_message = {
                "content": self.text,
                "role": self.role,
                "tool_call_id": self.tool_call_id,
            }