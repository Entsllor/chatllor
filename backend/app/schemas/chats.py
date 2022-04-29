from app.schemas.base import BaseScheme


class ChatBase(BaseScheme):
    pass


class ChatCreate(ChatBase):
    name: str


class ChatOut(ChatCreate):
    id: int
