from app import models
from .base import BaseCrudDB, create_instance, delete_by_query, get_many_by_query
from ..utils.options import GetManyOptions


class ChatUserCrud(BaseCrudDB):
    model = models.ChatUser

    async def create(self, chat_id: int, user_id: int) -> models.ChatUser:
        chat = self.model(chat_id=chat_id, user_id=user_id)
        return await create_instance(chat)

    async def delete(self, **filters) -> None:
        query = self._delete.filter_by(**filters)
        return await delete_by_query(query)

    async def get_user_chats(self, user_id: int, options: GetManyOptions = None) -> list[models.Chat]:
        query = self._select.where(self.model.user_id == user_id)
        return await get_many_by_query(query, options)

    async def get_chat_users(self, chat_id: int, options: GetManyOptions = None) -> list[models.User]:
        query = self._select.join().where(self.model.chat_id == chat_id)
        return await get_many_by_query(query, options)


ChatUsers = ChatUserCrud()
