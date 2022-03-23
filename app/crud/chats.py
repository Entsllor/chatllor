from app import models
from .base import BaseCrudDB, create_instance, delete_by_query
from .chat_users import ChatUsers


class ChatCrud(BaseCrudDB):
    model = models.Chat

    async def create(self, name: str) -> models.Chat:
        chat = self.model(name=name)
        return await create_instance(chat)

    async def delete(self, chat_id: int) -> None:
        await ChatUsers.delete(chat_id=chat_id)
        query = self._delete.where(self.model.id == chat_id)
        return await delete_by_query(query)


Chats = ChatCrud()
