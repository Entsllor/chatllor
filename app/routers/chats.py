from fastapi import APIRouter, Depends

from app.schemas.chats import ChatCreate, ChatOut
from app.services import chats
from app.utils.dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/chats")


@router.post("/", response_model=ChatOut, status_code=201)
async def create_chat(chat: ChatCreate, db=Depends(get_db), user=Depends(get_current_active_user)):
    return await chats.user_create_a_chat(db, user_id=user.id, chat_name=chat.name)


@router.delete("/{chat_id}", status_code=200)
async def delete_chat(chat_id: int, db=Depends(get_db), user=Depends(get_current_active_user)):
    await chats.user_delete_a_chat(db, user_id=user.id, chat_id=chat_id)
