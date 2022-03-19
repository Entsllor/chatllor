from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud import Users, AccessTokens, RefreshTokens
from app.utils.exceptions import IncorrectLoginOrPassword, InstanceNotFound, InvalidAuthTokens, CredentialsException, \
    InActiveUser, UserNotFoundError
from app.utils.options import GetOneOptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authorize_by_username_and_password(db, username: str, password: str) -> models.User:
    user = await Users.get_by_username(db, username=username)
    if not user or not user.password_match(plain_password=password):
        raise IncorrectLoginOrPassword
    return user


async def create_auth_token_pair(db, user_id: int) -> tuple[models.AccessToken, models.RefreshToken]:
    access_token = await AccessTokens.create(user_id)
    refresh_token = await RefreshTokens.create(db, user_id)
    return access_token, refresh_token


async def validate_auth_tokens(db: AsyncSession, access_token_body: str, refresh_token_body: str) -> int:
    try:
        access_token = models.AccessToken(body=access_token_body)
        access_token.validate()
        user_id = access_token.user_id
        await RefreshTokens.get_valid_token(db, user_id=user_id, body=refresh_token_body)
    except (JWTError, InstanceNotFound):
        raise InvalidAuthTokens
    return user_id


async def authorize_by_refresh_token(
        db, access_token_body: str, refresh_token_body: str) -> tuple[models.AccessToken, models.RefreshToken]:
    authorized_user_id = await validate_auth_tokens(db, access_token_body, refresh_token_body)
    return await create_auth_token_pair(db, authorized_user_id)


async def get_user_by_access_token(db, token_body=Depends(oauth2_scheme), only_active=True) -> models.User:
    try:
        access_token = models.AccessToken(body=token_body)
        access_token.validate()
        user_id = access_token.user_id
        user = await Users.get_by_id(db, user_id=user_id, options=GetOneOptions(raise_if_none=True))
        if only_active and not user.is_active:
            raise InActiveUser
    except JWTError:
        raise CredentialsException
    except InstanceNotFound:
        raise UserNotFoundError
    return user
