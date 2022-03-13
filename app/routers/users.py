from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError

from app.repos.users import UserRepo
from app.schemas.users import UserPrivate, UserCreate, UserPublic
from app.utils.dependencies import get_db

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db=Depends(get_db)):
    try:
        created = await UserRepo(db).create(**user.dict())
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"This username '{user.username}' is already taken.")
    await db.commit()
    return created


@router.get("/", response_model=list[UserPublic])
async def read_users(db=Depends(get_db)):
    return await UserRepo(db).get_many()
