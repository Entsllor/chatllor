from fastapi import APIRouter, Depends

from app.schemas.messages import MessageOut, MessageCreate
from app.services import messages
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/chats")


@router.get("/{chat_id}/messages/", response_model=list[MessageOut])
async def read_messages(chat_id, user=Depends(get_current_active_user)):
    return await messages.read_messages(user_id=user.id, chat_id=chat_id)


@router.post("/{chat_id}/messages/", response_model=MessageOut, status_code=201)
async def create_message(message: MessageCreate, chat_id, user=Depends(get_current_active_user)):
    return await messages.send_message_to_chat(user_id=user.id, chat_id=chat_id, text=message.body)


@router.delete("/{chat_id}/messages/{message_id}", status_code=200)
async def delete_message(message_id: int, user=Depends(get_current_active_user)):
    await messages.delete_message_from_chat(user_id=user.id, message_id=message_id)
