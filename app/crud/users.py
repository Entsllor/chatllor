from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.crud.base import create, get_one
from app.utils.options import GetOneOptions
from app.utils.passwords import get_password_hash, verify_password


class UserRepo:
    model = models.User

    async def create(self, db: AsyncSession, *, username: str, password: str, email: str) -> models.User:
        hashed_password = get_password_hash(password)
        return await create(self.model, db, username=username, hashed_password=hashed_password, email=email)

    @staticmethod
    async def do_password_match(user: models.User, plain_password: str) -> bool:
        return verify_password(plain_password, user.hashed_password)

    async def get_by_username(
            self, db: AsyncSession, username: str, options: GetOneOptions | dict = None) -> models.User:
        return await get_one(self.model, db, filters={'username': username}, options=options)

    async def get_by_email(
            self, db: AsyncSession, email: str, options: GetOneOptions | dict = None) -> models.User:
        return await get_one(self.model, db, filters={'email': email}, options=options)

    async def get_by_id(
            self,
            db: AsyncSession,
            user_id: int,
            is_active=None,
            options: GetOneOptions = None
    ) -> models.User:
        filters = {'id': user_id}
        if is_active is not None:
            filters["is_active"] = is_active
        return await get_one(self.model, db, filters=filters, options=options)


Users = UserRepo()
