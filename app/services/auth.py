from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app import models
from app.crud import Users, AccessTokens, RefreshTokens
from app.schemas.tokens import AuthTokens
from app.utils.exceptions import IncorrectLoginOrPassword, InstanceNotFound, InvalidTokenPair, CredentialsException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authorize_by_username_and_password(db, username: str, password: str) -> models.User:
    user = await Users.get_by_username(db, username=username)
    if not user or not await Users.do_password_match(user, password):
        raise IncorrectLoginOrPassword
    return user


async def create_auth_token_pair(db, user_id: int) -> AuthTokens:
    access_token = await AccessTokens.create(user_id)
    refresh_token = await RefreshTokens.create(db, user_id)
    return AuthTokens(access_token=access_token, refresh_token=refresh_token)


async def is_correct_token_pair(db, access_token: str, refresh_token: str) -> int | None:
    payload = await AccessTokens.get_payload(access_token, options={"verify_exp": False})
    user_id = int(payload.get("sub"))
    try:
        await RefreshTokens.get_by_body_and_user_id(db, user_id=user_id, body=refresh_token, raise_if_none=True)
    except (JWTError, InstanceNotFound):
        return None
    return user_id


async def authorize_by_refresh_token(db, access_token: str, refresh_token: str) -> AuthTokens:
    authorized_user_id = await is_correct_token_pair(db, access_token, refresh_token)
    if authorized_user_id:
        return await create_auth_token_pair(db, authorized_user_id)
    else:
        raise InvalidTokenPair


async def get_user_by_access_token(db, token_body=Depends(oauth2_scheme), only_active=True) -> models.User | None:
    try:
        payload = await AccessTokens.get_payload(token_body)
        user_id = payload.get("sub")
        filters = dict(id=user_id)
        if only_active:
            filters["is_active"] = True
        user = await Users.get_by_id(db, raise_if_none=True, user_id=user_id)
    except (JWTError, InstanceNotFound):
        raise CredentialsException
    return user
