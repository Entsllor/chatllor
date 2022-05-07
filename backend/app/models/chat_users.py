from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import ModelInDB


class ChatUser(ModelInDB):
    __tablename__ = 'chat_user'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), index=True, nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.id", ondelete="CASCADE", onupdate="CASCADE"), index=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.now)

    chat = relationship("Chat", backref='chat_users', lazy=False)
    user = relationship("User", backref='chats_user', lazy=False)
