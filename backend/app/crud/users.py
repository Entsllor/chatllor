from app import models
from app.crud.base import create_instance, get_one_by_query, BaseCrudDB
from app.utils.options import GetOneOptions
from app.utils.passwords import get_password_hash


class UserRepo(BaseCrudDB):
    model = models.User

    async def create(self, *, username: str, password: str, email: str) -> models.User:
        hashed_password = get_password_hash(password)
        user = self.model(username=username, hashed_password=hashed_password, email=email)
        return await create_instance(user)

    async def get_by_username(
            self, username: str, options: GetOneOptions | dict = None) -> models.User:
        q = self._select.where(self.model.username == username)
        return await get_one_by_query(q, options=options)

    async def get_by_email(
            self, email: str, options: GetOneOptions | dict = None) -> models.User:
        q = self._select.where(self.model.email == email)
        return await get_one_by_query(q, options=options)

    async def get_by_id(self, user_id: int, options: GetOneOptions = None) -> models.User:
        q = self._select.where(self.model.id == user_id)
        return await get_one_by_query(q, options=options)


Users = UserRepo()
