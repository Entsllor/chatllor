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


class AuthTokensBodies(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthTokensOut(AuthTokensBodies):
    access_token_expire_at: float
    refresh_token_expire_at: float
