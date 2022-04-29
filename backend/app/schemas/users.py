from datetime import datetime

from app.schemas.base import BaseScheme


class UserBase(BaseScheme):
    username: str


class UserCreate(UserBase):
    password: str
    email: str


class UserPublic(UserBase):
    """Public user data"""
    id: int
    created_at: datetime


class UserPrivate(UserPublic):
    """Private user data (other users shouldn't see this)"""
    email: str


class User(UserPrivate):
    """Secret user data (even the user should not know it)"""
    hashed_password: str
    is_active: bool = True
