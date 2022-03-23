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
