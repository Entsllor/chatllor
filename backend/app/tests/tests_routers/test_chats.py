import pytest
from fastapi import status

from ...crud import Chats
from ...schemas.chats import ChatCreate, ChatOut
from ..conftest import urls

CHAT_CREATE_DATA = ChatCreate(name="_TEST_CHAT")


@pytest.mark.asyncio
async def test_create_chat(client, auth_header):
    response = await client.post(url=urls.create_chat, headers=auth_header, json=CHAT_CREATE_DATA.dict())
    chat = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert chat['name'] == CHAT_CREATE_DATA.name


@pytest.mark.asyncio
async def test_failed_create_chat_unauthorized(client, auth_header):
    response = await client.post(url=urls.create_chat, json=CHAT_CREATE_DATA.dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_chat(client, auth_header, chat_with_default_user):
    response = await client.delete(url=urls.delete_chat(chat_id=chat_with_default_user.id), headers=auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert not await Chats.get_one(id=chat_with_default_user.id)


@pytest.mark.asyncio
async def test_failed_delete_chat_user_not_in_the_chat(client, auth_header, empty_chat):
    response = await client.delete(url=urls.delete_chat(chat_id=empty_chat.id), headers=auth_header, )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert await Chats.get_one(id=empty_chat.id) is empty_chat


@pytest.mark.asyncio
async def test_failed_delete_unauthorized(client, auth_header, empty_chat):
    response = await client.delete(url=urls.delete_chat(chat_id=empty_chat.id))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert await Chats.get_one(id=empty_chat.id) is empty_chat


@pytest.mark.asyncio
async def test_read_chats(client, empty_chat):
    response = await client.get(url=urls.read_chats)
    assert response.status_code == status.HTTP_200_OK
    assert [ChatOut.validate(chat) for chat in response.json()]
