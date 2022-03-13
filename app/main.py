import uvicorn
from fastapi import FastAPI

from app.core.database import engine, Base
from app.core.settings import settings

from app.routers import users

app = FastAPI()
app.include_router(users.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
