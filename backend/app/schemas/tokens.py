from app.schemas.base import BaseScheme


class Token(BaseScheme):
    expire_at: int | None
    body: str


class AccessToken(Token):
    type: str = "Bearer"


class RefreshToken(Token):
    user_id: int = None


class AuthTokens(BaseScheme):
    access_token: AccessToken
    refresh_token: RefreshToken


class AccessTokenOut(BaseScheme):
    access_token: str
    token_type: str = "bearer"


class AuthTokensBodies(AccessTokenOut):
    refresh_token: str
