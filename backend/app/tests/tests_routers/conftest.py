# Test client utils
import pytest
from httpx import AsyncClient

from app.core.database import db_context
from app.core.settings import test_settings
from app.main import create_app
from app.utils.app_utils import get_app_urls
from app.utils.dependencies import get_db

urls = get_app_urls(create_app(test_settings))


async def clean_db_context_before_request(_):
    db_context.set(None)


def set_db_context_after_response(session):
    async def inner(_):
        db_context.set(session)

    return inner


def get_test_db_dependency(test_db_session):
    async def inner():
        db_context.set(test_db_session)
        yield test_db_session
        db_context.set(None)

    return inner


# end of test client utils
@pytest.fixture(scope="function")
async def client(app, db) -> AsyncClient:
    app.dependency_overrides[get_db] = get_test_db_dependency(db)
    async with AsyncClient(
            app=app,
            base_url="http://test/",
            event_hooks={
                'request': [clean_db_context_before_request],
                'response': [set_db_context_after_response(db)]
            }
    ) as test_client:
        yield test_client


@pytest.fixture
async def auth_header(access_token) -> dict[str, str]:
    yield get_auth_header(access_token.body)


def get_auth_header(access_token_body: str) -> dict:
    return {"Authorization": f"Bearer {access_token_body}"}
