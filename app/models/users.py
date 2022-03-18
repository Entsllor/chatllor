from sqlalchemy import Column, Integer, Text, String, DateTime, func, Boolean

from app.core.database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, index=True, unique=True)
    hashed_password = Column(String(length=255))
    created_at = Column(DateTime, index=True, server_default=func.now())
    is_active = Column(Boolean, default=True)
    email = Column(String(length=255))