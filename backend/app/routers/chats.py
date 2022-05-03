from fastapi import APIRouter, Depends

from app.schemas.chats import ChatCreate, ChatOut
from app.services import chats
from app.utils.dependencies import get_current_active_user, get_db

router = APIRouter(prefix="/chats")


@router.post("/", response_model=ChatOut, status_code=201)
async def create_chat(chat: ChatCreate, user=Depends(get_current_active_user), db=Depends(get_db)):
    db_chat = await chats.user_create_a_chat(user_id=user.id, chat_name=chat.name)
    await db.commit()
    return db_chat


@router.delete("/{chat_id}", status_code=200)
async def delete_chat(chat_id: int, user=Depends(get_current_active_user), db=Depends(get_db)):
    if await chats.user_delete_a_chat(user_id=user.id, chat_id=chat_id):
        await db.commit()
