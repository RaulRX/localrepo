from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from .Status import Status

class Message_response(BaseModel):
    chain: str = Field(..., serialization_alias="content", description="Message content")
    updated_date: datetime = Field(..., serialization_alias="updatedDate", description="Date of last change")
    user: str = Field(..., description = "Name of user")
    user_id: str = Field(..., serialization_alias = "userId", description = "User identification")

    @field_serializer("updated_date")
    def datetime_to_str(self, date: datetime) -> str:
        return date.isoformat()

class Message_list_response(BaseModel):
    message_list: list[Message_response] = Field(..., serialization_alias="messages", description = "List of messages")