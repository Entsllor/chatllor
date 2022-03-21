from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from .base import BaseCrudDB, create_instance, delete_by_query


class ChatUserCrud(BaseCrudDB):
    model = models.ChatUser

    async def create(self, db: AsyncSession, chat_id: int, user_id: int) -> models.ChatUser:
        chat = self.model(chat_id=chat_id, user_id=user_id)
        return await create_instance(db, chat)

    async def delete(self, db: AsyncSession, instance_id: int) -> None:
        query = self._delete.where(self.model.id == instance_id)
        return await delete_by_query(db, query)


ChatUser = ChatUserCrud()
