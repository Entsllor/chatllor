import pytest

from app import models
from app.crud import Chats


@pytest.mark.asyncio
async def test_chat_can_be_created(db):
    chat = await Chats.create(name="test_chat_can_be_created")
    assert isinstance(chat, models.Chat)
    assert chat.name == "test_chat_can_be_created"


@pytest.mark.asyncio
async def test_chat_can_be_deleted(db, empty_chat):
    assert isinstance(await db.get(models.Chat, empty_chat.id), models.Chat)
    await Chats.delete(empty_chat.id)
    assert await db.get(models.Chat, empty_chat.id) is None
