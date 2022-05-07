from datetime import datetime

from app.schemas.base import BaseScheme
from .chats import ChatOut


class ChatUserBase(BaseScheme):
    pass


class ChatUserJoin(ChatUserBase):
    chat_id: int
    user_id: int


class ChatUserJoined(ChatUserJoin):
    joined_at: datetime


class ChatUserDetail(BaseScheme):
    joined_at: datetime
    chat: ChatOut
