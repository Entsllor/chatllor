from sqlalchemy import Column, Integer, func, DateTime

from app.core.database import Base


class ChatUser(Base):
    __tablename__ = 'chat_user'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    chat_id = Column(Integer, index=True)
    joined_at = Column(DateTime, server_default=func.now())
