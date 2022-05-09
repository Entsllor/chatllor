from fastapi import Depends, APIRouter

from app import crud
from app.schemas.chat_users import ChatUserJoined, ChatUserDetail
from app.services import chats
from app.utils.dependencies import get_current_active_user, get_db

router = APIRouter(prefix="/chats")


@router.get('/my/', dependencies=[Depends(get_db)], response_model=list[ChatUserDetail])
async def read_my_chats(user=Depends(get_current_active_user)):
    return await crud.ChatUsers.get_user_chats(user_id=user.id)


@router.post("/{chat_id}/users/", response_model=ChatUserJoined)
async def join_chat(chat_id: int, user=Depends(get_current_active_user), db=Depends(get_db)):
    chat_user = await chats.add_user_to_chat(user_id=user.id, chat_id=chat_id)
    await db.commit()
    return chat_user


@router.delete("/{chat_id}/users/", status_code=204)
async def leave_chat(chat_id: int, user=Depends(get_current_active_user), db=Depends(get_db)):
    if await chats.remove_user_from_chat(user_id=user.id, chat_id=chat_id):
        await db.commit()
