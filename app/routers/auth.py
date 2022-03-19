from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.tokens import AuthTokensBodies, AuthTokensOut
from app.services.auth import authorize_by_username_and_password, revoke_tokens, create_auth_token_pair
from app.utils.dependencies import get_db

router = APIRouter(prefix="/token")


@router.post("/", response_model=AuthTokensOut)
async def login_by_password(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authorize_by_username_and_password(db, form_data.username, form_data.password)
    access_token, refresh_token = await create_auth_token_pair(db, user.id)
    return AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        access_token_expire_at=access_token.expire_at,
        refresh_token_expire_at=refresh_token.expire_at
    )


@router.post("/refresh", response_model=AuthTokensOut)
async def login_by_refresh_token(auth_tokens: AuthTokensBodies, db=Depends(get_db)):
    access_token, refresh_token = await revoke_tokens(
        db=db,
        access_token_body=auth_tokens.access_token,
        refresh_token_body=auth_tokens.refresh_token
    )
    return AuthTokensOut(
        access_token=access_token.body,
        refresh_token=refresh_token.body,
        access_token_expire_at=access_token.expire_at,
        refresh_token_expire_at=refresh_token.expire_at
    )
