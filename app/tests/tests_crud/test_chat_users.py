import pytest

from app import models
from app.crud import ChatUser


@pytest.mark.asyncio
async def test_can_create_chat_user(db, chat, default_user):
    chat_user = await ChatUser.create(db, chat_id=chat.id, user_id=default_user.id)
    assert isinstance(chat_user, models.ChatUser)
    assert chat_user.chat_id == chat.id
    assert chat_user.user_id == default_user.id


@pytest.mark.asyncio
async def test_can_delete_chat_user(db, chat, default_user):
    chat_user = await ChatUser.create(db, chat_id=chat.id, user_id=default_user.id)
    assert isinstance(await db.get(models.ChatUser, chat_user.id), models.ChatUser)
    await ChatUser.delete(db, chat_user.id)
    assert await db.get(models.ChatUser, chat_user.id) is None
