import os
from pathlib import Path

from pydantic import BaseSettings

BASE_PATH = Path(__file__).parent.parent


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    LOG_LEVEL: str = "debug"
    DB_URL: str = "postgresql+asyncpg:///user:pass@localhost:5432/postgres"
    TEST_DB_URL: str = "postgresql+asyncpg:///user:pass@localhost:5432/test"
    JWT_ALGORITHM: str = "HS256"
    SECRET_KEY: str
    ALEMBIC_PATH: Path | str = BASE_PATH.parent.joinpath("migrations")
    ALLOWED_ORIGINS: list = ["https://localhost:3000", "http://localhost:3000"]
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
