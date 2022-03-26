from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from app.core.database import Base


class ChatUser(Base):
    __tablename__ = 'chat_user'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), index=True, nullable=False)
    chat_id = Column(Integer, ForeignKey("chat.id", ondelete="CASCADE", onupdate="CASCADE"), index=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.now)
