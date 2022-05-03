import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import settings, Settings
from app.routers import users, auth, messages, chats, chat_users
from app.utils import exceptions
from app.utils.exceptions import app_exception_handler

app = FastAPI()  # create this for pycharm fastapi runner


def create_app(app_settings: Settings) -> FastAPI:
    new_app = FastAPI()
    new_app.include_router(users.router)
    new_app.include_router(auth.router)
    new_app.include_router(messages.router)
    new_app.include_router(chats.router)
    new_app.include_router(chat_users.router)

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    new_app.add_exception_handler(exceptions.BaseAppException, app_exception_handler)
    return new_app


app = create_app(settings)  # noqa

if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
