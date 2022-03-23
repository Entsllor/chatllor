from app import models, crud
from app.utils import exceptions
from app.utils.options import GetManyOptions


async def send_message_to_chat(user_id: int, chat_id: int, text: str) -> models.Message:
    chat_user = await crud.ChatUsers.get_one(user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.create(user_id=user_id, chat_id=chat_id, body=text)


async def read_messages(user_id: int, chat_id: int) -> list[models.Message]:
    chat_user = await crud.ChatUsers.get_one(user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.get_user_available_chat_messages(
        user_id=user_id,
        chat_id=chat_id,
        _options=GetManyOptions(ordering_fields=["created_at"])
    )
