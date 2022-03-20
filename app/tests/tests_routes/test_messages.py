import pytest

from app import schemas
from .. import paths
from ..conftest import DEFAULT_USER_PASS
from ...crud import Messages, Users


def token_auth(access_token_body: str) -> dict:
    return {"Authorization": f"Bearer {access_token_body}"}


AUTH_BEARER = "Authorization: Bearer {}"
MESSAGE_CREATE_DATA = schemas.messages.MessageCreate(body="__MESSAGE_TEXT__")


def test_create_message(token_pair, client):
    response = client.post(paths.MESSAGES, headers=token_auth(token_pair.access_token), json=MESSAGE_CREATE_DATA.dict())
    assert response.json()["body"] == MESSAGE_CREATE_DATA.body
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_failed_create_message_user_does_not_exist(db, default_user, token_pair, client):
    await db.delete(default_user)
    response = client.post(paths.MESSAGES, headers=token_auth(token_pair.access_token), json=MESSAGE_CREATE_DATA.dict())
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_read_messages(db, client, token_pair):
    await Users.create(db, username="second_user", password=DEFAULT_USER_PASS, email="second@mail.com")
    await Messages.create(db, 1, "__test_read_messages_1")
    await Messages.create(db, 2, "__test_read_messages_2")
    response = client.get(paths.MESSAGES, json=MESSAGE_CREATE_DATA.dict())
    db_messages = [schemas.messages.MessageOut.from_orm(msg) for msg in await Messages.get_all(db)]
    assert response.status_code == 200
    assert len(db_messages) == 2
    assert response.json() == db_messages
