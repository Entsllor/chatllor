from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.repos.base import BaseAsyncCrudRepo
from app.utils.passwords import get_password_hash, verify_password


class UserRepo(BaseAsyncCrudRepo):
    model = models.User

    async def create(self, db: AsyncSession, username, password, email) -> models.User:
        hashed_password = get_password_hash(password)
        return await super(UserRepo, self).create(db, username=username, hashed_password=hashed_password, email=email)

    @staticmethod
    async def do_password_match(user: models.User, plain_password) -> bool:
        return verify_password(plain_password, user.hashed_password)


Users = UserRepo()
