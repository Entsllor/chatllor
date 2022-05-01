import asyncio
import os
from asyncio import AbstractEventLoop

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, AsyncEngine

os.environ.setdefault("APP_MODE", "test")
from app import models
from app.core.database import create_db_engine, Base, db_context
from app.core.settings import settings
from app.crud import Users, Chats, ChatUsers, AccessTokens, RefreshTokens
from app.main import app
from app.schemas import users, tokens
from app.utils.dependencies import get_db

DEFAULT_USER_PASS = "SomeUserPassword"
DEFAULT_USER_EMAIL = "defaultUser@example.com"
DEFAULT_USER_NAME = "SomeUserName"
AUTH_BEARER = "Authorization: Bearer {}"
USER_CREATE_DATA = users.UserCreate(username=DEFAULT_USER_NAME, password=DEFAULT_USER_PASS, email=DEFAULT_USER_EMAIL)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_engine() -> AsyncEngine:
    engine = create_db_engine(settings.DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture(scope="session")
async def db_tables(db_engine) -> AsyncConnection:
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def db(db_tables, db_engine, event_loop: AbstractEventLoop) -> AsyncSession:
    session = AsyncSession(bind=db_engine)
    try:
        db_context.set(session)
        yield session
    finally:
        db_context.set(None)
        # use run-until-complete instead of await else context var will not set
        event_loop.run_until_complete(session.rollback())
        event_loop.run_until_complete(session.close())


@pytest.fixture(scope="function")
async def client(db, event_loop) -> AsyncClient:
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(app=app, base_url="http://test/") as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def default_user(db) -> models.User:
    yield await Users.create(**USER_CREATE_DATA.dict())


@pytest.fixture(scope="function")
async def second_user(db) -> models.User:
    yield await Users.create(**USER_CREATE_DATA.dict() | {'username': "SECOND_USER", 'email': "second@example.com"})


@pytest.fixture
async def empty_chat(db) -> models.Chat:
    yield await Chats.create(name="EMPTY_CHAT")


@pytest.fixture
async def chat_with_default_user(empty_chat, default_user) -> models.Chat:
    await ChatUsers.create(user_id=default_user.id, chat_id=empty_chat.id)
    yield empty_chat  # now not empty


@pytest.fixture
async def access_token(default_user) -> models.AccessToken:
    yield await AccessTokens.create(user_id=default_user.id)


@pytest.fixture
async def auth_header(access_token) -> dict[str, str]:
    yield get_auth_header(access_token.body)


@pytest.fixture
async def token_pair(default_user, client, access_token) -> tokens.AuthTokensBodies:
    refresh_token = await RefreshTokens.create(user_id=default_user.id)
    yield tokens.AuthTokensBodies(access_token=access_token.body, refresh_token=refresh_token.body)


def get_auth_header(access_token_body: str) -> dict:
    return {"Authorization": f"Bearer {access_token_body}"}
