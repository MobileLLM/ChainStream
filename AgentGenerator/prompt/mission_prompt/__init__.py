if __name__ == "__main__":
    from for_gpt_based_agent import GPT_BASED_MISSION_PROMPT
    from for_batch_based_agent import BATCH_BASED_PROMPT
    from for_stream_based_agent import STREAM_BASED_MISSION_PROMPT, STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM
else:
    from .for_gpt_based_agent import GPT_BASED_MISSION_PROMPT
    from .for_batch_based_agent import BATCH_BASED_PROMPT
    from .for_stream_based_agent import STREAM_BASED_MISSION_PROMPT, STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM


def get_mission_prompt(output_stream, input_stream, mission_type, framework_type="None"):

    if mission_type == "native_gpt":
        return GPT_BASED_MISSION_PROMPT.format(output_stream=output_stream, input_stream=input_stream, input_data="[input_data]")
    elif mission_type == "batch":
        return BATCH_BASED_PROMPT.format(output_stream=output_stream, input_stream=input_stream)
    elif mission_type == "stream":
        if framework_type == "chainstream":
            return STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM.format(output_stream=output_stream, input_stream=input_stream)
        else:
            return STREAM_BASED_MISSION_PROMPT.format(output_stream=output_stream, input_stream=input_stream)
    else:
        raise ValueError("Invalid mission type or framework type")

if __name__ == '__main__':
    print(get_mission_prompt("output_stream", "input_stream", "gpt"), end="\n*************\n")
    print(get_mission_prompt("output_stream", "input_stream", "batch"), end="\n*************\n")
    print(get_mission_prompt("output_stream", "input_stream", "stream", "chainstream"), end="\n*************\n")
