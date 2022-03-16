import os
import time

from jose import jwt

from app import models
from app.core.settings import settings
from app.crud.base import create, delete, get_one
from app.schemas.tokens import RefreshToken, AccessToken


class RefreshTokenCRUD:
    model = models.RefreshToken

    @staticmethod
    async def create_body() -> str:
        return os.urandom(63).hex()

    async def create(self, db, user_id, expire_delta: int = None) -> RefreshToken:
        await delete(self.model, db, filters={'user_id': user_id})
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        db_token = await create(
            model=self.model,
            db=db,
            user_id=user_id,
            expire_at=expire_at,
            body=await self.create_body()
        )
        return RefreshToken.from_orm(db_token)

    @staticmethod
    def is_active(token: RefreshToken, user_id: int):
        return token.user_id == user_id and (time.time() < token.expire_at)

    async def get_by_body_and_user_id(self, db, user_id: int, body: str, raise_if_none=True) -> models.RefreshToken:
        return await get_one(self.model, db, filters={'user_id': user_id, 'body': body}, raise_if_none=raise_if_none)


class AccessTokenCRUD:
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


AccessTokens = AccessTokenCRUD()
RefreshTokens = RefreshTokenCRUD()
