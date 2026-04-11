if __name__ == "__main__":
    from for_gpt_based_agent import GPT_BASED_MISSION_PROMPT
    from for_batch_based_agent import BATCH_BASED_PROMPT
    from for_stream_based_agent import STREAM_BASED_MISSION_PROMPT, STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM
    from for_chat_based_agent import CHAT_BASED_MISSION_PROMPT_FOR_CHAINSTREAM
else:
    from .for_gpt_based_agent import GPT_BASED_MISSION_PROMPT
    from .for_batch_based_agent import BATCH_BASED_PROMPT
    from .for_stream_based_agent import STREAM_BASED_MISSION_PROMPT, STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM
    from .for_chat_based_agent import CHAT_BASED_MISSION_PROMPT_FOR_CHAINSTREAM


def get_mission_prompt(output_stream, input_stream, mission_type, framework_type="None", chat_message=None):
    if mission_type == "native_gpt":
        return GPT_BASED_MISSION_PROMPT.format(output_stream=output_stream, input_stream=input_stream, input_data="[input_data]")
    elif mission_type == "batch":
        return BATCH_BASED_PROMPT.format(output_stream=output_stream, input_stream=input_stream)
    elif mission_type == "stream":
        if framework_type == "chainstream":
            return STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM.format(output_stream=output_stream, input_stream=input_stream)
        else:
            return STREAM_BASED_MISSION_PROMPT.format(output_stream=output_stream, input_stream=input_stream)
    elif mission_type == "chat":
        # Chat mode for interactive agent development
        if chat_message is None:
            raise ValueError("chat_message is required for chat mission type")
        if not isinstance(chat_message, dict):
            raise ValueError("chat_message must be a dict with keys: 'history', 'code', 'message'")
        
        history = chat_message.get('history', '')
        code = chat_message.get('code', '')
        message = chat_message.get('message', '')
        
        # Format chat context
        chat_context = ""
        if history:
            chat_context += f"**Conversation History:**\n{history}\n\n"
        if code:
            chat_context += f"**Current Code:**\n```\n{code}\n```\n"
        
        if framework_type == "chainstream":
            return CHAT_BASED_MISSION_PROMPT_FOR_CHAINSTREAM.format(
                output_stream=output_stream, 
                input_stream=input_stream,
                chat_context=chat_context,
                user_message=message
            )
        else:
            raise ValueError("Chat mode currently only supports chainstream framework")
    else:
        raise ValueError("Invalid mission type or framework type")

if __name__ == '__main__':
    print(get_mission_prompt("output_stream", "input_stream", "gpt"), end="\n*************\n")
    print(get_mission_prompt("output_stream", "input_stream", "batch"), end="\n*************\n")
    print(get_mission_prompt("output_stream", "input_stream", "stream", "chainstream"), end="\n*************\n")
