from app.schemas.base import BaseScheme


class Token(BaseScheme):
    expire_at: int | None
    body: str


class AccessTokenOut(BaseScheme):
    access_token: str
    token_type: str = "bearer"


class AuthTokensBodies(AccessTokenOut):
    refresh_token: str
