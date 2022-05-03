import uvicorn
from fastapi import FastAPI
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.routers import users, auth, messages, chats, chat_users
from app.utils import exceptions

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(messages.router)
app.include_router(chats.router)
app.include_router(chat_users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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
