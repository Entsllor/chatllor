from fastapi import APIRouter, Depends

from app.services import messages
from app.schemas.messages import MessageOut, MessageCreate
from app.utils.dependencies import get_db, get_current_active_user

router = APIRouter()


@router.get("/chats/{chat_id}/messages/", response_model=list[MessageOut])
async def read_messages(chat_id, db=Depends(get_db), user=Depends(get_current_active_user)):
    return await messages.read_messages(db, user_id=user.id, chat_id=chat_id)


@router.post("/chats/{chat_id}/messages/", response_model=MessageOut, status_code=201)
async def create_message(message: MessageCreate, chat_id, db=Depends(get_db), user=Depends(get_current_active_user)):
    created_message = await messages.send_message_to_chat(
        db, message_body=message.body, chat_id=chat_id, user_id=user.id)
    return created_message
