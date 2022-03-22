"""This module describes logic related to the chat system:
— creating a chat
— deleting a chat
— joining to a chat
— leaving a chat
— chat roles system
— etc.
This module does NOT describe such logic as sending/deleting messages or post creating.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import ChatUsers, Chats
from app.utils import exceptions


async def user_create_a_chat(db: AsyncSession, user_id: int, chat_name: str) -> models.Chat:
    chat = await Chats.create(db, name=chat_name)
    await ChatUsers.create(db, user_id=user_id, chat_id=chat.id)
    return chat


async def user_delete_a_chat(db: AsyncSession, user_id: int, chat_id: int) -> None:
    chat_user = await ChatUsers.get_one(db, user_id=user_id, chat_id=chat_id)
    if chat_user:
        await Chats.delete(db, chat_id=chat_user.chat_id)
        await ChatUsers.delete(db, chat_id=chat_user.chat_id)
    else:
        raise exceptions.Forbidden


async def add_user_to_chat(db: AsyncSession, user_id: int, chat_id: int) -> None:
    await ChatUsers.create(db, user_id=user_id, chat_id=chat_id)


async def remove_user_from_chat(db: AsyncSession, user_id: int, chat_id: int) -> None:
    await ChatUsers.delete(db, user_id=user_id, chat_id=chat_id)
