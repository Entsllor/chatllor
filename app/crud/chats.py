from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from .base import BaseCrudDB, create_instance, delete_by_query
from .chat_users import ChatUsers


class ChatCrud(BaseCrudDB):
    model = models.Chat

    async def create(self, db: AsyncSession, name: str) -> models.Chat:
        chat = self.model(name=name)
        return await create_instance(db, chat)

    async def delete(self, db: AsyncSession, chat_id: int) -> None:
        await ChatUsers.delete(db, chat_id=chat_id)
        query = self._delete.where(self.model.id == chat_id)
        return await delete_by_query(db, query)


Chats = ChatCrud()
