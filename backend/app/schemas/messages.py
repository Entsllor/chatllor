from datetime import datetime

from app.schemas.base import BaseScheme
from app.schemas.users import UserPublic


class MessageBase(BaseScheme):
    pass


class MessageCreate(MessageBase):
    body: str


class MessageOut(MessageCreate):
    user_id: int
    id: int
    created_at: datetime


class UserMessage(MessageOut):
    user: UserPublic


class Message(MessageOut):
    pass
