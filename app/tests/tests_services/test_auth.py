import pytest

from app import crud, models
from app.crud.base import update_instance
from app.services.auth import get_user_by_access_token
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
    assert exc.value is exceptions.CredentialsException


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
    assert exc.value is exceptions.CredentialsException
