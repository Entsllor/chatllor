import asyncio
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

os.environ.setdefault("APP_MODE", "test")
from app import models
from app.core.database import create_db_engine, Base
from app.core.settings import settings
from app.crud import Users
from app.main import app
from app.schemas import users, tokens
from app.utils.dependencies import get_db

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
async def db_connection(event_loop) -> AsyncConnection:
    engine = create_db_engine(settings.TEST_DB_URL)
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield conn
    engine.dispose()


@pytest.fixture(scope="function")
async def db(db_connection) -> AsyncSession:
    session = AsyncSession(bind=db_connection)
    try:
        yield session
    finally:
        await session.rollback()
        await session.close()


@pytest.fixture(scope="function")
async def client(db) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
async def default_user(db) -> models.User:
    yield await Users.create(db, **USER_CREATE_DATA.dict())


@pytest.fixture(scope="function")
async def token_pair(default_user, client) -> tokens.AuthTokensOut:
    response = client.post(
        "/token/",
        data={'username': default_user.username, 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    yield tokens.AuthTokensOut(**response.json())
