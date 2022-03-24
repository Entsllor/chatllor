from datetime import datetime

from pydantic import BaseModel


class ChatUserBase(BaseModel):
    class Config:
        orm_mode = True


class ChatUserJoin(ChatUserBase):
    chat_id: int
    user_id: int


class ChatUserJoined(ChatUserJoin):
    joined_at: datetime
