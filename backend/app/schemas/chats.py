from pydantic import BaseModel


class ChatBase(BaseModel):
    class Config:
        orm_mode = True


class ChatCreate(ChatBase):
    name: str


class ChatOut(ChatCreate):
    id: int
