STREAM_BASED_MISSION_PROMPT = """
Your mission is to programme an agent with chainstream framework to get the following output streams: 
{output_stream_description}
There are multiple input streams available. The agent should select some of them:
{input_stream_description}
"""

STREAM_BASED_MISSION_PROMPT_FOR_CHAINSTREAM = STREAM_BASED_MISSION_PROMPT + """\n
All the input streams and output streams listed above are already defined in the chainstream framework, you can directly use them through `chainstream.stream.get_stream(agent, stream_id)`. Besides, you can also define your own stream if needed by using the `chainstream.stream.create_stream(agent, stream_id)` API. Note that you don't need to create the output stream list beforehand.
"""
