from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app import models
from app.crud import Users, AccessTokens, RefreshTokens
from app.utils import exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def authorize_by_username_and_password(username: str, password: str) -> models.User:
    user = await Users.get_one(username=username)
    if not user or not user.password_match(plain_password=password):
        raise exceptions.IncorrectLoginOrPassword
    return user


async def create_auth_token_pair(user_id: int) -> [models.AccessToken, models.RefreshToken]:
    access_token = await AccessTokens.create(user_id)
    refresh_token = await RefreshTokens.create(user_id)
    return access_token, refresh_token


async def revoke_tokens(access_token_body: str, refresh_token_body: str) -> [models.AccessToken, models.RefreshToken]:
    access_token = models.AccessToken(body=access_token_body)
    if not access_token.validate(verify_exp=False):
        raise exceptions.CredentialsException
    user_id = access_token.user_id
    if not await RefreshTokens.get_valid_token(user_id=user_id, body=refresh_token_body):
        raise exceptions.CredentialsException
    return await create_auth_token_pair(user_id)


async def get_user_by_access_token(token_body=Depends(oauth2_scheme), only_active=True) -> models.User:
    access_token = models.AccessToken(body=token_body)
    if not access_token.validate():
        raise exceptions.CredentialsException
    user_id = access_token.user_id
    user = await Users.get_one(id=user_id)
    if not user:
        raise exceptions.UserNotFoundError
    if only_active and not user.is_active:
        raise exceptions.InActiveUser
    return user


async def delete_refresh_token(access_token_body: str, refresh_token_body: str) -> bool:
    """Delete refresh token from DB if access token signature is valid"""
    access_token = models.AccessToken(access_token_body)
    if not access_token.validate(verify_exp=False):
        return False
    is_refresh_token_deleted = await RefreshTokens.delete(user_id=access_token.user_id, body=refresh_token_body)
    return bool(is_refresh_token_deleted)
