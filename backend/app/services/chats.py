"""This module describes logic related to the chat system:
— creating a chat
— deleting a chat
— joining to a chat
— leaving a chat
— chat roles system
— etc.
This module does NOT describe such logic as sending/deleting messages or post creating.
"""

from app import models
from app.crud import ChatUsers, Chats
from app.utils import exceptions


async def user_create_a_chat(user_id: int, chat_name: str) -> models.Chat:
    chat = await Chats.create(name=chat_name)
    await ChatUsers.create(user_id=user_id, chat_id=chat.id)
    return chat


async def user_delete_a_chat(user_id: int, chat_id: int) -> None:
    chat_user = await ChatUsers.get_one(user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    await Chats.delete(chat_id=chat_user.chat_id)


async def add_user_to_chat(user_id: int, chat_id: int) -> models.ChatUser:
    chat = await Chats.get_one(id=chat_id)
    if chat is None:
        raise exceptions.InstanceNotFound
    return await ChatUsers.create(user_id=user_id, chat_id=chat_id)


async def remove_user_from_chat(user_id: int, chat_id: int) -> None:
    chat = await Chats.get_one(id=chat_id)
    if chat is None:
        raise exceptions.InstanceNotFound
    await ChatUsers.delete(user_id=user_id, chat_id=chat_id)
