from pydantic import BaseModel, Field, ValidationError, Extra
from typing import List, Dict, Optional


class StreamDescription(BaseModel):
    stream_id: str = Field(..., description="The stream ID")
    description: str = Field(..., description="Description of the stream")
    fields: Dict[str, str] = Field(..., description="Fields of the stream")

    class Config:
        extra = Extra.forbid  # Forbid any extra fields not defined in the model


class StreamListDescription(BaseModel):
    streams: List[StreamDescription] = Field(..., description="A list of stream descriptions")

    class Config:
        extra = Extra.forbid  # Forbid any extra fields not defined in the model


class TaskDescription(BaseModel):
    input_description: StreamListDescription = Field(..., description="Description of the input streams")
    output_description: StreamListDescription = Field(..., description="Description of the output streams")


if __name__ == '__main__':

    # 示例数据
    data = {

        "output_description": [
            {
                "stream_id": "summary_by_sender",
                "description": "A list of email summaries for each email sender, excluding ads",
                "fields": {
                    "sender": "name xxx, string",
                    "summary": "sum xxx, string",
                    "extra_field": "user specified field, string"
                }
            }
        ]
    }

    # 验证和实例化
    try:
        task_description = TaskDescription(**data)
        print(task_description.json(indent=2))
    except ValidationError as e:
        print(e)
