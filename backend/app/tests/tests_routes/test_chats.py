import pytest
from fastapi import status

from app.schemas.chats import ChatCreate
from .. import paths
from ..conftest import token_auth
from ...crud import Chats

CHAT_CREATE_DATA = ChatCreate(name="_TEST_CHAT")


@pytest.mark.asyncio
async def test_create_chat(client, token_pair):
    response = await client.post(
        url=paths.CHATS,
        headers=token_auth(token_pair.access_token),
        json=CHAT_CREATE_DATA.dict()
    )
    chat = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert chat['name'] == CHAT_CREATE_DATA.name


@pytest.mark.asyncio
async def test_failed_create_chat_unauthorized(client, token_pair):
    response = await client.post(url=paths.CHATS, json=CHAT_CREATE_DATA.dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_chat(client, token_pair, chat_with_default_user):
    response = await client.delete(
        url=paths.CHATS + str(chat_with_default_user.id),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_200_OK
    assert not await Chats.get_one(id=chat_with_default_user.id)


@pytest.mark.asyncio
async def test_failed_delete_chat_user_not_in_the_chat(client, token_pair, empty_chat):
    response = await client.delete(
        url=paths.CHATS + str(empty_chat.id),
        headers=token_auth(token_pair.access_token),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert await Chats.get_one(id=empty_chat.id) is empty_chat


@pytest.mark.asyncio
async def test_failed_delete_unauthorized(client, token_pair, empty_chat):
    response = await client.delete(url=paths.CHATS + str(empty_chat.id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert await Chats.get_one(id=empty_chat.id) is empty_chat
