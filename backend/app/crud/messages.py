from sqlalchemy import select
from datetime import datetime

from app import models
from .base import BaseCrudDB, create_instance, get_many_by_query
from ..utils.options import GetManyOptions


class MessagesCrud(BaseCrudDB):
    model = models.Message

    async def create(self, user_id: int, body: str, chat_id: int) -> models.Message:
        message = self.model(user_id=user_id, body=body, chat_id=chat_id)
        return await create_instance(message)

    async def get_all(self, options: GetManyOptions = None, **filters) -> list[models.Message]:
        query = self._select.filter_by(**filters)
        return await get_many_by_query(query, options)

    async def get_messages_since_datetime(
            self, period_start: datetime, chat_id: int, _options: GetManyOptions = None) -> list[models.Message]:
        query = (select(self.model)
                 .join(models.User)
                 .where(self.model.chat_id == chat_id)
                 .where(self.model.created_at >= period_start))
        return await get_many_by_query(query, options=_options)


Messages = MessagesCrud()
