import pytest
from fastapi import status

from .. import paths
from ..conftest import token_auth


@pytest.mark.asyncio
async def test_user_join_chat(token_pair, empty_chat, client):
    response = await client.post(
        url=paths.CHAT_USERS.format(chat_id=empty_chat.id),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_user_join_not_existing_chat(token_pair, client):
    response = await client.post(url=paths.CHAT_USERS.format(chat_id=1), headers=token_auth(token_pair.access_token))
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_user_leave_chat(token_pair, chat_with_default_user, client):
    response = await client.delete(
        url=paths.CHAT_USERS.format(chat_id=chat_with_default_user.id),
        headers=token_auth(token_pair.access_token)
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_user_left_not_existing_chat(token_pair, client):
    response = await client.delete(url=paths.CHAT_USERS.format(chat_id=1), headers=token_auth(token_pair.access_token))
    assert response.status_code == status.HTTP_404_NOT_FOUND
