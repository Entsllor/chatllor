from datetime import datetime

from app.schemas.base import BaseScheme


class MessageBase(BaseScheme):
    pass


class MessageCreate(MessageBase):
    body: str


class MessageOut(MessageCreate):
    user_id: int
    id: int
    created_at: datetime


class Message(MessageOut):
    pass
