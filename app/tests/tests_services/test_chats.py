import pytest

from app import models
from app.crud import ChatUsers, Chats
from app.services import chats
from app.utils import exceptions
from app.utils.options import GetOneOptions


@pytest.mark.asyncio
async def test_user_create_a_chat(db, default_user):
    chat = await chats.user_create_a_chat(db, user_id=default_user.id, chat_name="_test_user_create_a_chat")
    assert isinstance(chat, models.Chat)
    assert chat.name == "_test_user_create_a_chat"
    await ChatUsers.get_one(db, user_id=default_user.id, chat_id=chat.id, _options=GetOneOptions(raise_if_none=True))


@pytest.fixture(scope='function')
async def chat(db, default_user):
    yield await chats.user_create_a_chat(db, user_id=default_user.id, chat_name="_test_user_delete_a_chat")


@pytest.mark.asyncio
async def test_user_delete_a_chat(db, default_user, chat):
    await chats.user_delete_a_chat(db, user_id=default_user.id, chat_id=chat.id)
    assert not await Chats.get_many(db, id=chat.id)
    assert not await ChatUsers.get_many(db, user_id=default_user.id, chat_id=chat.id)


@pytest.mark.asyncio
async def test_failed_user_delete_a_chat_user_not_a_chat_user(db, default_user):
    chat = await Chats.create(db, "_test_failed_user_delete_a_chat_user_not_a_chat_user")
    with pytest.raises(exceptions.HTTPException) as exc:
        await chats.user_delete_a_chat(db, user_id=default_user.id, chat_id=chat.id)
    assert exc.value is exceptions.Forbidden
