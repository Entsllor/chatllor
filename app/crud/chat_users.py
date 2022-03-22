from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from .base import BaseCrudDB, create_instance, delete_by_query, get_many_by_query
from ..utils.options import GetManyOptions


class ChatUserCrud(BaseCrudDB):
    model = models.ChatUser

    async def create(self, db: AsyncSession, chat_id: int, user_id: int) -> models.ChatUser:
        chat = self.model(chat_id=chat_id, user_id=user_id)
        return await create_instance(db, chat)

    async def delete(self, db: AsyncSession, **filters) -> None:
        query = self._delete.filter_by(**filters)
        return await delete_by_query(db, query)

    async def get_user_chats(self, db: AsyncSession, user_id: int, options: GetManyOptions = None) -> list[models.Chat]:
        query = self._select.where(self.model.user_id == user_id)
        return await get_many_by_query(db, query, options)

    async def get_chat_users(self, db: AsyncSession, chat_id: int, options: GetManyOptions = None) -> list[models.User]:
        query = self._select.join().where(self.model.chat_id == chat_id)
        return await get_many_by_query(db, query, options)


ChatUsers = ChatUserCrud()
