import datetime

from pydantic import BaseModel, Field
from typing import Optional, List
import enum


class MessageData(BaseModel):
    thread_id: int
    text: str
    pictures: Optional[List[str]] = Field(None, max_length=4)


class MessageEdit(BaseModel):
    id: int
    text: Optional[str] = None
    pictures: Optional[List[str]] = Field(None, max_length=4)


class MessageResponse(MessageData):
    id: int
    user_id: int
    date: datetime.datetime
