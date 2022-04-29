from datetime import datetime

from app.schemas.base import BaseScheme


class ChatUserBase(BaseScheme):
    pass


class ChatUserJoin(ChatUserBase):
    chat_id: int
    user_id: int


class ChatUserJoined(ChatUserJoin):
    joined_at: datetime
