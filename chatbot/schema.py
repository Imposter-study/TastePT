from ninja import Schema
from pydantic import BaseModel
from datetime import datetime


class UserSchema(Schema):
    id: int
    nickname: str

class ChatRoomSchema(Schema):
    id: int = None
    name: str
    created_by: UserSchema= None


class MessageSchema(BaseModel):
    id: int
    room_id: int
    user: str
    content: str
    timestamp: datetime


class ChatbotRequestSchema(Schema):
    question: str


class ChatbotResponseSchema(Schema):
    answer: str


class ErrorSchema(Schema):
    detail: str
