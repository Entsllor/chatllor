import pytest

from app import schemas
from .. import paths
from ...crud import Messages
from ...services import chats


def token_auth(access_token_body: str) -> dict:
    return {"Authorization": f"Bearer {access_token_body}"}


AUTH_BEARER = "Authorization: Bearer {}"
MESSAGE_CREATE_DATA = schemas.messages.MessageCreate(body="__MESSAGE_TEXT__")


def test_send_message(token_pair, client, chat_with_default_user):
    response = client.post(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.json()["body"] == MESSAGE_CREATE_DATA.body
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_failed_send_message_user_does_not_exist(db, default_user, token_pair, client, chat_with_default_user):
    await db.delete(default_user)
    response = client.post(
        paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.status_code == 401


def test_failed_send_message_user_not_in_chat(db, default_user, token_pair, client, empty_chat):
    response = client.post(
        paths.MESSAGES.format(chat_id=empty_chat.id),
        headers=token_auth(token_pair.access_token),
        json=MESSAGE_CREATE_DATA.dict()
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_read_messages(db, client, token_pair, chat_with_default_user, second_user, default_user):
    await chats.add_user_to_chat(db, second_user.id, chat_with_default_user.id)
    await Messages.create(db, default_user.id, "__test_read_messages_1", chat_id=chat_with_default_user.id)
    await Messages.create(db, second_user.id, "__test_read_messages_2", chat_id=chat_with_default_user.id)
    response = client.get(
        url=paths.MESSAGES.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token)
    )
    db_messages = [schemas.messages.MessageOut.from_orm(msg)
                   for msg in await Messages.get_all(db, chat_id=chat_with_default_user.id)]
    assert response.status_code == 200
    assert len(db_messages) == 2
    assert response.json() == db_messages
