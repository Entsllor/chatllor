import asyncio
import os
from asyncio import AbstractEventLoop

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

os.environ.setdefault("APP_MODE", "test")
from app import models
from app.core.database import create_db_engine, Base, db_context
from app.core.settings import settings
from app.crud import Users, Chats, ChatUsers
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
async def db_engine(event_loop) -> AsyncConnection:
    engine = create_db_engine(settings.TEST_DB_URL)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield conn
        await conn.run_sync(Base.metadata.drop_all)
    engine.dispose()


@pytest.fixture(scope="function")
def db(db_engine, event_loop: AbstractEventLoop) -> AsyncSession:
    session = AsyncSession(bind=db_engine)
    try:
        db_context.set(session)
        yield session
    finally:
        db_context.set(None)
        event_loop.run_until_complete(session.rollback())
        event_loop.run_until_complete(session.close())


@pytest.fixture(scope="function")
async def client(db) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def default_user(db) -> models.User:
    yield await Users.create(**USER_CREATE_DATA.dict())


@pytest.fixture(scope="function")
async def second_user(db) -> models.User:
    yield await Users.create(**USER_CREATE_DATA.dict() | {'username': "Luidji", 'email': "luidji@example.com"})


@pytest.fixture(scope="function")
async def empty_chat(db) -> models.Chat:
    yield await Chats.create(name="test_chat_can_be_created")


@pytest.fixture(scope="function")
async def chat_with_default_user(empty_chat, default_user) -> models.Chat:
    await ChatUsers.create(user_id=default_user.id, chat_id=empty_chat.id)
    yield empty_chat  # now not empty


@pytest.fixture(scope="function")
async def token_pair(default_user, client) -> tokens.AuthTokensOut:
    response = client.post(
        "/token/",
        data={'username': default_user.username, 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    yield tokens.AuthTokensOut(**response.json())


def token_auth(access_token_body: str) -> dict:
    return {"Authorization": f"Bearer {access_token_body}"}
