from app import models, crud
from app.utils import exceptions
from app.utils.options import GetManyOptions


async def send_message_to_chat(user_id: int, chat_id: int, text: str) -> models.Message:
    chat_user = await crud.ChatUsers.get_one(user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.create(user_id=user_id, chat_id=chat_id, body=text)


async def delete_message_from_chat(user_id: int, message_id: int) -> models.Message:
    message = await crud.Messages.get_one(id=message_id)
    if not message:
        raise exceptions.InstanceNotFound
    chat_user = await crud.ChatUsers.get_one(user_id=user_id, chat_id=message.chat_id)
    if (not chat_user) or (chat_user.user_id != message.user_id):
        raise exceptions.Forbidden
    return await crud.Messages.delete(id=message.id)


async def user_read_chat_messages(user_id: int, chat_id: int) -> list[models.Message]:
    chat_user = await crud.ChatUsers.get_one(user_id=user_id, chat_id=chat_id)
    if not chat_user:
        raise exceptions.Forbidden
    return await crud.Messages.get_user_available_chat_messages(
        user_id=user_id,
        chat_id=chat_id,
        _options=GetManyOptions(ordering_fields=["created_at"])
    )
