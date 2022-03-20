from fastapi import APIRouter, Depends

from app.crud import Messages
from app.schemas.messages import MessageOut, MessageCreate
from app.utils.dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/messages")


@router.get("/", response_model=list[MessageOut])
async def read_messages(db=Depends(get_db)):
    return await Messages.get_all(db)


@router.post("/", response_model=MessageOut, status_code=201)
async def create_message(message: MessageCreate, db=Depends(get_db), user=Depends(get_current_active_user)):
    created_message = await Messages.create(db, body=message.body, user_id=user.id)
    return created_message
