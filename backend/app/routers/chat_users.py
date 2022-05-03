from fastapi import Depends, APIRouter

from app.schemas.chat_users import ChatUserJoined
from app.services import chats
from app.utils.dependencies import get_current_active_user, get_db

router = APIRouter(prefix="/chats")


@router.post("/{chat_id}/users/", response_model=ChatUserJoined)
async def join_chat(chat_id: int, user=Depends(get_current_active_user), db=Depends(get_db)):
    chat_user = await chats.add_user_to_chat(user_id=user.id, chat_id=chat_id)
    await db.commit()
    return chat_user


@router.delete("/{chat_id}/users/")
async def leave_chat(chat_id: int, user=Depends(get_current_active_user), db=Depends(get_db)):
    if await chats.remove_user_from_chat(user_id=user.id, chat_id=chat_id):
        await db.commit()
