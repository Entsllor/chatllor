from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud.base import create_instance, get_one_by_query, BaseCrudDB
from app.utils.options import GetOneOptions
from app.utils.passwords import get_password_hash, verify_password


class UserRepo(BaseCrudDB):
    model = models.User

    async def create(self, db: AsyncSession, *, username: str, password: str, email: str) -> models.User:
        hashed_password = get_password_hash(password)
        user = self.model(username=username, hashed_password=hashed_password, email=email)
        return await create_instance(db, user)

    async def get_by_username(
            self, db: AsyncSession, username: str, options: GetOneOptions | dict = None) -> models.User:
        q = self._select.where(self.model.username == username)
        return await get_one_by_query(db, q, options=options)

    async def get_by_email(
            self, db: AsyncSession, email: str, options: GetOneOptions | dict = None) -> models.User:
        q = self._select.where(self.model.email == email)
        return await get_one_by_query(db, q, options=options)

    async def get_by_id(
            self,
            db: AsyncSession,
            user_id: int,
            options: GetOneOptions = None
    ) -> models.User:
        q = self._select.where(self.model.id == user_id)
        return await get_one_by_query(db, q, options=options)


Users = UserRepo()
