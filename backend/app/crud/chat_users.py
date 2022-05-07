from sqlalchemy import select

from app import models
from .base import BaseCrudDB, create_instance, get_many_by_query
from ..utils.options import GetManyOptions


class ChatUserCrud(BaseCrudDB):
    model = models.ChatUser

    async def create(self, chat_id: int, user_id: int) -> models.ChatUser:
        chat = self.model(chat_id=chat_id, user_id=user_id)
        return await create_instance(chat)

    async def get_user_chats(self, user_id: int, options: GetManyOptions = None) -> list[models.Chat]:
        query = select(models.ChatUser, models.Chat).join(models.Chat).where(self.model.user_id == user_id)
        return await get_many_by_query(query, options)

    async def get_chat_users(self, chat_id: int, options: GetManyOptions = None) -> list[models.User]:
        query = select(models.ChatUser, models.User).join(models.User).where(self.model.chat_id == chat_id)
        return await get_many_by_query(query, options)


ChatUsers = ChatUserCrud()
