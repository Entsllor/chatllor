import pytest

from app import crud, models
from app.crud import RefreshTokens, AccessTokens
from app.crud.base import update_instance
from app.services.auth import get_user_by_access_token, revoke_tokens, authorize_by_username_and_password
from app.tests.conftest import DEFAULT_USER_PASS
from app.utils import exceptions


@pytest.mark.asyncio
async def test_get_user_by_access_token(db, token_pair, default_user):
    found_user = await get_user_by_access_token(db, token_pair.access_token)
    assert found_user.id == default_user.id
    assert isinstance(found_user, models.User)


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_invalid_token(db, token_pair, default_user):
    with pytest.raises(exceptions.HTTPException) as exc:
        await get_user_by_access_token(db, token_pair.access_token + "_invalid")
    assert exc.value is exceptions.CredentialsException


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_not_exist(db, token_pair, default_user):
    await db.delete(default_user)
    with pytest.raises(exceptions.HTTPException) as exc:
        await get_user_by_access_token(db, token_pair.access_token)
    assert exc.value is exceptions.UserNotFoundError


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_token_expired(db, default_user):
    new_token = await crud.AccessTokens.create(default_user.id, expire_delta=-100)
    with pytest.raises(exceptions.HTTPException) as exc:
        await get_user_by_access_token(db, token_body=new_token.body)
    assert exc.value is exceptions.CredentialsException


@pytest.mark.asyncio
async def test_failed_get_user_by_access_token_if_user_is_not_active(db, default_user, token_pair):
    await update_instance(db, default_user, is_active=False)
    with pytest.raises(exceptions.HTTPException) as exc:
        await get_user_by_access_token(db, token_body=token_pair.access_token)
    assert exc.value is exceptions.InActiveUser


@pytest.mark.asyncio
async def test_revoke_tokens(db, default_user):
    refresh_token = await RefreshTokens.create(db, user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id)
    new_access_token, new_refresh_token = await revoke_tokens(
        db, access_token_body=access_token.body, refresh_token_body=refresh_token.body)
    assert isinstance(new_access_token, models.AccessToken)
    assert isinstance(new_refresh_token, models.RefreshToken)
    assert refresh_token.body != new_refresh_token.body
    assert access_token.body != new_access_token.body


@pytest.mark.asyncio
async def test_revoke_tokens_with_expired_access_token(db, default_user):
    refresh_token = await RefreshTokens.create(db, user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id, expire_delta=-100)
    new_access_token, new_refresh_token = await revoke_tokens(
        db, access_token_body=access_token.body, refresh_token_body=refresh_token.body)
    assert refresh_token.body != new_refresh_token.body
    assert access_token.body != new_access_token.body


@pytest.mark.asyncio
async def test_failed_revoke_tokens_invalid_refresh_token(db, default_user):
    refresh_token = await RefreshTokens.create(db, user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.HTTPException) as exc:
        await revoke_tokens(db, access_token_body=access_token.body, refresh_token_body=refresh_token.body + "_invalid")
    assert exc.value is exceptions.InvalidAuthTokens


@pytest.mark.asyncio
async def test_failed_revoke_tokens_expired_refresh_token(db, default_user):
    refresh_token = await RefreshTokens.create(db, user_id=default_user.id, expire_delta=-100)
    access_token = await AccessTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.HTTPException) as exc:
        await revoke_tokens(db, access_token_body=access_token.body, refresh_token_body=refresh_token.body)
    assert exc.value is exceptions.InvalidAuthTokens


@pytest.mark.asyncio
async def test_failed_revoke_tokens_invalid_access_token(db, default_user):
    refresh_token = await RefreshTokens.create(db, user_id=default_user.id)
    access_token = await AccessTokens.create(user_id=default_user.id)
    with pytest.raises(exceptions.HTTPException) as exc:
        await revoke_tokens(db, access_token_body=access_token.body + "_invalid", refresh_token_body=refresh_token.body)
    assert exc.value is exceptions.InvalidAuthTokens


@pytest.mark.asyncio
async def test_authorize_by_username_and_password(db, default_user):
    user = await authorize_by_username_and_password(db, default_user.username, DEFAULT_USER_PASS)
    assert isinstance(user, models.User)
    assert user.id == default_user.id


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_password(db, default_user):
    with pytest.raises(exceptions.HTTPException) as exc:
        await authorize_by_username_and_password(db, default_user.username, DEFAULT_USER_PASS + "_invalid")
    assert exc.value is exceptions.IncorrectLoginOrPassword


@pytest.mark.asyncio
async def test_failed_authorize_by_username_and_password_with_incorrect_username(db, default_user):
    with pytest.raises(exceptions.HTTPException) as exc:
        await authorize_by_username_and_password(db, "another" + default_user.username, DEFAULT_USER_PASS)
    assert exc.value is exceptions.IncorrectLoginOrPassword
