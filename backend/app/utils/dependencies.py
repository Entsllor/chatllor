from fastapi import Depends

from app import models
from app.core.database import async_session, db_context
from app.services.auth import oauth2_scheme, get_user_by_access_token


async def get_db():
    session = async_session()
    try:
        db_context.set(session)
        yield session
    finally:
        await session.close()


async def get_current_user(token: str = Depends(oauth2_scheme), _=Depends(get_db)) -> models.User:
    return await get_user_by_access_token(token_body=token, only_active=False)


async def get_current_active_user(token: str = Depends(oauth2_scheme), _=Depends(get_db)) -> models.User:
    return await get_user_by_access_token(token_body=token, only_active=True)
