from datetime import datetime

from sqlalchemy import Text, Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import ModelInDB


class Message(ModelInDB):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    chat_id = Column(Integer, ForeignKey('chat.id', ondelete="CASCADE"))
    body = Column(Text, default="")
    created_at = Column(DateTime, index=True, default=datetime.now)
    user = relationship("User", backref="messages")
