import pytest

from app import models
from app.crud import Messages
from app.utils.options import GetManyOptions


@pytest.mark.asyncio
async def test_create_message(default_user):
    message = await Messages.create(user_id=default_user.id, chat_id=None, body="__test_create_message")
    assert isinstance(message, models.Message)


@pytest.mark.asyncio
async def test_get_all_messages(default_user):
    msg_1 = await Messages.create(user_id=default_user.id, chat_id=None, body="__test_create_message_1")
    msg_2 = await Messages.create(user_id=default_user.id, chat_id=None, body="__test_create_message_2")
    msg_3 = await Messages.create(user_id=default_user.id, chat_id=None, body="__test_create_message_3")
    messages = await Messages.get_all(options=GetManyOptions(ordering_fields=["-body"]))
    assert messages == [msg_3, msg_2, msg_1]
    messages = await Messages.get_all(options=GetManyOptions(ordering_fields=["created_at"]))
    assert messages == [msg_1, msg_2, msg_3]
    messages = await Messages.get_all(options=GetManyOptions(ordering_fields=["-created_at"]))
    assert messages == [msg_3, msg_2, msg_1]
