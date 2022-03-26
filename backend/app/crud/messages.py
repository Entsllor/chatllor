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

    async def get_user_available_chat_messages(
            self, user_id: int, chat_id: int, _options: GetManyOptions = None) -> list[models.Message]:
        query = self._select.join(models.ChatUser, models.ChatUser.user_id == user_id) \
            .filter_by(chat_id=chat_id).where(self.model.created_at >= models.ChatUser.joined_at)
        return await get_many_by_query(query, options=_options)


Messages = MessagesCrud()
