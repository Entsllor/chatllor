import os
from pathlib import Path

from pydantic import BaseSettings

BASE_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    LOG_LEVEL: str = "debug"
    DB_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    TEST_DB_URL: str = "sqlite+aiosqlite:///test_db.sqlite3"
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 20
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30
    HASHING_SCHEMAS: list = ["bcrypt"]

    class Config:
        case_sensitive = True
        env_file = BASE_PATH.joinpath('.env')
        env_prefix = "APP_"


class TestSettings(Settings):
    HASHING_SCHEMAS: list = ["md5_crypt"]


APP_MODE = os.getenv("APP_MODE", "dev").lower()

if "test" in APP_MODE:
    settings = TestSettings()
else:
    settings = Settings()
