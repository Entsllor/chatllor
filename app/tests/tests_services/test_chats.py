import pytest

from app import models
from app.crud import ChatUsers, Chats, Users
from app.services import chats
from app.utils import exceptions
from app.utils.options import GetOneOptions


@pytest.mark.asyncio
async def test_user_create_a_chat(default_user):
    chat = await chats.user_create_a_chat(user_id=default_user.id, chat_name="_test_user_create_a_chat")
    assert isinstance(chat, models.Chat)
    assert chat.name == "_test_user_create_a_chat"
    await ChatUsers.get_one(user_id=default_user.id, chat_id=chat.id, _options=GetOneOptions(raise_if_none=True))


@pytest.mark.asyncio
async def test_user_delete_a_chat(default_user, chat_with_default_user):
    await chats.user_delete_a_chat(user_id=default_user.id, chat_id=chat_with_default_user.id)
    assert not await Chats.get_many(id=chat_with_default_user.id)
    assert not await ChatUsers.get_many(user_id=default_user.id, chat_id=chat_with_default_user.id)


@pytest.mark.asyncio
async def test_failed_user_delete_a_chat_user_not_a_chat_user(default_user):
    chat = await Chats.create("_test_failed_user_delete_a_chat_user_not_a_chat_user")
    with pytest.raises(exceptions.Forbidden):
        await chats.user_delete_a_chat(user_id=default_user.id, chat_id=chat.id)


@pytest.mark.asyncio
async def test_user_can_join_the_chat(empty_chat):
    new_user = await Users.create(username="new_user", password="pass", email="new_user@mail.com")
    await chats.add_user_to_chat(new_user.id, chat_id=empty_chat.id)
    assert (await ChatUsers.get_one(user_id=new_user.id, chat_id=empty_chat.id)).user_id == new_user.id


@pytest.mark.asyncio
async def test_user_can_left_the_chat(default_user, empty_chat):
    new_user = await Users.create(username="new_user", password="pass", email="new_user@mail.com")
    await chats.add_user_to_chat(user_id=new_user.id, chat_id=empty_chat.id)
    await chats.remove_user_from_chat(user_id=new_user.id, chat_id=empty_chat.id)
    assert not await ChatUsers.get_one(user_id=new_user.id, chat_id=empty_chat.id)
