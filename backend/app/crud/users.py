from app import models
from app.crud.base import create_instance, BaseCrudDB
from app.utils.passwords import get_password_hash


class UserRepo(BaseCrudDB):
    model = models.User

    async def create(self, *, username: str, password: str, email: str) -> models.User:
        hashed_password = get_password_hash(password)
        user = self.model(username=username, hashed_password=hashed_password, email=email)
        return await create_instance(user)


Users: UserRepo = UserRepo()
