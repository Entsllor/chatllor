import secrets
import time

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import ModelInDB


class RefreshToken(ModelInDB):
    __tablename__ = "refresh_token"
    body = Column(String(length=127), primary_key=True, default=lambda: secrets.token_urlsafe(90))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref="refresh_tokens")
    expire_at = Column(Integer, index=True)  # Unix time

    @property
    def is_active(self):
        return time.time() < self.expire_at
