from pydantic import BaseModel


class MessageBase(BaseModel):
    class Config:
        orm_mode = True


class MessageCreate(MessageBase):
    body: str


class MessageOut(MessageCreate):
    user_id: int
    id: int


class Message(MessageOut):
    pass
