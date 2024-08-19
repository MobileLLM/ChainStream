GPT_BASED_MISSION_PROMPT = """
Please take on the role of a data processor and help me derive the desired output data from a batch of input data. These input data come from a streaming framework, and I've already converted all the stream data into a JSON list. Please return the data in the same JSON format.

Each input stream and output stream has a unified format, as follows:

```json
[{{
    "stream_id": "xxx",
    "description": "xxx",
    "fields": {{
        "AAA": "xxx xxx, string",
        "BBB": "xxx xxx, int"
    }}
}}]
```

The data includes the stream's ID (`stream_id`), the stream's description (`description`), and the stream's field descriptions (`fields`). You need to understand the task based on the output stream's description and ultimately return the output stream's content.

Now, your task is to return the output stream:
```json
{output_stream}
```

You can choose from the following input streams:
```json
{input_stream}
```

The input data is as follows:
```json
{input_data}
```

Please process the input data and directly return the output stream data in JSON format.

Output Data:
"""



