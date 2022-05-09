import pytest
from fastapi import status

from app import schemas
from ...crud import Messages
from ...services import chats

MESSAGE_CREATE_DATA = schemas.messages.MessageCreate(body="__MESSAGE_TEXT__")


@pytest.mark.asyncio
async def test_send_message(auth_header, client, urls, chat_with_default_user):
    response = await client.post(
        urls.create_message(chat_id=chat_with_default_user.id),
        headers=auth_header,
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.json()["body"] == MESSAGE_CREATE_DATA.body
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_delete_self_message_from_chat(default_user, chat_with_default_user, client, urls, auth_header):
    message = await Messages.create(user_id=default_user.id, body="_DELETE_THIS", chat_id=chat_with_default_user.id)
    response = await client.delete(
        urls.delete_message(chat_id=chat_with_default_user.id, message_id=message.id),
        headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_delete_message_if_not_found(default_user, chat_with_default_user, client, urls, auth_header):
    response = await client.delete(
        urls.delete_message(chat_id=chat_with_default_user.id, message_id=1000),
        headers=auth_header
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_failed_delete_message_from_chat_no_auth(default_user, chat_with_default_user, client, urls, auth_header):
    message = await Messages.create(user_id=default_user.id, body="_DELETE_THIS", chat_id=chat_with_default_user.id)
    response = await client.delete(urls.delete_message(chat_id=chat_with_default_user.id, message_id=message.id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_delete_foreign_message_from_chat(second_user, chat_with_default_user, client, urls, auth_header):
    await chats.add_user_to_chat(user_id=second_user.id, chat_id=chat_with_default_user.id)
    message = await Messages.create(user_id=second_user.id, body="_DELETE_THIS", chat_id=chat_with_default_user.id)
    response = await client.delete(
        urls.delete_message(chat_id=chat_with_default_user.id, message_id=message.id),
        headers=auth_header
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_failed_send_message_user_not_in_chat(default_user, auth_header, client, urls, empty_chat):
    response = await client.post(
        urls.create_message(chat_id=empty_chat.id),
        headers=auth_header,
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_read_messages(client, urls, auth_header, chat_with_default_user, second_user, default_user):
    await chats.add_user_to_chat(second_user.id, chat_with_default_user.id)
    await Messages.create(default_user.id, "__test_read_messages_1", chat_id=chat_with_default_user.id)
    await Messages.create(second_user.id, "__test_read_messages_2", chat_id=chat_with_default_user.id)
    response = await client.get(url=urls.read_messages(chat_id=chat_with_default_user.id), headers=auth_header)
    assert [schemas.messages.UserMessage.validate(message) for message in response.json()]  # response validation
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_read_messages_user_not_in_chat(client, urls, auth_header, empty_chat, second_user, default_user):
    await chats.add_user_to_chat(second_user.id, empty_chat.id)
    await Messages.create(second_user.id, "__test_messages_1", chat_id=empty_chat.id)
    response = await client.get(url=urls.read_messages(chat_id=empty_chat.id), headers=auth_header)
    assert response.status_code == status.HTTP_403_FORBIDDEN
