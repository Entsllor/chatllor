import pytest

from app import models
from app.services import messages, chats


@pytest.mark.asyncio
async def test_user_send_message_to_chat(chat_with_default_user, default_user):
    message = await messages.send_message_to_chat(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id,
        text="msg_1"
    )
    assert isinstance(message, models.Message)
    assert message.body == "msg_1"
    assert message.user_id == default_user.id
    assert message.chat_id == chat_with_default_user.id


@pytest.mark.asyncio
async def test_user_can_read_message_from_chat(chat_with_default_user, default_user):
    message_1 = await messages.send_message_to_chat(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id,
        text="msg_1"
    )
    message_2 = await messages.send_message_to_chat(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id,
        text="msg_2"
    )
    chat_messages = await messages.read_messages(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id)
    assert chat_messages == [message_1, message_2]


@pytest.mark.asyncio
async def test_user_cannot_read_messages_created_before_his_joining(chat_with_default_user, second_user, default_user):
    await messages.send_message_to_chat(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id, text="msg_1"
    )
    await chats.add_user_to_chat(user_id=second_user.id, chat_id=chat_with_default_user.id)
    message_2 = await messages.send_message_to_chat(
        user_id=default_user.id,
        chat_id=chat_with_default_user.id,
        text="msg_2"
    )
    message_3 = await messages.send_message_to_chat(
        user_id=second_user.id,
        chat_id=chat_with_default_user.id,
        text="msg_3"
    )
    chat_messages = await messages.read_messages(user_id=second_user.id, chat_id=chat_with_default_user.id)
    assert chat_messages == [message_2, message_3]
