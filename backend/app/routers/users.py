from fastapi import APIRouter, status, Depends

from app.crud import Users
from app.schemas.users import UserPrivate, UserCreate, UserPublic, User
from app.utils import exceptions
from app.utils.dependencies import get_current_active_user, get_db
from app.utils.filtering import filter_by_model
from app.utils.options import GetManyOptions

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserPrivate, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db=Depends(get_db)):
    if await Users.get_one(username=user.username):
        raise exceptions.ExpectedUniqueUsername
    created = await Users.create(**user.dict())
    await db.commit()
    return created


@router.get("/me", response_model=UserPrivate, dependencies=[Depends(get_db)])
async def read_user_me(user: User = Depends(get_current_active_user)):
    return user


@router.get("/", response_model=list[UserPublic], dependencies=[Depends(get_db)])
async def read_users(filters=Depends(filter_by_model(UserPublic))):
    return await Users.get_many(_options=GetManyOptions(filters=filters))
