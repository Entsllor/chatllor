import uvicorn
from fastapi import FastAPI

from app.core.database import Base, engine
from app.core.settings import settings
from app.routers import users, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
