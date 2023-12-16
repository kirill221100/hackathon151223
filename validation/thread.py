import datetime
from validation.message import MessageResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import enum


class ThreadData(BaseModel):
    title: str
    text: str
    pictures: Optional[List[str]] = Field(None, max_length=4)


class ThreadDataEdit(ThreadData):
    id: int
    title: Optional[str] = None
    text: Optional[str] = None


class ThreadResponse(ThreadData):
    id: int
    user_id: int
    date: datetime.datetime


class ThreadResponseWithMessages(ThreadResponse):
    messages: List[MessageResponse]