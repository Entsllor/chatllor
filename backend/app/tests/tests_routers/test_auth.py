import time

import pytest
from fastapi import status

from app.crud import Users, RefreshTokens, AccessTokens
from app.schemas.tokens import AccessTokenOut
from app.schemas.users import UserPrivate
from app.tests.conftest import DEFAULT_USER_PASS, DEFAULT_USER_EMAIL, DEFAULT_USER_NAME, USER_CREATE_DATA
from conftest import get_auth_header, urls, is_valid_schema


@pytest.mark.asyncio
async def test_registration_with_valid_data(client):
    assert not await Users.get_one(username=DEFAULT_USER_NAME)
    response = await client.post(urls.create_user, json=USER_CREATE_DATA.dict())
    response_data = response.json()
    assert response_data["username"] == DEFAULT_USER_NAME
    assert response_data["email"] == DEFAULT_USER_EMAIL
    assert response.status_code == status.HTTP_201_CREATED
    assert DEFAULT_USER_PASS not in response.text


@pytest.mark.asyncio
async def test_failed_registration_if_no_email(client):
    response = await client.post(urls.create_user, json=USER_CREATE_DATA.dict(exclude={"email"}))
    assert not await Users.get_one(username=DEFAULT_USER_NAME)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_failed_registration_if_no_password(client):
    response = await client.post(urls.create_user, json=USER_CREATE_DATA.dict(exclude={"password"}))
    assert not await Users.get_one(username=DEFAULT_USER_NAME)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_failed_registration_if_no_username(client):
    response = await client.post(urls.create_user, json=USER_CREATE_DATA.dict(exclude={"username"}))
    assert not await Users.get_one(email=DEFAULT_USER_EMAIL)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_failed_registration_if_not_unique_username(default_user, client):
    assert await Users.get_one(username=DEFAULT_USER_NAME)
    user_with_same_username = USER_CREATE_DATA.copy()
    user_with_same_username.email = "ANOTHER" + DEFAULT_USER_EMAIL
    response = await client.post(urls.create_user, json=user_with_same_username.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login(default_user, client):
    response = await client.post(
        urls.login_by_password,
        data={'username': default_user.username, 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert is_valid_schema(AccessTokenOut, response.json())


@pytest.mark.asyncio
async def test_failed_login_wrong_password(default_user, client):
    response = await client.post(
        urls.login_by_password,
        data={'username': default_user.username, 'password': "__WRONG_PASSWORD"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not is_valid_schema(AccessTokenOut, response.json())


@pytest.mark.asyncio
async def test_failed_login_user_does_not_exist(default_user, client):
    response = await client.post(
        urls.login_by_password,
        data={'username': "__WRONG_USERNAME", 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not is_valid_schema(AccessTokenOut, response.json())


@pytest.mark.asyncio
async def test_revoke_tokens(client, token_pair):
    response = await client.post(urls.revoke_token, cookies=token_pair.dict())
    assert response.status_code == status.HTTP_200_OK
    assert is_valid_schema(AccessTokenOut, response.json())


@pytest.mark.asyncio
async def test_failed_revoking_token_if_refresh_token_expired(client, token_pair, default_user):
    await RefreshTokens.change_expire_term(default_user.id, token_pair.refresh_token, time.time() - 100)
    response = await client.post(urls.revoke_token, cookies=token_pair.dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_revoking_token_if_invalid_access_token(client, token_pair):
    token_pair.access_token = token_pair.access_token + "_invalid"
    response = await client.post(urls.revoke_token, cookies=token_pair.dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_revoking_token_if_access_token_belongs_to_another_user(client, token_pair, second_user):
    another_access_token = await RefreshTokens.create(user_id=second_user.id)
    token_pair.access_token = another_access_token.body
    response = await client.post(urls.revoke_token, cookies=token_pair.dict())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_private_user_data(client, auth_header):
    response = await client.get(urls.read_user_me, headers=auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert is_valid_schema(UserPrivate, response.json())


@pytest.mark.asyncio
async def test_failed_get_private_user_data_invalid_token(client, auth_header):
    auth_header_with_invalid_token = auth_header | {"Authorization": auth_header["Authorization"] + "_invalid"}
    response = await client.get(urls.read_user_me, headers=auth_header_with_invalid_token)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not is_valid_schema(UserPrivate, response.json())


@pytest.mark.asyncio
async def test_failed_get_private_user_data_expired_token(client, default_user):
    access_token = await AccessTokens.create(user_id=default_user.id, expire_delta=-10)
    response = await client.get(urls.read_user_me, headers=get_auth_header(access_token.body))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not is_valid_schema(UserPrivate, response.json())


@pytest.mark.asyncio
async def test_failed_get_private_user_data_without_token(client, token_pair):
    response = await client.get(urls.read_user_me)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not is_valid_schema(UserPrivate, response.json())


@pytest.mark.asyncio
async def test_logout(client, token_pair):
    response = await client.post(urls.logout, cookies=token_pair.dict())
    assert response.status_code == status.HTTP_204_NO_CONTENT
