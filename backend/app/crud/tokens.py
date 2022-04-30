import time

from jose import jwt

from app import models
from app.core.settings import settings
from app.crud.base import create_instance, delete_by_query, get_one_by_query, BaseCrudDB
from app.utils.options import GetOneOptions


class RefreshTokenCRUD(BaseCrudDB):
    model = models.RefreshToken

    async def create(self, user_id, expire_delta: int = None) -> models.RefreshToken:
        await delete_by_query(self._delete.where(self.model.user_id == user_id))
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        refresh_token = self.model(user_id=user_id, expire_at=expire_at)
        return await create_instance(refresh_token)

    async def get_valid_token(self, user_id, body) -> models.RefreshToken | None:
        q = self._select.where(
            self.model.user_id == user_id,
            self.model.body == body,
            self.model.expire_at >= time.time()
        )
        return await get_one_by_query(q)

    async def change_expire_term(self, user_id: int, token_body: str, expire_at: int):
        return await self.update(
            values={'expire_at': expire_at},
            filters={'user_id': user_id, 'body': token_body}
        )


class AccessTokenCRUD:
    @staticmethod
    async def create_with_custom_data(data: dict = None, expire_delta: int = None) -> models.AccessToken:
        if not isinstance(data, dict):
            data = dict()
        else:
            data = data.copy()
        if expire_delta is None:
            expire_delta = settings.REFRESH_TOKEN_EXPIRE_SECONDS
        expire_at = time.time() + expire_delta
        data["exp"] = expire_at
        body = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return models.AccessToken(body=body)

    async def create(self, user_id: int, expire_delta: int = None) -> models.AccessToken:
        return await self.create_with_custom_data(data={'sub': str(user_id)}, expire_delta=expire_delta)


AccessTokens = AccessTokenCRUD()
RefreshTokens = RefreshTokenCRUD()
