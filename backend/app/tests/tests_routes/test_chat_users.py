import pytest
from fastapi import status

from .. import paths


@pytest.mark.asyncio
async def test_user_join_chat(auth_header, empty_chat, client):
    response = await client.post(
        url=paths.CHAT_USERS.format(chat_id=empty_chat.id),
        headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_user_join_not_existing_chat(auth_header, client):
    response = await client.post(url=paths.CHAT_USERS.format(chat_id=1), headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_user_leave_chat(auth_header, chat_with_default_user, client):
    response = await client.delete(
        url=paths.CHAT_USERS.format(chat_id=chat_with_default_user.id),
        headers=auth_header
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_failed_user_left_not_existing_chat(auth_header, client):
    response = await client.delete(url=paths.CHAT_USERS.format(chat_id=1), headers=auth_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
