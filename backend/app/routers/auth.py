from fastapi import APIRouter, Depends, Response, Cookie, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import settings
from app.schemas.tokens import AccessTokenOut
from app.services import auth
from app.utils import exceptions

AUTH_PREFIX = '/auth'
router = APIRouter(prefix=AUTH_PREFIX)


@router.post('/login', response_model=AccessTokenOut)
async def login_by_password(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth.authorize_by_username_and_password(form_data.username, form_data.password)
    access_token, refresh_token = await auth.create_auth_token_pair(user.id)
    response.set_cookie(
        key="access_token",
        value=access_token.body,
        httponly=True,
        expires=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        path=AUTH_PREFIX
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=AUTH_PREFIX
    )
    return AccessTokenOut(access_token=access_token.body)


@router.post('/revoke', response_model=AccessTokenOut)
async def revoke_token(response: Response, access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
    if not access_token or not refresh_token:
        raise exceptions.CredentialsException
    access_token, refresh_token = await auth.revoke_tokens(
        access_token_body=access_token,
        refresh_token_body=refresh_token
    )
    response.set_cookie(
        key="access_token",
        value=access_token.body,
        httponly=True,
        expires=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        path=AUTH_PREFIX
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token.body,
        httponly=True,
        expires=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        path=AUTH_PREFIX
    )
    return AccessTokenOut(access_token=access_token.body)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, access_token: str = Cookie(None), refresh_token: str = Cookie(None)):
    """Clear auth cookies and delete refresh token from db if access token signature is valid"""
    await auth.delete_refresh_token(access_token_body=access_token, refresh_token_body=refresh_token)
    response.delete_cookie(key="access_token", httponly=True, path=AUTH_PREFIX)
    response.delete_cookie(key="refresh_token", httponly=True, path=AUTH_PREFIX)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
