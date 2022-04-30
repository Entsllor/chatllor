import pytest

from app import crud, models
from app.crud import RefreshTokens, AccessTokens
from app.crud.base import update_instance
from app.services.auth import get_user_by_access_token, revoke_tokens, authorize_by_username_and_password, \
    delete_refresh_token
from app.tests.conftest import DEFAULT_USER_PASS
from app.utils import exceptions


@pytest.mark.asyncio
async def test_get_user_by_access_token(token_pair, default_user):
    found_user = await get_user_by_access_token(token_pair.access_token)
    assert found_user.id == default_user.id
    assert isinstance(found_user, models.User)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_invalid_token(token_pair, default_user):
    with pytest.raises(exceptions.CredentialsException):
        await get_user_by_access_token(token_pair.access_token + "_invalid")


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_not_exist(db, token_pair, default_user):
    await db.delete(default_user)
    with pytest.raises(exceptions.UserNotFoundError):
        await get_user_by_access_token(token_pair.access_token)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_token_expired(default_user):
    new_token = await crud.AccessTokens.create(default_user.id, expire_delta=-100)
    with pytest.raises(exceptions.CredentialsException):
        await get_user_by_access_token(token_body=new_token.body)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_is_not_active(default_user, token_pair):
    await update_instance(default_user, is_active=False)
    with pytest.raises(exceptions.InActiveUser):
        await get_user_by_access_token(token_body=token_pair.access_token)


@pytest.mark.asyncio
async def test_revoke_tokens(token_pair):
    new_access_token, new_refresh_token = await revoke_tokens(
        access_token_body=token_pair.access_token,
        refresh_token_body=token_pair.refresh_token
    )
    assert isinstance(new_access_token, models.AccessToken)
    assert isinstance(new_refresh_token, models.RefreshToken)
    assert token_pair.refresh_token != new_refresh_token.body
    assert token_pair.access_token != new_access_token.body


@pytest.mark.asyncio
async def test_revoke_tokens_with_expired_access_token(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id, expire_delta=-100)
    new_access_token, new_refresh_token = await revoke_tokens(
        access_token_body=access_token.body,
        refresh_token_body=refresh_token.body
    )
    assert refresh_token.body != new_refresh_token.body
    assert access_token.body != new_access_token.body


@pytest.mark.asyncio
async def test_failed_revoke_tokens_invalid_refresh_token(token_pair):
    with pytest.raises(exceptions.InvalidAuthTokens):
        await revoke_tokens(
            access_token_body=token_pair.access_token,
            refresh_token_body=token_pair.refresh_token + "_invalid"
        )


@pytest.mark.asyncio
async def test_failed_revoke_tokens_expired_refresh_token(default_user):
    refresh_token = await RefreshTokens.create(user_id=default_user.id, expire_delta=-100)
    access_token = await AccessTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.InvalidAuthTokens):
        await revoke_tokens(access_token_body=access_token.body, refresh_token_body=refresh_token.body)


@pytest.mark.asyncio
async def test_failed_revoke_tokens_invalid_access_token(token_pair):
    with pytest.raises(exceptions.InvalidAuthTokens):
        await revoke_tokens(
            access_token_body=token_pair.access_token + "_invalid",
            refresh_token_body=token_pair.refresh_token
        )


@pytest.mark.asyncio
async def test_authorize_by_username_and_password(default_user):
    user = await authorize_by_username_and_password(default_user.username, DEFAULT_USER_PASS)
    assert isinstance(user, models.User)
    assert user.id == default_user.id


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_password(default_user):
    with pytest.raises(exceptions.IncorrectLoginOrPassword):
        await authorize_by_username_and_password(default_user.username, DEFAULT_USER_PASS + "_invalid")


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_username(default_user):
    with pytest.raises(exceptions.IncorrectLoginOrPassword):
        await authorize_by_username_and_password("another" + default_user.username, DEFAULT_USER_PASS)


@pytest.mark.asyncio
async def test_delete_refresh_token(token_pair):
    is_deleted = await delete_refresh_token(
        access_token_body=token_pair.access_token,
        refresh_token_body=token_pair.refresh_token
    )
    assert is_deleted


@pytest.mark.asyncio
async def test_delete_refresh_token_with_expired_access_token(token_pair, default_user):
    expired_access_token = await AccessTokens.create(user_id=default_user.id, expire_delta=-10)
    is_deleted = await delete_refresh_token(
        access_token_body=expired_access_token.body,
        refresh_token_body=token_pair.refresh_token
    )
    assert is_deleted


@pytest.mark.asyncio
async def test_delete_refresh_token_if_expired(access_token, default_user):
    expired_refresh_token = await RefreshTokens.create(user_id=default_user.id, expire_delta=-10)
    is_deleted = await delete_refresh_token(
        access_token_body=access_token.body,
        refresh_token_body=expired_refresh_token.body
    )
    assert is_deleted


@pytest.mark.asyncio
async def test_failed_delete_invalid_refresh_token(token_pair):
    is_deleted = await delete_refresh_token(
        access_token_body=token_pair.access_token,
        refresh_token_body=token_pair.refresh_token + "_invalid"
    )
    assert not is_deleted


@pytest.mark.asyncio
async def test_failed_delete_refresh_token_if_invalid_access_token(token_pair):
    is_logout = await delete_refresh_token(
        access_token_body=token_pair.access_token + "_invalid",
        refresh_token_body=token_pair.refresh_token
    )
    assert not is_logout
