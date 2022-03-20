from fastapi import Depends

from app import models
from app.core.database import async_session, AsyncSession
from app.services.auth import oauth2_scheme, get_user_by_access_token


async def get_db() -> AsyncSession:
    session = async_session()
    try:
        yield session
    except Exception as exc:
        await session.rollback()
        raise exc
    else:
        await session.commit()


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> models.User:
    return await get_user_by_access_token(db, token_body=token, only_active=False)


async def get_current_active_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> models.User:
    return await get_user_by_access_token(db, token_body=token, only_active=True)
