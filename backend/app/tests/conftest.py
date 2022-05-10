import asyncio
import os
from asyncio import AbstractEventLoop

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, AsyncEngine

# use only testing settings
os.environ.setdefault("APP_MODE", "test")  # noqa

from app import models, crud
from app.core.database import create_db_engine, Base, db_context
from app.core.settings import test_settings
from app.main import create_app
from app.schemas import users, tokens

DEFAULT_USER_PASS = "SomeUserPassword"
DEFAULT_USER_EMAIL = "defaultUser@example.com"
DEFAULT_USER_NAME = "SomeUserName"
USER_CREATE_DATA = users.UserCreate(username=DEFAULT_USER_NAME, password=DEFAULT_USER_PASS, email=DEFAULT_USER_EMAIL)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    engine = create_db_engine(test_settings.DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
async def db_tables(db_engine) -> AsyncConnection:
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def async_pass(*_, **__):
    """Do nothing but asynchronously"""


@pytest.fixture(scope="function")
def db(db_tables, db_engine, event_loop: AbstractEventLoop) -> AsyncSession:
    session = AsyncSession(bind=db_engine)
    try:
        db_context.set(session)
        session.commit = async_pass  # don't commit while testing
        yield session
    finally:
        db_context.set(None)
        # use run-until-complete instead of await else context var will not set
        event_loop.run_until_complete(session.rollback())
        event_loop.run_until_complete(session.close())


@pytest.fixture(scope="session")
async def app():
    yield create_app(test_settings)


@pytest.fixture(scope="function")
async def default_user(db) -> models.User:
    yield await crud.Users.create(**USER_CREATE_DATA.dict())


@pytest.fixture(scope="function")
async def second_user(db) -> models.User:
    second_user_data = USER_CREATE_DATA.dict() | {'username': "SECOND_USER", 'email': "second@example.com"}
    yield await crud.Users.create(**second_user_data)


@pytest.fixture
async def empty_chat(db) -> models.Chat:
    yield await crud.Chats.create(name="EMPTY_CHAT")


@pytest.fixture
async def chat_with_default_user(empty_chat, default_user) -> models.Chat:
    await crud.ChatUsers.create(user_id=default_user.id, chat_id=empty_chat.id)
    yield empty_chat  # now not empty


@pytest.fixture
async def access_token(default_user) -> models.AccessToken:
    yield await crud.AccessTokens.create(user_id=default_user.id)


@pytest.fixture
async def token_pair(default_user, access_token) -> tokens.AuthTokensBodies:
    refresh_token = await crud.RefreshTokens.create(user_id=default_user.id)
    yield tokens.AuthTokensBodies(access_token=access_token.body, refresh_token=refresh_token.body)
