from sqlalchemy.ext.asyncio import AsyncSession

from app import models, crud
from app.utils import exceptions
from app.utils.options import GetManyOptions


async def send_message_to_chat(db: AsyncSession, user_id: int, chat_id: int, message_body: str) -> models.Message:
    chat_user = await crud.ChatUsers.get_one(db, user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.create(db, user_id=user_id, chat_id=chat_id, body=message_body)


async def read_messages(db: AsyncSession, user_id: int, chat_id: int) -> list[models.Message]:
    chat_user = await crud.ChatUsers.get_one(db, user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.get_user_available_chat_messages(
        db, _options=GetManyOptions(ordering_fields=["created_at"]), user_id=user_id, chat_id=chat_id)
