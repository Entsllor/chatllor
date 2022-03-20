from sqlalchemy import Text, Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    body = Column(Text, default="")
    created_at = Column(DateTime, index=True, server_default=func.now())
    user = relationship("User", backref="messages")
