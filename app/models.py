from sqlalchemy import Column, Integer, Text, DateTime, String, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, index=True, unique=True)
    hashed_password = Column(String(length=255))
    created_at = Column(DateTime, index=True, server_default=func.now())
    is_active = Column(Boolean, default=True)
    email = Column(String(length=255))


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    body = Column(String(length=63), primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="refresh_tokens")
    expire_at = Column(Integer, index=True)  # Unix time
