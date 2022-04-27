import pytest
from fastapi import status

from app import schemas
from .. import paths
from ..conftest import token_auth
from ...crud import Messages
from ...services import chats

MESSAGE_CREATE_DATA = schemas.messages.MessageCreate(body="__MESSAGE_TEXT__")


@pytest.mark.asyncio
async def test_send_message(token_pair, client, chat_with_default_user):
    response = await client.post(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.json()["body"] == MESSAGE_CREATE_DATA.body
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_failed_send_message_user_does_not_exist(db, default_user, token_pair, client, chat_with_default_user):
    await db.delete(default_user)
    response = await client.post(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_self_message_from_chat(default_user, chat_with_default_user, client, token_pair):
    message = await Messages.create(user_id=default_user.id, body="_DELETE_THIS", chat_id=chat_with_default_user.id)
    response = await client.delete(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id) + str(message.id),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_delete_message_from_chat_no_message(default_user, chat_with_default_user, client, token_pair):
    response = await client.delete(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id) + str(1),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_failed_delete_message_from_chat_no_auth(default_user, chat_with_default_user, client, token_pair):
    response = await client.delete(paths.MESSAGES.format(chat_id=chat_with_default_user.id) + str(1))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_delete_foreign_message_from_chat(second_user, chat_with_default_user, client, token_pair):
    await chats.add_user_to_chat(user_id=second_user.id, chat_id=chat_with_default_user.id)
    message = await Messages.create(user_id=second_user.id, body="_DELETE_THIS", chat_id=chat_with_default_user.id)
    response = await client.delete(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id) + str(message.id),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_failed_send_message_user_not_in_chat(default_user, token_pair, client, empty_chat):
    response = await client.post(
        paths.MESSAGES.format(chat_id=empty_chat.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_messages(client, token_pair, chat_with_default_user, second_user, default_user):
    await chats.add_user_to_chat(second_user.id, chat_with_default_user.id)
    await Messages.create(default_user.id, "__test_read_messages_1", chat_id=chat_with_default_user.id)
    await Messages.create(second_user.id, "__test_read_messages_2", chat_id=chat_with_default_user.id)
    response = await client.get(
        url=paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token)
    )
    db_messages = [schemas.messages.MessageOut.from_orm(msg)
                   for msg in await Messages.get_all(chat_id=chat_with_default_user.id)]
    assert response.status_code == status.HTTP_200_OK
    assert len(db_messages) == 2
    assert response.json() == db_messages
