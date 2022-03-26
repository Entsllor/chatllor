from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
