from sqlalchemy import Column, Integer, String

from app.core.database import Base
from app.models.base import ModelInDB


class Chat(ModelInDB):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
