import os
import time

from jose import jwt

from app import models
from app.core.settings import settings
from app.repos.base import BaseAsyncCrudRepo
from app.schemas.tokens import RefreshToken, AccessToken


class RefreshTokenRepo(BaseAsyncCrudRepo):
    model = models.RefreshToken

    @staticmethod
    async def create_body() -> str:
        return os.urandom(63).hex()

    async def create(self, db, user_id, expire_delta: int = None) -> RefreshToken:
        await self.delete(db, user_id=user_id)
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        db_token = await super(RefreshTokenRepo, self).create(
            db=db,
            user_id=user_id,
            expire_at=expire_at,
            body=await self.create_body()
        )
        return RefreshToken.from_orm(db_token)

    @staticmethod
    def is_active(token: RefreshToken, user_id):
        return token.user_id == user_id and (time.time() < token.expire_at)


class AccessTokenRepo:
    @staticmethod
    async def _create(data: dict = None, expire_delta: int = None):
        if not isinstance(data, dict):
            data = dict()
        else:
            data = data.copy()
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = int(time.time() + expire_delta)
        data["exp"] = expire_at
        body = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return AccessToken(expire_at=expire_at, body=body)

    async def create(self, user_id: int, expire_delta: int = None) -> AccessToken:
        return await self._create(data={'sub': str(user_id)}, expire_delta=expire_delta)

    @staticmethod
    async def get_payload(token: str, options: dict = None) -> dict:
        options = options or dict()
        if "verify_exp" not in options:
            options["verify_exp"] = True
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options=options)


AccessTokens = AccessTokenRepo()
RefreshTokens = RefreshTokenRepo()
