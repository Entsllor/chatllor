from pydantic import BaseModel


class Token(BaseModel):
    expire_at: int | None
    body: str


class AccessToken(Token):
    type: str = "Bearer"


class RefreshToken(Token):
    user_id: int = None

    class Config:
        orm_mode = True


class AuthTokens(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AuthTokensBodies(AccessTokenOut):
    refresh_token: str
