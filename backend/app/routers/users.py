from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError

from app.crud import Users
from app.schemas.users import UserPrivate, UserCreate, UserPublic, User
from app.utils.dependencies import get_current_active_user
from app.utils.filtering import filter_by_model
from app.utils.options import GetManyOptions

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    try:
        created = await Users.create(**user.dict())
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"This username '{user.username}' is already taken.")
    return created


@router.get("/me", response_model=UserPrivate)
async def read_user_me(user: User = Depends(get_current_active_user)):
    return user


@router.get("/", response_model=list[UserPublic])
async def read_users(filters=Depends(filter_by_model(UserPublic))):
    return await Users.get_many(_options=GetManyOptions(filters=filters))
