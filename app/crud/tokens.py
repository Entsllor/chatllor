import os
import time

from jose import jwt
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.settings import settings
from app.crud.base import update_by_query, create_instance, delete_by_query, get_one_by_query
from app.schemas.tokens import RefreshToken, AccessToken
from app.utils.options import GetOneOptions


class RefreshTokenCRUD:
    model = models.RefreshToken

    @staticmethod
    async def create_body() -> str:
        return os.urandom(63).hex()

    async def create(self, db, user_id, expire_delta: int = None) -> RefreshToken:
        await delete_by_query(db, delete(self.model).where(self.model.user_id == user_id))
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        refresh_token = self.model(user_id=user_id, expire_at=expire_at, body=await self.create_body())
        db_token = await create_instance(db, refresh_token)
        return RefreshToken.from_orm(db_token)

    @staticmethod
    def is_active(token: RefreshToken, user_id: int):
        return token.user_id == user_id and (time.time() < token.expire_at)

    async def get_by_body_and_user_id(
            self,
            db: AsyncSession,
            user_id: int,
            body: str,
            options: GetOneOptions = None
    ) -> models.RefreshToken:
        q = select(self.model).where(self.model.user_id == user_id, self.model.body == body)
        return await get_one_by_query(db, q, options=options)

    async def change_expire_term(self, db, user_id: int, token_body: str, expire_at: int):
        q = update(self.model). \
            where(self.model.user_id == user_id, self.model.body == token_body). \
            values(expire_at=expire_at)
        return await update_by_query(db, q)


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
