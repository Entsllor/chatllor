from app import models
from app.repos.base import BaseAsyncCrudRepo
from app.utils.passwords import get_password_hash


class UserRepo(BaseAsyncCrudRepo):
    model = models.User

    async def create(self, username, password, email) -> models.User:
        hashed_password = get_password_hash(password)
        return await super(UserRepo, self).create(username=username, hashed_password=hashed_password, email=email)
