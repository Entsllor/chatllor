from app import models
from .base import BaseCrudDB, create_instance, get_many_by_query
from ..utils.options import GetManyOptions


class MessagesCrud(BaseCrudDB):
    model = models.Message

    async def create(self, db, user_id: int, body: str) -> models.Message:
        message = self.model(user_id=user_id, body=body)
        return await create_instance(db, message)

    async def get_all(self, db, options: GetManyOptions = None) -> list[models.Message]:
        query = self._select
        return await get_many_by_query(db, query, options)


Messages = MessagesCrud()
