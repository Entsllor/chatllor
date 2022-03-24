import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exception_handlers import http_exception_handler

from app.core.database import Base, engine
from app.core.settings import settings
from app.routers import users, auth, messages, chats, chat_users
from app.utils import exceptions
from app.utils.dependencies import get_db

app = FastAPI(dependencies=[Depends(get_db)])
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(chats.router)
app.include_router(chat_users.router)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.exception_handler(exceptions.BaseAppException)
async def app_exception_handler(request, exc: exceptions.BaseAppException):
    return await http_exception_handler(request, exc.as_http)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
